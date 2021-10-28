import os
import json
import requests

filename = 'fedReporterData.json'

NUM_CASES = 10000
url = 'https://api.case.law/v1/cases/?reporter=983&full_case=true&page_size=' + str(NUM_CASES)
responses = 0

def parseResponse():
	global responses
	i = 1
	data = responses["results"]

	for case in data:
		opinions = case["casebody"]["data"]["opinions"]
		print(i)
		i += 1

	return

def callNextResponse(responsesToSave):
	global url
	global responses

	response = requests.get(
    url,
    headers={
        'Authorization': 'Token ***REMOVED***'
    })

	responses = response.json()

	for case in responses["results"]:
		opinions = case["casebody"]["data"]["opinions"]
		if len(opinions) == 0:
			#print(case["frontend_pdf_url"])
			continue
		#elif opinions[0]["text"].endswith("denied."):
		else:
			responsesToSave["results"].append(case)

	url = responses["next"]
	print("done")



responsesToSave = {"results": []}
callNextResponse(responsesToSave)
while (url != None):
	callNextResponse(responsesToSave)

with open(filename, 'w') as f:
			json.dump(responsesToSave, f)