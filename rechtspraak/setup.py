# This file is required to create a python library

from setuptools import find_packages, setup
from pathlib import Path

this_dir = Path('rechtspraak_extractor')
long_descr = (this_dir / "README.md").read_text()

setup(
    name='rechtspraak_extractor',
    packages=find_packages(include=['rechtspraak_extractor']),
    version='1.0.39',
    description='Library for extracting rechtspraak data',
    author='LawTech Lab',
    license='MIT',
    install_requires=['bs4', 'lxml==4.6.3', 'requests==2.26.0', 'xmltodict==0.13.0', 'python_dotenv==0.15.0'],
    author_email='pranav.bapat@student.maastrichtuniversity.nl',
    keywords=['rechtspraak', 'extractor'],
    long_description=long_descr,
    long_description_content_type='text/markdown',
    project_urls={
        "Bug Tracker": "https://github.com/maastrichtlawtech/case-law-explorer",
    },
)