"""/*******************************************
 *
 * K out of K Scheme. ( For now. )
 *
 *
 *  Made by Sabrina Au, Sabrina Tsui, Romeo.
 *  Supervised by Matthew Rhea.
 *  Finished by Evan West
 *
 *  Part of the CS Makerspace VSS Project.
 *
 *******************************************/"""
from __future__ import print_function
import itertools
import numpy as np
import random
import time

# K out of K scheme
# constructs K shares from a black and white image

"""/**
    * MakeW function.
    *
    * generates the groundset W.
    *
    * @param k the number of elements in the groundset
    *
    * @return W the groundset
    */"""
def makeW (k):
   W = []
   i = 1;
   while (i <= k):
      W.append(i)
      i += 1
   return W

# returns a tuple of pi,sigma as a list based on k
# credit to: http://pythonfiddle.com/a-list-of-subsets-of-a-list/
"""/**
    * MakePiSigma function.
    *
    * generates the pi set (the even cardinality set)
    * and the sigma set (the odd cardinality set) from
    * the ground set.
    *
    * @param W the groundset
    * @return the fullset the set with pi and sigma
    *
    */"""
def makePiSigma (W):
   pi = []
   sigma = []
   for i in xrange(0, len(W)+1):
      listing = [list(subset) for subset in itertools.combinations(W, i)]
      if (len(subset)%2 == 0):
         pi.extend(listing)
      else:
         sigma.extend(listing)
   pi[0] =[0]
   return([pi, sigma])

"""/**
    * Search function.
    *
    * search through the given
    * set for the search target.
    *
    * @param search_space
    * @retun bool value according to the
    *
    */"""
def search (target, search_space):
   if target in search_space:
      return True
   else:
      return False

# creates an S0 matrix such that S0 = S0[i,j] = 1 iff ei in pij
"""/**
    * MakeS0 function.
    *
    * generates a S0 set.
    *
    * @param W the groundset
    * @param ps pi or sigma
    * @return nothing yet
    *
    */"""
def makeS (W, ps):
   #set size of s0 to be list of lists with sizes k and 2^(k-1)
   k = len(W)
   col = pow(2,(k-1))
   s = [[2 for x in range(col)] for y in range(k)]
   for i in range(len(s)):
      for j in range(len(s[i])):
         if ( search(W[i],ps[j]) ):
            s[i][j] = 0
         else:
            s[i][j] = 1
   return s

"""/**
    * PermuteMatrix function.
    *
    * permuting the matrix.
    *
    * @param matrix The matrix to be permuted
    * @return the column permuted matrix
    *
    */"""
def permuteMatrix (matrix):
   matrix = np.array(matrix)
   cols = len(matrix[0])
   for i in range(0,cols):
      rand1 = random.randint(0,cols-1)
      rand2 = random.randint(0,cols-1)

      #taken out until such time that we decide it should go back in
      #made the results somewhat more regular but it was a performance overhead
      # while(rand1 == rand2 and cols<100):
      #    rand1 = random.randint(0,cols-1)
      #    rand2 = random.randint(0,cols-1)
      matrix[:,[rand1,rand2]] = matrix[:,[rand2,rand1]]
   return matrix

"""/**
    * koutofk function.
    *
    * the main function for carrying out k out of k
    * image secret splitting.
    *
    * @return nothing
    *
    */"""
