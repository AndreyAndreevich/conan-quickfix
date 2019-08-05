import os
from conans import ConanFile, CMake, tools


class QuickFixConan(ConanFile):
    name = "quickfix"
    version = "1.15.1"
    url = "https://github.com/quickfix/quickfix"
    author = "l.a.r.p@yandex.ru"
    license = "MIT"
    description = "QuickFIX C++ Fix Engine Library"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "ssl": [True, False]
    }
    default_options = {
        "ssl": False
    }
    generators = "cmake"

    def source(self):
        git = tools.Git(folder=self.name)
        git.clone("https://github.com/quickfix/quickfix")
        git.checkout("v%s" % self.version)
        os.rename(os.path.join(self.name, "CMakeLists.txt"),
                  os.path.join(self.name, "CMakeListsOriginal.txt"))
        fd = os.open(os.path.join(self.name, "CMakeLists.txt"),
                     os.O_RDWR | os.O_CREAT)
        os.write(fd, '''cmake_minimum_required(VERSION 3.0)
            project(cmake_wrapper)

            include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
            conan_basic_setup()

            set(CMAKE_CXX_STANDARD 17)

            include("CMakeListsOriginal.txt")
            '''.encode())
        os.close(fd)

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder=self.name)
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src=os.path.join(self.name, "include"))
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)