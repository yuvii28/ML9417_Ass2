#!/usr/bin/python
import csv
import string
import math

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

fakeNewsList = []

with open('competition_test_bodies.csv','rb') as tb:
    with open('competition_test_stances.csv','rb') as ts:
        tbreader = csv.reader(tb)
        tsreader = csv.reader(ts)
        fakeNewsList = [FakeNews(int(row[0]),row[1]) for row in tbreader]
        tempHead = []
        tempStance = []
        for row in tsreader:
            bodyId = int(row[1])
            numItems = bodyId
            for x in fakeNewsList:
                if(x.bodyId == bodyId):
                    x.addStance(row[2])
                    x.addHeadline(row[0])
#   The probability P (Category | words in article) is given by
#      P (word_1 | Category) * P (word_2 | Category) * ... * P (word_n | Category) * P (Category)

#   Denominator is usually used, however only exists to scale result so not needed
#   (denominator will be consistent for all cetegories)

with open('compResults_1000.csv', 'wb') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
#    filewriter.writerow(['Body ID','Body', 'Stance'])
    for i in range(900):
        stance = 'unrelated'
        if (fakeNewsList[i].stance != stance):
            stance = 'discuss'
        filewriter.writerow([fakeNewsList[i].bodyId, stance])