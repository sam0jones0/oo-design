from setuptools import setup, find_packages

setup(
    name="casino",
    version="0.0.1",
    packages=find_packages(include=["casino", "casino.*"]),
)
