import os
import json
import requests

filename = 'fedReporterData.json'

NUM_CASES = 10000
url = 'https://api.case.law/v1/cases/?reporter=983&full_case=true&page_size=' + \
    str(NUM_CASES)
responses = 0


def callNextResponse(responsesToSave):
    global url
    global responses

    response = requests.get(
        url,
        headers={
            'Authorization': 'Token '
        })

    responses = response.json()

    for case in responses["results"]:
        if len(case["casebody"]["data"]["opinions"]) == 0:
            continue
        else:
            responsesToSave["results"].append(case)

    url = responses["next"]


responsesToSave = {"results": []}
callNextResponse(responsesToSave)
while (url != None):
    callNextResponse(responsesToSave)

with open(filename, 'w') as f:
    json.dump(responsesToSave, f)
