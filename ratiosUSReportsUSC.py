import shutil
import zipfile
import lzma
import json
import requests
from pathlib import Path
from eyecite import clean_text
from extractionHelpers import process


# download data file if not already downloaded
download_url = "https://case.law/download/bulk_exports/latest/by_reporter/case_text_restricted/us/us_text.zip"
output_path = "us_text.zip"

if not Path(output_path).exists():
    print("Downloading to %s ..." % output_path)
    with open(output_path, 'wb') as out_file:
        shutil.copyfileobj(requests.get(download_url, stream=True, headers={
                           'Authorization': 'Token ***REMOVED***'}).raw, out_file)
    print("Done.")


# yield case texts from data file
def get_case_texts():
    with zipfile.ZipFile(output_path, 'r') as zip_archive:
        xz_path = next(path for path in zip_archive.namelist()
                       if path.endswith('/data.jsonl.xz'))
        with zip_archive.open(xz_path) as xz_archive, lzma.open(xz_archive) as jsonlines:
            for line in jsonlines:
                record = json.loads(str(line, 'utf-8'))
                case_body = record['casebody']['data']
                # case_text = "\n".join(
                #     [case_body['head_matter']]+[opinion['text'] for opinion in case_body['opinions']])
                case_text = "\n".join(
                    [opinion['text'] for opinion in case_body['opinions']])
                yield record['frontend_url'], case_text


def custom_cleaner(s):
    return s.replace('’', '\'').replace('‘', '\'').replace('”', '"').replace('“', '"').replace('´', '\'').replace('–', '-').replace("U. S. C. ", 'USC')


def cleaned_text(s):
    return clean_text(s, ['html', 'all_whitespace', 'underscores', custom_cleaner]) if len(s) > 0 else ""


i = 0
# extract citations
for url, case_text in get_case_texts():
    case_text = cleaned_text(case_text)
    #i += 1
    # print(i)
    if "denied." in case_text[:200]:
        continue
    if "U.S.C." in case_text and len(case_text) < 10000:
        print(case_text)
        exit()
