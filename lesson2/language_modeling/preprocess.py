import jieba

def filter_word(word):
    return word in word_to_filter or word in stopwords

def read_stopwords(filename):
    f = open(filename)
    for word in f.readlines():
        stopwords.append(word[:-1])
    f.close()

def process(sentence):
    out = []
    words = jieba.cut(sentence)
    for word in words:
        if not filter_word(word):
            out.append(word)
    return out

word_to_filter = ' \n（）《》〈〉「」"\'()/?-,.·:;—'
stopword_file = 'stopwords.txt'
stopwords = []
read_stopwords(stopword_file)