from itertools import product
from nltk.corpus import wordnet
# retrive the markshceme.

#tage the markscheme

# retrive only the nouns from the markshcme.

# store the nouns in a list

# loop retireve  all the answers one by one.
    get the first answer
    do the tagging
    retrive the nouns list

#retrive the second file

# tag the first

sims = []
initialList = []
list1 = ['Compare', 'require']
list2 = ['choose', 'copy', 'define', 'duplicate', 'find', 'how', 'identify', 'label', 'list', 'listen', 'locate', 'match', 'memorise', 'name', 'observe', 'omit', 'quote', 'read', 'recall', 'recite', 'recognise', 'record', 'relate', 'remember', 'repeat', 'reproduce', 'retell', 'select', 'show', 'spell', 'state', 'tell', 'trace', 'write']

for word1, word2 in product(list1, list2):
    syns1 = wordnet.synsets(word1)
    print(syns1)
    syns2 = wordnet.synsets(word2)
    print(syns2)
    for word1 in syns1:
        for word2 in syns2:
            s = word1.wup_similarity(word2)
            if str(s) == 'None':
                s = 0


            initialList.append(s)
            print(str(word1) + " second word"+  str(word2))
#insert  into checksimilalrity(doc1,doc2,word1,word2,value) values( '','','','','')
            print(s)
    print(initialList)