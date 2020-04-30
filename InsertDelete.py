#Program to test theorem for a single deletion error and a single insertion error occuring in the same word.

import itertools
import random

def codebook(n):                                        #Program for generating all code words of length n.
    code = []                                           #Establish an empty array
    pool = '0', '1'                                     #Set the list of possible bits as 0 and 1
    for item in itertools.product(pool, repeat=n):      #Generate a code word using the 0 and 1 bits of given length n
        a = list(item)                                  #Assign a to be the code word
        code.append(a)                                  #Add the generated code word to the array
    return code                                         #Return(Save) the list of all possible code words of length n.

def genweight(n, s):                                    #Program for generating the recursive weights for words of length n with a maximum of s errors.
    empty = []                                          #Establish an empty array
    for i in range(s-1):
        empty.append(0)                                 #Add s-1 0 bits to the empty array
    empty.append(1)                                     #Add a 1-bit to the array
    for i in range(n+s):                                #Assign the range to be the length n of the code word plus the maximum number of errors
        t = 0                                           #Initialize variable t as 0
        sum = 1                                         #Initialize the sum to start at 1
        while t < (s):                                  #While t is less than the maximum number of errors given
            sum = sum + empty[i+t]                      #Recursively add the weights of the s-previous bits
            t = t + 1                                   #Increase t by a factor of 1 (t will increase as long as it is strictly less than s)
        empty.append(sum)                               #Add the calculated sum the array
    for i in range(s-1):
        empty.remove(0)                                 #Remove the beginning 0-bits from the array
    return empty                                        #Store the array in memory


def moment(x, s):                                       #Program to calculate the moment of a codeword, x, with a maximum of s errors
    w = genweight(len(x), s)                            #Assign w to be the weights generated from the weight program
    moment = 0                                          #Initialize moment to be 0
    for i in range(len(x)):                             #For the length of the given word
        moment += (int(x[i])*w[i])                      #Calculate moment by multiplying the weight of the bit by the value of the bit (either 0 or 1)
    return moment                                       #Store the calculated moment

def codebookfile(n, s, a):                              #Program to generate all words in a given code book (Either Levenshtein or Helberg)
    code = []                                           #Establish an empty array
    file = codebook(n)                                  #Call the codebook program and assign it to the variable 'file'
    w = genweight(n, s)                                 #Assign w to be the weights generated from the weight program
    num = w[n]                                          #Assign the variable 'num' to be the weight of the nth bit
    for t in file:                                      #For each element in file
        m = moment(t, s)                                #Calculate the moment of each word
        if m % num == a:                                #If the moment of the word mod num is conguent to a
            code.append(t)                              #Add that word to the array
        else:                                           #If the moment does not satisfy the conditions
            pass                                        #Do nothing
    return code                                         #Store the array of codewords as a code book

def insert(x):                                          #Program to insert one random bit into a code word x
    pool = [0, 1]                                       #Assign an array called pool to contain the integers 0 and 1.
    r = random.choice(pool)                             #Randomly select a number from the above array and asign this number to variable r.
    c = random.randint(0, len(x))                       #Assign variable c to be a random position in the code word
    ins = [f for f in x]                                #Define ins as the separate array of bits of the given code word
    ins.insert(c, r)                                    #Insert the randomly chosen bit into the randomly chosen position
    return ins                                          #Store the code word with the inserted bit


def delete(y):                                          #Program to delete a random bit from a code word y.
    r = random.randint(0, len(y)-1)                     #Randomly choose a position in the code word
    dt = [g for g in y]                                 #Define dt as the separate array of bits of the given code word
    del dt[r]                                           #Delete the bit in the randomly selected position
    return dt                                           #Store the code word with the deleted bit


def determine(z, s):                                    #Program to find the moment of the word with the rightmost 1-bit deleted
    word = z                                            #Assign word to be the given word z
    l = len(word)                                       #Assign l to be the length of the word
    pos = l - 1                                         #Assign variable pos to be equal to one less than the length of the word
    counter = 1                                         #Keep track of how many 1 bits are found, initialize this counter as 1
    count = word.count(1)                               #Count the number of 1's in the word
    my = 0                                              #Initialzie moment to be 0
    if count < 1:                                       #If the number of 1-bits in the word is less than 1 (equal to 0)
        my = 0                                          #The moment must be 0
    else:                                               #If there is at least one 1-bit, proceed to do the following
        while counter <= 1 and pos >= 0:                #As the counter is less than or equal to 1, do the following
            if word[pos] == 1:                          #If the bit at the specified position is a 1-bit
                del word[pos]                           #Continue to delete the 1-bit
                counter = counter + 1                   #Increase the number of 1's found/deleted by one
            else:                                       #If the bit is not a 1-bit
                pass                                    #Do nothing
            pos = pos - 1                               #Go to the next position from right to left
        my = moment(word, s)                            #Calculate the moment of the word with the rightmost 1-bit deleted
    return my                                           #Store the found moment


def testheory(n, s, a):                                 #Program to test the proposed moment theoerem
    t = codebookfile(n, s, a)                           #Assign t to call the code book consisting of the specific length, errors, and residue
    x = [int(d) for d in random.choice(t)]              #Assign x to be the randomly chosen word from the above code book
    mx = moment(x, s)                                   #Calculate the moment of x using the moment program
    w = insert(x)                                       #Insert a random bit into x, rename this word as w
    y = delete(w)                                       #Delete a random bit from w, rename this word as y.
    z2 = determine(y, s)                                #Find the moment of y with the rightmost 1-bit deleted
    weights = genweight(n, s)                           #Calculate the list of weights for a code word of length n
    moment1 = weights[n] + a                            #Assign the first possible moment to be the n+1 weight (in the nth position of the list of weights) added to a
    moment2 = a                                         #Assign the second possible moment to be the value of a
    if z2 > a and mx == moment1:                        #If the moment of y (z2) is greater than a, and the moment is equal to moment 1
        print ("Moment theorem is true.")               #The moment theorem is found to be true.
    elif z2 > a and mx != moment1:                      #If the moment of y (z2) is greater than a, but the moment is NOT equal to moment 1
        print ("Moment theorem is false.")              #The moment theorem is incorrect.
    if z2 <= a and mx == moment2:                       #If the moment of y (z2) is less than or equal to a, and the moment is equal to moment 2
        print ("Moment theorem is true.")               #The moment theorem is found to be true.
    elif z2 <= a and mx != moment2:                     #If the moment of y (z2) is less than or equal to a, and the moment is NOT equal to moment 2
        print ("Moment theorem is false.")              #The moment theorem is found to be incorrect.