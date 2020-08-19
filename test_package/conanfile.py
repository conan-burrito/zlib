from conans import tools, ConanFile, CMake
import os


class Test(ConanFile):
    settings = 'os', 'arch', 'compiler', 'build_type'

    generators = 'cmake'

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        assert os.path.exists(os.path.join(self.deps_cpp_info["zlib"].rootpath, "licenses", "LICENSE"))
        if "x86" in self.settings.arch and not tools.cross_building(self.settings):
            self.run(os.path.join("bin", "test"), run_environment=True)
