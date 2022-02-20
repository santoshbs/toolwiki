import numpy as np
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup
import copy
import unicodedata

def get_dataframes(url = '', by_class= 'wikitable', table_indices= [], raw=False, header=True, errors_ignore=True):
    """
    Extract information from tables on a Wikipedia page.
    Handles table cells with non-conflicting rowspan and colspan attributes.
    Note that this function assumes that the first row is a header.

    :param url: wikipedia page url (e.g., https://en.wikipedia.org/wiki/List_of_UFC_events).
    :param by_class: class name of table to fetch; if None, fetches all tables.
    :param table_indices: list of indices of tables to process (e.g., [0, 2, 5]); defaults to all tables.
    :param raw: get raw inner html (useful for downstream processing); or (default) get raw text from each cell.
    :param header: assume that first row is a header (default); create a generic header column (['HEADER_1', 'HEADER_2'...]).
    :param errors_ignore: if True, tables that cannot be processed will be skipped (default); if False, aborts when tables cannot be processed.
    :return: list of dataframes extracted from tables in wikipedia page.
    """

    ##read webpage
    assert url != '', "No URL provided."
    try:
        page_exists= False
        page= urllib.request.urlopen(url)
        page_exists= True
    except:
        pass
    assert page_exists, "Page does not exist."
    soup= BeautifulSoup(page, "lxml")

    ##find tables
    if by_class is None:
        tables= soup.find_all('table')
    else:
        tables= soup.find_all('table', class_=by_class)
    assert len(tables) > 0, "No tables found on the page."
    if len(table_indices) > 0:
        ##table index check
        for ti in table_indices:
            assert type(ti) == int, "Non-integer table index provided."
        ##filter tables
        tables= [e for i, e in enumerate(tables) if i in table_indices]
    assert len(tables) > 0, "No tables matching the provided table indices found on the page."

    ##0. process one table at a time
    list_pds= []
    for table in tables:
        try:
            bErrorTable = True
            trs = table.findAll('tr')
            if trs is not None and len(trs) > 0:
                ##1. find what max columns to assign by scanning the entire table
                max_col = 0
                for tr in trs:
                    ncol = 0
                    children = tr.findChildren(recursive=False)
                    for i in range(0, len(children)):
                        cspan = int(children[i].get('colspan')) if children[i].get('colspan') else 1
                        ncol = ncol + cspan
                    max_col = max(max_col, ncol)

                ##2. assign header as column names
                header_list= []
                if header:
                    children = trs[0].findChildren(recursive=False)
                    for i in range(0, len(children)):
                        colname = unicodedata.normalize('NFKD', u' '.join(children[i].findAll(text=True)).strip())
                        if not colname:
                            colname= 'HEADER_' + str(i+1)
                        header_list.append(colname)
                    while len(header_list) < max_col:
                        header_list.append('HEADER_' + str(len(header_list) + 1))
                else:
                    while len(header_list) < max_col:
                        header_list.append('HEADER_' + str(len(header_list) + 1))

                ##3. create dataframe to capture table values
                df_table_values = pd.DataFrame(index=np.arange(len(trs)), columns=header_list)
                df_table_values = df_table_values.replace({np.nan: None})

                ##4. prepare tds that have both rowspan and colspan
                rstart = 1 if header else 0
                for i in range(rstart, len(trs)):
                    children= trs[i].findChildren('td', recursive=False)
                    if not children:
                        children= trs[i].findChildren('th', recursive=False)

                    for j in range(0, len(children)):
                        cspan = int(children[j].get('colspan')) if children[j].get('colspan') else 1
                        rspan = int(children[j].get('rowspan')) if children[j].get('rowspan') else 1
                        if cspan > 1 and rspan > 1:
                            del children[j]['colspan']
                            for c in range(1, cspan):
                                td_copy = copy.copy(children[j])
                                children[j].insert_after(td_copy)

                ##5. assign cell values bases on table spans
                for i in range(rstart, len(trs)):
                    val_row = i
                    children= trs[i].findChildren('td', recursive=False)
                    if not children:
                        children= trs[i].findChildren('th', recursive=False)
                    for j in range(0, len(children)):
                        ##what value to assign to cell(s)
                        if raw:
                            val = children[j].decode_contents()
                        else:
                            val = unicodedata.normalize('NFKD', u' '.join(children[j].findAll(text=True)).strip())

                        val_col = j
                        while True:
                            if df_table_values.iloc[val_row, val_col] is None:
                                break
                            val_col= val_col + 1
                        df_table_values.iloc[val_row, val_col]= val

                        cspan = int(children[j].get('colspan')) if children[j].get('colspan') else 1
                        rspan = int(children[j].get('rowspan')) if children[j].get('rowspan') else 1

                        ##handle when colspan alone is present
                        if cspan > 1 and rspan == 1:
                            for c in range(val_col+1, val_col+cspan):
                                df_table_values.iloc[val_row, c] = val

                        ##handle when rowspan alone is present
                        if rspan > 1 and cspan == 1:
                            c= val_col
                            for r in range(val_row+1, val_row+rspan):
                                while True:
                                    if df_table_values.iloc[r, c] is None:
                                        break
                                    c = c + 1
                                df_table_values.iloc[r, c] = val


                ##6. drop first row and add to list
                if header:
                    df_table_values= df_table_values.iloc[1:, :]
                    df_table_values.reset_index(inplace=True, drop= True)
                list_pds.append(df_table_values)
                bErrorTable = False
        except:
            pass
        if not errors_ignore:
            assert not bErrorTable, "Error processing table on the page."

    return list_pds
