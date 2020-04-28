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

print codebookfile(8, 2, 6)

def randominsert(x, s):                                 #Program to randomly insert up to s random 0 or 1 bits into code word x
    pool = [0, 1]                                       #The possible bits to be inserted are 0 and 1 bits, assigned to the array called pool
    randomlist = []                                     #Establish an empty array called randomlist
    e = random.randint(1,s)                             #Assign e to be a random number between 1 and s
    count = 0                                           #Initialize count to be 0
    r = random.choice(pool)                             #Assign r to be a random selection of either a 0 or 1 bit
    for i in range(1, e+1):                             #For elements in the range from 1 to e+1
        n = random.randint(0, len(x)-1)                 #Assign n to be a random position in the code word
        randomlist.append(n)                            #Add the random position to the empty randomlist array
    randomlist.sort()                                   #Sort the positions in the randomlist array from smallest to largest
    while count <= e-1:                                 #While the count variable is one less than the e value
        g = (randomlist[-1])                            #Take the last number in the random list array to be g
        x.insert(g, r)                                  #Insert the randomly chosen bit (0 or 1) into position g in the code word x
        randomlist.remove(g)                            #Remove g from the randomlist array
        count = count + 1                               #Increase the count variable by 1 until it is equal to e-1
    return x                                            #Store x with the inserted bits.


def momenttest(y, s):                                   #Program to find the moment of y, the corrupted word with the inserted 1-bits
    word = y                                            #Assign word to be the given word y
    d = len(word)                                       #Assign d to be the length of the word
    pos = d-1                                           #Assign variable pos to be equal to one less than the length of the word
    counter = 0                                         #Keep track of how many 1 bits are found, initialize this value to be 0
    while counter <= (s-1) and pos >= 0:                #Until the counter gets to s-1 (s 1-bits are found)
        if word[pos] == 1:                              #If the bit at the specified position is a 1-bit
            del word[pos]                               #Delete the 1-bit
            counter = counter + 1                       #Increase the number of 1's found/deleted by one
        else:                                           #If the bit is not a 1-bit
            pass                                        #Do nothing
        pos = pos - 1                                   #Go to the next position from right to left
    if counter < s:                                     #If there are less 1 bit-s in the word than maximum number of errors
        print ("Exception")                             #This is considered an expection case
    else:                                               #If there are enough 1-bits in the word
        my = moment(word, s)                            #Calculate the moment of the word with the s-rightmost 1-bits deleted
        return my                                       #Store the moment


def possmoments(n, s, a):                               #Program to find all possible moments of a code book
    pm = []                                             #Establish an empty array called pm
    lc = codebookfile(n, s, a)                          #Assign the variable lc to call the program to determine a specific code book
    for x in lc:                                        #For elements in the generated codebook
        mom = moment(x, s)                              #Assign the variable mom to be the moment of the word found using the moment program
        if mom not in pm:                               #If the moment is not already in the array
            pm.append(mom)                              #Add the specific moment to the array
        pm.sort()                                       #Sort the array of moments from smallest to largest
    return pm                                           #Store the list of possible moments

print possmoments(8, 2, 6)

def computej3(n, s, a):                                 #Program to compute the j-value used in the theorem
    w = codebookfile(n, s, a)                           #Assign the variable w to call the program to generate a specific code book
    x = [int(z) for z in random.choice(w)]              #Assign x to be a randomly chosen codeword from the generated code book
    y = randominsert(x, s)                              #Assign y to generate the program that randomly inserts at most s random bits into the word x
    my = moment(y, s)                                   #Assign my to be the program that generates the moment of y (the corrupted code word)
    j = 0                                               #Initialize j to be 0
    while j < float('inf'):                             #While j is less than infinity
        one = a + (j * (n + 1))                         #The left hand side of the inequality is set to be called one
        two = a + ((j + 1) * (n + 1))                   #The right hand side of the inequality is set to be called two
        if one <= my and my < two:                      #If the moment of y is in between the calculated values for one and two based on the current j-value
            break                                       #Stop the loop
            j = j                                       #Assign this j-value to be the current value of j
        else:                                           #If the moment of y does not fall in between the calculated values for one and two
            j = j + 1                                   #Increase j by a factor of 1
    return j                                            #Store the j-value


