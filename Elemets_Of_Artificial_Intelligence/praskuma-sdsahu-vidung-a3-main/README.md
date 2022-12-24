# sdsahu-praskuma-vidung-a3

# Part 1:-

#References : https://medium.com/data-science-in-your-pocket/pos-tagging-using-hidden-markov-models-hmm-viterbi-algorithm-in-nlp-mathematics-explained-d43ca89347c4

For this question we were to use viterbi algorithm and gibbs sampling. First we tried to understand these methods and learn how we can implement these in our POS tagging:

**Viterbi Algorithm:-** 

The purpose of the Viterbi algorithm is to make an inference based on a trained model and observed data. It works by asking a question given the trained parameter matrices and data, what's the choice of states such that of the common probability reaches maximum? In other words, what's the most likely choice given the data and the trained model?
This statement can be seen in the following formula:

			


**Gibbs Sampling:-**

The Gibbs Sampling is a Monte Carlo Markov Chain system that iteratively draws a case from the distribution of each variable, tentative on the current values of the other variables in order to estimate complex common distributions. And hence, Gibbs Sampling can be much more effective than Metropolis- Hastings algorithm.

**How the program works :**

First of all we read the data from bc.train and store it. We then train our model using a function named def train(…). In this function we separate the word from their respective POS from the data that we receive for further calculations. In this function we also calculate the POS probability. Here we also calculate the frequencies of all the POS tags and also the frequencies of each word in our training dataset.

We further use the function def solve(…) to pass each sentence along with the model to be tested in.
It goes through all the models’ respective functions i.e. def simplified(…), def hmm_viterbi(…), def complex_mcmc(…) .

In def simplified(…) we utilize the values returned from the functions named calculateEmissionProbability and calculateInitialProbability(…) to get the probability of each suspected POS for each word and then assign the most probable POS by using the POS with the maximum probability. By looping this we finally get an array of POS tags of the sentences in a variable named result_tags.

Similarly in def hmm_viterbi(…) we and def complex_mcmc(…) we have a similar approach but with the Viterbi algorithm and Gibbs Sampling respectively utilizing the Transition probability and Emission probability in both of the functions. 

***Emission Probability:-***

 - Emission Probability is the probability of observation of network event data conditioned on 	 thestate of the mobile device, in a dynamical approach based on a hidden Markov model. We have calculated this in our calculateEmissionProbability(…) function.

***Transition Probability:-***

 - Transition Probability is the probability of transition between consecutive states, in a dynamical approach based on a hidden Markov model. We have calculated this in our calculateTransitionProbability(…) function.

And we finally return the set of POS tags for that sentence in variables named hmm_v_path in def hmm_viterbi(…) and s_list in def complex_mcmc(…)

After this we calculate posteriors for each output under each model using posteriors(…) function and print the results using print_scores(…) function under class Score.

**Assumptions:-**

 - We have also assumed the probability 0.00000001 at some places where the POS tag or a word is unavailable we have assumed 0.00000001 as the default value.

**How to run this Code:-**

./label.py bc.train bc.test
 
**Result:-**

    ==> So far scored 2000 sentences with 29442 words.
                   Words correct:     Sentences correct:
    0. Ground truth:      100.00%              100.00%
         1. Simple:       93.92%               47.45%
            2. HMM:       94.64%               53.55%
        3. Complex:       93.92%               47.45%
----

# Part 2:-


#References : https://www.dfki.de/fileadmin/user_upload/import/5456_Rashid-Screen-OCR-ICDAR11.pdf

**Preprocessing:-**

Initially we load the set of training letters which is performed by the starter code which stores the letters as list of characters representing black dots with * and white areas as spaces. 
The text training file containing the texts for representation of English language utilized here is the cleaned output which consists only of sentences from the first part of this question. We removed all the POS which were there after each of the words in the bc.train file from first part and then finally consider the cleaned output with just the sentences as the text training file. Given that the file was too large, so we just considered a part of the bc.train file as we just needed the representation of English language which was achieved using a part of the whole text and also reduced the running time of the code for training the dataset.

Under the letter_train function, we aim to split the whole sentence of the text file and then calculate and store the count of occurence of each of the individual alphabets and similarly, count the occurence of bigrams of each of the pair of alphabets. This is done, so that we can use this count in probabilities to find which pairs of alphabets occur the most, i.e., for example, there is a higher chance of occurence of {'T','e'} as compared to {'T','F'}. We also assume that if a given pair of letters have not appeared earlier in the input sample text file and a new pair of alphabets come in the test data set, since its appearing for the first time, we set its initial probability to 0.0000000000000001 (significantly small value)

**Simplified :-**

Here we assume n% of pixels are noisy, that implies the noisy pixels of the test image will match with the reference letter with (100-n)%. Thus, after performing various tests against various noise percentages, we found that assuming 10% noise (mismatched pixels) and 85% matched pixels resulted in accurate prediction and results.
In this algorithm, the character assigned to each of the noisy letters is simply decided by the probability of the occurence of characters in the whole dataset. 

Parameters:-

 - letters - Actual observed pixels of the letters which we receive
 
 - train_letters -  The pixels of the letters which were there in the training letters dataset
 
 - noise - The output is then multiplied by the noise parameter with different values for case when match is found, when NULL and when either of them don't happen to get     the best possible prediction.


**HMM Viterbi :-**

Here we predict the letters by applying Viterbi algorithm on Hidden Markov Model developed by keeping test letters as observed, calculate the likely values of hidden states. Here after performing various tests, we found that assuming 20% noise (mismatched pixels) and 70% matched pixels resulted in accurate prediction. The probabilities calculated here -

 - Transition probabilities: The transition probability is stored in the transition_prob variable which stores the probability of transitioning from one letter to        another letter based on the count of occurence 

- Emission Probabilities: We calculate the probability of the test letters using Naive Bayes approach for the particular character. The grid of the train letters is matched with the grid of the test letters, which is performed under the viterbi_probability function. The probability of occurence of noise in character is also taken care of here by assigning the weights of 0.7 for matched pixels and considering 20% as noise. The emission probability is calculated by taking log of product of each of the character pixel probabilities.

Parameters -
- test letters (test[i]) - Observed pixels of letters
- train letters (LETTERS[j]) -  Actual pixels of training letters
    
Finally, we append the values to last_word after calculating probability of 1 character and as and when the new characters come in the test data set, we append each of them to the last_word variable to recognize the input test words


**How to run this Code:-**

We have all the images inside the folder along with the training text file. Hence, use below to call the program on specific image:

**./image2text.py ./test_images/courier-train.png ./test_images/train-text.txt ./test_images/test-1-0.png**

We have also attached a text file containing the output of all the images by the name, output-text.txt
