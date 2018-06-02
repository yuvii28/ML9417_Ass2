#!/usr/bin/python
import csv
import string
import math


##############################################################
# Main Python File for COMP9417 ASSIGNMENT 2 SEMESTER 1 2018 #
# Authors: Ambrose Hill & Yuvraj Singh                       #
##############################################################



#Class to store each FakeNewsArticle
#Contains a headline, body id, body and a stance. 
class FakeNews:
    def __init__(self,bodyId, headline, stance):
        self.bodyId = bodyId
        self.body = ''
        self.stance = stance
        self.headline = headline
    def addStance(self,stance):
        self.stance = stance 

    def addBody(self,body):
        self.body = body
    
    def printO(self):
        print("Printing Object:{0}\nHeadline: {1}\nStance: {2}\nBody length: {3}\n").format(self.bodyId,self.headline,self.stance,len(self.body))

#Class to classify articles, begins by going over training set
#Has methods to train and predict FakeNews objects.
class NewsClassifier:
    def __init__(self):
        #What words have been seen
        self.dictionary = set()
        #Counts for each word. access dictionary as self.wordCounts[category][word] = count
        self.wordCounts = {}
        #Count how many times each stance appears in training set
        self.stanceCounts = {} 
        #Ignore list for exessive or meangingless words
        self.ignore = ['the', 'a', 'an', 'he', 'she', 'him', 'her', 'them','it','that','this','and','or']


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
            if word not in self.ignore:
                if (word not in self.dictionary):
                    self.dictionary.add(word)
                if (word not in self.wordCounts[article.stance]):
                    self.wordCounts[article.stance][word] = 0.0
                self.wordCounts[article.stance][word] += 1.0

    #Categorise the article as related or unrelated 
    def doesDiscuss(self, articles):
        result = []
        for i in range(len(articles)):
            article = articles[i]

            #If all words from headline appear once, assume discussion
            headline = self.cleanup(str(article.headline))
            body = self.cleanup(str(article.body))
            stance = 'discuss'
            numNot = 0.0
            size_headline = 0.0
            for word in headline:
                size_headline += 1
                if word not in body:
                    numNot += 1
            if (numNot > size_headline*3 / 5):
                stance = 'unrelated'
            result.append(stance)
        return result

    #Take articles, and produce a list of stances for these
    def makePrediction(self, article):
        result = 'discuss'
        headline = self.cleanup(str(article.headline))
        body = self.cleanup(str(article.body))
        words = headline + body
        #Scores of Discuss, Agree and Disagree stances
        scores = [0.0, 0.0, 0.0]    

        for word in words:
            if word not in self.ignore:
                if (word in self.dictionary):
                    #Check for word in diff possible stances.
                    #Add 1 in  case there is no example of the word
                    discuss_Prob = math.log( (self.wordCounts['discuss'].get(word, 0.0) + 1) / (sum(self.wordCounts['discuss'].values()) + len(self.dictionary))) 
                    agree_Prob = math.log( (self.wordCounts['agree'].get(word, 0.0) + 1) / (sum(self.wordCounts['agree'].values()) + len(self.dictionary))) 
                    disagree_Prob = math.log( (self.wordCounts['disagree'].get(word, 0.0) + 1) / (sum(self.wordCounts['disagree'].values()) + len(self.dictionary))) 
                    
                    scores[0] += discuss_Prob
                    scores[1] += agree_Prob
                    scores[2] += disagree_Prob

        #Take the best of the scores
        if (max(scores) == scores[0]):
            result = 'discuss'
        elif (max(scores) == scores[1]):
            result = 'agree'
        elif (max(scores) == scores[2]):
            result = 'disagree'

        return result





if __name__ == "__main__":
    #List to store the training Fake News articles
    fakeNewsList = []
    #The Classifer
    newsClass = NewsClassifier()
    #List to store the test Fake News Articles
    realNewsList = []


    #Load the training data from the training sets
    #Data contained in two csv files. 
    #One containing, headline, body id and a stance
    #Other contating body id and body
    with open('train_bodies.csv','rb') as tb:
        with open('train_stances.csv','rb') as ts:
            tbreader = csv.reader(tb)
            tsreader = csv.reader(ts)
            fakeNewsList = [FakeNews(int(row[1]),row[0], row[2]) for row in tsreader]

            for row in tbreader:
                bodyId = int(row[0])
                for x in fakeNewsList:
                    if(x.bodyId == bodyId):
                        x.addBody(row[1])
            #Train our classifer with all the new articles           
            for x in fakeNewsList:
                newsClass.readInput(x)
    #Print the length of the training set.
    #print(len(fakeNewsList))

    #Load the unlabeled test data 
    #Similiar to above but without the stance.
    with open('competition_test_bodies.csv','rb') as tb2:
        with open('competition_test_stances_unlabeled.csv','rb') as ts2: 
            tbreader = csv.reader(tb2)
            tsreader = csv.reader(ts2)

            realNewsList = [FakeNews(int(row[1]), row[0], '') for row in tsreader]

            for row in tbreader:
                bodyId = int(row[0])
                for x in realNewsList:
                    if(x.bodyId == bodyId):
                        x.addBody(row[1])

    #Determine the stances for each article as related or unrelated
    #The splitting of test data based on initial stance
    resultStances = newsClass.doesDiscuss(realNewsList)

    #For each article which is related, categorise as agree, disagree or discuss using naive bayes
    #   The probability P (Category | words in article) is given by
    #      P (word_1 | Category) * P (word_2 | Category) * ... * P (word_n | Category) * P (Category)
    for i in range(len(realNewsList)):
        #Status print statement
        if (i % 100 == 0):
            print(str(i) + " completed")
        #If the article was related, make a prediction
        if (resultStances[i] == 'discuss'):
            resultStances[i] = newsClass.makePrediction(realNewsList[i])


    #Write the results to a csv file
    #Using format: Headline,Body ID,Stance -- for usage with scorer.py
    with open('results.csv', 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in range(len(realNewsList)):
            filewriter.writerow([realNewsList[i].headline, realNewsList[i].bodyId, resultStances[i]])
     #       filewriter.writerow([realNewsList[i].bodyId, resultStances[i]])
