import re
import math
import ast

class Sentiment:
    data = {}
    language = "ang"

    def setLanguage(language):
         self.language = language

#usuwanie końcówki ze słowa - dla języka angielskiego
    def cleanWordAng(self, word):
        word = word.lower()
        if ( len(word) > 3 and (word.endswith("es") or word.endswith("ed"))):
            word = word[:-2]
        elif(len(word) > 5 and word.endswith("ing")):
            word = word[:-3]
        elif (len(word) > 3 and (word.endswith("s") or word.endswith("e"))):
            word = word[:-1]
        return word


    def cleanWord(self, word):
        word = word.lower()
        if (self.language == "pl"):
            word = self.cleanWordPl(word)
        else:
            word = self.cleanWordAng(word)
        return word
        

#pobiera string z jednym komentarzem oraz jego wage (-1 - neg; 1 - pos)
    def training(self, comment, weight):
        comment = re.sub('[^A-Z^a-z]', ' ', comment)
        list = comment.split()
        for i in range(0,len(list)):
            pom = self.cleanWord(list.pop(0))
            if pom in self.data.keys():
                tuple = (round(self.data[pom][0]+weight, 3),self.data[pom][1]+1)
                self.data[pom] = tuple
            else:
                self.data[pom] = (weight, 1)

#pobiera string ze ścieżką do pliku z komentarzami oraz ich wage  (-1 - neg; 1 - pos; musi być jednakowa dla każdego komentarza z pliku)
    def trainFromFile(self, fileName, sentiment):
        file = open(fileName, "r")
        for line in file:
            self.training(line, sentiment)

#zapisanie nauczonych słów i ich wag do pliku
    def saveSentimentsToFile(self, filename):
        file = open(filename, "w")
        file.write(str(self.data))

#pobranie z pliku wcześniej wygenerowanych danych (słów i wag)
    def getTrainFromFile(self, fileName):
        file = open(fileName, "r")
        self.data = ast.literal_eval(file.read())

#analiza pojedyńczego komentarzu
#zwracany jest wynik analizy komentarzu
    def analysis(self, comment, sentiment):
        comment = re.sub('[\W]', ' ', comment)
        list = comment.split()
        result = 0
        pos = 0
        neg = 0
        score=0
        count=0
        sent=""
        pom2=0
        count2=0;
        for i in range(0,len(list)):
            word = self.cleanWord(list.pop(0))
            pom2=0
            if word in self.data.keys():
                pom2 = self.data[word][0]/self.data[word][1]
                if self.data[word][1] < 5:
                    pom2 = pom2/2
                score += pom2
                if pom2 > 0.15:
                    pos+=pom2;
                    count2+=1;
                if pom2 < -0.15:
                    neg +=pom2;
                    count2+=1;
                count+=1;
            sent += "  "+str(pom2)
        if pos-neg != 0:
            posm = pos/count
            negm = neg/count
            norm_score = (posm+negm)/((posm-negm))
            if norm_score > 1:
                norm_score = 1
            if norm_score < -1:
                norm_score = -1;
        else:
            norm_score = 0
        grade = ""
        if count == 0:
            count = 1
        if  norm_score < -0.4:
            grade = "NEG"
        if norm_score > -0.1 and norm_score < 0.1:
            grade = "NEU"
        if norm_score > 0.4:
            grade = "POS"
        if grade != "":
            print(comment+"\npos: " + repr(round(pos/count,3)) + " i neg: " + repr(round(neg/count,3)) + " ocena: "+grade)
        if sentiment == -1 and norm_score < -0.4:
            return (comment+"\n")
        if sentiment == 0 and norm_score > -0.1 and norm_score < 0.1:
            return (comment+"\n")
        if sentiment == 1 and norm_score > 0.4:
            return (comment+"\n")
        return ""

#pobiera ścieżkę do pliku, w którym znajdują się komentarze do ocenienia (oddzielone 'enterem')
#zwraca wynik analiz każdego komentarzu
    def analysisFromFile(self, fileName, sentiment):
        result = ""
        file = open(fileName, "r");
        for line in file:
            result += self.analysis(line, sentiment)
        return result


sen = Sentiment();

	#zakomentowane: uczenie - tworzenie bazy danych
#sen.trainFromFile("pos.txt", 1.0)
#sen.trainFromFile("neg.txt", -1.0)

#sen.trainFromFile("pozytywne.txt", 1.0)
#sen.trainFromFile("negatywne.txt", -1.0)

#sen.trainFromFile("new_pos.txt", 0.8)
#sen.trainFromFile("new_neg.txt", -0.8)

#sen.saveSentimentsToFile("dataFilmy")

sen.getTrainFromFile("dataFilmy")	#pobranie gotowej bazy danych
result = sen.analysisFromFile("komentarzeDoAnalizy.txt", 0)	#analiza komentarzy
