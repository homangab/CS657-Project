import pygtrie as trie
import sys
uposorgos = open("uposorgo.txt","r").read().split("\n")
common_suffs = open("known_suff.txt").read().split("\n")

upotree = trie.CharTrie()
for i in uposorgos:
    upotree[i] = True

suff_tree = trie.CharTrie()
for i in common_suffs:
    suff_tree[i[::-1]] = True
#print(upotree, suff_tree)

kars = open("karlist.txt","r").read().split("\n")
k = open("karlist.txt","a")
inp = open(sys.argv[1],"r").read().split("\n")
inp.remove("")

abyays = open("abyay.txt","r").read().split("\n")
ab_tree = trie.CharTrie()
for i in abyays:
    ab_tree[i] = True

gras = open("gras_roots.txt","r").read().split("\n")
gras_tree = trie.CharTrie()

for i in gras:
    gras_tree[i] = True
gras = open("gras_suffs.txt","r").read().split("\n")
gras_suff_tree = trie.CharTrie()

for i in gras:
    gras_suff_tree[i[::-1]] = True

def stem(inp):
    for word in inp:
        unstemmed = word
    #        print("Input Word : " + word)
    #        print("removing known suffixes (5 iterations).............")
        try:                                                                        # check for known abyay
            ab_tree[word]
            print(unstemmed + " ----> " + word)
            continue
        except:
            pass
        try:
            for i in range(5):                                                      # iterate on primary prefixes       
                k = len(suff_tree.longest_prefix(word[::-1])[0])
                if(k > 0):
                    #print(len(suff_tree.longest_prefix(word[::-1])[0]))
                    word = word[:-k]
                #   print(word)
                #print("removing known prefixes (3 iterations).............")
            for i in range(1):                                                      # iterate on word_roots generated by grass
                try:
                    k = len(gras_tree.longest_prefix(word)[0])
                    if(k > 0):
                    #print(len(suff_tree.longest_prefix(word[::-1])[0]))
              #      print(word)
                        word = word[:k]
                except:
                    pass

            for i in range(3):                                                      # iterate on freq_suffs generated by gras and cut off
                k = len(gras_suff_tree.longest_prefix(word[::-1])[0])
                if(k > 0 and k < 5):
                    #print(len(suff_tree.longest_prefix(word[::-1])[0]))
                    word = word[:-k]
                    
            for i in range(1):                                                      # finally removing uposorgo but loof for meaningfulness(cannot start with a vowel kar) 
                k = len(upotree.longest_prefix(word)[0])                            # and do not do for very small words
                if(k > 0):
                    #k.write(word[len(upotree.longest_prefix(word)[0])])
                    if(word[k] not in kars and len(word[k:]) > 5):
                        word = word[k:]
                #       print(word)

        except:
            pass
        print(unstemmed + " ----> " + word)
#        print(word)

stem(inp)
