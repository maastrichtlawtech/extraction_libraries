# This file is required to create a python library

from setuptools import find_packages, setup
from pathlib import Path

p = Path("README.md")
long_descr = p.read_text()

setup(
    name='echr_extractor',
    packages=find_packages(include=['echr_extractor']),
    version='1.0.7',
    description='Library for extracting ECHR data',
    author='LawTech Lab',
    license='MIT',
    install_requires=["requests~=2.26.0","pandas~=1.2.5","beautifulsoup4~=4.9.3"],
    author_email='a.gade@student.maastrichtuniversity.nl',
    keywords=['echr', 'extractor', 'european', 'convention', 'human', 'rights', 'european convention', 'human rights',
              'european convention on human rights'],
    long_description=long_descr,
    long_description_content_type='text/markdown',
    project_urls={
        "Bug Tracker": "https://github.com/maastrichtlawtech/case-law-explorer",
        "Build Source": "https://github.com/maastrichtlawtech/extraction_libraries",
    },
)