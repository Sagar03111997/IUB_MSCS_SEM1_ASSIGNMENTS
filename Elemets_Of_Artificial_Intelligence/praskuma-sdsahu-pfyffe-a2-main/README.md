# a2-release-res

## Part 1

### How we formulated our solution

We knew that minimax is an effective means of solving chess and similar games, so we first generated some ideas for our evaluation function:
	1. Weighted sum of pieces
		- Example: Pichus + 2*Pikachus + 4*Raichus.
		- Subtract opponent's pieces.
	2. Number of possible moves
	3. Weighted sum of opponent pieces that can be captured from one state.
		- If a piece is poised to capture a Raichu, e(s) increases dramatically. 
	4. Weighted number of pieces at risk
		- This should lower e(s).
		- Stronger penalty when a Raichu or Pikachu is at risk.
	5. Total distance each non-Raichu piece is from the end of the board

We decided on #1 (weighted sum of pieces) and #5 (total distance from the end of the board), partly because of their simplicity but also because some of these ideas are redundant. We had our algorithm play against itself and hand-tuned the weights of these metrics to achieve better results.
These are a few but not all of our test cases. We also tested on smaller boards such as 5x5.
'........W.W.W.W..w.w.w.w................b.b.b.b..B.B.B.B........'
'...........WW.W..w.w.w..W.b..B.........B..b.b.b..B.B............'
'............W.W..w.w.w.B.....B...BWB......b.b.b.........@.......'

To compute each successor, we run a function makeMoveOrCapture(...) that adds a copy of the board to the input list only if the path from a given start location to a destination is clear or has exactly one opponent to jump over.

Our MAX_H variable, or depth horizon, starts small but is increased after returning each answer for as long as the program is allowed to run. Thus, we assume the autograder to only check the last line printed. Also, implementing alpha-beta pruning made a tremendous difference in our performance, allowing us to support higher values of h.

### How the program works

We transform the board into a numpy array for easier manipulation. For each turn of the game, find all the pieces belonging to the player and create a copy of the board for all the possible moves that team could make. Then, find for each of those successors, recursively evaluate it by checking all the different successors for the opposing team. This recursion continues until our depth horizon h. Since our minimax function only returns integers from the evaluations, we track the best state that maximizes e(s) and print it when h = 0.

When to prune?
	- Alpha is the lower bound for MAX's e(s)
	- Beta is the upper bound for MIN's e(s)
	- Prune when a MIN node's beta is <= the alpha value of one of its MAX ancestors.

### Future considerations
	- We could increase MAX_H based on the amount of time the autograder allows. 
	- Our Raichus are not very aggressive. This could be because each team prioritizes moving their other pieces out of danger.
	- If there are no successors, the code could get stuck.
	- Some of the functions take a lot of parameters and could use cleanup.



## Part 2:-


**Pre-Process:**

Initially we define the data pre-process function which will:

- Firstly, convert the sentence/corpus to lowercase and then remove some of the special characters, replace some of the contractions to full words
- Remove the filler words of sentences which do not have any significant impact on the accuracy and reduce the sentence length for run-time optimization.

**Initializing Dictionary:**

Using bag of words model approach, the two dictionaries, i.e., truthful and deceptive are created and initialized which then stores the count of each word appearing in the training dataset post the preprocessing of the sentences. The deception_dict = {} and truth_dict = {} holds the count for words for the sentences for their respective labels.

Moreover, we also remove the words having smaller count than a specific threshold as the ones with smaller count will have least impact on the final decision and also improve the accuracy of the classification algorithm. After performing multiple runs against different counts, we found that for count = 5, i.e., when we remove all the words which occur less than 5 times in the dictionary, we obtain the optimum accuracy. Although this choice of number could raise the potential for overfitting, we believe removing the outlier words is important.

Iterating through the same dictionary and deleting the keys parallely led to runtime error. As a result, we are creating a copy of both of them and iterating through it while performing deletion in the original set of dictionaries for words having count < 5.

**Initial Probability:**

Initial probability of occurence of 'truthful' and 'deceptive' is calculated (=0.5) and stored which shall be later used in the Naive Bayes formula.

Finally, we implement the Naive Bayes algorithm after preprocessing the test data and calculate the probability of each of the words appearing in truthful or deceptive for the corresponding hotel reviews. If the probability of truthful is more than deceptive for the words in a sentence then we classify the sentence as truthful or vice-versa and return the label for each of the sentence. 

**Laplace Smoothing:**

For cases when, a new data comes in the test data set which is not yet seen in the training data set while calculating probabilities, we arrive at the problem of Zero Probability issue. 

**P(truthful/review) ∝ P(x1/truthful)*P(x2/truthful)*P(x’/truthful)*P(truthful)**

For example, in the above case, if x1 is appearing for the first time and its probability turns out to be 0, then the whole probability will change to 0 resulting in both the probabilities, i.e., P(truthful/review) and P(deceptive/ review) as equal, which is not correct ideally. Hence to deal with the problem of zero probability, we introduce Laplace Smoothing wherein: 

1. A small-sample correction, or pseudo-count, will be incorporated in every probability estimate.

2. Consequently, no probability will be zero.

Reference : https://www.analyticsvidhya.com/blog/2021/04/improve-naive-bayes-text-classifier-using-laplace-smoothing/

Therefore, we add 1 count to each of the probability and calculate all the posterior probabilities for naive Bayes and thus based on the result, we return the label of the new sentence from the test data and classify it as truthful/deceptive.
