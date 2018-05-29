#!/usr/bin/python
import csv
import string
import math

ignore = ['the', 'a', 'an']

#Class to store each FakeNewsArticle
class FakeNews:
    def __init__(self,bodyId,body):
        self.bodyId = bodyId
        self.body = body
        self.stance = ''
        self.headline = ''
    def addStance(self,stance):
        self.stance = stance 

    def addHeadline(self,headline):
        self.headline = headline
    
    def printO(self):
        print("Printing Object:{0}\nHeadline: {1}\nStance: {2}\nBody length: {3}\n").format(self.bodyId,self.headline,self.stance,len(self.body))

#Class to classify articles, begins by going over training set
class newsClassifier:
    def __init__(self):
        #What words have been seen
        self.dictionary = set()
        #Counts for each word. access dictionary as self.wordCounts[category][word] = count
        self.wordCounts = {}
        #Count how many times each stance appears in training set
        self.stanceCounts = {}


    #Function to clean up all punctuation and make all words lowercase s
    def cleanup(self, inputString):
        ret = inputString.translate(None, string.punctuation)
        return ret.lower().split(" ")

    #Takes in a FakeNews object and adds as training data
    def readInput(self, article):
        #Remove punctuation, and split vocabulary up
        headline = self.cleanup(str(article.headline))
        body = self.cleanup(str(article.body))
        words = headline + body

        #Is it a new stance?
        if (article.stance not in self.stanceCounts):
            self.stanceCounts[article.stance] = 0.0
            self.wordCounts[article.stance] = {}

        #Add word into data
        for word in words:
            if (word not in self.dictionary):
                self.dictionary.add(word)
            if (word not in self.wordCounts[article.stance]):
                self.wordCounts[article.stance][word] = 0.0
            self.wordCounts[article.stance][word] += 1.0

    def doesDiscuss(self, articles):
        result = []
        for i in range(900):
            article = articles[i]
            #If all words from headline appear once, assume discussion
            headline = self.cleanup(str(article.headline))
            body = self.cleanup(str(article.body))
            stance = 'discuss'
            numNot = 0.0
            size_headline = 0.0
            for word in headline:
                if word not in ignore:
                    size_headline += 1
                    if word not in body:
                        numNot += 1
            if (numNot > size_headline*3 / 5):
                stance = 'unrelated'
            result.append(stance)
        return result

    #Take articles, and produce a list of stances for these
    def makePrediction(self, articles):
        result = []
        numread = 0
        for i in range(900):
            article = articles[i]
            if (numread % 1000 == 0):
                print (str(numread) + " articles predicted")
            numread += 1
            headline = self.cleanup(str(article.headline))
            body = self.cleanup(str(article.body))
            words = headline.split(" ") + body.split(" ")


            scores = [0.0, 0.0, 0.0, 0.0]

            for word in words:
                if (word in self.dictionary):
                    #Check for word in diff possible stances.
                    #Add 1 in  case there is no example of the word
                    unrelated_Prob = math.log( (self.wordCounts['unrelated'].get(word, 0.0) + 1) / (sum(self.wordCounts['unrelated'].values()) + len(self.dictionary))) 
                    discuss_Prob = math.log( (self.wordCounts['discuss'].get(word, 0.0) + 1) / (sum(self.wordCounts['discuss'].values()) + len(self.dictionary))) 
                    agree_Prob = math.log( (self.wordCounts['agree'].get(word, 0.0) + 1) / (sum(self.wordCounts['agree'].values()) + len(self.dictionary))) 
                    disagree_Prob = math.log( (self.wordCounts['disagree'].get(word, 0.0) + 1) / (sum(self.wordCounts['disagree'].values()) + len(self.dictionary))) 
                    
                    scores[0] += unrelated_Prob        
                    scores[1] += discuss_Prob
                    scores[2] += agree_Prob
                    scores[3] += disagree_Prob

            if (max(scores) == scores[0]):
                result.append('unrelated')
            elif (max(scores) == scores[1]):
                result.append('discuss')
            elif (max(scores) == scores[2]):
                result.append('agree')
            elif (max(scores) == scores[3]):
                result.append('disagree')
        return result

fakeNewsList = []
newsClass = newsClassifier()

with open('tb.csv','rb') as tb:
    with open('ts.csv','rb') as ts:
        tbreader = csv.reader(tb)
        tsreader = csv.reader(ts)
        fakeNewsList = [FakeNews(int(row[0]),row[1]) for row in tbreader]
        tempHead = []
        tempStance = []
        for row in tsreader:
            bodyId = int(row[1])
            for x in fakeNewsList:
                if(x.bodyId == bodyId):
                    x.addStance(row[2])
                    x.addHeadline(row[0])

        for x in fakeNewsList:
            newsClass.readInput(x)

realNewsList = []
with open('competition_test_bodies.csv','rb') as tb2:
    with open('competition_test_stances_unlabeled.csv','rb') as ts2: 
        tbreader = csv.reader(tb2)
        tsreader = csv.reader(ts2)
        realNewsList = [FakeNews(int(row[0]),row[1]) for row in tbreader]
        tempHead = []
        tempStance = []
        for row in tsreader:
            bodyId = int(row[1])
            for x in realNewsList:
                if(x.bodyId == bodyId):
                    x.addHeadline(row[0])

resultStances = newsClass.doesDiscuss(realNewsList)


#   The probability P (Category | words in article) is given by
#      P (word_1 | Category) * P (word_2 | Category) * ... * P (word_n | Category) * P (Category)

#   Denominator is usually used, however only exists to scale result so not needed
#   (denominator will be consistent for all cetegories)

with open('results.csv', 'wb') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in range(900):
#        filewriter.writerow([realNewsList[i].headline, realNewsList[i].bodyId, resultStances[i]])
        filewriter.writerow([realNewsList[i].bodyId, resultStances[i]])