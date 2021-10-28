import lzma, json, re
with lzma.open("F.2d-20200303-text/data/data.jsonl.xz") as in_file:
	for line in in_file:
		case = json.loads(str(line,'utf8'))

		caseYear = case['decision_date']
		caseCitation = case['citations'][0]['cite']
		caseCourtAbbrev = case['court']['name_abbreviation']

		#print(caseYear, caseCitation, caseCourtAbbrev, sep='\n')

		#regex = r'(?:^|\.\s)((?!\.(?: [A-Z]|["\'])).*?(?:U\.?S\.?(?:C\.| Code)|USC).+?\.)(?: [A-Z]|["\']|$)'
		#regex = r'(?:\.\s(?=[A-Z]|["\']))(.*?(?:U\.?S\.?(?:C\.| Code)|USC).+?\.)(?: [A-Z]|["\']|$)'
		#regex = r'(?:\.["\']?\s(?=[^a-z]))((?:(?!\.["\']?\s(?:[^a-z]|$)).)*?(?:U\.?S\.?(?:C\.| Code)|USC).*?\.)(?:\s[A-Z]|["\']|$)'
		regex1 = r'(?:\.["\'‘’“”]?\s(?=[^a-z]))((?:(?!\.["\'‘’“”]?\s(?:[^a-z]|$)).)*?(?:U\.?S\.?(?:C\.| Code)|USC).*?\.)(?:\s[A-Z]|["\'‘’“”]|$)'
		regex2 = r'\.\s((?:(?!\.\s).)*?\.\s(?:(?!\.\s).)*?\.\s(?:(?!\.\s).)*?;\s(?:(?!\.\s).)*?(?:U\.?S\.?(?:C\.| Code)|USC).*?\.)(?:\s[A-Z]|["\'‘’“”]|$)'
		regex3 = r'\.\s(["\'‘’“”](?:(?!\.["\'‘’“”]).)*?\.["\'‘’“”].{,6}(?:U\.?S\.?(?:C\.| Code)|USC).*?\.)(?:\s[^a-z]|$)'
		#string = '. Id.\nOn July 20, 2001, the United States made an ex parte application pursuant to 18 U.S.C. § 2703(d) for an Order requiring Cablevision to provide information to the Government concerning a subscriber to Cablevision’s cable internet service. I'
		#string = '.'
		#print(re.findall(regex, string))

		opinions = case['casebody']['data']['opinions']
		for opinion in opinions:
			resp = 0
			print('test')
			if re.search(regex1, opinion['text']):
				#print(opinion['text'])
				resp = re.findall(regex1, opinion['text'])
				print(resp)
			if re.search(regex2, opinion['text']):
				resp = re.findall(regex2, opinion['text']) 
				print(resp) 
			if re.search(regex3, opinion['text']):
				resp = re.findall(regex3, opinion['text'])
				print(resp)
			if (resp != 0):
				exit()
			#print(re.findall(regex, opinion['text']))
		#exit()