def koutofk (k, Matrix):
   W = makeW(k)
   fullset = makePiSigma(W)
   pi = fullset[0]
   sigma = fullset[1]
   # creates an S0 matrix such that S0 = S0[i,j] = 1 iff ei in pij
   s0 = makeS(W, pi)
   # creates an S1 matrix such that S1 = S1[i,j] = 1 iff e1 in sigmaj
   s1 = makeS(W, sigma)

   #TODO: will probably want to change this to binary writing to reduce size of the file
   # startTime = time.time()
   shares = [object] * k
   for i in range(0, k):
      shares[i] = open("share" + str(i), "w")

   # print("Creating files took:", time.time() - startTime)
   # convert a 2D array to k shares and write those shares to files
   # startTime = time.time()

   for line in Matrix:
      for pixel in line:
         # pixelTime = time.time()
         #choose a permutation randomly of either S0 or S1
         # matrixTime = time.time()
         if pixel == 1:
            out = permuteMatrix(s0) # white pixel
         else:
            out = permuteMatrix(s1) # black pixel
         # print("time to permutate:", time.time() - matrixTime)
         # distribute the permutation among the shares
         for i in range(0, k):
            for subpixel in out[i]:
               shares[i].write(str(subpixel))
         # print("time for one pixel:", time.time() - pixelTime)
      for i in range(0, k):
         shares[i].write("\n")
   for i in range(0, k):
      shares[i].close()

   # print("Creating shares took:", time.time() - startTime)

   return 0

def koutofk_to3D_Matrix(k, Matrix):
   if  k % 2 == 0:
      print("Invalid k:",k)
      return [[]]
   W = makeW(k)
   fullset = makePiSigma(W)
   pi = fullset[0]
   sigma = fullset[1]
   # creates an S0 matrix such that S0 = S0[i,j] = 1 iff ei in pij
   s0 = makeS(W, pi)
   # creates an S1 matrix such that S1 = S1[i,j] = 1 iff e1 in sigmaj
   s1 = makeS(W, sigma)

   # startTime = time.time()
   side_len = 2 << ((k-1)/2) - 1  #(2^(k-1))/2 is the size of a side of a pixel in subpixels
   #print(side_len)
   pixels = 0
   for pixel in Matrix[0]:
      pixels += 1
   matrix_width = side_len * pixels #side_length * k^(k-1) * width of picture
   lines = 0
   for line in Matrix:
      lines += 1
   matrix_depth = side_len * lines
   outMatrix = np.zeros((k, matrix_depth, matrix_width), dtype=np.uint8)
   doffset = 0
   for line in Matrix:
      woffset = 0
      for pixel in line:
         # pixelTime = time.time()
         #choose a permutation randomly of either S0 or S1
         # matrixTime = time.time()
         if pixel == 1:
            out = permuteMatrix(s0) # white pixel
         else:
            out = permuteMatrix(s1) # black pixel
         # print("time to permutate:", time.time() - matrixTime)
         #distribute the permutation among the shares
         for i in range(0, k):
            pos = 0
            for depth in range(doffset, doffset + side_len):
               for width in range(woffset, woffset + side_len):
                  #print("i, woffset, depth, width, subpixel:",i,woffset,depth,width,out[i][pos])
                  outMatrix[i][depth][width] = out[i][pos]
                  pos += 1
         woffset += side_len
         # print("time for one pixel:", time.time() - pixelTime)
      doffset += side_len

   # print("Creating shares took:", time.time() - startTime)

   return outMatrix

def toImage(k):
   #TODO: eventually shares will come as arguments
   # startTime = time.time()
   share = open("share0", "r")
   num_lines = sum(1 for line in share) #assume the files are the same sizes (should be anyway)
   share.close()
   shares = [object] * k
   for i in range(0, k):
      shares[i] = open("share" + str(i), "r")

   #compute the length of a individual pixel's share
   length = 2 << (k-2) #same as 2^(k-1)
   # print("num_lines", num_lines)
   num_pixels = len(shares[0].readline())/length
   shares[0].seek(0,0)
   Matrix = np.zeros((num_lines, num_pixels), dtype=np.uint8)
   for i in range(0, num_lines):
      lines = [object] * k
      for x in range(0, k):
         lines[x] = shares[x].readline()
         lines[x] = lines[x][:-1] #slice off the newline character of the line

      beg = 0 #The first digit of a share

      while beg < len(lines[0]):
         white=False
         for x in range(beg, beg + length):
            #if there's a single matching of all white subpixels than the pixel must be white
            w = True
            for line in lines:
               if line[x] != "1":
                  w = False
            if w:
               white=True
         #print results out to console
            #Prints out in as 0 or 1 in the place where that pixel would be in the image
            #ie
            #  100
            #  011
            #  101
            #for a image that is 3x3 pixels
         #TODO: for generating the image, what is the proper format? -> 2D array
         # print(i, beg/length, end="")
         if(white):
            Matrix[i][beg/length] = 1
            # print("-> 0")
         else:
            Matrix[i][beg/length] = 0
            # print("-> 1")
         beg += length
   # print("Shares -> pixels took:", time.time() - startTime)
   return Matrix

