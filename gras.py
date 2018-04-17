import sys
import os


lamdaVals = [5,6,7]  #average word length
lamda = 6

alphavalues = [2,4,6] #minimum occurence of a pair of suffixes to consider them FREQUENT
alpha = 7

gammaValues = [0.7,0.8,0.9]
gamma = 0.9

lexiconsPath = "lexicons.txt"
outputPath = ""

suffixPairDict = dict()
nodePairDict = dict()

f = open(lexiconsPath,"r")
original_lexemes = f.read().split("\n")
lexemes = []
def chopKnownSuffixes(freq_suffix=[],suffListFlag=False):
    lexemes = []
    if(suffListFlag):
        for lexeme in original_lexemes:
            if(suffListFlag == True):
                for suffix in freq_suffix:
                    k = len(suffix)
                    if(lexeme[-k:] == suffix):
                        lexeme = lexeme[:-k]
                        lexemes.append(lexeme)
                        break
            lexemes.append(lexeme)
    else:
        lexemes = original_lexemes

#it makes a pass over the lexicon and computes the frequency of the different suffix pairs.
def LongestCommonSubstr(a,b):
    common = a[0:lamda]
    for i in range(lamda,min(len(a),len(b))):
            if(a[i] == b[i]):
                common = common + a[i]
            else:
                return common
    return common

def KeyCreate(boolean, a, b):
    key = ""
    if(boolean):
        key = a + ":" + b
    else:
        key = b + ":" + a
    return key


def ComputeFreqSuffixPairs():
    print("ComputeFreqSuffixPairs")
    f = open(lexiconsPath,"r")
    lexemes = f.read().split("\n")
    arr = []
    prefix = ""
    for lexeme in lexemes:
        if(len(lexeme) >= lamda):
            if(len(arr) == 0):
                prefix = lexeme[0:lamda]
                arr.append(lexeme)
            else:
                if(lexeme in arr):
                    continue
                currPrefix = lexeme[0:lamda]
                
                if(prefix == currPrefix):
                    arr.append(lexeme)
                else:
                    for i in range(len(arr)):
                        for j in range(i+1,len(arr)):
                            lcs = LongestCommonSubstr(arr[i],arr[j])
                            leftsuff = arr[i][len(lcs):]
                            rightsuff = arr[j][len(lcs):]
                            if(leftsuff != rightsuff):
                                suffixPairKey=KeyCreate(leftsuff > rightsuff, leftsuff, rightsuff)
                                if(suffixPairKey in suffixPairDict):
                                    suffixPairDict[suffixPairKey] += 1
                                else:
                                    suffixPairDict[suffixPairKey] = 1
                    arr = []


def FormClasses(output):
    print("FormClasses")
    f = open(lexiconsPath,"r")
    lexemes = f.read().split("\n")
    arr = []
    prefix = ""
    for lexeme in lexemes:
        if(len(lexeme) >= lamda):
            if(len(arr) == 0):
                prefix = lexeme[0:lamda]
                arr.append(lexeme)
            else:
                if(lexeme in arr):
                    continue
                currPrefix = lexeme[0:lamda]
                if(prefix == currPrefix):
                    arr.append(lexeme)
                else:
                    nodePairDict = dict()
                    for i in range(len(arr)):
                        for j in range(i,len(arr)):
                            lcs = LongestCommonSubstr(arr[i],arr[j])
                            leftsuff = arr[i][len(lcs):]
                            rightsuff = arr[j][len(lcs):]
                            if(leftsuff != rightsuff):
                                suffixPairKey=KeyCreate(leftsuff > rightsuff, leftsuff, rightsuff)
                                edgeWeight = suffixPairDict.get(suffixPairKey)
                                if (edgeWeight >= alpha):
                                    leftLexeme = arr[i]
                                    rightLexeme = arr[j]
                                    if (leftLexeme != rightLexeme):
                                        nodePairKey = KeyCreate(leftsuff > rightsuff, leftLexeme, rightLexeme);
                                        nodePairDict[nodePairKey] = edgeWeight
#                    print("nodePairDict",nodePairDict.keys())
                    GraphandCluster(nodePairDict,output)
                    arr = []

