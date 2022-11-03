# This file is required to create a python library
# And this file is directly copied from rechspraak :)

from setuptools import find_packages, setup
from pathlib import Path

p = Path("README.md")
long_descr = p.read_text()

setup(
    name='cellar_extractor',
    packages=find_packages(include=['cellar_extractor']),
    version='1.0.10',
    description='Library for extracting cellar data',
    author='LawTech Lab',
    license='MIT',
    install_requires=['bs4','SPARQLWrapper==2.0.0', 'requests==2.26.0', 'pandas==1.2.5'],
    author_email='p.lewandowski@student.maastrichtuniversity.nl',
    keywords=['cellar', 'extractor'],
    long_description=long_descr,
    long_description_content_type='text/markdown',
    project_urls={
        "Bug Tracker": "https://github.com/maastrichtlawtech/case-law-explorer",
    },
)