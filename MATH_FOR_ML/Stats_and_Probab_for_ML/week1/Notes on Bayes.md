# Quick exercise on Bayes theorem and spam probability 

We have
*  100 emails 
   *  of these, 20 of these are spam

We also notice a correlation between the word lottery and spam and we see that
*  we have a total of 24 emails with the word: **lottery**
   *  14 of these are spam
   *  10 are not spam 

```
total emails           = 100
P(A) = spam    = 0.2   = 20 spam emails  (this is called also *prior*)
P(B) = lottery = 0.24  = 24 emails with word: lottery
```
Normal probability rules for intersection of events gives us:
*  **P(A and B) = P(A|B) * P(B)**  
*  **P(A and B) = P(B|A) * P(A)**

So I can use those to get value of a conditional probability 
```
                P(A and B)
P(A|B) = --------------------------------  # note A nd B are not mutually exclusive so P (A and B) is not P(A) * P(B) and we can say it is HARD to find
         P(B|A) * P(A) + P(B|^A) * P(^A)
```
### From the data above we can also get:
*  P(B|A ) = the ratio of spam emails that have the word lottery (to all the spam emails), we assume 14 out of 20   so = **0.7**  
*  P(B|^A) = the ratio of non spam emails that have the word lottery (to all non spam email), this is 10 out of 80  so = **0.125**  
*  P(A|B)  = the ratio of spam emails (to all the emails that have the word lottery), this is 14 out of 24          so = **0.583** 

We can also get to the same result with **Bayes formula** (replace ```P(A and B)``` with ```P(B|A) * P(A)``` )
```
                P(B|A) * P(A)
P(A|B) = -------------------------------- = (0.7 * 0.2) / ((0.7*0.2) + (0.125*0.8)) = 0.583  -> same as above
         P(B|A) * P(A) + P(B|^A) * P(^A)
```

The **prior** is the original probability of an event with no other information givem,  
the **posterior** is the new value of the probability of an even, given some extra information (an event has been discolsed).  
In this case the the **prior** is the P(spam) = 0.2  
The **posterior**  is the P(spam|lottery) = 0.583 which is (always) better than the **prior**  


If you want to make the filter more generic and use more than one word to identify **spam**, we have to adopt the
**naive** assumption that those words are indipendent.  
**Note:** this is clearly not true in an email context but it does simplify the mathematical model a lot..   
For instance let's say you check for the word *winning* in addition to *lottery*, then:  

```P(lottery,winning|spam) = P(lottery|spam) * P(winning|spam)```

There are a few other things to consider (have a look also at the related chapter of DSFS)

