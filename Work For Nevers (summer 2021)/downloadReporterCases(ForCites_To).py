import os
import json
import requests

filename = 'fedReporterData(cites_to).json'

NUM_CASES = 10000
url = 'https://api.case.law/v1/cases/?reporter=983&page_size=' + str(NUM_CASES)
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
        responsesToSave["results"].append(case)

    url = responses["next"]
    print("done")


responsesToSave = {"results": []}
callNextResponse(responsesToSave)
while (url != None):
    callNextResponse(responsesToSave)

with open(filename, 'w') as f:
    json.dump(responsesToSave, f)
