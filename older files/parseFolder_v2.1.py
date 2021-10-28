import lzma, json, re, os
import xlsxwriter

#'''
workbook = xlsxwriter.Workbook('USC_Citations_FR_2d.xlsx')
col_width = 130

cell_format = workbook.add_format()
cell_format.set_text_wrap()
bold = workbook.add_format({'bold':True})
underline = workbook.add_format({'underline':True})
wrap = workbook.add_format({'text_wrap':True})

totalsSheet = workbook.add_worksheet("Totals")
totalsSheet.set_column(0, 0, col_width / 5)
totalsSheet.write("A1", "Total USC Citations:")
totalCount = 0
totals = {}

citationsSheet = workbook.add_worksheet("Citations")
citationsSheet.set_column('A:C', col_width / 5)
citationsSheet.set_column('D:D', col_width)
citationsSheet.write("A1", "Year")
citationsSheet.write("B1", "Court")
citationsSheet.write("C1", "Title")
citationsSheet.write("D1", "Citation")
#'''

regex1 = r'(?:\.["\'‘’“”]?\s(?=[^a-z]))((?:(?!\.["\'‘’“”]?\s(?:[^a-z]|$)).)*?(\d\d?.?)\s?(?:U\.?S\.?(?:C\.| Code)|USC).*?\.)(?:\s[A-Z]|["\'‘’“”]|$)'
regex2 = r'\.\s((?:(?!\.\s).)*?\.\s(?:(?!\.\s).)*?\.\s(?:(?!\.\s).)*?;\s(?:(?!\.\s).)*?(\d\d?.?)\s?(?:U\.?S\.?(?:C\.| Code)|USC).*?\.)(?:\s[A-Z]|["\'‘’“”]|$)'
regex3 = r'\.\s(["\'‘’“”](?:(?!\.["\'‘’“”]).)*?\.["\'‘’“”].{,6}(\d\d?.?)\s?(?:U\.?S\.?(?:C\.| Code)|USC).*?\.)(?:\s[^a-z]|$)'

#regex = regex1+'|'+regex2+'|'+regex3

with lzma.open("F.2d-20200303-text/data/data.jsonl.xz") as in_file:
	for line in in_file:
		case = json.loads(str(line,'utf8'))

		caseYear = case['decision_date']
		caseCitation = case['citations'][0]['cite']
		caseCourtAbbrev = case['court']['name_abbreviation']

		#a = caseYear + "\n" + caseCitation + "\n" + caseCourtAbbrev

		opinions = case['casebody']['data']['opinions']
		for opinion in opinions:
			if re.search(regex1, opinion['text']):
				#resp = [[i for i in m if i] for m in re.findall(regex, opinion['text'])]
				#resp = [j for i in resp for j in i]
				#'''
				for r in re.findall(regex1, opinion['text']):
					if 'U.S. Code Con' not in r[0] and 'U.S. Code & Con' not in r[0] and 'U.S.C.C.A.N' not in r[0]:
						totalCount += 1
						if r[1] not in totals:
							totals[r[1]] = 1
						else:
							totals[r[1]] += 1

						cite = caseCitation + "\n" + r[0]

						citationsSheet.write(totalCount, 0, caseYear)
						citationsSheet.write(totalCount, 1, caseCourtAbbrev)
						citationsSheet.write(totalCount, 2, r[1])
						citationsSheet.write(totalCount, 3, cite, wrap)
				#'''
			if re.search(regex2, opinion['text']):
				#resp = [[i for i in m if i] for m in re.findall(regex, opinion['text'])]
				#resp = [j for i in resp for j in i]
				#'''
				for r in re.findall(regex2, opinion['text']):
					if 'U.S. Code Con' not in r[0] and 'U.S. Code & Con' not in r[0]:
						totalCount += 1
						if r[1] not in totals:
							totals[r[1]] = 1
						else:
							totals[r[1]] += 1
						cite = caseCitation + "\n" + r[0]
						
						citationsSheet.write(totalCount, 0, caseYear)
						citationsSheet.write(totalCount, 1, caseCourtAbbrev)
						citationsSheet.write(totalCount, 2, r[1])
						citationsSheet.write(totalCount, 3, cite, wrap)
				#'''
			if re.search(regex3, opinion['text']):
				#resp = [[i for i in m if i] for m in re.findall(regex, opinion['text'])]
				#resp = [j for i in resp for j in i]
				#'''
				for r in re.findall(regex3, opinion['text']):
					if 'U.S. Code Con' not in r[0] and 'U.S. Code & Con' not in r[0]:
						totalCount += 1
						if r[1] not in totals:
							totals[r[1]] = 1
						else:
							totals[r[1]] += 1
						cite = caseCitation + "\n" + r[0]
						
						citationsSheet.write(totalCount, 0, caseYear)
						citationsSheet.write(totalCount, 1, caseCourtAbbrev)
						citationsSheet.write(totalCount, 2, r[1])
						citationsSheet.write(totalCount, 3, cite, wrap)
				#'''

#'''
totalsSheet.write("B1", totalCount)
row = 2
for t in sorted(totals):
	totalsSheet.write(row, 0, t)
	totalsSheet.write(row, 1, totals[t])
	row += 1
workbook.close()
#'''