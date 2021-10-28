import lzma, json, re, os
import xlsxwriter
from collections import OrderedDict

workbook = xlsxwriter.Workbook('Both_Citations_FR_2d.xlsx')
#	**Producing spreadsheet version 1.0**
col_width = 130

cell_format = workbook.add_format()
cell_format.set_text_wrap()
bold = workbook.add_format({'bold':True})
underline = workbook.add_format({'underline':True})
wrap = workbook.add_format({'text_wrap':True})

totalsSheet = workbook.add_worksheet("Totals")
totalsSheet.set_column(0, 0, col_width / 4)
totalsSheet.set_column('B:E', col_width / 8)
totalsSheet.write("A1", "Total Citations With USC & Stat:")
totalsSheet.write("A3", "Year")
totalsSheet.write("B3", "Count")
totalsSheet.write("D2", "Title")
totalsSheet.write("E1", "Count")
totalsSheet.write("E3", "Total")
totalsSheet.write("F2", "Year")
totalCount = 0
years = "1921 1927 1928 1929 1930 1931 1932 1933 1934 1935 1936 1937 1938 1939 1940 1941 1942 1943 1944 1945 1946 1947 1948 1949 1950 1951 1952 1953 1954 1955 1956 1957 1958 1959 1960 1961 1962 1963 1964 1965 1966 1967 1968 1969 1970 1971 1972 1973 1974 1975 1976 1977 1978 1979 1980 1981 1982 1983 1984 1985 1986 1987 1988 1989 1990 1991 1992 1993".split()
totals = {}
yearTotals = {y:0 for y in years}

citationsSheet = workbook.add_worksheet("Citations")
citationsSheet.set_column('A:D', col_width / 8)
citationsSheet.set_column('E:E', col_width)
citationsSheet.write("A1", "Year")
citationsSheet.write("B1", "Court")
citationsSheet.write("C1", "Title")
citationsSheet.write("D1", "Case")
citationsSheet.write("E1", "Citation")

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
					if re.search(r'\d\sStats?\.', r[0]) and 'U.S. Code Con' not in r[0] and 'U.S. Code & Con' not in r[0] and 'U.S.C.C.A.N' not in r[0] and 'U.S.Code Con' not in r[0]:
						title = int(r[1])
						totalCount += 1

						if title not in totals:
							totals[title] = {y:0 for y in years}
						totals[title][caseYear[:4]] += 1

						yearTotals[caseYear[:4]] += 1

						citationsSheet.write(totalCount, 0, caseYear)
						citationsSheet.write(totalCount, 1, caseCourtAbbrev)
						citationsSheet.write(totalCount, 2, title)
						citationsSheet.write(totalCount, 3, caseCitation)
						citationsSheet.write(totalCount, 4, r[0], wrap)

totalsSheet.write("B1", totalCount)
row = 3
column = 5
#for t in OrderedDict(sorted(yearTotals.items())):
for t in years:
	totalsSheet.write(row, 0, t)
	totalsSheet.write(row, 1, yearTotals[t])
	totalsSheet.write(2, column, t)
	column += 1
	row += 1
row = 3
for t in OrderedDict(sorted(totals.items())):
	totalsSheet.write(row, 3, t)
	totalsSheet.write(row, 4, sum(totals[t].values()))
	column = 5
	for year in years:
		if totals[t][year] != 0:
			totalsSheet.write(row, column, totals[t][year])
		column += 1
	row += 1
workbook.close()
#'''