def momentth3(n, s, a):                                 #Program to test the moment theorem for one insertion error
    w = codebookfile(n, s, a)                           #Assign the variable w to call the program to generate a specific code book
    ex = [int(z) for z in random.choice(w)]             #Assign ex to be a randomly chosen word from the generated code book
    mx = moment(ex, s)                                  #Calculate the moment of x using the moment program
    pm = possmoments(n, s, a)                           #Generate the list of all possible moments for the specified code book
    y = randominsert(ex, s)                             #Corrupte the chosen code word by generating the random insertion of at most s-bits
    my = moment(y, 1)                                   #Find the moment of the corrupted code word
    j = 0                                               #Initialize the j-value to start at 0 (begins the calculation of the j-value)
    while j < float('inf'):                             #While j is less than infinity
        one = a + (j * (n + 1))                         #The left hand side of the inequality is set to be called one
        two = a + ((j + 1) * (n + 1))                   #The right hand side of the inequality is set to be called two
        if one <= my and my < two:                      #If the moment of y is in between the calculated values for one and two based on the current j-value
            break                                       #Stop the loop
            j = j                                       #Assign this j-value to be the current value of j
        else:                                           #If the moment of y does not fall in between the calculated values for one and two
            j = j + 1                                   #Increase j by a factor of 1
    b = n + 1                                           #Assign b to be the value of one more than the given length of the original code word
    c = j - 1                                           #Assign c to be one less than the found j-value
    mmt = a + (b * c)                                   #Set the moment #1 to be equal to the given a value added to b multipled by c
    mmt2 = a + (b * j)                                  #Set the moment #2 to be equal to the given a value added to b multiplied by the found j-value
    myprime = momenttest(y, s)                          #Find the moment of the word with the rightmost one bit deleted (this word is called "y prime")
    if myprime <= mmt:                                  #If the moment of y-prime is less than or equal to moment #1
        mx1 = mmt                                       #The moment of x is set equal to moment #1
    elif myprime > mmt:                                 #If the moment of y-prime is greater than moment #1
        mx1 = mmt2                                      #The moment of x is set equal to moment #2
    if mx1 == mx:                                       #If the moment that x is set to based on the above calculations is equal to the original calculated moment of x
        print "Moment theorem is true."                 #The moment theorem is found to be true.
    else:                                               #If the moment that x is set to based on the above calculations differs from the original calculated moment of x
        print "Moment theorem is false."                #The moment theorem is found to be false.


def momentcheck(n,s,a):                                 #Program to test the moment theorem for a maximum number of s-insertion (greater than or equal to 2)
    w = codebookfile(n, s, a)                           #Assign the variable w to call the program to generate a specific code book
    z = [int(d) for d in random.choice(w)]              #Select code word from the generated Helberg code book
    mz = moment(z, s)                                   #Calculate the moment of that codeword
    w = randominsert(z, s)                              #Randomly insert at most s-number of bits
    c = momenttest(w, s)                                #Calculate the moment of "y-s-prime", the code word with the s-rightmost 1-bits deleted
    w2 = genweight(n, s)                                #Assign w2 to generate the program that calculates the recursive weights
    mx = w2[n] + a                                      #Assign mx as the value of the n+1 weight + a (what the moment of the original codeword should be based on the algorithm)
    if c <= a and mz == a:                              #If the moment of y-s-prime is less than or equal to a and the original moment of the code word is equal to a
        print ("Moment theorem is true.")               #The moment theorem is found to be true
    elif c <= a and mz != a:                            #If the moment of y-s-prime is less than or equal to a and the original moment of the code word is NOT equal to a
        print ("Moment theorem is false.")              #The moment theorem is found to be false
    elif c > a and mz == mx:                            #If the moment of y-s-prime is greater than a and the original moment of the code word is equal the calculated value mx
        print ("Moment theorem is true.")               #The moment theorem is found to be true
    elif c > a and mz != mx:                            #If the moment of y-s-prime is greater than a and the original moment of the code word is NOT equal the calculated value mx
        print ("Moment theorem is false.")              #The moment theorem is found to be false
    elif c == 0 and mz == 0:                            #If the moment of y-s-prime is equal to 0 and the moment of the original code word is also 0
        print ("Exception Case")                        #This is considered an exception case


def gentest1():                                         #Program to randomly generate values of n, s, a and run the program to test the moment theorems
    n = random.randint(3, 10)                           #Randomly generate a code word length between 3 and 10
    s = random.randint(1, 10)                           #Randomly choose a maximum number of insertion errors between 1 and 10
    a = random.randint(0, (n - 1))                      #Randomly choose a residue between 1 and one less than the length
    if s == 1:                                          #If s is randomly chosen to be 1
        test = momentth3(n, s, a)                       #Run the specified moment theorem check program
    elif s >= 2:                                        #If s is greater than or equal to 2
        test = momentcheck(n, s, a)                     #Run the other moment theorem check program


