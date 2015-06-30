#!/usr/bin/env python
"""
CECS 310  Programming Assignments 1 & 2
Combinations and Permutations
Joseph Slone - 12/1/2014 Initial coding, Combinations working
             - 12/2/2014 Got the permutations working
             - 12/3/2014 Cleaned up the code and comments

Notes:  All output goes to stdout and stderr; using standard
        command line redirection to send output to output.dat

        I'm not doing much in the way of error checking, a malformed
        input file will probably cause the program to crash.
"""

from math import factorial
import itertools

# Globals
input_file = 'infile.dat'   # Name of input file

def main():

    # Open the file and determine how many
    # sets of data are to be processed.

    input_list = []
    f = open(input_file, 'r')
    items_to_process = int(f.readline())

    for item in range(0, items_to_process):

        # Read an instruction line, determine
        # - the type of operation to be performed
        # - the number of items
        # - the number of combinations or permutations
        #  
        # strip() is used to make certain no extraneous whitespace
        # interferes with the split function.

        (routine, items_s, count_s ) = f.readline().strip().split(' ')
        items = int(items_s)
        comb = int(count_s)  # Yes, I'm wasting space, but it 
        perm = int(count_s)  # helps with readability later on

        # Start with an empty list 
        # Read the appropriate number of lines
        # from the datafile and append to the list.
        # then sort the list.

        del input_list[:]        
        for i in range(0, items):
            input_list.append(f.readline().rstrip())

        input_list.sort()

        # Call the appropriate function

        if (routine == 'C'):
            combination(input_list, comb, items)
        else: 
            if (routine == 'P'):
                permutation(input_list, perm, items)
                # perm_python was used to check my code
                # for accuracy
                # perm_python(input_list, perm, items)

    f.close()
    return


#
# n Choose R function
#

def ncr(n, r):
    #   n choose r = n! /((n-r)! * r!)        
    num = factorial(n)
    den = factorial(r) * factorial(n-r)
    return num/den
#
# n Permutations r function
#

def npr(n, r):
    num = factorial(n)
    den = factorial(n-r)
    return num/den

# 
# swap two list elements
#

def swap(s,a,b):
     
    #  Yes, it is a one-liner function, but it is still easier
    #  to read and not that much overhead.

    s[a],s[b] = s[b],s[a]  
    return

#
# Print a formated segment of the input list
#

def print_segment(input_list, l, n):

    #   input_list is the list of items to be printed
    #   l is a list of indexes into input_list
    #   n is the number of items to be printed.

    segment = []    
    for i in range(0,n):
        segment.append(input_list[l[i]])

    print "[{0}]".format(",".join(segment)) 
    return

# 
# Create a sub-segment of the original list
# This is used when permuting a single combination
# from the original list.
#
# Returns a new list

def make_segment(input_list, l, n):

    # input_list is the list of items to be copied from
    # l is a list of indexes into input_list
    # n is the number of items to be printed

    segment = []
    for i in range(0,n):
        segment.append(input_list[l[i]])
        
    return segment

# 
# Print all n choose r combinations
#

def combination(input_list,r,n):

    print 
    print "============"
    print "Combinations"
    print "============"
    print "Input List: ", input_list    
    print "n, r: ", n, r
    print "n choose r: ", ncr(n,r)

    s = range(0,r)
    print_segment(input_list,s,r)

    for i in range(2, ncr(n,r)+1):
        m = r-1 
        max_val = n-1

        # find the rightmost element not at it's maximum value

        while (s[m] == max_val):
            m = m-1
            max_val = max_val-1 

        # the rightmost value is incremented

        s[m] += 1

        # the rest of the elements are succors of s[m]

        for j in range(m+1, r):
            s[j] = s[j-1]+1

        # and print the ith combination

        print_segment(input_list, s, r)

    return

#
# print n permutations of the input list
#

def permutation_n(input_list,n):
    
    # First permutation
    
    s = range(0,n)

    # and print it.

    print_segment(input_list, s, n )


    for i in range(2, factorial(n) + 1):
        
        m = n-2 

        # find the first decrease working from the right

        while (s[m] > s[m+1]):
            m = m-1

        k = n-1  
    
        # find the first decrease working from the right

        while (s[m] > s[k]):
            k = k-1

        swap(s,m,k)
        p = m+1
        q = n-1 

        # swap s[m+1] and s[n], swap s[m+2] and s[n-1], and so on

        while (p < q):
            swap(s,p,q)
            p += 1
            q -= 1

        # and print the ith perumtation
        print_segment(input_list, s, n)
        
    return

#
# generate n r-length permutations of the input list
#

def permutation(input_list, r, n):
    print 
    print "============"
    print "Permutations"
    print "============"
    print "Input List: ", input_list
    print "n, r: ", n, r
    print "Permutations: ", npr(n,r)

    # First combination
    s = range(0,r)

    # Copy it to a new list
    seg = make_segment(input_list, s, r)    

    # and generate all of the permutations of the new list
    permutation_n(seg, r)

    for i in range(2, ncr(n,r)+1):
        m = r-1 
        max_val = n-1
        # find the rightmost element not at its maximum value
        while (s[m] == max_val):
            m = m-1
            max_val = max_val-1 

        # rightmost value is incremented
        s[m] += 1

        # the rest of the elements are the successors of s[m]
        for j in range(m+1, r):
            s[j] = s[j-1]+1

        # copy the ith combination to a new list
        seg = make_segment(input_list, s, r)

        # and generate all of the permutations of the new list
        permutation_n(seg,r)

    return

#
# Generate lexicographic ordered permutations the python way
#

def perm_python(input_list,r,n):

    # This is only to test my work,  python has a permutations function
    # in the standard library.

    print "Using the itertools function"
    print "Input List: ", input_list
    print "n, r:", n, r
    print "Permutations: ", npr(n,r)

    for l in itertools.permutations(input_list, r):
        print l

    return

if __name__=='__main__':
    main()

