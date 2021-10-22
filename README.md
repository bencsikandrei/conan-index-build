# Error with lockfiles when using build_requirements

1) Run `pip3 install -r requirements.txt` (will install conan 1.41.0)

2) Run the `python3 .ci/build2.py` script from the root folder

## Expected behavior

All packets should be built correctly without any errors.

## Actual behavior

```
...
Running command: conan install apr/1.7.0@user/stable#1bd1f8f50232d0a5b1f7d37148d3cd49 --build=missing --lockfile=/home/user/Source/conan-index-build/recipes/../locks/apr_1.7.0.lock --lockfile-out=/home/user/Source/conan-index-build/recipes/../locks/apr_1.7.0.lock
Using lockfile: '/home/user/Source/conan-index-build/recipes/../locks/apr_1.7.0.lock'
Configuration:
[settings]
arch=x86_64
arch_build=x86_64
build_type=Release
compiler=gcc
compiler.libcxx=libstdc++11
compiler.version=9
os=Linux
os_build=Linux
[options]
[build_requires]
[env]

ERROR: Build-require 'libtool' cannot be found in lockfile
Traceback (most recent call last):
  File "./.ci/build2.py", line 146, in <module>
    ci_pipeline(recipes_dir, packages)
  File "./.ci/build2.py", line 136, in ci_pipeline
    _conan_build_missing_packages(package_bundle, package_build_order, version_dir_cache)
  File "./.ci/build2.py", line 95, in _conan_build_missing_packages
    run(f"conan install {ref} --build=missing --lockfile={lockfile} --lockfile-out={lockfile}")
  File "./.ci/build2.py", line 14, in run
    raise Exception("Failed command: {}".format(command))
Exception: Failed command: conan install apr/1.7.0@user/stable#1bd1f8f50232d0a5b1f7d37148d3cd49 --build=missing --lockfile=/home/user/Source/conan-index-build/recipes/../locks/apr_1.7.0.lock --lockfile-out=/home/user/Source/conan-index-build/recipes/../locks/apr_1.7.0.lock
```

## Devcontainer

You can use vscode with a devcontainer if you can't install the requirements.
See the documentation for that here: https://code.visualstudio.com/docs/remote/containers.
