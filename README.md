# toolwiki 

This is a python library to extract information from Wikipedia pages. 

## Contents

- `tables.py` module includes function to extract information from a wikipedia table as a pandas dataframe.
- `pages.py` module includes:
  - function to extract inferred gender based on the ratio of male and female pronouns on a wikipedia page.
  - function to get all category members.

## Installation

You can install `toolwiki` package from [PyPI](https://pypi.org/project/toolwiki/):

    python -m pip install toolwiki

`toolwiki` is supported on Python 3.7 and above.

## How to use

You can use this package in your own Python code by importing from the `toolwiki` package:

    >>> from toolwiki import tables
    >>> dfs= tables.get_dataframes(url='https://en.wikipedia.org/wiki/List_of_UFC_events', by_class='wikitable', table_indices= [], raw=False)
    >>> dfs
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
    >>> page.get_gender('https://en.wikipedia.org/wiki/Karolina_Kowalkiewicz', gender_threshold=0.8)
    ('female', '1.0')

    >>> from toolwiki import page
    >>> page.get_category_members('https://en.wikipedia.org/wiki/Category:Leadership', type=['pages', 'subcategories'])
               category           type                                   title                                           url
    0   Category:Leadership          pages                              Leadership                              /wiki/Leadership
    1   Category:Leadership          pages                                3C-model                                /wiki/3C-model
    2   Category:Leadership          pages  African Nutrition Leadership Programme  /wiki/African_Nutrition_Leadership_Programme
    3   Category:Leadership          pages                      Agentic leadership                      /wiki/Agentic_leadership
    4   Category:Leadership          pages                        Agile leadership                        /wiki/Agile_leadership
    ..                  ...            ...                                     ...                                           ...
    78  Category:Leadership  subcategories                     Leadership scholars            /wiki/Category:Leadership_scholars
    79  Category:Leadership  subcategories                      Leadership studies             /wiki/Category:Leadership_studies
    80  Category:Leadership  subcategories                              Management                     /wiki/Category:Management
    81  Category:Leadership  subcategories                  Positions of authority         /wiki/Category:Positions_of_authority
    82  Category:Leadership  subcategories                     Leadership training            /wiki/Category:Leadership_training
    
    [83 rows x 4 columns]
