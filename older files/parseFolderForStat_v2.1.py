import lzma, json, re, os
import xlsxwriter


workbook = xlsxwriter.Workbook('Stat_Citations_FR_2d.xlsx')
#	**Producing spreadsheet version 3.0**
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
totalsSheet.write("A3", "Year")
totalsSheet.write("B3", "Count")
totalCount = 0
totals = {}

citationsSheet = workbook.add_worksheet("Citations")
citationsSheet.set_column('A:B', col_width / 5)
citationsSheet.set_column('C:C', col_width)
citationsSheet.write("A1", "Year")
citationsSheet.write("B1", "Court")
citationsSheet.write("C1", "Citation")

CHAR_BUFFER = 80

regex1 = r'\d\sStats?\.'

regex = regex1

with lzma.open("F.2d-20200303-text/data/data.jsonl.xz") as in_file:
	for line in in_file:
		case = json.loads(str(line,'utf8'))

		caseYear = case['decision_date']
		caseCitation = case['citations'][0]['cite']
		caseCourtAbbrev = case['court']['name_abbreviation']

		opinions = case['casebody']['data']['opinions']
		for opinion in opinions:
			if re.search(regex, opinion['text']):
				resp = [m.start() for m in re.finditer(regex, opinion['text'])]

				for index in resp:
					totalCount += 1

					cite = caseCitation + "\n" + opinion['text'][index - CHAR_BUFFER:index + len(regex) + CHAR_BUFFER]

					citationsSheet.write(totalCount, 0, caseYear)
					citationsSheet.write(totalCount, 1, caseCourtAbbrev)
					citationsSheet.write(totalCount, 2, cite, wrap)

					if caseYear[:4] not in totals:
						totals[caseYear[:4]] = 1
					else:
						totals[caseYear[:4]] += 1

totalsSheet.write("B1", totalCount)
row = 3
for t in sorted(totals):
	totalsSheet.write(row, 0, t)
	totalsSheet.write(row, 1, totals[t])
	row += 1
workbook.close()