###################################
# CS B551 Fall 2022, Assignment #3
#
# 
# (praskuma Prashul Kumar, sdsahu Sagar Sahu, vidung Vishal Dung)
#
# (Based on skeleton code by D. Crandall)
#

import math

# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.


#Reference:- https://medium.com/data-science-in-your-pocket/pos-tagging-using-hidden-markov-models-hmm-viterbi-algorithm-in-nlp-mathematics-explained-d43ca89347c4
#Reference2:- https://web.stanford.edu/~jurafsky/slp3/8.pdf

class Solver:
    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling. Right now just returns -999 -- fix this!
    def __init__(self):
    
        self.emissionProbabiltiyDict = {}
        self.levelTwoTotalTransitionCount = {}
        self.transitionProbabilityDict = {}
        self.totalWordCount = {}
        self.levelTWoTransitionProbabilityDict = {}
        self.totalPosCount = {}
        self.totalEmissionCount = {}
        self.fWordPosCount = {} 
        self.totalTransitionCount = {}
        
    def train(self, data):
    
        self.calculateSecondLevelTotalTransitionCount(data)
        
        for l1 in data:
        
            word, word_pos = l1[0], l1[1]
            for i in range(len(word)):
                if i == 0:
                    curr_word_val = word[i]
                    curr_POS_val = word_pos[i]
                    self.fWordPosCount[word_pos[i]] = self.fWordPosCount[word_pos[i]] + 1.0 if curr_POS_val in self.fWordPosCount else 1.0
            
                else:
                    curr_word_val = word[i]
                    prev_pos_val = curr_POS_val
                    curr_POS_val = word_pos[i]

                    if prev_pos_val in self.totalTransitionCount:
                         self.totalTransitionCount[prev_pos_val][curr_POS_val] =  self.totalTransitionCount[prev_pos_val][curr_POS_val] + 1.0 if curr_POS_val in self.totalTransitionCount[prev_pos_val] else 1.0
                    else:
                        self.totalTransitionCount[prev_pos_val] = {curr_POS_val: 1}

                if curr_word_val in self.totalEmissionCount:
                    self.totalEmissionCount[curr_word_val][curr_POS_val] = self.totalEmissionCount[curr_word_val][curr_POS_val] + 1.0 if curr_POS_val in self.totalEmissionCount[curr_word_val] else 1.0
                else:
                    self.totalEmissionCount[curr_word_val] = {curr_POS_val: 1}

                self.totalPosCount[curr_POS_val] = self.totalPosCount[curr_POS_val] + 1.0 if curr_POS_val in self.totalPosCount else 1.0

                self.totalWordCount[curr_word_val] = self.totalWordCount[curr_word_val] + 1.0 if curr_word_val in self.totalWordCount else 1.0

    def posterior(self, model, sentence, label):
    
        if model == "Simple":
            prob_simple = 0
            for i in range(len(sentence)):
                prob_simple += math.log(self.calculateEmissionProbability(sentence[i], label[i])) + math.log((self.fWordPosCount[label[i]] / sum(self.fWordPosCount.values())))
            return prob_simple

        elif model == "HMM":
            prob_simple = 0
            prob_simple = math.log(self.fWordPosCount[label[0]] / sum(self.fWordPosCount.values()))

            for i in range(len(sentence)):
                w = self.calculateEmissionProbability(sentence[i], label[i])
                prob_simple += math.log(w)

            prev_pos = label[0]
            for i in range(1, len(label)):
                w = self.calculateTransitionProbability(prev_pos, label[i])
                prob_simple += math.log(w)
                prev_pos = label[i]

            return prob_simple

        elif model == "Complex":
        
            prob_complex = 0
            for i in range(len(sentence)):
            
                word, pos = sentence[i], label[i]

                if word in self.emissionProbabiltiyDict:
                    prob_complex += math.log(self.calculateEmissionProbability(word, pos))
                else:
                    prob_complex = 0.00000000001
                if i == 0:
                    prob_complex += math.log(self.fWordPosCount[pos] / sum(self.fWordPosCount.values()))
                elif i == 1:
                    prob_complex += math.log(self.calculateTransitionProbability(label[i - 1], label[i]))
                else:
                    prob_complex += math.log(self.calculateSecondLevelTransitionProbability(label[i - 2], label[i - 1], label[i]))
            return prob_complex

        else:
            print("Unknown algo!")

    def calculateEmissionProbability(self, word, pos):

        if word in self.totalEmissionCount:
            if pos in self.totalEmissionCount[word]:
                p_em_prob = self.totalEmissionCount[word][pos] / self.totalPosCount[pos]
                self.emissionProbabiltiyDict[word] = {pos: p_em_prob}
                return p_em_prob
        elif word in self.emissionProbabiltiyDict:
            if pos in self.emissionProbabiltiyDict[word]:
                return self.emissionProbabiltiyDict[word][pos]
        return 0.00000000001

    def calculateTransitionProbability(self, prev_POS_val, curr_POS_val):
    
        for key, value in self.totalTransitionCount.items():
            if key == prev_POS_val:
                 if curr_POS_val in self.totalTransitionCount[prev_POS_val]:
                    prob = self.totalTransitionCount[prev_POS_val][curr_POS_val] / sum(self.totalPosCount.values())
                    self.transitionProbabilityDict[prev_POS_val] = {curr_POS_val: prob}
                    return prob
        
        for key, value in self.transitionProbabilityDict.items():
            if key == prev_POS_val:
                if curr_POS_val in self.transitionProbabilityDict[prev_POS_val]:
                    return self.transitionProbabilityDict[prev_POS_val][curr_POS_val]
        
        return 0.00000000001

    def calculateInitialProbability(self, pos, modelName):
    
        if modelName == "simplified":
            if pos in self.totalPosCount:
                return self.totalPosCount[pos] / sum(self.totalPosCount.values())
            else:
                return 0.00000000001
        elif modelName == "hmm_viterbi":
            if pos in self.totalPosCount:
                return self.totalPosCount[pos] / sum(self.fWordPosCount.values())
            else:
                return 0.00000000001

    def calculateSecondLevelTotalTransitionCount(self, data):
    
        for l in data:
            w_trans_ct, pos_trans_ct = l[0], l[1]

            for i in range(len(w_trans_ct) - 2):
            #Taking 3 POS at a time 
                pos1, pos2, pos3 = pos_trans_ct[i], pos_trans_ct[i + 1], pos_trans_ct[i + 2]

                if pos1 in self.levelTwoTotalTransitionCount:

                    if pos2 in self.levelTwoTotalTransitionCount[pos1]:

                        self.levelTwoTotalTransitionCount[pos1][pos2][pos3] = self.levelTwoTotalTransitionCount[pos1][pos2][pos3] + 1.0 if pos3 in self.levelTwoTotalTransitionCount[pos1][pos2] else 1.0

                    else:
                        self.levelTwoTotalTransitionCount[pos1][pos2] = {pos3: 1}

                else:
                    self.levelTwoTotalTransitionCount[pos1] = {pos2: {pos3: 1}}

        return self.levelTwoTotalTransitionCount

    def calculateSecondLevelTransitionProbability(self, pos1, pos2, pos3):
    
        if pos1 in self.levelTwoTotalTransitionCount and pos2 in self.levelTwoTotalTransitionCount[pos1] and pos3 in self.levelTwoTotalTransitionCount[pos1][pos2]:
            p_pos = self.levelTwoTotalTransitionCount[pos1][pos2][pos3] / sum(self.totalPosCount.values())
            self.levelTWoTransitionProbabilityDict[pos1] = {pos2: {pos3: p_pos}}
            return p_pos
        elif pos1 in self.levelTWoTransitionProbabilityDict and pos2 in self.levelTWoTransitionProbabilityDict[pos1] and pos3 in self.levelTWoTransitionProbabilityDict[pos1][pos2]:
            return self.levelTWoTransitionProbabilityDict[pos1][pos2][pos3]
        else:
            return 0.00000000001

    def simplified(self, sentence):
    
        result_tags = []
        
        for i in range(len(sentence)):
            
            max_simplified = 0
            pos_simplified = ""
            
            for posKeys, posValues in self.totalPosCount.items():
            
                prob = self.calculateEmissionProbability(sentence[i], posKeys) * self.calculateInitialProbability(posKeys, "simplified")
                if max_simplified < prob:
                    max_simplified = prob
                    pos_simplified = posKeys
            result_tags.append(pos_simplified)
            
        return result_tags

    def hmm_viterbi(self, sentence):
    
        hmm_v_path = {}
        viterbi_matrix = [{}]
        
        for posKeys, posValues in self.totalPosCount.items():
            viterbi_matrix[0][posKeys] = self.calculateInitialProbability(posKeys, "hmm_viterbi") * self.calculateEmissionProbability(sentence[0], posKeys)
            hmm_v_path[posKeys] = [posKeys]
    
        for i in range(1, len(sentence)):
        
            temp_tr = {}
            viterbi_matrix.append({})
            
            for current_pos_Keys, current_pos_values in self.totalPosCount.items():
                max_v = 0
                for previous_pos_keys, previous_pos_values in self.totalPosCount.items():
                    curr_val = viterbi_matrix[i - 1][previous_pos_keys] * self.calculateTransitionProbability(previous_pos_keys,
                                                                                                 current_pos_Keys)
                    if curr_val > max_v:
                        max_v = curr_val
                        t1 = previous_pos_keys
                viterbi_matrix[i][current_pos_Keys] = max_v * self.calculateEmissionProbability(sentence[i], current_pos_Keys)
                temp_tr[current_pos_Keys] = hmm_v_path[t1] + [current_pos_Keys]

            hmm_v_path = temp_tr
            
        max_value = 0

        for posKeys, posValues in self.totalPosCount.items():
        
            if viterbi_matrix[len(sentence) - 1][posKeys] >= max_value:
                max_value = viterbi_matrix[len(sentence) - 1][posKeys]
                new_state = posKeys
                
        st1 = new_state

        return hmm_v_path[st1]

    def complex_mcmc(self, sentence):
        
        sample_sentence = self.simplified(sentence)
        word_mcmc = list(sentence)
        prob_mcmc = ["Noun"] * len(word_mcmc)

        for _ in range(len(sentence)):
        
            s_list = []
            
            for i in range(len(word_mcmc)):
                for j in range(len(sample_sentence)):
                
                    prob = math.log(self.calculateEmissionProbability(word_mcmc[i], sample_sentence[j]))
                    prob_mcmc[j] = prob
                    
            x = min(prob_mcmc)
            
            for t in range(len(sentence)):

                if prob_mcmc[t] == x:
                    s_list.append(sample_sentence[t])
                else:
                    s_list.append(sample_sentence[t])

        return s_list

    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #
    def solve(self, model, sentence):
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        elif model == "Complex":
            return self.complex_mcmc(sentence)
        else:
            print("Unknown algo!")
