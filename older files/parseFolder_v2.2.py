import lzma, json, re, os
import xlsxwriter
from collections import OrderedDict

#'''
workbook = xlsxwriter.Workbook('USC_Citations_FR_2d.xlsx')
#	**Producing spreadsheet version 4.0**
col_width = 130

cell_format = workbook.add_format()
cell_format.set_text_wrap()
bold = workbook.add_format({'bold':True})
underline = workbook.add_format({'underline':True})
wrap = workbook.add_format({'text_wrap':True})

totalsSheet = workbook.add_worksheet("Totals")
totalsSheet.set_column(0, 0, col_width / 5)
totalsSheet.write("A1", "Total USC Citations:")
totalsSheet.write("A2", "Title")
totalsSheet.write("B2", "Count")
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

regexNormalStart = r'(?<=[\.?!"\'’”])\s([^a-z0-9\.!?\\§]'
#extract title and USC
regexUSC = r'\s([0-5]?\d)(?:,|" of the")?\s(?:U\.?S\.?(?:C\.?| Code)|USC|United States Code)'
#read until it has sentence including USC; stops after reading USC
readToUSC = r'(?:(?![\.?!"\'’”]\s[^a-z0-9\.!?\\§]).)*?' + regexUSC
regexEnd = r'.*?[\.?!"\'’”])(?=\s[^a-z0-9\.!?\\§]|$)'

regex1 = regexNormalStart + readToUSC + regexEnd
with lzma.open("F.2d-20200303-text/data/data.jsonl.xz") as in_file:
	for line in in_file:
		case = json.loads(str(line,'utf8'))

		caseYear = case['decision_date']
		caseCitation = case['citations'][0]['cite']
		caseCourtAbbrev = case['court']['name_abbreviation']

		opinions = case['casebody']['data']['opinions']
		for opinion in opinions:
			if re.search(regex1, opinion['text']):
				for r in re.findall(regex1, opinion['text']):
					if 'U.S. Code Con' not in r[0] and 'U.S. Code & Con' not in r[0] and 'U.S.C.C.A.N' not in r[0] and 'U.S.Code Con' not in r[0]:
						totalCount += 1

						title = int(r[1])
						if title not in totals:
							totals[title] = 1
						else:
							totals[title] += 1

						cite = caseCitation + "\n" + r[0]

						citationsSheet.write(totalCount, 0, caseYear)
						citationsSheet.write(totalCount, 1, caseCourtAbbrev)
						citationsSheet.write(totalCount, 2, r[1])
						citationsSheet.write(totalCount, 3, cite, wrap)
				#'''
			'''if re.search(regex2, opinion['text']):
				for r in re.findall(regex2, opinion['text']):
					if 'U.S. Code Con' not in r[0] and 'U.S. Code & Con' not in r[0]:
						totalCount += 1
						title = int(r[1])
						if title not in totals:
							totals[title] = 1
						else:
							totals[title] += 1
						cite = caseCitation + "\n" + r[0]
						
						citationsSheet.write(totalCount, 0, caseYear)
						citationsSheet.write(totalCount, 1, caseCourtAbbrev)
						citationsSheet.write(totalCount, 2, r[1])
						citationsSheet.write(totalCount, 3, cite, wrap)
'''
#'''
totalsSheet.write("B1", totalCount)
row = 3
for t in OrderedDict(sorted(totals.items())):
	totalsSheet.write(row, 0, t)
	totalsSheet.write(row, 1, totals[t])
	row += 1
workbook.close()
#'''