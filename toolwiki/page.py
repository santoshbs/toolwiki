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
    total = count_male + count_female
    threshold_m = count_male/total
    threshold_f =  1 - threshold_m

    ##assign gender, if above threshold
    if threshold_m >= gender_threshold:
        return ('male', threshold_m)
    if threshold_f >= gender_threshold:
        return ('female', threshold_f)

    return ('unknown', max(threshold_m, threshold_f))



