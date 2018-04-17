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

def stem(inp):
    for word in inp:
        unstemmed = word
    #        print("Input Word : " + word)
    #        print("removing known suffixes (5 iterations).............")
        try:
            ab_tree[word]
            print(unstemmed + " ----> " + word)
            continue
        except:
            pass
        for i in range(5):
            if(len(suff_tree.longest_prefix(word[::-1])[0]) > 0):
                #print(len(suff_tree.longest_prefix(word[::-1])[0]))
                word = word[:-len(suff_tree.longest_prefix(word[::-1])[0])]
    #                print(word)
    #        print("removing known prefixes (3 iterations).............")
        for i in range(3):
            if(len(upotree.longest_prefix(word)[0]) > 0):
                #k.write(word[len(upotree.longest_prefix(word)[0])])
                if(word[len(upotree.longest_prefix(word)[0])] not in kars):
                    word = word[len(upotree.longest_prefix(word)[0]):]
    #                print(word)
        print(unstemmed + " ----> " + word)

stem(inp)
