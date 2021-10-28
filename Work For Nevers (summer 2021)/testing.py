import lzma, json, re, os

with open('fedReporterData.json') as in_file:
	data = json.load(in_file)
	for case in data['results']:
		caseYear = case['decision_date'][:4]

		if caseYear == 1976:
			print(case)