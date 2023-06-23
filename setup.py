import setuptools

with open("README.md", "r", encoding = "utf-8") as file:
    read_me = file.read()

with open("requirements.txt", "r") as file:
    requirements = file.read().splitlines()

setuptools.setup(
    name = "water_drop_detection",
    version = "0.7",
    author = "Aleksandr Leisle, Sofia Volodina, Alina Shitenko",
    author_email = "a.leisle@g.nsu.ru, s.volodina@g.nsu.ru, a.shitenko@g.nsu.ru",
    description = "A neural network that detects water drops on the surface from an image.",
    long_description = read_me,
    long_description_content_type = "text/markdown",
    project_urls = {
        'Documentation': 'https://github.com/HerrPhoton/Water_drop_detection/blob/master/Documentation.pdf',
        'Bug Tracker': 'https://github.com/HerrPhoton/Water_drop_detection/issues',
        'Homepage': 'https://github.com/HerrPhoton/Water_drop_detection',
    },
    packages = ['water_drop_detection', 'water_drop_detection/NN', 'water_drop_detection/ui'],
    install_requires = requirements,
    classifiers = [
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    python_requires = '==3.9.*',
)
