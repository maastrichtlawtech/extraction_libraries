# This file is required to create a python library
# And this file is directly copied from rechspraak :)

from setuptools import find_packages, setup
from pathlib import Path

this_dir = Path('cellar_extractor')
long_descr = (this_dir / "README.md").read_text()

setup(
    name='cellar_extractor',
    packages=find_packages(include=['cellar_extractor']),
    version='1.0.0',
    description='Library for extracting cellar data',
    author='LawTech Lab',
    license='MIT',
    install_requires=['bs4', 'lxml==4.6.3', 'requests==2.26.0', 'xmltodict==0.13.0', 'python_dotenv==0.15.0'],
    author_email='p.lewandowski@student.maastrichtuniversity.nl',
    keywords=['cellar', 'extractor'],
    long_description=long_descr,
    long_description_content_type='text/markdown',
    project_urls={
        "Bug Tracker": "https://github.com/maastrichtlawtech/case-law-explorer",
    },
)