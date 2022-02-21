import numpy as np
import pandas as pd
import spacy
from bs4 import BeautifulSoup
import urllib.request
import unicodedata

def get_gender(url = '', gender_threshold = 0.8):
    """
    Get gender information based on ratio of male (e.g., he) and female (e.g., she) pronouns on a Wikipedia page.
    :param url: (str) wikipedia page url (e.g., https://en.wikipedia.org/wiki/Mickey_Gall).
    :param gender_threshold: (int) ratio of gender pronouns to be used as minimum when determining gender.
    :return: (tuple) (gender, threshold).
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
    soup= BeautifulSoup(page, "html.parser")
    tag = soup.body
    pg_strings = [s for s in tag.strings]
    pg_content = unicodedata.normalize('NFKD', ' '.join(pg_strings))

    ##nlp tokenize
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(pg_content)
    count_male= 0
    count_female= 0

    ##get female/male pronoun ratio
    for token in doc:
        if token.text.lower() in ['he', 'his', 'him', 'himself']:
            count_male = count_male + 1
        if token.text.lower() in ['she', 'her', 'hers', 'herself']:
            count_female = count_female + 1

    ##calculate threshold achieved
    threshold_m = 0
    threshold_f = 0
    total = count_male + count_female
    if total > 0:
        threshold_m = count_male/total
        threshold_f =  1 - threshold_m

        ##assign gender, if above threshold
        if threshold_m >= gender_threshold:
            return ('male', threshold_m)
        if threshold_f >= gender_threshold:
            return ('female', threshold_f)

    return ('unknown', max(threshold_m, threshold_f))


def get_category_members(url='', type=['pages', 'subcategories']):
    """
    Extract pages and subcategories of a given Wikipedia category.
    :param url: (str) wikipedia page url (e.g., https://en.wikipedia.org/wiki/Category:Governance).
    :param type: (list) if 'pages' in list, get pages; if 'subcategories' in list, get subcategories.
    :return: (dataframe) category members.
    """

    url_prefix = 'https://en.wikipedia.org'

    ##check params
    valid_type = ['pages', 'subcategories']
    for e in type:
        assert e in valid_type, "Invalid type supplied as parameter. Valid values include = " + ', '.join(valid_type)

    ##read webpage
    assert url != '', "No URL provided."
    try:
        page_exists= False
        page= urllib.request.urlopen(url)
        page_exists= True
    except:
        pass
    assert page_exists, "Page does not exist."
    soup = BeautifulSoup(page, "html.parser")

    bFirstPage = True
    while True:
        total = 0

        ##get pages
        if 'pages' in type:
            try:
                cat_pages = soup.find(id='mw-pages').find(class_='mw-content-ltr')
                pages = cat_pages.findChildren('a', recursive=True)
                total = total + len(pages)
            except:
                pass

        ##get subcategories
        if 'subcategories' in type:
            try:
                cat_subcats = soup.find(id='mw-subcategories').find(class_='mw-content-ltr')
                subcats = cat_subcats.findChildren('a', recursive=True)
                total = total + len(subcats)
            except:
                pass

        ##create dataframe to store members
        header_list = ['category', 'type', 'title', 'url']
        df_table_all = pd.DataFrame(index=np.arange(total), columns=header_list)
        df_table_all = df_table_all.replace({np.nan: None})

        ##assign category name
        title = unicodedata.normalize('NFKD', u' '.join(soup.find('title').findAll(text=True)))
        title = title.replace(' - Wikipedia', '')
        df_table_all['category'] = title

        ##populate pages
        rstart = 0
        if 'pages' in type:
            for i, tag in enumerate(pages):
                df_table_all.loc[i, 'type'] = 'pages'
                df_table_all.loc[i, 'title'] = unicodedata.normalize('NFKD', u' '.join(tag.findAll(text=True)))
                df_table_all.loc[i, 'url'] = tag.get('href')
            rstart = i + 1

        ##populate subcategories
        if 'subcategories' in type:
            for i, tag in enumerate(subcats):
                df_table_all.loc[rstart + i, 'type'] = 'subcategories'
                df_table_all.loc[rstart + i, 'title'] = unicodedata.normalize('NFKD', u' '.join(tag.findAll(text=True)))
                df_table_all.loc[rstart + i, 'url'] = tag.get('href')

        if bFirstPage:
            bFirstPage = False
            df_out = df_table_all
        else:
            df_out = pd.concat([df_out, df_table_all], ignore_index=True)

        ##check if nextpage exists
        nextPage = soup.find(lambda tag:tag.name == 'a' and 'next page' in tag.text)
        if nextPage:
            url = url_prefix + nextPage.get('href')
            page = urllib.request.urlopen(url)
            soup = BeautifulSoup(page, "html.parser")
        else:
            break

    return df_out

