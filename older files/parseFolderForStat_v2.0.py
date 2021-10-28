import lzma, json, re, os
import xlsxwriter

workbook = xlsxwriter.Workbook('Stat_Citations_FR_2d.xlsx')
col_width = 130

cell_format = workbook.add_format()
cell_format.set_text_wrap()
bold = workbook.add_format({'bold':True})
underline = workbook.add_format({'underline':True})
wrap = workbook.add_format({'text_wrap':True})

totalsSheet = workbook.add_worksheet("Totals")
totalsSheet.set_column(0, 0, col_width / 2)
totalsSheet.set_column('B:B', col_width / 7)
totalsSheet.write("A1", "Total Stat Citations:")
totalCount = 0

citationsSheet = workbook.add_worksheet("Citations")
citationsSheet.set_column('A:B', col_width / 5)
citationsSheet.set_column('C:C', col_width)
citationsSheet.write("A1", "Year")
citationsSheet.write("B1", "Court")
citationsSheet.write("C1", "Citation")

CHAR_BUFFER = 80

regex1 = r'\d\sStats?\.'

#regex1 = r'((?:(?!\d\sStats?\.).){5,70}?\d\sStats?\.(?:(?!\d\sStats?\.).){5,70}?)'

#regex1 = r'(.{70}\d\sStats?\.(?:(?!\d\sStats?\.).){,70})'
#regex2 = r'(?!Stats?\..{,70})(.{70}\d\sStats?\..{70})'

#regex3 = r'((?:.{50})(?:\d\sStats?\.)(?:.{50}))$'
#regex2 = r'\.\s((?:(?!\.\s).)*?\.\s(?:(?!\.\s).)*?\.\s(?:(?!\.\s).)*?;\s(?:(?!\.\s).)*?(?:\d\sStats?\.).*?\.)(?:\s[^a-z]|["\'‘’“”]|$)'
#regex3 = r'\.\s(["\'‘’“”](?:(?!\.["\'‘’“”]).)*?\.["\'‘’“”].{,3}(?:\d\sStats?\.).*?\.)(?:\s[^a-z]|$)'

#regex = regex3+'|'+regex2+'|'+regex1
#regex = regex2+'|'+regex1
regex = regex1

with lzma.open("F.2d-20200303-text/data/data.jsonl.xz") as in_file:
	for line in in_file:
		case = json.loads(str(line,'utf8'))

		caseYear = case['decision_date']
		caseCitation = case['citations'][0]['cite']
		caseCourtAbbrev = case['court']['name_abbreviation']

		#a = caseYear + "\n" + caseCitation + "\n" + caseCourtAbbrev

		opinions = case['casebody']['data']['opinions']
		for opinion in opinions:
			if re.search(regex, opinion['text']):
				#resp = re.findall(regex, opinion['text'])
				resp = [m.start() for m in re.finditer(regex, opinion['text'])]

				#resp = [[i for i in m if i] for m in re.findall(regex, opinion['text'])]
				#resp = [j for i in resp for j in i]

				for index in resp:
					totalCount += 1

					cite = caseCitation + "\n" + opinion['text'][index - CHAR_BUFFER:index + len(regex) + CHAR_BUFFER]

					citationsSheet.write(totalCount, 0, caseYear)
					citationsSheet.write(totalCount, 1, caseCourtAbbrev)
					citationsSheet.write(totalCount, 2, cite, wrap)

totalsSheet.write("A2", totalCount)
workbook.close()