def GraphandCluster(nodePairDict,output):
    print("GraphandCluster")
    adjacencyDict = dict()
    for key in nodePairDict.keys():
        keyparts = key.split(":")
        # print(key)
        for i in range(2):
            if (keyparts[i] in adjacencyDict.keys()):
                temp =  adjacencyDict[keyparts[i]]
                temp.append(keyparts[(i+1)%2])
                adjacencyDict[keyparts[i]] = temp
            else:
                temp = []
                temp.append(keyparts[(i+1)%2])
                adjacencyDict[keyparts[i]] = temp

    #SORT THE ADJACENCY LISTS
    for key in adjacencyDict.keys():
        currentList = adjacencyDict[key];
        destNodes = [""]*len(currentList)
        edgeWeights = [""]*len(currentList)
        for i in range(len(currentList)):
            destNodes[i] = currentList[i]
            edgeWeights[i] = nodePairDict[createKey(key, destNodes[i])]

        sortedDestNodes = []
        for i in range(len(edgeWeights)):
            maxidx = edgeWeights.index(max(edgeWeights[i:]))
            if(i!=maxidx):
                edgeWeights[i],edgeWeights[maxidx] = edgeWeights[maxidx],edgeWeights[i]
                destNodes[i],destNodes[maxidx] = destNodes[maxidx],destNodes[i]
            sortedDestNodes.append(destNodes[i])
        adjacencyDict[key] = sortedDestNodes

    if(len(adjacencyDict.keys()) != 0):
        print("<<<---------------------------------CLUSTERING GRAPH------------------------------------>")
    while(len(adjacencyDict.keys()) != 0):
        #NODE WITH LONGEST LIST
        longestlist = []
        longestlistNode = None
        for key in adjacencyDict.keys():
            if(len(adjacencyDict[key]) >= len(longestlist)):
                longestlistNode = key
                longestlist = adjacencyDict[key]
        newCluster = []
        newCluster.append(longestlistNode)
        while(True):
            longestlist = adjacencyDict[longestlistNode]
            checkedall = True
            nextd = ""
            for key in longestlist:
                if (key not in newCluster):
                    checkedall = False
                    nextd = key
            if(checkedall):
                break
            if(nextd not in adjacencyDict.keys()):
                break
            nextlist = adjacencyDict[nextd]
            if (ComputeCohesion(longestlist, nextlist) >= gamma):#is part of the cluster (longestListsNode is its root)
                newCluster.append(nextd);
            else:
                try:
                    longestlist.remove(nextd)
                except:
                    pass
                adjacencyDict[longestlistNode] = longestlist
                try:
                    nextlist.remove(longestlistNode) #reflect the change in the nextDest's list too
                except:
                    pass
                adjacencyDict[nextd] = nextlist
        
        print("===== new cluster =====")
        print("root: " + newCluster[0])

        if(len(newCluster) > 1):#only write the non-trivial clusters to the file
            output.write(min(newCluster, key=len) + "\n")
            #for key in newCluster:
            #    output.write(key+",")
            #output.write("\n------------------------------------------------------------\n")

        for key in newCluster:
            adjacencyDict.pop(key)

        for key in adjacencyDict.keys():
            tempArray = adjacencyDict[key][:]
            for innerKey in newCluster:
                if(innerKey in tempArray):
                    tempArray.remove(innerKey)
            adjacencyDict[key] = tempArray

def createKey(left, right):
    res = left > right
    return KeyCreate(res,left,right)

def ComputeCohesion(leftList, rightList):
    intersectionSize = 0;
    for key in leftList:
        if(key in rightList):
            intersectionSize+= 1
    if(len(rightList) == 0):
        return 0
    return (1+intersectionSize)/len(rightList)

# for i in range(len(lamdaVals)):
#     lamda = lamdaVals[i]
#     for j in range(len(alphavalues)):
#         alpha = alphavalues[j];
#         for k in range(len(gammaValues)):
#             gamma = gammaValues[k]
#outputPath= "stems/stems_lambda="+str(lamda)+"_alpha="+str(alpha)+"_gamma="+str(gamma)+".txt"
outputPath = "gras_roots.txt"
output = open(outputPath,"w")
#chopKnownSuffixes()
ComputeFreqSuffixPairs()
FormClasses(output) 
output.close()
freq_suffix = []
for key in suffixPairDict:
    if (suffixPairDict[key] > 100):
        freq_suffix += key.split(':')
        # print (key, suffixPairDict[key])

freq_suffix = sorted(list(set(freq_suffix)))
open("gras_suffs.txt","w").write("\n".join(freq_suffix))
suffListFlag = True
for i in range(0):
 #   chopKnownSuffixes(freq_suffix,suffListFlag)
    output = open(outputPath,"w")
    ComputeFreqSuffixPairs()
    FormClasses(output)
    for key in suffixPairDict:
        if (suffixPairDict[key] > 10):
            freq_suffix += key.split(':')
    freq_suffix = sorted(list(set(freq_suffix)))
