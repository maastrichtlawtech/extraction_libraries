# This file is required to create a python library
# And this file is directly copied from rechspraak :)

from setuptools import find_packages, setup
from pathlib import Path

p = Path("README.md")
long_descr = p.read_text()

setup(
    name='cellar_extractor',
    packages=find_packages(include=['cellar_extractor', 'cellar_extractor.operative_extractions']),
    version='1.1.0',
    description='Library for extracting cellar data',
    author='LawTech Lab',
    license='MIT',
    install_requires=['bs4','SPARQLWrapper', 'requests', 'pandas','xmltodict>=0.9.0','tqdm'],
    author_email='p.lewandowski@student.maastrichtuniversity.nl',
    keywords=['cellar', 'extractor'],
    long_description=long_descr,
    long_description_content_type='text/markdown',
    project_urls={
        "Bug Tracker": "https://github.com/maastrichtlawtech/extraction_libraries",
        "Build Source": "https://github.com/maastrichtlawtech/extraction_libraries",
    },
)
