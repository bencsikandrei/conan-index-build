from conans import ConanFile
from contextlib import contextmanager


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"

    def build_requirements(self):
        pass

    def build(self):
        pass

    def test(self):
        pass
