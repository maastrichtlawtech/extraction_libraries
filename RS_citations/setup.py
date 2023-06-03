# This file is required to create a python library

from setuptools import find_packages, setup
from pathlib import Path

p = Path("README.md")
long_descr = p.read_text()

setup(
    name='rechtspraak_citations_extractor',
    packages=find_packages(include=['rechtspraak_citations_extractor']),
    version='1.0.4',
    description='Library for extracting rechtspraak citations via LIDO',
    author='LawTech Lab',
    license='MIT',
    install_requires=['requests>=2.26.0', 'python_dotenv==0.15.0', 'pandas >=1.2.5','urllib3>=1.26.12','lxml>=4.6.3'],
    author_email='p.lewandowski@student.maastrichtuniversity.nl',
    keywords=['rechtspraak', 'citations', 'rechtspraak citations', 'RS citations'],
    long_description=long_descr,
    long_description_content_type='text/markdown',
    project_urls={
        "Bug Tracker": "https://github.com/maastrichtlawtech/extraction_libraries",
        "Build Source": "https://github.com/maastrichtlawtech/extraction_libraries",
    },
)