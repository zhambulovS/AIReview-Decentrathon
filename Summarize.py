from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
import nltk

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

def getWordFreqTable(words):
    stop_words = set(stopwords.words("english"))
    stemmer = PorterStemmer()
    table = dict()

    for word in words:
        word = stemmer.stem(word.lower()) 
        if word in stop_words:
            continue

        if word in table:
            table[word] += 1
        else:
            table[word] = 1

    return table

def getSentenceScoreTable(sentences, wordFreqTable, character_depth=10):
    table = dict()

    for sentence in sentences:
        num_words = len(word_tokenize(sentence))
        if num_words == 0:  
            continue

        for word in wordFreqTable:
            if word in sentence.lower():
                if sentence[:character_depth] in table:
                    table[sentence[:character_depth]] += wordFreqTable[word]
                else:
                    table[sentence[:character_depth]] = wordFreqTable[word]

        table[sentence[:character_depth]] = table[sentence[:character_depth]] / num_words

    return table

def getAverageScore(sentenceScoreTable):
    if not sentenceScoreTable: 
        return 0

    sumValues = sum(sentenceScoreTable.values())
    avg = sumValues / len(sentenceScoreTable)

    return avg

def getSummary(sentences, sentenceScoreTable, threshold, character_depth=10):
    summary = ""

    for sentence in sentences:
        if sentence[:character_depth] in sentenceScoreTable and sentenceScoreTable[sentence[:character_depth]] > threshold:
            summary += sentence + " "

    return summary

def summarize(text, thresholdScale=1.1):
    if not text:  
        return "No text provided."

    words = word_tokenize(text)
    sentences = sent_tokenize(text)

    wordFreqTable = getWordFreqTable(words)
    sentenceScores = getSentenceScoreTable(sentences, wordFreqTable)
    avgScore = getAverageScore(sentenceScores)
    threshold = avgScore * thresholdScale

    summary = getSummary(sentences, sentenceScores, threshold)
    
    return summary
