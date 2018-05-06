#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os
import shutil


class ColmConan(ConanFile):
    name = "colm"
    version = "0.13.0.5"
    description = "Colm is a programming language designed for the analysis and transformation of computer languages"
    url = "https://github.com/bincrafters/conan-colm"
    homepage = "https://www.colm.net/open-source/colm/"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt", "cmake/*"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        source_url = "https://www.colm.net/files/colm/colm-"
        tools.get("{0}{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        cmake_src_dir = os.path.join("cmake", "src")
        os.rename(extracted_dir, self.source_subfolder)
        shutil.copy(os.path.join("cmake", "CMakeLists.txt"), self.source_subfolder)
        for item in os.listdir(cmake_src_dir):
            file = os.path.join(cmake_src_dir, item)
            shutil.copy(file, os.path.join(self.source_subfolder, "src"))

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(build_folder=self.build_subfolder)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self.source_subfolder)
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
