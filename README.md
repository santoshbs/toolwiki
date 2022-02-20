# toolwiki 

This is a python library to extract information from Wikipedia pages. 

## Contents

- `tables.py` module includes function to extract information from a wikipedia table as a pandas dataframe.
- `pages.py` module includes function to extract inferred gender based on the ratio of male and female pronouns on a wikipedia page.

## Installation

You can install `toolwiki` package from [PyPI](https://pypi.org/project/toolwiki/):

    python -m pip install toolwiki

`toolwiki` is supported on Python 3.7 and above.

## How to use

You can use this package in your own Python code by importing from the `toolwiki` package:

    >>> from toolwiki import tables
    >>> dfs= tables.get_dataframes(url='https://en.wikipedia.org/wiki/List_of_UFC_events', by_class='wikitable', table_indices= [], raw=False)
    [                                         Event  ...  Ref.
    1                                      UFC 276  ...   [9]
    2                          UFC Fight Night 211  ...  [10]
    ..   ...                                         ...  ...        ...    ...
    14                         UFC Fight Night 202  ...  [20]
    15            UFC Fight Night: Walker vs. Hill  ...  [21]
    [15 rows x 5 columns],        #                                       Event  ... Attendance   Ref.
    1    593          UFC 271: Adesanya vs. Whittaker II  ...     17,872   [22]
    2    592  UFC Fight Night: Hermansson vs. Strickland  ...        N/A   [23]
    ..   ...                                         ...  ...        ...    ...
    601  002                           UFC 2: No Way Out  ...      2,000  [558]
    602  001                        UFC 1: The Beginning  ...      7,800  [559]
    [602 rows x 7 columns]]
    

    >>> from toolwiki import page
    >>> print(page.get_gender('https://en.wikipedia.org/wiki/Karolina_Kowalkiewicz', gender_threshold=0.8)
    ('female', '1.0')
