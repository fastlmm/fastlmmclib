import os
import platform
import shutil
import site
import sys
from distutils.command.clean import clean as Clean

import numpy
from setuptools import Extension, setup

# Work around https://github.com/pypa/pip/issues/7953
site.ENABLE_USER_SITE = "--user" in sys.argv[1:]

# Version number
version = "0.0.7a1"


def readme():
    with open("README.md") as f:
        return f.read()


try:
    from Cython.Distutils import build_ext
except ImportError:
    use_cython = False
else:
    use_cython = True


class CleanCommand(Clean):
    description = "Remove build directories, compiled files (including .pyc)"

    def run(self):
        Clean.run(self)
        if os.path.exists("build"):
            shutil.rmtree("build")
        for dirpath, dirnames, filenames in os.walk("."):
            for filename in filenames:
                if (
                    filename.endswith(".so")
                    or filename.endswith(".pyd")
                    or (
                        use_cython and filename.find("wrap_qfc.cpp") != -1
                    )  # remove automatically generated source file
                    or filename.endswith(".pyc")
                ):
                    tmp_fn = os.path.join(dirpath, filename)
                    print("removing", tmp_fn)
                    os.unlink(tmp_fn)


# set up macros
if platform.system() == "Darwin":
    macros = [("__APPLE__", "1")]
    extra_compile_args0 = []
elif platform.system() == "Windows":
    macros = [("_WIN32", "1")]
    extra_compile_args0 = ["/EHsc"]
else:
    macros = [("_UNIX", "1")]
    extra_compile_args0 = []

# see http://stackoverflow.com/questions/4505747/how-should-i-structure-a-python-package-that-contains-cython-code
print("use_cython? {0}".format(use_cython))
if use_cython:
    ext_modules = [
        Extension(
            name="fastlmmclib.quadform.qfc_src.wrap_qfc",
            language="c++",
            sources=[
                "fastlmmclib/quadform/qfc_src/wrap_qfc.pyx",
                "fastlmmclib/quadform/qfc_src/QFC.cpp",
            ],
            include_dirs=[numpy.get_include()],
            extra_compile_args=extra_compile_args0,
            define_macros=macros,
        ),
    ]
    cmdclass = {"build_ext": build_ext, "clean": CleanCommand}
else:
    ext_modules = [
        Extension(
            name="fastlmmclib.quadform.qfc_src.wrap_qfc",
            language="c++",
            sources=[
                "fastlmmclib/quadform/qfc_src/wrap_qfc.cpp",
                "fastlmmclib/quadform/qfc_src/QFC.cpp",
            ],
            include_dirs=[numpy.get_include()],
            extra_compile_args=extra_compile_args0,
            define_macros=macros,
        ),
    ]
    cmdclass = {}

for e in ext_modules:
    e.cython_directives = {"language_level": "3"}  # all are Python-3

setup(
    name="fastlmmclib",
    version=version,
    description="Fast GWAS C library",
    long_description=readme(),
    long_description_content_type="text/markdown",
    keywords="gwas bioinformatics LMMs MLMs linear mixed models genomics genetics python",
    url="https://fastlmm.github.io/",
    author="FaST-LMM Team",
    author_email="fastlmm-dev@python.org",
    project_urls={
        "Bug Tracker": "https://github.com/fastlmm/fastlmmclib/issues",
        "Source Code": "https://github.com/fastlmm/fastlmmclib",
    },
    license="Apache 2.0",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python",
    ],
    packages=[  # basically, everything with a __init__.py
        "fastlmmclib",
        "fastlmmclib/quadform",
        "fastlmmclib/quadform/qfc_src",
    ],
    package_data={},
    install_requires=["numpy"],
    cmdclass=cmdclass,
    ext_modules=ext_modules,
)
