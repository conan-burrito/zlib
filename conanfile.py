from conans import tools, ConanFile, CMake

import os


class ZlibConan(ConanFile):
    name = 'zlib'
    description = 'A Massively Spiffy Yet Delicately Unobtrusive Compression Library ' \
                  '(Also Free, Not to Mention Unencumbered by Patents)'
    homepage = 'http://www.zlib.net'
    license = 'Zlib'
    url = 'https://github.com/conan-burrito/zlib'

    generators = 'cmake'

    settings = 'os', 'arch', 'compiler', 'build_type'
    options = {'shared': [True, False], 'fPIC': [True, False]}
    default_options = {'shared': False, 'fPIC': True}

    # We make changes in a separate copy of the library sources depending on the `shared` option
    no_copy_source = False

    exports_sources = ['patches/*']

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

        # It's a C project - remove irrelevant settings
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    @property
    def zip_folder_name(self):
        return 'zlib-%s' % self.zlib_version

    @property
    def source_subfolder(self):
        return os.path.join(self.source_folder, 'src')

    def source(self):
        tools.get(**self.conan_data["sources"][self.version], destination=self.source_subfolder, strip_root=True)

        for patch in self.conan_data["patches"][self.version]:
            tools.patch(**patch)

    def build(self):
        original_install = 'install(TARGETS zlib zlibstatic'
        target_name = 'zlib' if self.options.shared else 'zlibstatic'
        install_text = 'install(TARGETS %s' % target_name
        tools.replace_in_file(os.path.join(self.source_subfolder, 'CMakeLists.txt'), original_install, install_text)

        with tools.chdir(self.source_subfolder):

            tools.mkdir("_build")
            with tools.chdir("_build"):
                cmake = CMake(self)
                cmake.configure(source_folder=self.source_subfolder)
                cmake.build()
                cmake.install()

    def _rename_libraries(self):
        if self.settings.os == "Windows":
            lib_path = os.path.join(self.package_folder, "lib")

            if not self.options.shared:
                if self.settings.compiler == "Visual Studio":
                    current_lib = os.path.join(lib_path, "zlibstatic.lib")
                    os.rename(current_lib, os.path.join(lib_path, "zlib.lib"))
                elif self.settings.compiler == "gcc":
                    current_lib = os.path.join(lib_path, "libzlibstatic.a")
                    os.rename(current_lib, os.path.join(lib_path, "libzlib.a"))
                elif self.settings.compiler == "clang":
                    current_lib = os.path.join(lib_path, "zlibstatic.lib")
                    os.rename(current_lib, os.path.join(lib_path, "zlib.lib"))

    def package(self):
        # Extract the License/s from the header to a file
        with tools.chdir(self.source_subfolder):
            tmp = tools.load("zlib.h")
            license_contents = tmp[2:tmp.find("*/", 1)]
            tools.save("LICENSE", license_contents)

        # Copy the license files
        self.copy("LICENSE", src=self.source_subfolder, dst="licenses")
        self._rename_libraries()

    def package_info(self):
        self.cpp_info.libs.append('zlib' if self.settings.os == "Windows" else "z")
        self.cpp_info.names["cmake_find_package"] = "zlib"
        self.cpp_info.names["cmake_find_package_multi"] = "zlib"

