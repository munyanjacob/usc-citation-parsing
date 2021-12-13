def process(s):
    # requires that all U. S. C. have spaces removed
    if 'U. S. C. ' in s:
        s = s.replace('U. S. C. ', 'USC')
    import re

    # Avoid Roman Numeral citations (example: Supp. IV)
    # as well as: U. S. C. (otherwise thinks S and C are start of new sentences)
    reFirstSentenceChar = r"(?![IVXLCDMUS])[A-Z]"

    # start of string or start of new sentence
    reSentenceStart = r"(?:^|(?<=\. ))(" + reFirstSentenceChar

    reTitle = r'\s+([0-5]?\da?)'

    reUSC = r"((?:U\.? ?S\.? ?(?:C\.?|Code)|United States Code)" + \
        r"(?: App| ?A\.?)?)"

    # need the title to be next to USC location
    reTitleAndUSC = reTitle + r'(?:,| of the)?\s+' + reUSC

    reSection = r"(?:§+|[sS]ection)\s*(\d+)"

    # reModifiedFirstChar = r"(?![IVXLCDM])[A-Z0-9]"

    reSentenceEnd = r"(?:\.|$))(?=\s*$|\s+" + reFirstSentenceChar + ")"

    # munch when not start of new sentence
    reMunchNonSentence = r"(?:(?!\.\s+(?![IVXLCDMUS])[A-Z]).)*?"

    full_regex = reMunchNonSentence.join([reSentenceStart,
                                          reTitleAndUSC, reSection, reSentenceEnd])

    toMatch = full_regex

    # this can find all of the corresponding sections, if each citation follows the format. unreliable.
    # print(len(re.findall(reSection, s)))

    # key is the sentence, values are all citations inside of it
    results = {}

    if re.search(toMatch, s):
        for r in re.findall(toMatch, s):
            key = r[0]
            if key in results:
                key += "."
            results[key] = [(title, 'USCA' if 'A' in code else 'USC')
                            for title, code in re.findall(reTitleAndUSC, r[0])]
    return results


if __name__ == '__main__':
    # from sampleCase import sample_full_text
    # sample_full_text = "All three are over 65 years old and have been denied enrollment in the Medicare Part B supplemental medical insurance program established by § 1831 et seq. of the Social Security Act of 1935, 49 Stat. 620, as added, 79 Stat. 301, and as amended, 42 U. S. C. § 1395j et seq. (1970 ed. and Supp. IV). They brought this action to challenge the statutory basis for that denial. Specifically, they attack 42 U. S. C. § 1395o (2) (1970 ed., Supp. IV), which grants eligibility to resident citi-zents who are 65 or older but denies eligibility to comparable aliens unless they have been admitted for permanent residence and also have resided in the United States for at least five years."
    sample_full_text = " A variety of other federal statutes provide for disparate treatment of aliens and citizens. These include prohibitions and restrictions upon Government employment of aliens, e. g., 10 U. S. C. § 5571; 22 U. S. C. § 1044 (e), upon private employment of aliens, e. g., 10 U. S. C. § 2279; 12 U. S. C. § 72, and upon investments and businesses of aliens, e. g., 12 U. S. C. §619; 47 U. S. C. § 17; statutes excluding aliens from benefits available to citizens, e. g., 26 U. S. C. § 931 (1970 ed. and Supp. IV); 46 U. S. C. § 1171 (a), and from protections extended to citizens, e. g., 19 U.S. C. § 1526; 29 U. S. C. § 633a (1970 ed., Supp. IV); and statutes imposing added burdens upon aliens, e. g., 26 U. S. C. § 6851 (d); 28 U. S. C. § 1391 (d). Several statutes treat certain aliens more favorably than citizens. E. g., 19 U. S. C. § 1586 (e); 50 U. S. C. App. § 453 (1970 ed., Supp. IV) "
    #sample_full_text = "Title 52 of the United States Code App. Section 200"
    print(process(sample_full_text))
