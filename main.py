from spacy.lang.en.tokenizer_exceptions import string

import pdf2text as p2t
import re

import preprocess as pre
import nltk.data
from nltk import sent_tokenize
# nltk.download()


# enter pdf document
doc_path = input("Enter the path of the pdf:")

# covert pdf to text file
p2t.pdf_to_text(doc_path)

# read the text file
file = open("myfile.txt", "rt")
data = file.read()

# remove page numbers
page = re.sub(r'(\s([?,.!"]))|(?<=\[|\()(.*?)(?=\)|\])', lambda x: x.group().strip(), data)
pageNumRegex = re.compile(r'(\([0-9]+\))')
result = pageNumRegex.sub("", page)

# pageNo = pageNumRegex.search(page)
# print(pageNo.group(1))

# convert text to upper case
result = result.upper()
#print(result)

# remove short forms
def preprocess(text):
    # vs
    text = text.replace("V.", "VS")
    text = text.replace("VS.", "VS")
    text = text.replace("VS", "VS")
    # primary court
    text = text.replace("P. C.", "PRIMARY COURT")
    text = text.replace("P. C", "PRIMARY COURT")
    text = text.replace("P.C.", "PRIMARY COURT")
    text = text.replace("PC", "PRIMARY COURT")
    text = text.replace("PC.", "PRIMARY COURT")
    text = text.replace("P.C", "PRIMARY COURT")
    # district court
    text = text.replace("D. C.", "DISTRICT COURT")
    text = text.replace("D. C", "DISTRICT COURT")
    text = text.replace("D.C.", "DISTRICT COURT")
    text = text.replace("DC", "DISTRICT COURT")
    text = text.replace("DC.", "DISTRICT COURT")
    text = text.replace("D.C", "DISTRICT COURT")
    # magistrate court
    text = text.replace("M. C.", "MAGISTRATE COURT")
    text = text.replace("M. C", "MAGISTRATE COURT")
    text = text.replace("M.C.", "MAGISTRATE COURT")
    text = text.replace("MC", "MAGISTRATE COURT")
    text = text.replace("MC.", "MAGISTRATE COURT")
    text = text.replace("M.C", "MAGISTRATE COURT")
    # supreme court
    text = text.replace("S.C.", "SUPREME COURT")
    text = text.replace("S. C", "SUPREME COURT")
    text = text.replace("S.C.", "SUPREME COURT")
    text = text.replace("SC", "SUPREME COURT")
    text = text.replace("SC.", "SUPREME COURT")
    text = text.replace("S.C", "SUPREME COURT")
    # commercial high court
    text = text.replace("CHC", "COMMERCIAL HIGH COURT")
    # high court
    text = text.replace("H.C.", "HIGH COURT")
    text = text.replace("H. C", "HIGH COURT")
    text = text.replace("H.C.", "HIGH COURT")
    text = text.replace("HC", "HIGH COURT")
    text = text.replace("HC.", "HIGH COURT")
    text = text.replace("H.C", "HIGH COURT")
    # other forms
    text = text.replace("NO.", "NO")
    text = text.replace("RS.", "RS")
    text = text.replace("HTTPS://WWW", " ")
    text = text.replace("10/31/2020", " ")
    return text


result = preprocess(result)
# print(result)

# split into sentences
sentences_list = []
from nltk import sent_tokenize
sentences_list = sent_tokenize(result)
# print(sentences_list)

previous_judgment_list = []


# ................find case name.............#

name = ''
for sentence in sentences_list:
    if sentence.count('VS') > 0:
        print("Case Name:" + sentence)
        name = sentence
    break



# ............... find court ................#

court_search = ["PRIMARY COURT", "DISTRICT COURT", "MAGISTRATE COURT", "SUPREME COURT", "COURT OF APPEAL",
                "LABOUR COURTS", "JUDICIAL SERVICE COMMISSION", "C.R"]
count = 0;
for sentence in sentences_list:
    for i in range(8):
        if sentence.count(court_search[i]) > 0:
            count = count + 1
            if count == 1:
                print("Court and Reference Number:" + sentence)



# ...............find judgement date........#

print('Judgment date:')
date_format = "\d{1,2}\w{0,2}\s\w+\W\s\d\d\d\d"   # 3RD FEBRUARY, 1887
matches = re.finditer(date_format, result, re.MULTILINE)
date_list = []  # get all the dates in the text

for matchNum, match in enumerate(matches, start=1):

    date_list = "{match}".format(match=match.group())
    print(date_list)
    # year_list = [int(i) for i in date_list.split() if i.isdigit()]
    # print(year_list)

    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1
        print("{group}".format(group=match.group(groupNum)))


# ................judges names and decision...............#

def check(sentences_list, words):
    res = [all([k in s for k in words]) for s in sentences_list]
    return [sentences_list[i] for i in range(0, len(res)) if res[i]]


words = ['J.']
judges_names = check(sentences_list, words)
print('Judges names and decision: ', *judges_names, sep="\n")

'''
there is problem that if there is any word with "J." it also taken as a judge name
'''

# .................find previous cases.......#

previous_judgments = ["THE CASE OF", "THE JUDGMENT OF", "VIDE", "VS", "HELD IN"]
count = 0
for sentence in sentences_list:
    tokens = nltk.word_tokenize(sentence)
    for i in range(4):
        for token in tokens:
            if token == previous_judgments[i]:
                if (i == 3):
                    count = count + 1
                    if (count > 1):
                        previous_judgment_list.append(sentence)

                else:
                    previous_judgment_list.append(sentence)

if len(previous_judgment_list) > 0:
    print("The Previous Judgements:")
else:
    print("No previous judgments")

for p in previous_judgment_list:
    if (p != name):
        print(p)

# print(name)




#.............keyword extraction...............#



