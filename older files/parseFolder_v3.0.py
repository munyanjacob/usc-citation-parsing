import lzma, json, re, os
import xlsxwriter
from collections import OrderedDict

workbook = xlsxwriter.Workbook('USC_Citations_FR_2d.xlsx')
#	**Producing spreadsheet version 4.0**
col_width = 130

cell_format = workbook.add_format()
cell_format.set_text_wrap()
bold = workbook.add_format({'bold':True})
underline = workbook.add_format({'underline':True})
wrap = workbook.add_format({'text_wrap':True})

totalsSheet = workbook.add_worksheet("Totals")
totalsSheet.set_column(0, 0, col_width / 6)
totalsSheet.set_column('B:D', col_width / 8)
totalsSheet.write("A1", "Total USC Citations:")
totalsSheet.write("A3", "Year")
totalsSheet.write("B3", "Count")
totalsSheet.write("C3", "Title")
totalsSheet.write("D3", "Count")
totalCounts = [0,0,0,0,0]
totals = {}
yearTotals = {}

citationsSheet0 = workbook.add_worksheet("Titles 0-9")
citationsSheet0.set_column('A:C', col_width / 5)
citationsSheet0.set_column('D:D', col_width)
citationsSheet0.write("A1", "Year")
citationsSheet0.write("B1", "Court")
citationsSheet0.write("C1", "Title")
citationsSheet0.write("D1", "Citation")

citationsSheet1 = workbook.add_worksheet("Titles 10-19")
citationsSheet1.set_column('A:C', col_width / 5)
citationsSheet1.set_column('D:D', col_width)
citationsSheet1.write("A1", "Year")
citationsSheet1.write("B1", "Court")
citationsSheet1.write("C1", "Title")
citationsSheet1.write("D1", "Citation")

citationsSheet2 = workbook.add_worksheet("Titles 20-29")
citationsSheet2.set_column('A:C', col_width / 5)
citationsSheet2.set_column('D:D', col_width)
citationsSheet2.write("A1", "Year")
citationsSheet2.write("B1", "Court")
citationsSheet2.write("C1", "Title")
citationsSheet2.write("D1", "Citation")

citationsSheet3 = workbook.add_worksheet("Titles 30-39")
citationsSheet3.set_column('A:C', col_width / 5)
citationsSheet3.set_column('D:D', col_width)
citationsSheet3.write("A1", "Year")
citationsSheet3.write("B1", "Court")
citationsSheet3.write("C1", "Title")
citationsSheet3.write("D1", "Citation")

citationsSheet4 = workbook.add_worksheet("Titles 40+")
citationsSheet4.set_column('A:C', col_width / 5)
citationsSheet4.set_column('D:D', col_width)
citationsSheet4.write("A1", "Year")
citationsSheet4.write("B1", "Court")
citationsSheet4.write("C1", "Title")
citationsSheet4.write("D1", "Citation")

sheets = [citationsSheet0,citationsSheet1,citationsSheet2,citationsSheet3,citationsSheet4]

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
						title = int(r[1])
						category = int(title/10)
						if category > 4:
							category = 4
						totalCounts[category] += 1

						if title not in totals:
							totals[title] = 1
						else:
							totals[title] += 1

						if caseYear[:4] not in yearTotals:
							yearTotals[caseYear[:4]] = 1
						else:
							yearTotals[caseYear[:4]] += 1

						cite = caseCitation + "\n" + r[0]


						sheets[category].write(totalCounts[category], 0, caseYear)
						sheets[category].write(totalCounts[category], 1, caseCourtAbbrev)
						sheets[category].write(totalCounts[category], 2, title)
						sheets[category].write(totalCounts[category], 3, cite, wrap)

totalsSheet.write("B1", sum(totalCounts))
row = 3
for t in OrderedDict(sorted(yearTotals.items())):
	totalsSheet.write(row, 0, t)
	totalsSheet.write(row, 1, yearTotals[t])
	row += 1
row = 3
for t in OrderedDict(sorted(totals.items())):
	totalsSheet.write(row, 2, t)
	totalsSheet.write(row, 3, totals[t])
	row += 1
workbook.close()
#'''