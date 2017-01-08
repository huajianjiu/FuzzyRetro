import numpy as np
import os.path
import cPickle as pickle
import sys


class PPDB_2(object):
    def __init__(self, ppdb="ppdb-2.0-tldr"):
        self.ppdb_paraphrases = ppdb_paraphrases = {}
        with open(ppdb, "r") as ppdb_f:
            lines = ppdb_f.readlines()
            print "Total lines: " + str(len(lines))
            n = 0
            for line in lines:
                baseword = line.split("|||")[1].strip()
                ppword = line.split("|||")[2].strip()
                score = line.split("|||")[3].split(" ")[1].split("=")[1]
                if (line.split("|||")[-1].strip() == "Equivalence"):
                    self.add_paraphrases(baseword, ppword, score)
                    self.add_paraphrases(ppword, baseword, score)
                elif (line.split("|||")[-1].strip() == "ForwardEntailment"):
                    self.add_paraphrases(baseword, ppword, score)
                elif (line.split("|||")[-1].strip() == "ReverseEntailment"):
                    self.add_paraphrases(ppword, baseword, score)
                n += 1
                if n%10000 == 0:
                    print str(n) + " lines processed."
        print "Finish. Totally "+str(n)+" lines processed."

    def search_baseword(self, inputword):
        return inputword in self.ppdb_paraphrases.keys()
    
    def add_paraphrases(self, baseword, ppword, score):
        if baseword == ppword:
            return
        if self.search_baseword(baseword):
            if ppword in self.ppdb_paraphrases[baseword].keys():
                return
            else:
                self.ppdb_paraphrases[baseword][ppword] = score
        else:
            self.ppdb_paraphrases[baseword] = {ppword: score}

    def save_ppdb(self):
        with open("ppdb2.pkl", "wb") as f_save:
            pickle.dump(self.ppdb_paraphrases, f_save)


if __name__ == "__main__":
    if len(sys.argv)>1:
        #python PPDB.py ppdb
        ppdb_s_corpus = PPDB_2(sys.argv[1])
    else:
        ppdb_s_corpus = PPDB_2()
    ppdb_s_corpus.save_ppdb()
