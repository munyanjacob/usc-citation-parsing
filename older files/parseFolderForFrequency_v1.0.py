import lzma, json, re, os
import xlsxwriter
from collections import OrderedDict

workbook = xlsxwriter.Workbook('Citation_Ratios_FR_2d.xlsx')
#	**Producing spreadsheet version 1.0**
#	** Spreadsheet contains total number of cases overall versus number with USC, number with Stat, number with either
col_width = 130

cell_format = workbook.add_format()
cell_format.set_text_wrap()
bold = workbook.add_format({'bold':True})
underline = workbook.add_format({'underline':True})
wrap = workbook.add_format({'text_wrap':True})

totalsSheet = workbook.add_worksheet("Totals")
totalsSheet.set_column('B:E', col_width / 6)
totalsSheet.write("A1", "Totals:")
totalsSheet.write("A2", "Year")
totalsSheet.write("B2", "Total # Cases")
totalsSheet.write("C2", "# Either (USC or Stat)")
totalsSheet.write("D2", "# Only USC")
totalsSheet.write("E2", "# Only Stat.")

totalCount = 0
#years = "1921 1924 1927 1928 1929 1930 1931 1932 1933 1934 1935 1936 1937 1938 1939 1940 1941 1942 1943 1944 1945 1946 1947 1948 1949 1950 1951 1952 1953 1954 1955 1956 1957 1958 1959 1960 1961 1962 1963 1964 1965 1966 1967 1968 1969 1970 1971 1972 1973 1974 1975 1976 1977 1978 1979 1980 1981 1982 1983 1984 1985 1986 1987 1988 1989 1990 1991 1992 1993".split()
years = [str(x) for x in range(1910, 1994)]
USCtotals = {y:0 for y in years}
STATtotals = {y:0 for y in years}
MIXEDtotals = {y:0 for y in years}
COUNTtotals = {y:0 for y in years}

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
			elif foundSTAT:
				STATtotals[caseYear] += 1
			break
			

totalsSheet.write("B1", sum(COUNTtotals.values()))
totalsSheet.write("C1", sum(MIXEDtotals.values()))
totalsSheet.write("D1", sum(USCtotals.values()))
totalsSheet.write("E1", sum(STATtotals.values()))
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
	row += 1
workbook.close()
#'''