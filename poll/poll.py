#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author Yash Pandey, Pritam Basnet
poll.py
July 11, 2019

This program reads in prefernce ballot data and gives the results for the Plurality, Majority, 
Broda, Approval and Condorcet methods.

The voters have voted in a preferance ranking manner, where first 
postion implies first preferance.
For example, consider an election with five candidates whom we will 
call A, B, C, D and E. One voter might rank the candidates this way:
DABCE


A PLurality winner is the candidate with the most mount of first preferance votes.

A Majority winner is the candidate who was able to achieve more than 50% of the first 
preferance votes.

A broda winner is decided by assigning a weight to the preferance ranking votes, adding 
them all up and then declaring a winner, which is the candidate with the most amount of points.

A Approval winner is decided where voters may vote for candidates that they approve off, here,
ranking does not matter. The candidate with the most votes wins.

A condorcet winner is a candidate who would win a two candidate election against all 
the other candidates in a plurality votes.
"""

#Function Definitons ==========================================================

def readFile(filename):
    """
    This function opens, reads and closes a text file. 
    The function then returns the whole text file as one string.
    PARAMETERS:
        filename - a string indicating the name of the file
    RETURN VALUE:
        a string containging the entire text file
    """    
    file = open(filename,"r")
    text = file.read()   
    file.close()
    
    voteList = []
    text=text.split("\n")
       
    for i in range(len(text)-1):
        text[i]=text[i].strip()
        voteList.append((text[i]).split(" "))
          
    return voteList

def plurality(voteList):
    '''
     This function takes the preference ballot data as an input and returns the
	counts for a plurality election. A dictionary was created to holde the 
    data of first place winner. All possible candiates were initialized to a value 
    of zero. After which the number of times thse candidates recieved 
    first place votes was calculated.
	Parameters:
        	voteList - This is the preference ballot data. It is a list.
	Return Value:
        	The counts for a plurality election.    
    '''
    d = {}

    flag = 0
    for i in voteList:
        if(flag == 0):
            for x in i:
                d[x] = 0
            flag = 1

        j = i[0]
        if j not in d:
            d[j] =  1
        else:
            d[j] = d[j] + 1
                          
    return d      

def majority(results):
    """
	This function takes the results of the plurality election and determies if
	there is a majority winner.
	Parameter:
        	results - The output from the plurality function.
	Return Value:
        	A majority winner if one exists.
    """

    frequencyValues = list(results.values())
    sumValues = sum(frequencyValues)
    maxFrequency = max(frequencyValues)
            
    if maxFrequency >= ((sumValues/2)+1):
        for key in results:
            if results[key] == maxFrequency:
                print("Majority Winner is",key)
                
    else:
        print("No Majority Winner in this data.")           
         
def borda(voteList):
    """
	This function takes the preference ranking data as an input parameter. It
	computes the Borda score for each candidate and returns the scores in a
	dictionary.
	Parameters:
        	voteList - The preference ranking data as a list of lists.
	Return Value:
        	The Borda results for each candidate.
	"""
    d = {} 
    for i in voteList:
        for j in i:
            if j not in d:
                d[j] = len(i)- i.index(j)
            else:
                d[j] = d[j] + len(i) - i.index(j)
            
    return d     

def approval(voteList):
    '''
	This function takes the data returned from the approval text function and
	returns a data structure holding the approval scores for each candidate.
	Parameters:
     	- The data from the readFile function
	Return Value:
    	The approval scores for each candidate.
	'''
    d={} 
    for i in voteList:
        for j in i:
            if j not in d:
                d[j] =  1
            else:
                d[j] = d[j] + 1
    
    return d 

def isWinner(data,c1,c2):
    """
	This function takes the preference ranking data as an input parameter. It computes the 
    head to head winner for the two candidates that are passed into it as parameters.
    If the first candidate passed as a paramter wins against the second candidate, then 
    the function will return true, else, the function will return false.
	Parameters:
        	data - The preference ranking data as a list of lists.
	Return Value:
        	True - if first candidate wins
         False - if first candidate does not win
	"""
    lenC1 = 0
    lenC2 = 0
    countC1 = 0 
    countC2 = 0
    
    for c in data:
        
        for i in range(len(c)):
            if c[i] == c1:
                lenC1 = i
            elif c[i] == c2:
                lenC2 = i
                            
        if lenC2 >= lenC1:
                        countC1 = countC1 + 1
        elif lenC2 <= lenC1:
                        countC2 = countC2 +1
                                            
    if countC1 >= countC2:
        return True 
    
    return False

def conCor(data):
    """
    This function takes in data containing voting results and returns the Condorcet 
    winner, if on exists, by using the isWinner function. The function returns 
    a string saying 'No Condorcet Winner exists in this data.' if there are no
    condorcet winners.
    PARAMETERS:
        - The output from the readFile function.
    RETURN VALUE:
        - The condorcent winner.
    """
    
    d = { }        
    
    for c in data[0]:
        if c not in d:
            d[c]= 0
        for i in range(len(data[0])):
            if isWinner(data,c,data[0][i]):
                    d[c] = d[c] +1 
   
    hi = max(d.values())      
    lenA = len(d) - 1
    
    if hi == lenA:
        for i in d:
            if hi == d[i]:
                return i 
            
    return "No Condorcet Winner exists in this data."

#Main Function Definition =====================================================
    
def main():            
#Calling function readFile to read data
    text1= readFile('data.txt')
    text2 = readFile('approval.txt')

#Calling plurality function and printing the output as a table
    resultP = plurality(text1)
    print("Plurality")        
    for c in resultP:
        print(c,"\t",resultP[c])
        
#Calling majority function and printing the output         
    print("\t")
    print("Majority")
    majority(resultP)

#Calling  borda function and printing the output as a table
    print("\t")
    print("Borda")
    resultBro = borda(text1)
    for c in resultBro:
        print(c,"\t",resultBro[c])

#Calling  approval function and printing the output as a table                  
    resultAp = approval(text2)         
    print("\t")
    print("Approval")
    for c in resultAp:
        print(c,"\t",resultAp[c])

#Calling  conCor function and printing the output           
    print("\nCondorcet")
    print(conCor(text1))


#Main Function Call ===========================================================
    
main()






























