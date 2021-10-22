from contextlib import contextmanager
import os
import re
from conans import AutoToolsBuildEnvironment, ConanFile, tools
from conans.errors import ConanException


class LibtoolConan(ConanFile):
    name = "libtool"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.gnu.org/software/libtool/"
    description = "GNU libtool is a generic library support script. "
    topics = ("conan", "libtool", "configure", "library", "shared", "static")
    license = ("GPL-2.0-or-later", "GPL-3.0-or-later")
    exports_sources = "patches/**"

    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }
    _autotools = None

    @property
    def _source_subfolder(self):
        return os.path.join(self.source_folder, "source_subfolder")

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

    def source(self):
        pass

    def requirements(self):
        pass

    def build_requirements(self):
        pass

    def build(self):
        pass

    def package(self):
        pass

    def package_info(self):
        pass