def gentest2():                                         #Program to randomly generate values of n, s, a and run the program to test the moment theorems
    n = random.randint(3, 10)                           #Randomly generate a code word length between 3 and 10
    s = random.randint(1, 10)                           #Randomly choose a maximum number of insertion errors between 1 and 10
    a = random.randint(0, (n-1))                        #Randomly choose a residue between 1 and one less than the length
    if s == 1:                                          #If s is randomly chosen to be 1
        w = codebookfile(n, s, a)                       #Assign the variable w to call the program to generate a specific Levenshtein code book
        ex = [int(z) for z in random.choice(w)]         #Assign ex to be a randomly chosen word from the generated code book
        mx = moment(ex, s)                              #Calculate the moment of x using the moment program
        pm = possmoments(n, s, a)                       #Generate the list of all possible moments for the specified code book
        y = randominsert(ex, s)                         #Corrupte the chosen code word by generating the random insertion of at most s-bits
        my = moment(y, 1)                               #Find the moment of the corrupted code word
        j = 0                                           #Initialize the j-value to start at 0 (begins the calculation of the j-value)
        while j < float('inf'):                         #While j is less than infinity
            one = a + (j * (n + 1))                     #The left hand side of the inequality is set to be called one
            two = a + ((j + 1) * (n + 1))               #The right hand side of the inequality is set to be called two
            if one <= my and my < two:                  #If the moment of y is in between the calculated values for one and two based on the current j-value
                break                                   #Stop the loop
                j = j                                   #Assign this j-value to be the current value of j
            else:                                       #If the moment of y does not fall in between the calculated values for one and two
                j = j + 1                               #Increase j by a factor of 1
        b = n + 1                                       #Assign b to be the value of one more than the given length of the original code word
        c = j - 1                                       #Assign c to be one less than the found j-value
        mmt = a + (b * c)                               #Set the moment #1 to be equal to the given a value added to b multipled by c
        mmt2 = a + (b * j)                              #Set the moment #2 to be equal to the given a value added to b multiplied by the found j-value
        myprime = momenttest(y, s)                      #Find the moment of the word with the rightmost one bit deleted (this word is called "y prime")
        if myprime <= mmt:                              #If the moment of y-prime is less than or equal to moment #1
            mx1 = mmt                                   #The moment of x is set equal to moment #1
        elif myprime > mmt:                             #If the moment of y-prime is greater than moment #1
            mx1 = mmt2                                  #The moment of x is set equal to moment #2
        if mx1 == mx:                                   #If the moment that x is set to based on the above calculations is equal to the original calculated moment of x
            print "Moment theorem is true."             #The moment theorem is found to be true.
        else:                                           #If the moment that x is set to based on the above calculations differs from the original calculated moment of x
            print "Moment theorem is false."            #The moment theorem is found to be false.
    elif s >= 2:                                        #If s is randomly chosen to be greater than or equal to 2
        w = codebookfile(n, s, a)                       #Assign the variable w to call the program to generate a specific Helberg code book
        z = [int(d) for d in random.choice(w)]          #Assign z to be a randomly chosen word from the generated code book
        mz = moment(z, s)                               #Calculate the moment of that code word using the moment program
        w = randominsert(z, s)                          #Randomly insert at most s-number of bits
        c = momenttest(w,s)                             #Calculate the moment of y-s-prime, the helberg codeword with at most s-random insertions and the s-rightmost 1-bitss deleted
        w2 = genweight(n, s)                            #Assign w2 to generate the program that calculates the recursive weights
        mx = w2[n] + a                                  #Assign mx as the value of the n+1 weight + a (what the moment of the original codeword should be based on the algorithm
        if c <= a and mz == a:                          #If the moment of y-s-prime is less than or equal to a and the original moment of the code word is equal to a
            print ("Moment theorem is true.")           #The moment theorem is found to be true
        elif c <= a and mz != a:                        #If the moment of y-s-prime is less than or equal to a and the original moment of the code word is NOT equal to a
            print ("Moment theorem is false.")          #The moment theorem is found to be false
        elif c > a and mz == mx:                        #If the moment of y-s-prime is greater than a and the original moment of the code word is equal the calculated value mx
            print ("Moment theorem is true.")           #The moment theorem is found to be true
        elif c > a and mz != mx:                        #If the moment of y-s-prime is greater than a and the original moment of the code word is NOT equal the calculated value mx
            print ("Moment theorem is false.")          #The moment theorem is found to be false
        elif c == 0 and mz == 0:                        #If the moment of y-s-prime is equal to 0 and the moment of the original code word is also 0
            print ("Exception Case")                    #This is considered an exception case
