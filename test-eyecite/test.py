
from eyecite import get_citations, clean_text, resolve_citations, annotate_citations
from eyecite.models import FullCaseCitation, Resource
from eyecite.resolve import resolve_full_citation
from eyecite.tokenizers import HyperscanTokenizer

import requests

opinion_url = 'https://api.case.law/v1/cases/3922151/?full_case=true'

opinion_text = " ".join([opinion["text"] for opinion in requests.get(
    opinion_url,
    headers={
        'Authorization': 'Token ***REMOVED***'
    }).json()["casebody"]["data"]["opinions"]])

cleaned_text = clean_text(opinion_text, ['html', 'all_whitespace'])

#print(cleaned_text[:1000])


citations = get_citations(cleaned_text)


from eyecite import get_citations

text = """
    Act of March 2,1907, c. 2564, 34 Stat.1246'; U.S.C., § 682, Title 18, and § 345, Title 28; Acts January 31, 1928, c. 14, 45 Stat. 54, and April 26, 1928, e. 440, 45 Stat. 466.
"""

print(get_citations(text))



print(f'Extracted {len(citations)} citations.\n')
print(f'First citation:\n {citations[0]}')