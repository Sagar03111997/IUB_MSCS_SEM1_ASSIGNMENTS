#!/usr/bin/python
#
# Perform optical character recognition, usage:
#     python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png
# 
# Authors: (praskuma Prashul Kumar, sdsahu Sagar Sahu, vidung Vishal Dung)
# (based on skeleton code by D. Crandall, Oct 2020)
#
#References : https://www.dfki.de/fileadmin/user_upload/import/5456_Rashid-Screen-OCR-ICDAR11.pdf
import math
from PIL import Image, ImageDraw, ImageFont
import sys

CHARACTER_WIDTH = 14
CHARACTER_HEIGHT = 25
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "


def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    #print(im.size)
    #print(int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH)
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [ [ "".join([ '*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg+CHARACTER_WIDTH) ]) for y in range(0, CHARACTER_HEIGHT) ], ]
    #print(result)
    return result


def load_training_letters(fname):
    TRAIN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    #print({TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS))})
    return {TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS))}

#Training the data to get the dictionary of characters and the transition of characters.
def letter_train():

    Sentence = []
    dict_train = {}
    
    c1 = {}
    c2 = {}
    
    for q in open(train_txt_fname, 'r'):
        struct = () 

        for sentence_d in q.split():
            struct = struct + tuple([sentence_d])
        Sentence = Sentence + [struct]
        
    #print("C",Sentence) basically printing all the words like  [('The', 'Fulton', 'County', 'Grand', 'Jury', 'said',...)]
    z = open(train_txt_fname, 'r')
    init = []
    
    for l in z:
        init.append(l.strip())

    #print("f",init) printing in this format -  ['The Fulton County Grand Jury said Friday an investigation of Atlanta\'s recent primary ele']
    for struct in Sentence:
        for sentence_d in struct[0]:
            c1[sentence_d[0]] = c1[sentence_d[0]] + 1 if sentence_d[0] in train_letters and sentence_d[0] in c1 else 1
                
        sentence_d = " ".join(struct)

        for i in range(len(sentence_d)):
            for j in range(1, len(sentence_d)):
                dict_train[sentence_d[i], sentence_d[j]] = dict_train[sentence_d[i], sentence_d[j]] + 1  if (sentence_d[i], sentence_d[j]) in dict_train else 1 
                
    #print("ld",sentence_d) opening the full sentence above minus [] and ''
    #print("dt",dict_train) dt {('T', 'h'): 77804, ('T', 'e'): 228006, ('T', ' '): 361460, ('T', 'F'): 3392, ('T', 'u'): 51622, ('T', 'l'): 83104, ('T', 't'): 166420, ('T', 'o'): 144160, ('T', 'n'): 116282, ('T', 'C'): 6042, ('T', 'y'): 29892, ('T', 'G'): 3604, ('T', 'r'): 112042,

    for i in range(len(init)):
        for j in range(len(init[i])):
            c2[init[i][j]] = c2[init[i][j]] + 1 if init[i][j] in c2 else 1

    #print('CH',c2)   {'T': 106, 'h': 734, 'e': 2151, ' ': 3410, 'F': 32, 'u': 487, 'l': 784, 't': 1570, 'o': 1360, 'n': 1097, 'C': 57, 'y': 282, 'G': 34, 'r': 1057, 'a': 1347,
   
    for i in LETTERS:
        for j in LETTERS:
            dict_train[i, j] = dict_train[i, j] / c2[i] if (i, j) in dict_train else 0.0000000000000001
            
    #print("c1,c2,dictfortraining",[c1, c2, dict_train]) 
    # above prints {'T': 1, 'h': 1, 'e': 1}, {'T': 106, 'h': 734, 'e': 2151, ' ': 3410, 'F': 32, 'u': 487, 'l': 784, 't': 1570, 'o': 1360, 'n': 1097, 'C': 57,}, {('T', 'h'): 734.0, ('T', 'e'): 2151.0, ('T', ' '): 3410.0, ('T', 'F'): 32.0, ('T', 'u'): 487.0, ('T', 'l'): 784.0,}
    return [c1, c2, dict_train]

def simplified(test_letters):
    
    size = CHARACTER_WIDTH * CHARACTER_HEIGHT
    output_word = ''
    
    for word in test_letters:

        s_words = {}
    
        for a in LETTERS:
        
            match, wrong, val_NULL = 0, 1.0, 0
            
            for l in range(len(word)):
                for m in range(len(word[l])):
                
                    if train_letters[a][l][m] == ' ' and word[l][m] == ' ':
                        val_NULL += 1
                    else:
                        if train_letters[a][l][m] == '*' and word[l][m] == '*':
                            match += 1
                        else:
                            wrong += 1
                            #assuming below as initial probabilities for each parameter
            s_words[a] = (0.85 * match + 0.1 * val_NULL + 0.05 * wrong) / size

        output_word += max(s_words.items(), key=lambda w: w[1])[0]

    return output_word

def viterbi_probability(letter, test_letters):

    match, wrong, val_NULL = 0, 1.0, 0
    size = CHARACTER_WIDTH * CHARACTER_HEIGHT
    for i in range(CHARACTER_HEIGHT):
        for j in range(CHARACTER_WIDTH):
            
            if train_letters[letter][i][j] == '*' and test_letters[i][j] ==  '*':
                match += 1
            elif train_letters[letter][i][j] == ' ' and test_letters[i][j] == ' ':
                val_NULL += 1
            else:
                wrong += 1

    #assuming below as initial probabilities for each parameter           
    ViterbiProbability = (0.7 * match + 0.2 * val_NULL + 0.1 * wrong) / size
    return ViterbiProbability

def HMM_Viterbi(test, dict_train):

    last_word = ''
    viterbi = []
    
    
    for i in range(len(LETTERS)):
        firstword = math.log(viterbi_probability(LETTERS[i], test_letters[0]))
        values.append(firstword)
    viterbi.append(values)


    for x in range(1, len(test)):
    
        values = []
        for y in range(len(LETTERS)):
        
            emission_prob = math.log(viterbi_probability(LETTERS[y], test[i]))
            max_val = 0
            
            for z in range(len(LETTERS)):
            
                transition_prob = math.log(dict_train.get((LETTERS[y], LETTERS[z]), 0.0000000000000001))
                new_val = transition_prob + viterbi[x - 1][z]
                max_val =  new_val if new_val > max_val else max_val
            res = max_val + emission_prob
            values.append(res)
        viterbi.append(values)
    
    for p in range(len(test)):
        
        temp = -(math.pow(10, 7))
        t = 0
        
        for j in range(len(LETTERS)):
            if temp < viterbi[p][q]:
                temp = viterbi[p][q]
                t = q
        last_word += LETTERS[t]

    return last_word

# main program
if len(sys.argv) != 4:
    raise Exception("Usage: python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png")

(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)

[c1, c2, dict_train] = letter_train()

print("Simple: " + simplified(test_letters))
print("   HMM: " + HMM_Viterbi(test, dict_train))
