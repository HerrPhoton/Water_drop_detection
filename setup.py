import setuptools

with open("README.md") as file:
    read_me = file.read()

setuptools.setup(
    name = "water-drops-detection",
    version = "0.1",
    author = "Aleksandr Leisle, Sofia Volodina, Alina Shitenko",
    author_email = "a.leisle@g.nsu.ru, s.volodina@g.nsu.ru, a.shitenko@g.nsu.ru",
    description = "A program that detects water drops on the surface",
    long_description = read_me,
    long_description_content_type = "text/markdown",
    url = "https://github.com/HerrPhoton/Water_drop_detection",
    packages = ['src'],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires = '==3.9',
)