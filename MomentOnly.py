#The following programs can be used to calculate the weight of a single code word with s-errors.

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
