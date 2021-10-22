from conans import ConanFile


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"

    def build(self):
        pass

    def test(self):
        pass
