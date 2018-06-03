#!/usr/bin/python
import csv
import string
import math
from FakeNewsChallenge import FakeNews,NewsClassifier

##############################################################
# Validation script. Performs 10-fold validation on the data #
# Authors: Ambrose Hill & Yuvraj Singh                       #
##############################################################


if __name__ == "__main__":

    #List of training articles
    fakeNewsList = []
    #List of the 10 subsets
    subSets = []
    #Load training data
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

    # Split the set into 10 different subsets
    # Read with each subset being the test data for one case, 
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
            fileName = "Labled_Results_" + str(indexSet) + ".csv"
            with open(fileName, 'wb') as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for i in range(len(subset)):
                    filewriter.writerow([subset[i].headline,subset[i].bodyId, subset[i].stance])
            break
        """
        print("Trying out Subset: " + str(indexSet) + " with size: " + str(len(subset)))
        #Make its classifier
        newsClass = NewsClassifier()
        #Read training data in
        trainingSize = 0
        for subset2 in subSets:
            #Make sure we don't use the test set
            if (subset != subset2):
                trainingSize += len(subset2)
                for x in subset2:
                    newsClass.readInput(x)

        print("Trained with size: " + str(trainingSize))

        #Write out the results of the training set
        fileName = "Labled_Results_" + str(indexSet) + ".csv"
        with open(fileName, 'wb') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for i in range(len(subset)):
                filewriter.writerow([subset[i].headline,subset[i].bodyId, subset[i].stance])


        #Determine the stances for each article in training set
        resultStances = newsClass.doesDiscuss(subset)

        #For each article which is related, categorise as agree, disagree or discuss using naive bayes
        for i in range(len(subset)):
            if (i % 100 == 0):
                print(str(i) + " completed")
            if (resultStances[i] == 'discuss'):
                resultStances[i] = newsClass.makePrediction(subset[i])

        #Write the results to a file
        resultsFile = "results_" + str(indexSet) + ".csv"
        with open(resultsFile, 'wb') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for i in range(len(subset)):
                filewriter.writerow([subset[i].headline, subset[i].bodyId, resultStances[i]])
        #        filewriter.writerow([subset[i].bodyId, resultStances[i]])
"""