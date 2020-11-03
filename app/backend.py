from random import randrange
import random
import re
from app import app
from flask import url_for


def GetLyrics(textfile):
    with app.open_resource("static/text/" + textfile + ".txt") as f:
        lyricString = f.read().decode('utf8') 
        f.close
    
    #Transformste to lowercase, removes punctuation, and splits to list of strings
    cleanLyrics = (re.sub("[^a-zA-Z \n']", '', lyricString.lower())).split()
    #Capitalize "I", "I'm", "I've" etc.
    for i in range (0, len(cleanLyrics)-1):
        if (cleanLyrics[i] == "i" or cleanLyrics[i][0:2] == "i'"):
            cleanLyrics[i] = "I" + cleanLyrics[i][1:]
        
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
    verseLines = randrange(2, 4)
    verseLineLength = randrange(5, 8) * 2
    verse1 = MakeText(lyricDict, verseLines, verseLineLength, "verse")
    verse2 = MakeText(lyricDict, verseLines, verseLineLength, "verse")
    verse3 = None
    #if the verses are short, then we can have a 3. verse
    if verseLines == 2:
        verse3 = MakeText(lyricDict, verseLines, verseLineLength, "verse")
    
    chorusLineLength = randrange(4, 7)
    chorus = MakeText(lyricDict, 3, chorusLineLength, "chorus")

    #the title is either the beginning of the 1. verse (1/3 chance) or the beginning of the chorus (2/3 chance)
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

def MakeText(lyricDict, lines, linelength, part):
    text=""
    for i in range (0, lines):
        line = ""
        chosenWord = random.choice(list(lyricDict.keys()))
        for j in range (0, linelength):           
            line += chosenWord
            if (j == 0):
                line = line.capitalize()
            line += "<br>" if (j == (linelength / 2) - 1 and part=="verse") else " "
            chosenWord = FindNextWord(chosenWord, lyricDict)
        text += line + "<br>"
    return text

def getSong(albums):
    lyrics = []
    for album in albums:
        lyrics = lyrics + GetLyrics(album)
    lyricDict = MakeLyricDictionary (lyrics)
    song = MakeSong(lyricDict)
    return song

