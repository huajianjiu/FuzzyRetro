import numpy as np
import os.path
import cPickle as pickle
import sys


class PPDB_2(object):
    def __init__(self, vocab="vocab.txt", ppdb="ppdb-2.0-tldr", output="ppdb2.txt"):
        self.vocab = vocab
        self.ppdb_paraphrases = ppdb_paraphrases = {}
        self.word_hash = {}
        self.output = output
        with open(vocab, "r") as f_vocab:
                words = f_vocab.readlines()
                self.words = words = [x.split()[0] for x in words]
                for n,w in enumerate(words):
                    self.word_hash[w]=n
        with open(ppdb, "r") as ppdb_f:
            lines = ppdb_f.readlines()
            print "Total lines: " + str(len(lines))
            n = 0
            for line in lines:
                if (self.search_hash(line.split("|||")[1].strip()) > 0) and (self.search_hash(line.split("|||")[2].strip()) > 0):
                    baseword = line.split("|||")[1].strip()
                    ppword = line.split("|||")[2].strip()
                    if (line.split("|||")[-1].strip() == "Equivalence"):
                        self.add_paraphrases(baseword, ppword)
                        self.add_paraphrases(ppword, baseword)
                    elif (line.split("|||")[-1].strip() == "ForwardEntailment"):
                        self.add_paraphrases(baseword, ppword)
                    elif (line.split("|||")[-1].strip() == "ReverseEntailment"):
                        self.add_paraphrases(ppword, baseword)
                n += 1
                if n%10000 == 0:
                    print str(n) + " lines processed."
        print "Finish. Totally "+str(n)+" lines processed."

    def search_hash(self, word):
        try:
            return self.word_hash[word]
        except KeyError:
            return -1
        except:
            print "Unexpected error:", sys.exc_info()[0]
            return -1

    def search_baseword(self, inputword):
        return inputword in self.ppdb_paraphrases.keys()
    
    def add_paraphrases(self, baseword, ppword):
        if self.search_baseword(baseword):
            self.ppdb_paraphrases[baseword].append(ppword)
        else:
            self.ppdb_paraphrases[baseword] = [ppword]

    def save_ppdb(self):
        print "Writing to ouput file.",
        with open(self.output, "w") as f_save:
            n = 0
            for word in self.words:
                if word == "UNK":
                    write_line = "</s> </s>\n"
                elif word in self.ppdb_paraphrases.keys():
                    write_line = str(word) + " "
                    for ppword in self.ppdb_paraphrases[word]:
                        write_line += ppword + " "
                    write_line += "</s>\n"
                else:
                    write_line = str(word) + " </s>\n"
                f_save.write(write_line)
                n += 1
                if n%1000 == 0:
                    print ".",
                    f_save.flush()


if __name__ == "__main__":
    if len(sys.argv)>1:
        #python PPDB.py vocab ppdb output
        ppdb_s_corpus = PPDB_2(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        ppdb_s_corpus = PPDB_2()
    ppdb_s_corpus.save_ppdb()
