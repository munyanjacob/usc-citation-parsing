import xlsxwriter
from helpersExtraction import extractFromFile


def initSheet(output_path):
    from pathlib import Path

    if output_path[-5] != ".xlsx":
        output_path += ".xlsx"

    while Path(output_path).exists():
        output_path = input("File " + output_path +
                            " exists. Enter a new name: ")
        if output_path[-5] != ".xlsx":
            output_path += ".xlsx"
    workbook = xlsxwriter.Workbook(output_path)

    return workbook


def createRatiosSpreadsheet(citations, output_path, citationType):
    initSheet(output_path)


def createFullSpreadsheet(citations, output_path, citationType=None):
    from collections import OrderedDict

    if citationType:
        citationType = " " + citationType
    else:
        citationType = ""

    workbook = initSheet(output_path)

    col_width = 130

    cell_format = workbook.add_format()
    cell_format.set_text_wrap()
    bold = workbook.add_format({'bold': True})
    underline = workbook.add_format({'underline': True})
    wrap = workbook.add_format({'text_wrap': True})

    totalsSheet = workbook.add_worksheet("Totals")
    totalsSheet.set_column(0, 0, col_width / 6)
    totalsSheet.set_column('B:E', col_width / 8)
    totalsSheet.write("A1", "Total" + citationType + " Citations:")
    totalsSheet.write("A3", "Year")
    totalsSheet.write("B3", "Count")
    totalsSheet.write("D3", "Title")
    totalsSheet.write("E3", "Total Count")
    totalsSheet.write("F2", "Year")

    totals = {}
    years = [str(i) for i in range(1905, 2021)]
    yearTotals = {y: 0 for y in years}
    totalSheetCounts = [0, 0, 0, 0, 0]
    sheets = []

    for i, titleRange in enumerate(["0-9", "10-19", "20-29", "30-39", "40+"]):
        sheets.append(workbook.add_worksheet("Titles " + titleRange))
        sheets[i].set_column('A:E', col_width / 8)
        sheets[i].set_column('F:F', col_width)
        sheets[i].write("A1", "Year")
        sheets[i].write("B1", "Title")
        sheets[i].write("C1", "Type")
        sheets[i].write("D1", "Court")
        sheets[i].write("E1", "Case")
        sheets[i].write("F1", "Citation")

    for citation in citations:
        year = citation["year"]
        cite = citation["cite"]
        court = citation["court"]

        # key: string citation , value: list of (title, USC) tuples
        foundCitations = citation["citations"]

        for foundSentence in foundCitations:
            for foundCite in foundCitations[foundSentence]:
                title = int(foundCite[0])
                category = int(title/10)

                if category > 4:
                    category = 4
                totalSheetCounts[category] += 1

                if title not in totals:
                    totals[title] = {y: 0 for y in years}
                totals[title][year] += 1

                yearTotals[year] += 1

                sheets[category].write(
                    totalSheetCounts[category], 0, year)
                sheets[category].write(totalSheetCounts[category], 1, title)
                sheets[category].write(
                    totalSheetCounts[category], 2, foundCite[1])
                sheets[category].write(
                    totalSheetCounts[category], 3, court)
                sheets[category].write(
                    totalSheetCounts[category], 4, cite)
                sheets[category].write(
                    totalSheetCounts[category], 5, foundSentence, wrap)

    totalsSheet.write("B1", sum(totalSheetCounts))
    row = 3
    column = 5
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


if __name__ == '__main__':
    citationType = None
    citations = extractFromFile("us_text.zip", None, citationType)
    createFullSpreadsheet(citations, "TestUSReporter", citationType)
