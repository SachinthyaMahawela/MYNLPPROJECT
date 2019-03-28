import mysql.connector
import nltk


from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

cnx = mysql.connector.connect(user='sachi', password='Abc123@#(', host='localhost', database='projectdb')
cursor = cnx.cursor()


class SimilarityChecker:

    def calculateChecker(self,assignment,markingscheme,doc_id, msdata_id, taxonomy_id):
       self.extract_nouns(self,assignment,markingscheme,doc_id, msdata_id, taxonomy_id)

    def extract_nouns(self,assignment,markingscheme,doc_id, msdata_id, taxonomy_id):
        ass=str(assignment)
        sentences = nltk.word_tokenize(ass)
        # print 'sentence'
        sentences = [nltk.word_tokenize(sent) for sent in sentences]
        # print 'word', sentences
        sentences = [nltk.pos_tag(sent) for sent in sentences]
        # print 'POS',sentences
        verbList =self.questionNouns(sentences,assignment,markingscheme,doc_id, msdata_id, taxonomy_id)

    def assignmentNouns(self, sentences,assignment,sub, level, sem):
        verbList = []
        isVB = False
        isNNP = False
        isWH = False

        for oneList in sentences:
            # print 'one list: ', oneList[0][0],oneList[0][1]

            if(oneList[0][1].startswith('NNP') or oneList[0][1].startswith('NN')):
                print (oneList[0][0])
                Lemmatizer = WordNetLemmatizer()
                noun_lemmatize=Lemmatizer.lemmatize(oneList[0][0])
                # print 'lemmatize ',noun_lemmatize
                insertsql = "insert into assignment_nouns_insert(subject,level,semester,assignment,no_of_nouns)values('" + str(sub) + "','" + str(level)+ "','" + str(sem) + "','" + str(getassignment)+ "','" + str(noun_lemmatize)+ "')"
                cursor.execute(insertsql)

    def extract_mscheme_nouns(self, mscheme, b_topic, com_text):

        sentences = nltk.sent_tokenize(str(mscheme))
        sentences = [nltk.word_tokenize(sent) for sent in sentences]
        # print 'content sentence', sentences

        for one_list in sentences:
            # print 'one sentence list', one_list
            list2 = []
            list3 = []
            list4 = []
            list2 = [el.replace('\\n', ' ') for el in one_list]
            # print 'list2',list2
            list3 = [el.replace('\\', ' ') for el in list2]
            list4 = [el.replace("'", " ") for el in list3]

            split_sentence = [words for segments in list4 for words in segments.split()]
            # print '>> ', split_sentence
            sentences1 = nltk.pos_tag(split_sentence)
            # print 'content POS', sentences1
            verbList = self.search_mscheme_nouns(sentences1, b_topic, com_text)


    def search_mscheme_nouns(self, mscheme_sentence, topic, com_text):
        print ('#####', topic, '######')

        for oneList in mscheme_sentence:
            if ([oneList][0][1].startswith('NNP') or [oneList][0][1].startswith('NN')):
                if (len([oneList][0][0]) == 3 and [oneList][0][0].startswith('x')):
                    continue;
                else:
                    if ([oneList][0][0].startswith('[') or [oneList][0][0].startswith(']') or len(
                            [oneList][0][0]) == 1):
                        continue;
                    else:
                        # print '>>', [oneList][0][0]
                        Lemmatizer = WordNetLemmatizer()
                        noun_lemmatize = Lemmatizer.lemmatize([oneList][0][0])

                        # print [oneList][0][0], ' >> lemmatize >> ', noun_lemmatize

                        insertsqlmscheme = "insert into content_noun_insert(subject,topic,no_of__noun)values('" + str(
                            com_text) + "','" + str(topic) + "','" + str(noun_lemmatize) + "')"
                        cursor.execute(insertsqlmscheme)

    def wordSynsetSimilarity(self,com_text):
        selectassignment = "SELECT distinct no_of_nouns FROM document_data where assignment_name='" + str(com_text) + "'"
        retriveassignment =  cursor.execute(selectassignment)

        b_assignment = [str(text[0]) for text in retriveassignment]
        print (b_assignment)
        for assignment in b_assignment:
            print (assignment)
            selectQuestionNoun = "select no_of_nouns FROM mscheme_data where subject='" + str(com_text) + "' " \
                                                "and assignment='" + str(assignment) + "' "
            retriveQuestionNoun = cursor.execute(selectQuestionNoun)

            b_assignment_noun = [str(text[0]) for text in retriveQuestionNoun]
            print (b_assignment_noun)

            for q_noun in b_assignment_noun:

                selectTopic = "select distinct topic from content_noun where subject='" + str(com_text) + "'"
                retriveTopic = cursor.execute(selectTopic)

                b_topic = [str(text[0]) for text in retriveTopic]
                # print b_topic

                for Topic in b_topic:
                    selectmschemeNoun = "select no_of_nouns from mscheme_data where subject='" + str(com_text) + "' and topic='" + str(Topic) + "'"
                    retrivemschemeNoun = cursor.execute(selectmschemeNoun)

                    b_mscheme_noun = [str(text[0]) for text in retrivemschemeNoun]
                    set_mscheme_noun = set(b_mscheme_noun)
                    print ('set mscheme /// > ', set_mscheme_noun)

                    for q_mscheme in set_mscheme_noun:

                        wordFromList1 = wordnet.synsets(q_noun)
                        wordFromList2 = wordnet.synsets(q_mscheme)

                        if wordFromList2 == [] or wordFromList1 == []:
                            print (wordFromList1)
                            print (wordFromList2)
                            print ('empty')
                        else:
                            listA = wordFromList1[0].name().partition('.')[0]
                            # print 'listA >>   ', listA
                            listB = wordFromList2[0].name().partition('.')[0]
                            # print 'listB >>   ',listB
                            s = wordFromList1[0].wup_similarity(wordFromList2[0])
                            if s != None:
                                print (listA, ' >> ', listB, ' >> ', s)
                                insertsqlSimilarity = "insert into synset_similarity_between_assignment_mscheme_insert(subject,assignment,topic,assignment_noun,mscheme_noun,similarity)values('" + str(
                                            com_text) + "','" + str(assignment) + "','" + str(Topic) + "','" + str(listA) + "','" + str(listB) + "','" + str(s) + "')"
                                cursor.execute(insertsqlSimilarity)

    def maxSimilarityTen(self,com_text):
        selectTopic = "SELECT distinct topic FROM synset_similarity_between_assignment_mscheme where subject='" + str(com_text) + "'"
        retriveTopic = cursor.execute(selectTopic)

        b_topic = [str(text[0]) for text in retriveTopic]
        print ('>>',b_topic)

        for topic in b_topic:
            print ('topic>> ',topic)
            selectassignment = "SELECT distinct assignment FROM synset_similarity_between_assignment_mscheme where subject='" + str(com_text) + "'"
            retriveassignment =cursor.execute(selectassignment)

            b_assignment = [str(text[0]) for text in retriveassignment]
            print ('>>', b_assignment)
            for assignment in b_assignment:
                print ('assignment .. >',assignment)

                selectMaxSimilarity = "SELECT similarity FROM synset_similarity_between_assignment_mscheme where subject='" + str(
                    com_text) + "' and topic='" + str(topic) + "' and question='" + str(assignment) + "' order by similarity  desc limit 15"
                retriveMaxSimilarity = cursor.execute(selectMaxSimilarity)

                b_maxSimilarity = [str(text[0]) for text in retriveMaxSimilarity]
                count_simialrity = 0
                for max_similarity in b_maxSimilarity:
                    print ('max similarity >>',max_similarity)
                    count_simialrity=count_simialrity+float(max_similarity)
                    print ('count similarity  >>   ',count_simialrity)
                print ('count similarity      >>   ', count_simialrity)
                insertsqlMaxSimilarity = "insert into max_similarity_insert(subject_name,topic,question,max_similarity)values('" + str(
                            com_text) + "','" + str(topic) + "','" + str(assignment) + "','" + str(count_simialrity) + "')"
                cursor.execute(insertsqlMaxSimilarity)