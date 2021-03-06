import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="heliPypter",
    version="0.0.7",
    author="Benjamin Crews",
    author_email="aceF22@gmail.com",
    description="A package for rotorcraft performance evaluation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/czarified/helipypter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)