# This file is required to create a python library

from setuptools import find_packages, setup
from pathlib import Path

this_dir = Path('README.md')
# check beforehand
if this_dir.exists():
    this_dir = this_dir.resolve()


long_descr = (this_dir).read_text()
# with open("%s\\README.md"%this_dir, "r") as file:
    # long_descr = file.read()

setup(
    name='echr_extractor',
    packages=find_packages(include=['echr_extractor']),
    version='1.0.0',
    description='Library for extracting ECHR data',
    author='LawTech Lab',
    license='MIT',
    install_requires=["requests==2.26.0","pandas","beautifulsoup4"],
    author_email='@student.maastrichtuniversity.nl',
    keywords=['echr', 'extractor', 'european', 'convention', 'human', 'rights', 'european convention', 'human rights',
              'european convention on human rights'],
    long_description=long_descr,
    long_description_content_type='text/markdown',
    project_urls={
        "Bug Tracker": "https://github.com/maastrichtlawtech/case-law-explorer",
        "Build Source": "https://github.com/maastrichtlawtech/extraction_libraries",
    },
)