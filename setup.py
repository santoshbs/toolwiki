#https://towardsdatascience.com/how-to-build-your-first-python-package-6a00b02635c9
#https://realpython.com/pypi-publish-python-package/

import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent ## The directory containing this file
README = (HERE / "README.md").read_text() ## The text of the README file

setup(
    name='toolwiki',
    version='0.1.13',
    author='Santosh Srinivas',
    author_email='santosh.b.srinivas@outlook.com',
    description='A python library to extract information from Wikipedia pages.',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/santoshbs/toolwiki',
    license='MIT',
    packages=find_packages(),
    install_requires=['numpy', 'pandas', 'beautifulsoup4', 'lxml'],
    keywords=['python', 'html table rowspan colspan', 'scrape parse extract', 'dataframe'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',],
)
