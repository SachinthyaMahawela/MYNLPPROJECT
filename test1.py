from itertools import product
from nltk.corpus import wordnet

sims = []

list1 = ['Compare', 'require']
list2 = ['choose', 'copy', 'define', 'duplicate', 'find', 'how', 'identify', 'label', 'list', 'listen', 'locate', 'match', 'memorise', 'name', 'observe', 'omit', 'quote', 'read', 'recall', 'recite', 'recognise', 'record', 'relate', 'remember', 'repeat', 'reproduce', 'retell', 'select', 'show', 'spell', 'state', 'tell', 'trace', 'write']

for word1, word2 in product(list1, list2):
    syns1 = wordnet.synsets(word1)
    syns2 = wordnet.synsets(word2)
    print(syns1)
    for sense1, sense2 in product(syns1, syns2):
        d= wordnet.wup_similarity(sense1, sense2)

        for word2 in list2:
            count=0
            countValue=0

            wordFromList1 = wordnet.synsets(word1,'v')
            wordFromList2 = wordnet.synsets(word2,'v')

            countValue = count +countValue

        if len(wordFromList1)>0 and len(wordFromList2)>0:

            for listA in wordFromList1:
                for listB in wordFromList2:
                    s = listA.wup_similarity(listB)
                    if str(s) == 'None':
                        s = 0
                    initialList=[]
                    initialList.append(s)

            if len(initialList)>0:
                average = 0
                average = sum(initialList)/len(initialList)
                print("sum = " +str(sum(initialList))+ " len = "+str(len(initialList))+" Avg = "+str(average))


allsyns1 = set(ss for word in list1 for ss in wordnet.synsets(word))
allsyns2 = set(ss for word in list2 for ss in wordnet.synsets(word))
best = max((wordnet.wup_similarity(s1, s2) or 0, s1, s2) for s1, s2 in product(allsyns1, allsyns2))

print(list1)
print(list2)
print(d)
print(best)

