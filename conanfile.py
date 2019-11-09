import os
import shutil
from conans import ConanFile, CMake, tools


class ColmConan(ConanFile):
    name = "colm"
    version = "0.13.0.5"
    description = "Colm is a programming language designed for the analysis and transformation of computer languages"
    url = "https://github.com/bincrafters/conan-colm"
    homepage = "https://www.colm.net/open-source/colm/"
    topics = ("conan", "coml", "computation", "analysis", "transformation")
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt", "cmake/*"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        source_url = "http://www.colm.net/files/colm/colm-"
        sha256 = "33e624677176958eaad76ebe6c391a68a0b4728fec8cc039efa1316f525f408c"
        tools.get("{0}{1}.tar.gz".format(source_url, self.version), sha256=sha256)
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _copy_cmake_files(self):
        cmake_src_dir = os.path.join("cmake", "src")
        shutil.copy(os.path.join("cmake", "CMakeLists.txt"), self._source_subfolder)
        for item in os.listdir(cmake_src_dir):
            file = os.path.join(cmake_src_dir, item)
            shutil.copy(file, os.path.join(self._source_subfolder, "src"))

    def _remove_headers(self):
        for file in ["config.h", "defs.h", "version.h"]:
            os.remove(os.path.join(self._source_subfolder, "src", file))

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        self._remove_headers()
        self._copy_cmake_files()
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="COPYING", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
