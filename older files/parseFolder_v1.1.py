import lzma, json, re
with lzma.open("F.2d-20200303-text/data/data.jsonl.xz") as in_file:
	for line in in_file:
		case = json.loads(str(line,'utf8'))

		caseYear = case['decision_date']
		caseCitation = case['citations'][0]['cite']
		caseCourtAbbrev = case['court']['name_abbreviation']

		#print(caseYear, caseCitation, caseCourtAbbrev, sep='\n')

		regex1 = r'(?:\.["\'‘’“”]?\s(?=[^a-z]))((?:(?!\.["\'‘’“”]?\s(?:[^a-z]|$)).)*?(?:U\.?S\.?(?:C\.| Code)|USC).*?\.)(?:\s[A-Z]|["\'‘’“”]|$)'
		regex2 = r'\.\s((?:(?!\.\s).)*?\.\s(?:(?!\.\s).)*?\.\s(?:(?!\.\s).)*?;\s(?:(?!\.\s).)*?(?:U\.?S\.?(?:C\.| Code)|USC).*?\.)(?:\s[A-Z]|["\'‘’“”]|$)'
		regex3 = r'\.\s(["\'‘’“”](?:(?!\.["\'‘’“”]).)*?\.["\'‘’“”].{,6}(?:U\.?S\.?(?:C\.| Code)|USC).*?\.)(?:\s[^a-z]|$)'

		regex = regex1+'|'+regex2+'|'+regex3

		opinions = case['casebody']['data']['opinions']
		for opinion in opinions:
			print('test')
			if re.search(regex, opinion['text']):
				#print(opinion['text'])
				resp = [[i for i in m if i] for m in re.findall(regex, opinion['text'])]
				resp = [j for i in resp for j in i]
				print(*resp, sep="\n")
				exit()
			#print(re.findall(regex, opinion['text']))
		#exit()