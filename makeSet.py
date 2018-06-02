#!/usr/bin/python
import csv
import string
import math

#Class to store each FakeNewsArticle
class FakeNews:
    def __init__(self,bodyId, headline, stance):
        self.bodyId = bodyId
        self.body = ''
        self.stance = headline
        self.headline = stance
    def addStance(self,stance):
        self.stance = stance 
    def addBody(self,body):
        self.body = body
    
    def printO(self):
        print("Printing Object:{0}\nHeadline: {1}\nStance: {2}\nBody length: {3}\n").format(self.bodyId,self.headline,self.stance,len(self.body))

fakeNewsList = []


with open('competition_test_bodies.csv','rb') as tb:
    with open('competition_test_stances.csv','rb') as ts:
        tbreader = csv.reader(tb)
        tsreader = csv.reader(ts)
        fakeNewsList = [FakeNews(int(row[1]),row[2], row[0]) for row in tsreader]
        fakeNewsList[0].printO()
        for row in tbreader:
            bodyId = int(row[0])
            for x in fakeNewsList:
                if(x.bodyId == bodyId):
                    x.addBody(row[1])

#   The probability P (Category | words in article) is given by
#      P (word_1 | Category) * P (word_2 | Category) * ... * P (word_n | Category) * P (Category)

#   Denominator is usually used, however only exists to scale result so not needed
#   (denominator will be consistent for all cetegories)

with open('compResults_5000.csv', 'wb') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
#    filewriter.writerow(['Body ID','Body', 'Stance'])
    for i in range(5000):
        filewriter.writerow([fakeNewsList[i].bodyId, fakeNewsList[i].stance])
