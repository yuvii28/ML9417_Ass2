#!/usr/bin/python
import csv
import string
import math

ignore = ['the', 'a', 'an', 'he', 'she', 'him', 'her', 'them']

#Class to store each FakeNewsArticle
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

fakeNewsList = []

with open('tb.csv','rb') as tb:
    with open('ts.csv','rb') as ts:
        tbreader = csv.reader(tb)
        tsreader = csv.reader(ts)
        fakeNewsList = [FakeNews(int(row[1]),row[0], row[2]) for row in tsreader]

        for row in tbreader:
            bodyId = int(row[0])
            for x in fakeNewsList:
                if(x.bodyId == bodyId):
                    x.addBody(row[1])

# Split the set into 10 different subsets
# Read with each subset being the test data for one case, 
subSets = []
size = len(fakeNewsList)
subSets.append(fakeNewsList[0: size/10])
subSets.append(fakeNewsList[size/10: 2*size/10])
subSets.append(fakeNewsList[2*size/10: 3*size/10])
subSets.append(fakeNewsList[3*size/10: 4*size/10])
subSets.append(fakeNewsList[4*size/10: 5*size/10])
subSets.append(fakeNewsList[5*size/10: 6*size/10])
subSets.append(fakeNewsList[6*size/10: 7*size/10])
subSets.append(fakeNewsList[7*size/10: 8*size/10])
subSets.append(fakeNewsList[8*size/10: 9*size/10])
subSets.append(fakeNewsList[9*size/10:])
# We now have the subsets
# For each one, treat it as a test for other training
for subset in subSets:
    indexSet = int(subSets.index(subset))
    if (indexSet == 0):
        continue
    print("Trying out Subset: " + str(indexSet) + " with size: " + str(len(subset)))
    #Make its classifier
    newsClass = newsClassifier()
    #Read training data in
    trainingSize = 0
    for subset2 in subSets:
        if (subset != subset2):
            trainingSize += len(subset2)
            for x in subset2:
                newsClass.readInput(x)

    print("Trained with size: " + str(trainingSize))

    #Write out the results of the training set
    fileName = "Labled_Results_" + str(indexSet) + ".csv"
    with open(fileName, 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in range(len(subset)):
            filewriter.writerow([subset[i].bodyId, subset[i].stance])

    #Determine the stances for each article in training set
    resultStances = newsClass.doesDiscuss(subset)

    #For each article which is related, categorise as agree, disagree or discuss using naive bayes
    for i in range(len(subset)):
        if (i % 100 == 0):
            print(str(i) + " completed")
        if (resultStances[i] == 'discuss'):
            resultStances[i] = newsClass.makePrediction(subset[i])

    resultsFile = "results_" + str(indexSet) + ".csv"
    with open(resultsFile, 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in range(len(subset)):
    #        filewriter.writerow([realNewsList[i].headline, realNewsList[i].bodyId, resultStances[i]])
            filewriter.writerow([subset[i].bodyId, resultStances[i]])