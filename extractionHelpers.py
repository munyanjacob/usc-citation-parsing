reFirstSentenceChar = r"(?![IVXLCDMUS])[A-Z]"

# start of string or start of new sentence
reSentenceStart = r"(?:^|(?<=\. ))(" + reFirstSentenceChar


reTitle = r'\s+([0-5]?\da?)'

reUSC = r"(?:U\.? ?S\.? ?(?:C\.?|Code)|United States Code)"

# need the title to be next to USC location
reTitleAndUSC = reTitle + r'(?:,| of the)?\s+' + reUSC

reSection = r"(?:§+|[sS]ection)\s*(\d+)"

#reModifiedFirstChar = r"(?![IVXLCDM])[A-Z0-9]"

reSentenceEnd = r"\.)(?=\s*$|\s+" + reFirstSentenceChar + ")"

# munch when not start of new sentence
reMunchNonSentence = r"(?:(?!\.\s+(?![IVXLCDMUS])[A-Z]).)*?"

full_regex = reMunchNonSentence.join([reSentenceStart,
                                      reTitleAndUSC, reSection, reSentenceEnd])


def process(s):
    import re

    toMatch = full_regex

    # this can find all titles within mini citation!!
    #print(len(re.findall(reTitleAndUSC, s)))
    # this can find all of the corresponding sections, if each citation follows the format. unreliable.
    #print(len(re.findall(reSection, s)))

    if re.search(toMatch, s):
        print(re.findall(toMatch, s))
        # for r in re.findall(toMatch, s):
        #    print(r)
    return


if __name__ == '__main__':
    #from sampleCase import sample_full_text
    #sample_full_text = ". All three are over 65 years old and have been denied enrollment in the Medicare Part B supplemental medical insurance program established by § 1831 et seq. of the Social Security Act of 1935, 49 Stat. 620, as added, 79 Stat. 301, and as amended, 42 U. S. C. § 1395j et seq. (1970 ed. and Supp. IV). Specifically, they attack 42 U. S. C. § 1395o (2) (1970 ed., Supp. IV), which grants eligibility to resident citi-zents who are 65 or older but denies eligibility to comparable aliens unless they have been admitted for permanent residence and also have resided in the United States for at least five years. A"
    #sample_full_text = "All three are over 65 years old and have been denied enrollment in the Medicare Part B supplemental medical insurance program established by § 1831 et seq. of the Social Security Act of 1935, 49 Stat. 620, as added, 79 Stat. 301, and as amended, 42 U. S. C. § 1395j et seq. (1970 ed. and Supp. IV). They brought this action to challenge the statutory basis for that denial. Specifically, they attack 42 U. S. C. § 1395o (2) (1970 ed., Supp. IV), which grants eligibility to resident citi-zents who are 65 or older but denies eligibility to comparable aliens unless they have been admitted for permanent residence and also have resided in the United States for at least five years."
    sample_full_text = "These include prohibitions and restrictions upon Government employment of aliens, e. g., 10 U. S. C. § 5571; 22 U. S. C. § 1044 (e), upon private employment of aliens, e. g., 10 U. S. C. § 2279; 12 U. S. C. § 72, and upon investments and businesses of aliens, e. g., 12 U. S. C. §619; 47 U. S. C. § 17; statutes excluding aliens from benefits available to citizens, e. g., 26 U. S. C. § 931 (1970 ed. and Supp. IV); 46 U. S. C. § 1171 (a), and from protections extended to citizens, e. g., 19 U.S. C. § 1526; 29 U. S. C. § 633a (1970 ed., Supp. IV); and statutes imposing added burdens upon aliens, e. g., 26 U. S. C. § 6851 (d); 28 U. S. C. § 1391 (d)."
    process(sample_full_text)


'''
. 
All three are over 65 years old and have been denied enrollment in the Medicare Part B supplemental medical insurance program established by § 1831 et seq. of the Social Security Act of 1935, 49 Stat. 620, as added, 79 Stat. 301, and as amended, 42 U. S. C. § 1395j et seq. (1970 ed. and Supp. IV). 
Specifically, they attack 42 U. S. C. § 1395o (2) (1970 ed., Supp. IV), which grants eligibility to resident citi-zents who are 65 or older but denies eligibility to comparable aliens unless they have been admitted for permanent residence and also have resided in the United States for at least five years. 
A
'''

#  . All three are over 65 years old and have been denied enrollment in the Medicare Part B supplemental medical insurance program established by § 1831 et seq. of the Social Security Act of 1935, 49 Stat. 620, as added, 79 Stat. 301, and as amended, 42 U. S. C. § 1395j et seq. (1970 ed. and Supp. IV). They brought this action to challenge the statutory basis for that denial. Specifically, they attack 42 U. S. C. § 1395o (2) (1970 ed., Supp. IV), which grants eligibility to resident citi-zents who are 65 or older but denies eligibility to comparable aliens unless they have been admitted for permanent residence and also have resided in the United States for at least five years. A
