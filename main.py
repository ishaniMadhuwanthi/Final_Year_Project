import pdf2text as p2t
import keywordList as kList
import functions as f
import preprocess as pre
import nltk.data
#nltk.download()


doc_path = input("Enter the path of the pdf:")
#doc_path="pdf1.pdf"
p2t.pdf_to_text(doc_path)

file = open("myfile.txt", "rt")
data = file.read()

##.............keyword extraction..........##


##
data = data.upper()
# print(data)
import re


def preprocess(text):
    text = text.replace("V.", "VS")
    text = text.replace("VS.", "VS")
    text = text.replace("P. C", "PRIMARY COURT")
    text = text.replace("D. C.", "DISTRICT COURT")
    text = text.replace("M. C", "MAGISTRATE COURT")
    text = text.replace("HTTPS://WWW", " ")
    text = text.replace("10/31/2020", " ")
    return text


data = preprocess(data)
# print(data)

sentences_list = []
previous_judgment_list = []
sentences_list = data.split(".")

# print(sentences_list)
####################################find date######################################
'''
from datetime import datetime

import datefinder
matches = list(datefinder.find_dates(data))
if len(matches) > 0:
		print(matches[0])   
# date returned will be a datetime.datetime object. here we are only using the first 
#match.
 #print(matches)
else:
   print ('No dates found')
'''

######################################find name###############################################################

name = ''
for sentence in sentences_list:
    if sentence.count('VS') > 0:
        print("Case Name:" + sentence)
        name = sentence
    break

######################################################################### find court ######################################################

court_search = ["PRIMARY COURT", "DISTRICT COURT", "MAGISTRATE COURT", "SUPREME COURT", "COURT OF APPEAL",
                "LABOUR COURTS", "JUDICIAL SERVICE COMMISION", "C.R"]
count = 0;
for sentence in sentences_list:
    for i in range(8):
        if sentence.count(court_search[i]) > 0:
            count = count + 1
            if count == 1:
                print("Court and Reference Number:" + sentence)

####################################################################find previous cases###############################################


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

#####################keyword extraction -just tfidf################################################################


vocab_dict, arr = pre.textProcessing(data)
tf = f.computeTF(vocab_dict, arr)
idf = f.computeIDF([vocab_dict])
tfidf = f.computeTfidf(tf, idf)

with open("keywords.txt", "w") as outfile:
    outfile.write("\n".join(tfidf))

print('keywords:')
print(tfidf)

##################################extra######################3

# import nltk
# nltk.download('punkt')
# tokens = nltk.word_tokenize(data)
# print(tokens[0])
# sentences_with_word.append(sentence)


#....2020/12/11...keyword extraction using nlp



