# Implementation of Levenshtein edit distance algorithm

def editDistance(str1, str2):
    str1 = str1.lower()
    str2 = str2.lower()
    distTable = [[0]*(len(str1)+1) for i in range(len(str2)+1)]

    for i in range(0, len(str2)+1):
        for j in range(0, len(str1)+1):
            if i == 0:
                distTable[i][j] = j
            elif j == 0:
                distTable[i][j] = i
            elif str2[i-1] == str1[j-1]:
                distTable[i][j] = distTable[i-1][j-1]
            else:
                distTable[i][j] = 1+min(distTable[i-1][j],
                                        distTable[i][j-1], distTable[i-1][j-1])

    return distTable[len(str2)][len(str1)]
