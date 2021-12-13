
from eyecite import get_citations, clean_text, resolve_citations, annotate_citations
from eyecite.models import FullCaseCitation, Resource
from eyecite.resolve import resolve_full_citation
from eyecite.tokenizers import HyperscanTokenizer

import requests

opinion_url = 'https://api.case.law/v1/cases/3922151/?full_case=true'
#opinion_url = 'https://api.case.law/v1/cases/3916937/?full_case=true'


opinion_text = " ".join([opinion["text"] for opinion in requests.get(
    opinion_url,
    headers={
        'Authorization': 'Token ***REMOVED***'
    }).json()["casebody"]["data"]["opinions"]])


def custom_cleaner(s):
    return s.replace('’', '\'').replace('‘', '\'').replace('”', '"').replace('“', '"').replace('´', '\'').replace('–', '-')


opinion_text = "Test 1 U.S.C. § 1 Act of March 2,1907, c. 2564, 34 Stat.1246'; U.S.C., § 682, Title 18, and § 345, Title 28; Acts January 31, 1928, c. 14, 45 Stat. 54, and April 26, 1928, e. 440, 45 Stat. 466."
cleaned_text = clean_text(
    opinion_text, ['html', 'all_whitespace', 'underscores', custom_cleaner])


citations = get_citations(cleaned_text)


'''
U.S.C.
U.S. Code
United States Code

Find any variation of USC

. \w{2,}.*<USC variation>.*."? \w{2,}


'''


print(f'Extracted {len(citations)} citations.')
for c in citations:
    print(c, "\n")
print(f'First citation:\n {citations[0]}')
