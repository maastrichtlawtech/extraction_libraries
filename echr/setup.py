# This file is required to create a python library

from setuptools import find_packages, setup
from pathlib import Path

this_dir = Path('echr_extractor')
long_descr = (this_dir / "README.md").read_text()

setup(
    name='echr_extractor',
    packages=find_packages(include=['echr_extractor']),
    version='1.0.0',
    description='Library for extracting ECHR data',
    author='LawTech Lab',
    license='MIT',
    install_requires=[],
    author_email='pranav.bapat@student.maastrichtuniversity.nl',
    keywords=['echr', 'extractor', 'european', 'convention', 'human', 'rights', 'european convention', 'human rights',
              'european convention on human rights'],
    long_description=long_descr,
    long_description_content_type='text/markdown',
    project_urls={
        "Bug Tracker": "https://github.com/maastrichtlawtech/case-law-explorer",
    },
)