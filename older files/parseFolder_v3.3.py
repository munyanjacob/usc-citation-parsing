import lzma
import json
import re
import os
import xlsxwriter
from collections import OrderedDict

workbook = xlsxwriter.Workbook('USC_Citations_FR_2d.xlsx')
#	**Producing spreadsheet version 4.2**
#	**	WAS GOING TO BE USED TO COMPILE EVERYTHING. PAUSED WORK 9/28/2020, moved to parseFolderForFrequency_v1.0
col_width = 130

cell_format = workbook.add_format()
cell_format.set_text_wrap()
bold = workbook.add_format({'bold': True})
underline = workbook.add_format({'underline': True})
wrap = workbook.add_format({'text_wrap': True})

totalsSheet = workbook.add_worksheet("Totals")
totalsSheet.set_column(0, 0, col_width / 6)
totalsSheet.set_column('B:E', col_width / 8)
totalsSheet.write("A1", "Total USC Citations:")
totalsSheet.write("A3", "Year")
totalsSheet.write("B3", "Count")
totalsSheet.write("D2", "Title")
totalsSheet.write("E1", "Count")
totalsSheet.write("E3", "Total")
totalsSheet.write("F2", "Year")
totalCounts = [0, 0, 0, 0, 0]
years = "1921 1927 1928 1929 1930 1931 1932 1933 1934 1935 1936 1937 1938 1939 1940 1941 1942 1943 1944 1945 1946 1947 1948 1949 1950 1951 1952 1953 1954 1955 1956 1957 1958 1959 1960 1961 1962 1963 1964 1965 1966 1967 1968 1969 1970 1971 1972 1973 1974 1975 1976 1977 1978 1979 1980 1981 1982 1983 1984 1985 1986 1987 1988 1989 1990 1991 1992 1993".split()
totals = {}
yearTotals = {}
numCasesPerYear = {}
numUSCPerYear = {}
numStatPerYear = {}

mixedtotalsSheet = workbook.add_worksheet("Mixed Totals")
mixedtotalsSheet.set_column(0, 0, col_width / 4)
mixedtotalsSheet.set_column('B:E', col_width / 8)
mixedtotalsSheet.write("A1", "Total Citations With USC & Stat:")
mixedtotalsSheet.write("A3", "Year")
mixedtotalsSheet.write("B3", "Count")
mixedtotalsSheet.write("D2", "Title")
mixedtotalsSheet.write("E1", "Count")
mixedtotalsSheet.write("E3", "Total")
mixedtotalsSheet.write("F2", "Year")
mixedtotalCount = 0
mixedtotals = {}
mixedyearTotals = {y: 0 for y in years}

mixedcitationsSheet = workbook.add_worksheet("Mixed Citations")
mixedcitationsSheet.set_column('A:D', col_width / 8)
mixedcitationsSheet.set_column('E:E', col_width)
mixedcitationsSheet.write("A1", "Year")
mixedcitationsSheet.write("B1", "Court")
mixedcitationsSheet.write("C1", "Title")
mixedcitationsSheet.write("D1", "Case")
mixedcitationsSheet.write("E1", "Citation")

citationsSheet0 = workbook.add_worksheet("Titles 0-9")
citationsSheet0.set_column('A:D', col_width / 8)
citationsSheet0.set_column('E:E', col_width)
citationsSheet0.write("A1", "Year")
citationsSheet0.write("B1", "Court")
citationsSheet0.write("C1", "Title")
citationsSheet0.write("D1", "Case")
citationsSheet0.write("E1", "Citation")

citationsSheet1 = workbook.add_worksheet("Titles 10-19")
citationsSheet1.set_column('A:D', col_width / 8)
citationsSheet1.set_column('E:E', col_width)
citationsSheet1.write("A1", "Year")
citationsSheet1.write("B1", "Court")
citationsSheet1.write("C1", "Title")
citationsSheet0.write("D1", "Case")
citationsSheet0.write("E1", "Citation")

citationsSheet2 = workbook.add_worksheet("Titles 20-29")
citationsSheet2.set_column('A:D', col_width / 8)
citationsSheet2.set_column('E:E', col_width)
citationsSheet2.write("A1", "Year")
citationsSheet2.write("B1", "Court")
citationsSheet2.write("C1", "Title")
citationsSheet0.write("D1", "Case")
citationsSheet0.write("E1", "Citation")

citationsSheet3 = workbook.add_worksheet("Titles 30-39")
citationsSheet3.set_column('A:D', col_width / 8)
citationsSheet3.set_column('E:E', col_width)
citationsSheet3.write("A1", "Year")
citationsSheet3.write("B1", "Court")
citationsSheet3.write("C1", "Title")
citationsSheet0.write("D1", "Case")
citationsSheet0.write("E1", "Citation")

