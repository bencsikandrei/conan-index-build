import os
import re
from conans import AutoToolsBuildEnvironment, ConanFile, CMake, tools
from conans.errors import ConanException


class AprConan(ConanFile):
    name = "apr"
    description = "The Apache Portable Runtime (APR) provides a predictable and consistent interface to underlying platform-specific implementations"
    license = "Apache-2.0"
    topics = ("conan", "apr", "apache", "platform", "library")
    homepage = "https://apr.apache.org/"
    url = "https://github.com/conan-io/conan-center-index"
    exports_sources = "CMakeLists.txt", "patches/**"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "force_apr_uuid": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "force_apr_uuid": True,
    }

    _autotools = None
    _cmake = None

    def config_options(self):
        pass

    def build_requirements(self):
        # if self.settings.os == "Macos":
        self.build_requires("libtool/2.4.6@user/stable")

    def configure(self):
        pass

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def source(self):
        pass

    def build(self):
        pass

    def package(self):
        pass

    def package_info(self):
        pass
