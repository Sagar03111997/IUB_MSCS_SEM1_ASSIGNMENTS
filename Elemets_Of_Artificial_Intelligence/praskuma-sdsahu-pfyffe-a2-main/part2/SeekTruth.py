# SeekTruth.py : Classify text objects into two categories
#
# Created by sdsahu, praskuma, pfyffe
#
# Based on skeleton code by D. Crandall, October 2021
#

import sys
import math
import string
from collections import defaultdict
import re
import numpy as np

def load_file(filename):
    objects=[]
    labels=[]
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ',1)
            labels.append(parsed[0] if len(parsed)>0 else "")
            objects.append(parsed[1] if len(parsed)>1 else "")

    return {"objects": objects, "labels": labels, "classes": list(set(labels))}

# classifier : Train and apply a bayes net classifier
#
# This function should take a train_data dictionary that has three entries:
#        train_data["objects"] is a list of strings corresponding to reviews
#        train_data["labels"] is a list of strings corresponding to ground truth labels for each review
#        train_data["classes"] is the list of possible class names (always two)
#
# and a test_data dictionary that has objects and classes entries in the same format as above. It
# should return a list of the same length as test_data["objects"], where the i-th element of the result
# list is the estimated classlabel for test_data["objects"][i]
#
# Do not change the return type or parameters of this function!
#

def preprocess(sentence):
    sentence = str(sentence).lower() 
    
    # We found that these list of words had least impact on the classification result, hence we decided to remove these from  the input data-set
    blacklisted_words  = ["over", "under", "again", "further",
                          "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves",
                          "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", 
                          "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their",
                          "but", "if", "or", "because", "as", "until", "while", "against", "between",
                          "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both",
                          "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", 
                          "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", 
                          "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", 
                          "each", "few", "more", "most", "other", "some", "such",
                          "can", "will", "just", "don", "should", "now"]
                          
    
    #We made changes to the below words, having similar/same meaning (eg:- I'm and I am are same words but according to the logic implemented, the 
    #algorithm would detect it as 2 different words. Hence we found a certain set of special characters and similar words on which we performed preprocessing) 
    sentence = sentence.replace("′", "'").replace("’", "'").replace("\"", " ").replace("#", " ").replace("&", " ")\
       .replace("won't", "will not").replace("wont", "will not").replace("cannot", "can not")\
       .replace("'ve", " have").replace("i'm", "i am").replace("'re", " are")\
       .replace("he's", "he is").replace("she's", "she is").replace("'s", " is")\
       .replace("'ll", " will").replace(".", "").replace("-", " ").replace("/", " ")\
       .replace("{", " ").replace("}", " ").replace("(", " ").replace(")", " ").replace("[", " ").replace("]", " ")\
       .replace(",", " ").replace("*", " ").replace("he'd", " he would").replace("i'd", " I had")\
       .replace("(!", " ").replace(")", "").replace("0", "") 

    pattern = re.compile(r'\b(' + r'|'.join(blacklisted_words) + r')\b\s*')
    sentence = pattern.sub('', sentence)
    
    return sentence


def classifier(train_data, test_data):
    deception_dict, truth_dict = {}, {} # creating & initializing deceptive, truthful dictionary to store count of each word appearing in the training dataset.
    test_data["labels"] = []

    for index in range(len(train_data["labels"])):
        object = preprocess(train_data["objects"][index])
        if train_data["labels"][index] == "deceptive":
            for word in object.split():
                if word not in deception_dict:
                    deception_dict[word] = 1
                else:
                    deception_dict[word] += 1
        elif train_data["labels"][index] == "truthful":
            for word in object.split():
                if word not in truth_dict:
                    truth_dict[word] = 1
                else:
                    truth_dict[word] += 1
    
    # removing words with count less to improve classification accuracy, as words with less counts will have least impact on the decision
    # We have checked for multiples values and found 5 giving the best results

    for key in deception_dict.copy():
        if deception_dict[key] < 5:
            del deception_dict[key]
    
    for key in truth_dict.copy():
        if truth_dict[key] < 5:
            del truth_dict[key]
    
    initial_prob = {} 
    initial_truth_count = 0
    initial_deceptive_count = 0

    for label in train_data["labels"]:
        if label == "truthful":
            initial_truth_count += 1
        else:
            initial_deceptive_count += 1
    
    initial_prob["truthful"] = initial_truth_count / len(train_data["labels"])
    initial_prob["deceptive"] = initial_deceptive_count / len(train_data["labels"])


    # Calculating for test data

    for index in range(len(test_data["objects"])):

        prob_truth = 1.0
        prob_deceptive = 1.0

        preprocessed_object = preprocess(test_data["objects"][index])
        
        #Performed Laplace smoothing, to deal with a word which is not at all in the current dataset
        for word in preprocessed_object.split():
            if truth_dict.get(word):
                prob_truth *= (float(truth_dict[word] + 1) / (len(truth_dict) + 100))
            else:
                prob_truth *= (1.0 / (len(truth_dict) + 100))

            if deception_dict.get(word):
                prob_deceptive *= (float(deception_dict[word] + 1) / (len(deception_dict) + 100))
            else:
                prob_deceptive *= (1.0 / (len(deception_dict) + 100))
            if truth_dict.get(word):
                prob_truth *= float(truth_dict[word])

            if deception_dict.get(word):
                prob_deceptive *= float(deception_dict[word])

        prob_truth *= initial_prob["truthful"]
        prob_deceptive *= initial_prob["deceptive"]

        if prob_truth > prob_deceptive:
            test_data["labels"].append("truthful")
        else:
            test_data["labels"].append("deceptive")

    return test_data["labels"]


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.
    train_data = load_file(train_file)
    test_data = load_file(test_file)
    if(sorted(train_data["classes"]) != sorted(test_data["classes"]) or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")

    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}

    results= classifier(train_data, test_data_sanitized)

    # calculate accuracy
    correct_ct = sum([ (results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"])) ])
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))