citationsSheet4 = workbook.add_worksheet("Titles 40+")
citationsSheet4.set_column('A:D', col_width / 8)
citationsSheet4.set_column('E:E', col_width)
citationsSheet4.write("A1", "Year")
citationsSheet4.write("B1", "Court")
citationsSheet4.write("C1", "Title")
citationsSheet0.write("D1", "Case")
citationsSheet0.write("E1", "Citation")

sheets = [citationsSheet0, citationsSheet1,
          citationsSheet2, citationsSheet3, citationsSheet4]

regexNormalStart = r'(?<=[\.?!"\'’”])\s([^a-z0-9\.!?\\§]'
regexUSC = r'\s([0-5]?\d)(?:,|" of the")?\s(?:U\.? ?S\.? ?(?:C\.?| Code)|United States Code)'
readToUSC = r'(?:(?![\.?!"\'’”]\s[^a-z0-9\.!?\\§]).)*?' + regexUSC
regexEnd = r'.*?[\.?!"\'’”])(?=\s[^a-z0-9\.!?\\§]|$)'

regex1 = regexNormalStart + readToUSC + regexEnd
with lzma.open("F.2d-20200303-text/data/data.jsonl.xz") as in_file:
    for line in in_file:
        case = json.loads(str(line, 'utf8'))

        caseYear = case['decision_date']
        caseCitation = case['citations'][0]['cite']
        caseCourtAbbrev = case['court']['name_abbreviation']

        opinions = case['casebody']['data']['opinions']
        for opinion in opinions:
            if re.search(regex1, opinion['text']):
                for r in re.findall(regex1, opinion['text']):
                    foundStat = False

                    if re.search(r'\d\sStats?\.', r[0]):
                        foundStat = True
                    if 'U.S. Code Con' not in r[0] and 'U.S. Code & Con' not in r[0] and 'U.S.C.C.A.N' not in r[0] and 'U.S.Code Con' not in r[0]:
                        title = int(r[1])
                        category = int(title/10)
                        if category > 4:
                            category = 4
                        totalCounts[category] += 1

                        if title not in totals:
                            totals[title] = {y: 0 for y in years}
                            totals[title][caseYear[:4]] += 1
                        else:
                            totals[title][caseYear[:4]] += 1

                        if caseYear[:4] not in yearTotals:
                            yearTotals[caseYear[:4]] = 1
                        else:
                            yearTotals[caseYear[:4]] += 1
                        sheets[category].write(
                            totalCounts[category], 0, caseYear)
                        sheets[category].write(
                            totalCounts[category], 1, caseCourtAbbrev)
                        sheets[category].write(totalCounts[category], 2, title)
                        sheets[category].write(
                            totalCounts[category], 3, caseCitation)
                        sheets[category].write(
                            totalCounts[category], 4, r[0], wrap)

                        if foundStat:
                            mixedtotalCount += 1
                            if title not in mixedtotals:
                                mixedtotals[title] = {y: 0 for y in years}
                            mixedtotals[title][caseYear[:4]] += 1

                            mixedyearTotals[caseYear[:4]] += 1

                            mixedcitationsSheet.write(
                                mixedtotalCount, 0, caseYear)
                            mixedcitationsSheet.write(
                                mixedtotalCount, 1, caseCourtAbbrev)
                            mixedcitationsSheet.write(
                                mixedtotalCount, 2, title)
                            mixedcitationsSheet.write(
                                mixedtotalCount, 3, caseCitation)
                            mixedcitationsSheet.write(
                                mixedtotalCount, 4, r[0], wrap)

totalsSheet.write("B1", sum(totalCounts))
row = 3
column = 5
# for t in OrderedDict(sorted(yearTotals.items())):
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
        # for data in totals[t].values():
        if totals[t][year] != 0:
            totalsSheet.write(row, column, totals[t][year])
        column += 1
    #totalsSheet.write(row, 5, totals[t])
    row += 1


mixedtotalsSheet.write("B1", mixedtotalCount)
row = 3
column = 5
# for t in OrderedDict(sorted(yearTotals.items())):
for t in years:
    mixedtotalsSheet.write(row, 0, t)
    mixedtotalsSheet.write(row, 1, mixedyearTotals[t])
    mixedtotalsSheet.write(2, column, t)
    column += 1
    row += 1
row = 3
for t in OrderedDict(sorted(mixedtotals.items())):
    mixedtotalsSheet.write(row, 3, t)
    mixedtotalsSheet.write(row, 4, sum(mixedtotals[t].values()))
    column = 5
    for year in years:
        if mixedtotals[t][year] != 0:
            mixedtotalsSheet.write(row, column, mixedtotals[t][year])
        column += 1
    row += 1

workbook.close()
# '''
