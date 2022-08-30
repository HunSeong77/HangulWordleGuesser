import math

#define
EXACT = 'O'
MATCH = 'V'
MISS = 'X'

def safe_log(x):
    if x <= 0:
        return 0
    else:
        return math.log2(x)

def getWordList():
    # wordlist.txt의 모든 word를 가져와 list로 반환함
    ret = []
    with open(".\constants\wordlist.txt", "r", encoding="utf8") as fp:
        for line in fp.readlines():
            ret.append(line[:5])
    return ret

def inputResult(Print = True):
    if Print:
        print("결과를 입력하세요. (초록색 : O, 노란색 : V, 회색 : X), 띄어쓰기 없음.")
    result = list(input())
    return result

def compare(word : str, key: str):
    # word와 key를 비교한 결과를 list로 리턴
    result = [MISS, MISS, MISS, MISS, MISS]
    word = list(word)
    key = list(key)
    # EXACT 검사
    for idx in range(5) :
        if word[idx] == key[idx] :
            word[idx] = 'O'
            key[idx] = 'O'
            result[idx] = EXACT
    
    #MATCH 검사
    for word_idx in range(5):
        if word[word_idx] == 'O' : continue
        for key_idx in range(5):
            if word[word_idx] == key[key_idx] :
                word[word_idx] = 'V'
                key[key_idx] = 'V'
                result[word_idx] = MATCH
                break
    
    return result

def getInformationOfWord(word, wordlist = getWordList()):
    # 해당 word가 갖고 있는 정보의 기대치를 리턴함
    probs = dict()
    tot = len(wordlist)
    ret = 0
    for key in wordlist:
        result = tuple(compare(word, key))
        if result in probs:
            probs[result] += 1
        else:
            probs[result] = 1
    for val in probs.values():
        p = val / tot
        ret += p * safe_log(1/p)
    return round(ret, 9)

def extractKeys(word, result, wordlist = getWordList()):
    # word와 비교했을 때 같은 result를 갖는 key들을 추출함
    ret = list()
    cnt = 0
    tot = len(wordlist)
    for key in wordlist:
        if result == compare(word, key):
            ret.append(key)
        cnt+=1
        print("\r가능한 단어 목록 추출중...({0}/{1})".format(cnt, tot), end ='')
    print("\n가능한 단어 총 {0}개".format(len(ret)))
    return ret

def getHighestInformationWord(wordlist):
    # 높은 정보를 갖는 단어를 추출함
    infos = dict()
    totList = getWordList()
    cnt = 0
    tot = len(totList)
    if(len(wordlist) <= 2) : return wordlist[0]
    for word in totList:
        info = getInformationOfWord(word, wordlist)
        infos[word] = info
        cnt += 1
        print("\r정보 계산중...({0}/{1})".format(cnt, tot), end = '')
    print()
    ret = sorted(infos.items(), key = lambda item: item[1], reverse=True)
    return ret[0][0]

def BEST_GUESS() :
    RUN = True
    cnt = 0
    wordlist = list()
    while RUN :
        if cnt == 0 :
            cnt = 1
            wordlist = getWordList()
            word = getBestStartingWord()
            print("\n추천 단어 :", word)

        elif cnt == 1 :
            cnt = 2
            result = inputResult()
            wordlist = extractKeys(word, result, wordlist)
            word = getBestSecondWord(result)
            print("\n추천 단어 :", word)

        else:
            cnt += 1
            result = inputResult()
            if result == [EXACT, EXACT, EXACT, EXACT, EXACT] :
                RUN = False
                break
            wordlist = extractKeys(word, result, wordlist)
            word = getHighestInformationWord(wordlist)
            print("\n추천 단어 :", word)
    print("\n프로그램을 종료합니다.")

def getFirstInformation() :
    wordlist = getWordList()
    infos = dict()
    cnt = 0
    tot = len(wordlist)
    for word in wordlist :
        infos[word] = getInformationOfWord(word)
        cnt += 1
        print("\rCalculating Informations...({0}/{1})".format(cnt, tot), end = '')
    print("\nSorting Datas...")
    sorted_infos = sorted(infos.items(), key = lambda x : x[1], reverse=True)
    with open("./constants/BestStartingWord.txt", "w", encoding = "utf8") as fp:
        cnt = 0
        for line in sorted_infos :
            fp.write(str(line))
            fp.write("\n")
            cnt += 1
            print("\rWriting informations...({0}/{1})".format(cnt, tot), end = '')

def getSecondInformationWithTheBestFirstWord() :
    bestStartingWord = getBestStartingWord
    secondInfo = dict()
    wordlist = getWordList()
    cnt = 0
    for word in wordlist:
        result = tuple(compare(bestStartingWord, word))
        if result not in secondInfo:
            extractedList = extractKeys(bestStartingWord, list(result), wordlist)
            secondInfo[result] = getHighestInformationWord(extractedList)
            cnt += 1
            print("{0}/{1}.... {2} percent".format(cnt, 243, round(cnt/243*100, 3)))
    with open("./constants/BestSecondWord.txt", "w", encoding="utf8") as fp:
        for infos in secondInfo:
            fp.write(str(infos))
            fp.write(str(secondInfo[infos]))
            fp.write("\n")

def getBestStartingWord():
    with open("./constants/BestStartingWord.txt", "r", encoding="utf8") as fp:
        bestStartingWord = fp.readline().split("'")[1]
    return bestStartingWord

def getBestSecondWord(result : list) :
    result = str(result).replace("[", '(').replace("]", ")") 
    with open("./constants/BestSecondWord.txt", "r", encoding="utf8") as fp:
        lines = fp.read().split("\n")
    for line in lines:
        resultAndWord = line.split(':')
        if(resultAndWord[0] == result) :
            bestSecondWord = resultAndWord[1]
            return bestSecondWord
    return "Error"
