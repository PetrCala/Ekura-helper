from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = [
    'numpy>=1.22.0',
    'Pillow>=9.3.0',
    'opencv-python>=4.5.5.64', #cv2
    'pynput>=1.7.6',
    'pytesseract>=0.3.9',
    'pypiwin32>=223',
    'pywin32>=303' #win32gui
]

setup(
    name="ekura_helper",
    version="0.0.1",
    author="Petr Čala",
    author_email = "cala.p@seznam.cz",
    description = "Automate tasks in an MMORPG",
    long_description = readme,
    long_description_content_type = "text/markdown",
    url = "https://github.com/PetrCala/Ekura-miner",
    packages = find_packages(),
    install_requires = requirements,
    classifiers = [
        "Programming Language :: Python :: 3.8",
        # License :: ...
    ],
)