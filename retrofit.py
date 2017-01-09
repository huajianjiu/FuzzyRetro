import argparse
import gzip
import math
import numpy
import re
import sys
import cPickle as pickle

from copy import deepcopy

isNumber = re.compile(r'\d+.*')
def norm_word(word):
  if isNumber.search(word.lower()):
    return '---num---'
  elif re.sub(r'\W+', '', word) == '':
    return '---punc---'
  else:
    return word.lower()

''' Read all the word vectors and normalize them '''
def read_word_vecs(filename):
  wordVectors = {}
  if filename.endswith('.gz'): fileObject = gzip.open(filename, 'r')
  else: fileObject = open(filename, 'r')
  
  for line in fileObject:
    line = line.strip().lower()
    word = line.split()[0]
    wordVectors[word] = numpy.zeros(len(line.split())-1, dtype=float)
    for index, vecVal in enumerate(line.split()[1:]):
      wordVectors[word][index] = float(vecVal)
    ''' normalize weight vector '''
    wordVectors[word] /= math.sqrt((wordVectors[word]**2).sum() + 1e-6)
    
  sys.stderr.write("Vectors read from: "+filename+" \n")
  return wordVectors

''' Write word vectors to file '''
def print_word_vecs(wordVectors, outFileName):
  sys.stderr.write('\nWriting down the vectors in '+outFileName+'\n')
  outFile = open(outFileName, 'w')  
  for word, values in wordVectors.iteritems():
    outFile.write(word+' ')
    for val in wordVectors[word]:
      outFile.write('%.4f' %(val)+' ')
    outFile.write('\n')      
  outFile.close()
  
''' Read the PPDB word relations as a dictionary '''
def read_lexicon(filename, wordVecs):
  lexicon = {}
  for line in open(filename, 'r'):
    words = line.lower().strip().split()
    lexicon[norm_word(words[0])] = [norm_word(word) for word in words[1:]]
  return lexicon

''' Retrofit word vectors to a lexicon '''
def retrofit(wordVecs, lexicon, numIters):
  newWordVecs = deepcopy(wordVecs)
  wvVocab = set(newWordVecs.keys())
  loopVocab = wvVocab.intersection(set(lexicon.keys()))
  for it in range(numIters):
    # loop through every node also in ontology (else just use data estimate)
    for word in loopVocab:
      wordNeighbours = set(lexicon[word]).intersection(wvVocab)
      numNeighbours = len(wordNeighbours)
      #no neighbours, pass - use data estimate
      if numNeighbours == 0:
        continue
      # the weight of the data estimate if the number of neighbours
      newVec = numNeighbours * wordVecs[word]
      # loop over neighbours and add to new vector (currently with weight 1)
      # with membership as the weight
      for ppWord in wordNeighbours:
        newVec += newWordVecs[ppWord]
      newWordVecs[word] = newVec/(2*numNeighbours)
  return newWordVecs

''' Read the PPDB2 word relations as a dictionary '''
def read_ppdb2(filename, wordVecs):
  lexicon = {}
  with open(filename, 'rb') as f_load:
    lexicon = pickle.load(f_load)
  return lexicon

''' Retrofit word vectors to a lexicon '''
def fuzzy_retrofit(wordVecs, lexicon, numIters):
  newWordVecs = deepcopy(wordVecs)
  wvVocab = set(newWordVecs.keys())
  loopVocab = wvVocab.intersection(set(lexicon.keys()))
  for it in range(numIters):
    # loop through every node also in ontology (else just use data estimate)
    for word in loopVocab:
      wordNeighbours = set(lexicon[word].keys()).intersection(wvVocab)
      numNeighbours = len(wordNeighbours)
      #no neighbours, pass - use data estimate
      if numNeighbours == 0:
        continue
      totalDegree = 0
      for ppword in wordNeighbours:
          totalDegree += float(lexicon[word][ppword])
      # the weight of the data estimate if the number of neighbours
      newVec = totalDegree * numNeighbours * wordVecs[word]
      # loop over neighbours and add to new vector (currently with weight 1)
      # with membership as the weight
      for ppWord in wordNeighbours:
        newVec += float(lexicon[word][ppword]) * newWordVecs[ppWord]
      newWordVecs[word] = newVec/(2*totalDegree*numNeighbours)
  return newWordVecs
  
if __name__=='__main__':

  parser = argparse.ArgumentParser()
  parser.add_argument("-i", "--input", type=str, default=None, help="Input word vecs")
  parser.add_argument("-l", "--lexicon", type=str, default=None, help="Lexicon file name")
  parser.add_argument("-o", "--output", type=str, help="Output word vecs")
  parser.add_argument("-n", "--numiter", type=int, default=10, help="Num iterations")
  args = parser.parse_args()

  numIter = int(args.numiter)
  outFileName = args.output

  wordVecs = read_word_vecs(args.input)
  if args.lexicon[-4:] == ".pkl":
    lexicon = read_ppdb2(args.lexicon, wordVecs)
    ''' Enrich the word vectors using ppdb and print the enriched vectors '''
    print_word_vecs(fuzzy_retrofit(wordVecs, lexicon, numIter), outFileName) 
  else:
    lexicon = read_lexicon(args.lexicon, wordVecs)
    ''' Enrich the word vectors using ppdb and print the enriched vectors '''
    print_word_vecs(retrofit(wordVecs, lexicon, numIter), outFileName) 
