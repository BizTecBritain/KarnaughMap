import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="KarnaughMap",
    version="1.0.1",
    author="Alexander Bisland",
    author_email="biztecbritain@gmail.com",
    description="Dependency-free library to create Karnaugh Map objects which can be solved and manipulated (GUI and "
                "CLI included)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BizTecBritain/KarnaughMap",
    project_urls={
        "Bug Tracker": "https://github.com/BizTecBritain/KarnaughMap/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)