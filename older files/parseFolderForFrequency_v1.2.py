import lzma, json, re, os
import xlsxwriter
from collections import OrderedDict

workbook = xlsxwriter.Workbook('Citation_Ratios_FR_2d.xlsx')
#	**Producing spreadsheet version 1.2**
#	** Spreadsheet contains total number of cases overall versus number with USC, number with Stat, number with either, both, both near each other
col_width = 130

cell_format = workbook.add_format()
cell_format.set_text_wrap()
bold = workbook.add_format({'bold':True})
underline = workbook.add_format({'underline':True})
wrap = workbook.add_format({'text_wrap':True})

totalsSheet = workbook.add_worksheet("Totals")
totalsSheet.set_column('B:F', col_width / 6)
totalsSheet.set_column('G:G', col_width / 5)
totalsSheet.set_column('H:K', col_width / 8)
totalsSheet.write("A1", "Totals:")
totalsSheet.write("A2", "Year")
totalsSheet.write("B2", "Total # Cases")
totalsSheet.write("C2", "# With Either (USC or Stat)")
totalsSheet.write("D2", "# Including USC")
totalsSheet.write("E2", "# Inlcuding Stat.")
totalsSheet.write("F2", "# With Both (USC & Stat)")
totalsSheet.write("G2", "# With Both Close Together")
totalsSheet.write("H2", "USC/Total")
totalsSheet.write("I2", "Stat/Total")
totalsSheet.write("J2", "Both/Total")
totalsSheet.write("K2", "Close/Total")

totalCount = 0
#years = "1921 1924 1927 1928 1929 1930 1931 1932 1933 1934 1935 1936 1937 1938 1939 1940 1941 1942 1943 1944 1945 1946 1947 1948 1949 1950 1951 1952 1953 1954 1955 1956 1957 1958 1959 1960 1961 1962 1963 1964 1965 1966 1967 1968 1969 1970 1971 1972 1973 1974 1975 1976 1977 1978 1979 1980 1981 1982 1983 1984 1985 1986 1987 1988 1989 1990 1991 1992 1993".split()
years = [str(x) for x in range(1910, 1994)]
USCtotals = {y:0 for y in years}
STATtotals = {y:0 for y in years}
MIXEDtotals = {y:0 for y in years}
COUNTtotals = {y:0 for y in years}
BOTHtotals = {y:0 for y in years}
TOGETHERtotals = {y:0 for y in years}

regexNormalStart = r'(?<=[\.?!"\'’”])\s([^a-z0-9\.!?\\§]'
regexUSC = r'\s([0-5]?\d)(?:,|" of the")?\s(?:U\.?S\.?(?:C\.?| Code)|USC|United States Code)'
readToUSC = r'(?:(?![\.?!"\'’”]\s[^a-z0-9\.!?\\§]).)*?' + regexUSC
regexEnd = r'.*?[\.?!"\'’”])(?=\s[^a-z0-9\.!?\\§]|$)'

regexUSC = regexNormalStart + readToUSC + regexEnd
regexSTAT = r'\d\sStats?\.'

with lzma.open("F.2d-20200303-text/data/data.jsonl.xz") as in_file:
	for line in in_file:
		case = json.loads(str(line,'utf8'))
		caseYear = case['decision_date'][:4]

		foundUSC = False
		foundSTAT = False

		foundTogether = False

		opinions = case['casebody']['data']['opinions']
		
		for opinion in opinions:
			if re.search(regexUSC, opinion['text']):
				foundUSC = True
			if re.search(regexSTAT, opinion['text']):
				foundSTAT = True

			COUNTtotals[caseYear] += 1
			if foundUSC or foundSTAT:
				MIXEDtotals[caseYear] += 1
			else:
				break
			if foundUSC:
				USCtotals[caseYear] += 1
				if foundSTAT:
					BOTHtotals[caseYear] += 1

					for r in re.findall(regexUSC, opinion['text']):
						if re.search(regexSTAT, r[0]) and 'U.S. Code Con' not in r[0] and 'U.S. Code & Con' not in r[0] and 'U.S.C.C.A.N' not in r[0] and 'U.S.Code Con' not in r[0]:
							TOGETHERtotals[caseYear] += 1
							break

			elif foundSTAT:
				STATtotals[caseYear] += 1
			break
			

totalsSheet.write("B1", sum(COUNTtotals.values()))
totalsSheet.write("C1", sum(MIXEDtotals.values()))
totalsSheet.write("D1", sum(USCtotals.values()))
totalsSheet.write("E1", sum(STATtotals.values()))
totalsSheet.write("F1", sum(BOTHtotals.values()))
totalsSheet.write("G1", sum(TOGETHERtotals.values()))

row = 2
for t in years:
	totalsSheet.write(row, 0, t)
	totalsSheet.write(row, 1, COUNTtotals[t])
	if MIXEDtotals[t] != 0:
		totalsSheet.write(row, 2, MIXEDtotals[t])
	if USCtotals[t] != 0:
		totalsSheet.write(row, 3, USCtotals[t])
	if STATtotals[t] != 0:
		totalsSheet.write(row, 4, STATtotals[t])
	if BOTHtotals[t] != 0:
		totalsSheet.write(row, 5, BOTHtotals[t])
	if TOGETHERtotals[t] != 0:
		totalsSheet.write(row, 6, TOGETHERtotals[t])

	if COUNTtotals[t] != 0:
		totalsSheet.write(row, 7, "{:.3f}".format(USCtotals[t] / float(COUNTtotals[t])))
		totalsSheet.write(row, 8, "{:.3f}".format(STATtotals[t] / float(COUNTtotals[t])))
		totalsSheet.write(row, 9, "{:.3f}".format(BOTHtotals[t] / float(COUNTtotals[t])))
		totalsSheet.write(row, 10, "{:.3f}".format(TOGETHERtotals[t] / float(COUNTtotals[t])))

	row += 1
workbook.close()
#'''