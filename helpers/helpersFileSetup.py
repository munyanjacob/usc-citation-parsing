def download(download_url, output_path):
    import shutil
    import requests
    from pathlib import Path
    from secret import caselawToken

    if not Path(output_path).exists():
        print("Downloading to %s ..." % output_path)
        with open(output_path, 'wb') as out_file:
            shutil.copyfileobj(requests.get(download_url, stream=True, headers={
                'Authorization': 'Token ' + caselawToken}).raw, out_file)
        print("Done.")


# yield case texts from data file
def get_case_texts(output_path):
    import zipfile
    import json
    import lzma
    with zipfile.ZipFile(output_path, 'r') as zip_archive:
        xz_path = next(path for path in zip_archive.namelist()
                       if path.endswith('/data.jsonl.xz'))
        with zip_archive.open(xz_path) as xz_archive, lzma.open(xz_archive) as jsonlines:
            for line in jsonlines:
                record = json.loads(str(line, 'utf-8'))
                case_body = record['casebody']['data']
                case_text = "\n".join(
                    [opinion['text'] for opinion in case_body['opinions']])
                yield case_text, record['decision_date'][:4], record['citations'][0]['cite'], record['court']['name_abbreviation']


def test_process(output_path):
    for case_text, case_year, case_cite, case_court in get_case_texts(output_path):
        continue


if __name__ == '__main__':
    download_url = "https://case.law/download/bulk_exports/latest/by_reporter/case_text_restricted/us/us_text.zip"
    output_path = "us_text.zip"
    download(download_url, output_path)
    test_process(output_path)
