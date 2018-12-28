#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
from conans import ConanFile, AutoToolsBuildEnvironment, CMake, tools


class ColmConan(ConanFile):
    name = "colm"
    version = "0.12.0"
    description = "Colm is a programming language designed for the analysis and transformation of computer languages"
    url = "https://github.com/bincrafters/conan-colm"
    homepage = "https://www.colm.net/open-source/colm/"
    author = "Bincrafters <bincrafters@gmail.com>"
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
    _autotools = None

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        source_url = "http://www.colm.net/files/colm/colm-"
        sha256 = "7b545d74bd139f5c622975d243c575310af1e4985059a1427b6fdbb1fb8d6e4d"
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

    def _configure_autotools(self):
        if not self._autotools:
            args = [ "--enable-shared=%s" % ("yes" if self.options.shared else "no"),
                     "--enable-static=%s" % ("no" if self.options.shared else "yes"),
                     "--with-pic=%s" % ("yes" if self.options.fPIC else "no") ]
            self._autotools = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)
            self._autotools.configure(args=args)
        return self._autotools

    def build(self):
        if self.settings.compiler == "Visual Studio":
            self._remove_headers()
            self._copy_cmake_files()
            cmake = self._configure_cmake()
            cmake.build()
        else:
            with tools.chdir(self._source_subfolder):
                autotools = self._configure_autotools()
                autotools.make()

    def package(self):
        self.copy(pattern="COPYING", dst="licenses", src=self._source_subfolder)
        if self.settings.compiler == "Visual Studio":
            cmake = self._configure_cmake()
            cmake.install()
        else:
            with tools.chdir(self._source_subfolder):
                autotools = self._configure_autotools()
                autotools.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
