import shutil
import zipfile
import lzma
import json
import requests
from pathlib import Path
from eyecite import get_citations


# download data file if not already downloaded
download_url = "https://case.law/download/bulk_exports/latest/by_reporter/case_text_restricted/us/us_text.zip"
output_path = "us_text.zip"

if not Path(output_path).exists():
    print("Downloading to %s ..." % output_path)
    with open(output_path, 'wb') as out_file:
        shutil.copyfileobj(requests.get(download_url, stream=True, headers={
                           'Authorization': 'Token '}).raw, out_file)
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
                case_text = "\n".join(
                    [case_body['head_matter']]+[opinion['text'] for opinion in case_body['opinions']])
                yield record['frontend_url'], case_text


# extract citations
for url, case_text in get_case_texts():
    cites = get_citations(case_text)
    print(url, [c.corrected_citation() for c in cites])
