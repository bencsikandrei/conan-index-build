#!/usr/bin/env python3
 
import os, shutil, yaml, json
from contextlib import contextmanager

from conans.client.conan_api import ConanFileReference

def run(command, assert_error=False):
    print("Running command: {}".format(command))
    ret = os.system(command)
    if ret == 0 and assert_error:
        raise Exception("Command unexpectedly succedeed: {}".format(command))
    if ret != 0 and not assert_error:
        raise Exception("Failed command: {}".format(command))

def load(filename):
    with open(filename, "r") as f:
        return f.read()

def save(filename, content):
    with open(filename, "w") as f:
        return f.write(content)

def rm(path):
    if os.path.isfile(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)

@contextmanager
def chdir(path):
    current_path = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(current_path)

@contextmanager
def setenv(key, value):
    old_value = os.environ.get(key)
    os.environ[key] = value
    try:
        yield
    finally:
        if old_value is not None:
            os.environ[key] = old_value

def clean():
    rm("locks")

def _create_version_directory_cache(recipes_dir, packages):
    version_dir_cache = {}
    for package in packages:
        version_dir_cache[package] = {}
        with open(os.path.join(recipes_dir, package, "config.yml")) as config_file:
            config = yaml.load(config_file, Loader=yaml.FullLoader)
            for version, version_dict in config["versions"].items():
                version_dir = version_dict["folder"]
                version_dir_cache[package][version] = version_dir
    return version_dir_cache

def _conan_export_all(recipes_dir, packages, version_dir_cache):
    for package in packages:
        for package_version, package_version_dir in version_dir_cache[package].items():
            # print(f"Package {package}, version {package_version}, version directory: {package_version_dir}")
            run(f"conan export {recipes_dir}/{package}/{package_version_dir} {package_version}@user/stable")

def _conan_create_lockfiles(lockfiles_dir, version_dir_cache):
    lockfile_paths = []
    for package, package_cache in version_dir_cache.items():
        # TODO use list comprehensions
        for package_version, _ in package_cache.items():
            lockfile_path = os.path.join(lockfiles_dir, f"{package}_{package_version}.lock")
            run(f"conan lock create --reference {package}/{package_version}@user/stable --lockfile-out={lockfile_path}")
            lockfile_paths.append(lockfile_path)
    return lockfile_paths

def _conan_build_missing_packages(package_bundle, package_build_order, version_dir_cache):
    bundle = package_bundle["lock_bundle"]

    for level in package_build_order:
        for ref in level:
            packages = bundle[ref]["packages"]
            for package in packages:
                if not package["prev"]:
                    lockfiles = package["lockfiles"]
                    print(f"Lockfiles {lockfiles}")
                    lockfile = next(iter(sorted(lockfiles)))
                    print(f"Lockfile {lockfile}")

                    # To solve build_requires not appearing inside lockfiles
                    # rewrite the lockfile with 
                    # WORKAROUND: add '--build=missing' to the conan lock create command solves the issue. but why?
                    # run(f"conan lock create --reference {ref} --lockfile={lockfile} --lockfile-out={lockfile}")
                    run(f"conan install {ref} --build={ref} --lockfile={lockfile} --lockfile-out={lockfile}")

                    conan_ref = ConanFileReference.loads(ref)
                    print(f"Conan ref {conan_ref}")

                    package_version_dir = version_dir_cache[conan_ref.name][conan_ref.version]
                    run(f"conan test --lockfile {lockfile} {recipes_dir}/{conan_ref.name}/{package_version_dir}/test_package {ref}")


def ci_pipeline(recipes_dir, packages):
    print("Cleaning CI artifacts")
    clean()

    version_dir_cache = _create_version_directory_cache(recipes_dir, packages)
    print(f"Version directory cache: {version_dir_cache}")

    _conan_export_all(recipes_dir, packages, version_dir_cache)

    lockfiles_dir = os.path.join(recipes_dir, "..", "locks")
    os.mkdir(lockfiles_dir)
    
    lockfile_paths = _conan_create_lockfiles(lockfiles_dir, version_dir_cache)
    print(f"Lockfile paths: {lockfile_paths}")

    lockfile_bundle_path = os.path.join(lockfiles_dir, "lock.bundle")
    run(f"conan lock bundle create {' '.join(lockfile_paths)} --bundle-out={lockfile_bundle_path}")

    package_bundle = json.loads(load(lockfile_bundle_path))
    print(f"Build order: {package_bundle}")
    
    lockfile_bundle_build_order_path = os.path.join(lockfiles_dir, "build_order.json")
    run(f"conan lock bundle build-order {lockfile_bundle_path} --json {lockfile_bundle_build_order_path}")

    package_build_order = json.loads(load(lockfile_bundle_build_order_path))
    print(f"Build order: {package_build_order}")

    if len(package_build_order) == 0:
        print("Nothing to build")
        return
    
    print("Building missing packages")
    _conan_build_missing_packages(package_bundle, package_build_order, version_dir_cache)
    
if __name__ == '__main__':
    recipes_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "recipes"))
    print(f"Recipes from: {recipes_dir}")

    packages = os.listdir(recipes_dir)
    packages.sort()
    print(f"Found the following packages: {packages}")

    ci_pipeline(recipes_dir, packages)
