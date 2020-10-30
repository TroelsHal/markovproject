from random import randrange
import random
import re


def GetLyrics(textfile):
    #Reads string from file
    #THIS WORKS WITH FLASK:
    #with app.open_resource(textfile) as f:
    #    lyricString = f.read().decode('utf8') 
    #    f.close
    #THIS WITHOUT FLASK:
    f = open(textfile, "r")
    print(f.read())
    f.close()

    #Transformste to lowercase, removes punctuation, and splits to list of strings
    cleanLyrics = (re.sub("[^a-zA-Z \n']", '', lyricString.lower())).split()
    return cleanLyrics

def MakeLyricDictionary(lyrics):
    lyricDict = {}
    for i in range (0, len(lyrics)-1):
        word = lyrics[i]
        nextWord = lyrics[i+1]
        
        if not (word in lyricDict):
            lyricDict[word] = [[nextWord, 1]]
        else:
            index = -1
            for j in range (0, len(lyricDict[word])):
                if lyricDict[word][j][0] == nextWord:
                    index = j
            if index == -1:
                lyricDict[word].append([nextWord, 1])
            else:
                lyricDict[word][index][1] += 1
    #print("Dictionary made. Number of distinct words : %d" % len (lyricDict))
    return lyricDict
    
def FindNextWord(presentWord, lyricDict):
    potentialNextWords = lyricDict[presentWord]
    totalProbability = 0
    for candidate in potentialNextWords:
        totalProbability += candidate[1]
    r = randrange(1, totalProbability+1)
    
    for candidate in potentialNextWords:
        r -= candidate[1]
        if r <= 0:
            return candidate[0]

def MakeSong(lyricDict):
    verseLines = randrange(2, 4) * 2
    verseLineLength = randrange(5, 8)
    verse1 = MakeText(lyricDict, verseLines, verseLineLength)
    verse2 = MakeText(lyricDict, verseLines, verseLineLength)
    verse3 = None
    #if the verses are short, we can have a 3. verse
    if verseLines <= 4:
        verse3 = MakeText(lyricDict, verseLines, verseLineLength)
    
    chorusLineLength = randrange(4, 7)
    chorus = MakeText(lyricDict, 3, chorusLineLength)

    #the title is the beginning of the 1. verse (1/3 chance) or the beginning of the chorus
    titleLength = randrange(2, 5)
    if randrange(0,3) == 0:
        title = verse1.split()
    else:
        title = chorus.split()
    title = ' '.join((title)[0:titleLength]).upper()    

    song = f"<h1>{title}</h1>" + f"<p>{verse1}<p>"
    if verse3:
        song = song + f"<p>{verse2}<p>" + f"<p><i>{chorus}</i><p>" + f"<p>{verse3}<p>" + f"<p><i>{chorus}</i><p>" 
    else:
        song = song + f"<p><i>{chorus}</i><p>" + f"<p>{verse2}<p>" + f"<p><i>{chorus}</i><p>" + f"<p><i>{chorus}</i><p>"
    return song  


def MakeText(lyricDict, lines, linelength):
    text=""
    for i in range (0, lines):
    #Choose first word in the chain
        line = ""
        chosenWord = random.choice(list(lyricDict.keys()))
        for j in range (0, linelength):
            line = line + chosenWord + " "
            chosenWord = FindNextWord(chosenWord, lyricDict)
        text = text + line + "<br>"
    return text

def getSong(albums):
    print("hello")
    lyrics = ""
    for album in albums:
        lyrics += GetLyrics(album)
    lyricDict = MakeLyricDictionary (lyrics)
    song = MakeSong(lyricDict)
    print(song)

def main():
    print("main")
    getSong("/ahard.txt")

if __name__ == "__main__":
    main()

