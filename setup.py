import setuptools

with open("README.md", "r", encoding = "utf-8") as file:
    read_me = file.read()

with open("requirements.txt", "r") as file:
    requirements = file.read().splitlines()

setuptools.setup(
    name = "water-drops-detection",
    version = "0.4",
    author = "Aleksandr Leisle, Sofia Volodina, Alina Shitenko",
    author_email = "a.leisle@g.nsu.ru, s.volodina@g.nsu.ru, a.shitenko@g.nsu.ru",
    description = "A neural network that detects water drops on the surface from an image.",
    long_description = read_me,
    long_description_content_type = "text/markdown",
    project_urls = {
        'Homepage': 'https://github.com/HerrPhoton/Water_drop_detection',
        'Bug Tracker': 'https://github.com/HerrPhoton/Water_drop_detection/issues',
    },
    packages = setuptools.find_packages(),
    install_requires = requirements,
    classifiers = [
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    python_requires = '==3.9.*',
)