def stack_images(Images):
   #set up the output Matrix which will be the dimensions of the original matrix
   num_pixels = sum(1 for subpixel in Images[0][0])
   num_lines = sum(1 for subpixel in Images[0])
   outMatrix = np.zeros((num_lines, num_pixels), dtype=np.uint8)
   for line in range(0, num_lines):
      for pixel in range(0, num_pixels):
         white = True
         for image in Images:
            if image[line][pixel] == 0:
               white = False
         if white:
            outMatrix[line][pixel] = 1
         else:
            outMatrix[line][pixel] = 0
   return outMatrix

def toImage_fr3D(k, Matrix):
   #set up the output Matrix which will be the dimensions of the original matrix
   subpixels = 2 << ((k-1) /2) - 1
   num_pixels = sum(1 for subpixel in Matrix[0][0])/subpixels
   num_lines = sum(1 for subpixel in Matrix[0]) /subpixels
   outMatrix = np.zeros((num_lines, num_pixels), dtype=np.uint8)
   #Calculate the value of each pixel by combining squares of subpixels between the shares
   for i in range(num_lines):
      for j in range(num_pixels):
         white = False
         for depth in range(i*subpixels, (i+1)*subpixels):
            for width in range(j*subpixels, (j+1)*subpixels):
               w = True
               for share in Matrix:
                  # Can be used with 0 or 1 or with 0 or 255 images
                  if share[depth][width] == 0:
                     w = False
               if w:
                  white = True
         if white:
            outMatrix[i][j] = 1
         else:
            outMatrix[i][j] = 0
   return outMatrix
      # beg = 0 #The first digit of a share

      # while beg < len(lines[0]):
      #    white=False
      #    for x in range(beg, beg + length):
      #       #if there's a single matching of all white subpixels than the pixel must be white
      #       w = True
      #       for line in lines:
      #          if line[x] != "0":
      #             w = False
      #       if w:
      #          white=True
      #    #print results out to console
      #       #Prints out in as 0 or 1 in the place where that pixel would be in the image
      #       #ie
      #       #  100
      #       #  011
      #       #  101
      #       #for a image that is 3x3 pixels
      #    #TODO: for generating the image, what is the proper format? -> 2D array
      #    # print(i, beg/length, end="")
      #    if(white):
      #       Matrix[i][beg/length] = 0
      #       # print("-> 0")
      #    else:
      #       Matrix[i][beg/length] = 1
      #       # print("-> 1")
      #    beg += length



   #for prow in range(fakepic):
   #   for pcol in range(fakepic[prow]):
   #      if  fakepick[prow][pcol] == 0:
   #         C0matrix = permuteMatrix(s0)
   #         #distribute the rows to k shares
   #         for s in range(0,k):
   #           share[s][c] = C0matrix[s]
   #           c = c+1
   #      else:
   #         C1matrix = permuteMatrix S1


###MAIN###
# k = 15
# fakepic = [[0,1,1,1],[0,1,1,0],[0,1,0,1],[1,0,0,0]]

# If you want to put shares into an image
# Matrix = koutofk_to3D_Matrix(k, fakepic)
# # for share in Matrix:
# #    for line in share:
# #       print(line)
# #    print()
# Matrix = toImage_fr3D(k, Matrix)
# print(Matrix)

# If you want to put shares in files
# koutofk(k, fakepic)
# print(toImage(k))