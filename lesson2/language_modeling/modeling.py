from collections import Counter
from functools import reduce
from collections import defaultdict
from operator import mul

from preprocess import process

THRESHOLD = 10
TOTAL_WORDS = 400000

def compute_N(counter):
    result = defaultdict(int)
    for each in counter:
        key = counter[each]
        result[key] += 1
    return result

def read_corpus(file_name):
    total = []
    f = open(file_name)
    for line in f.readlines():
        wordlist = eval(line)
        total += wordlist
    f.close()
    return total

def get_bigrams(words):
    dic = defaultdict(int)
    for idx, word in enumerate(words):
        if idx < len(words) - 1:
            word_tuple = word, words[idx + 1]
            dic[word_tuple] += 1
    return dic

words = read_corpus('zh_words')
unigram_counter = Counter(words)
bigram_counter = Counter(get_bigrams(words))
all_word_count = len(words)
N_unigram = compute_N(unigram_counter)
N_bigram = compute_N(bigram_counter)
all_bigram_count = sum(bigram_counter.values())

def word_occurences(word):
    occur = unigram_counter[word]
    if occur >= THRESHOLD:
        return occur
    
    # Good Turing Estimation
    if occur == 0:
        return N_unigram[1] / TOTAL_WORDS

    #  occur < THRESHOLD
    N_r = N_unigram[occur]
    N_r1 = N_unigram[occur + 1]
    return (occur + 1) * N_r1/N_r

def get_prob_from_counter(counter):
    all_occurences = sum(counter.values())
    def get_prob(word):
        return word_occurences(word) / all_occurences
    return get_prob

word_prob = get_prob_from_counter(unigram_counter)

def prob_of_string_unigram(word_list):
    product = 1
    for word in word_list:
        pro = word_prob(word)
        product *= pro
        print('{}:{}'.format(word, pro))
    return product
    # return reduce(mul, [get_word_prob(word) for word in word_list])

def bigram_prob(bigram):
    occur = bigram_counter[bigram]
    if occur >= THRESHOLD:
        return occur / all_bigram_count

    if occur == 0:
        return smooth_bigram(bigram)

    # occur < THRESHOLD
    N_r = N_bigram[occur]
    N_r1 = N_bigram[occur + 1]
    occur = (occur + 1) * N_r1/N_r
    return occur / all_bigram_count

def smooth_bigram(bigram):
    first, second = bigram
    seen_prob = 0
    seen_words = []
    for word_tuple in bigram_counter:
        if word_tuple[0] == first:
            seen_prob += bigram_prob(word_tuple)
            seen_words.append(word_tuple[1])

    unseen_occur = 0
    for word in unigram_counter:
        if word not in seen_words:
            unseen_occur += word_prob(word)
    unseen_occur += N_unigram[0]

    return (1 - seen_prob) * (word_prob(second)/unseen_occur)

def prob_of_string_bigram(word_list):
    product = 1
    for i, word in enumerate(word_list):
        if i == 0:
            pro = word_prob(word)
            product *= pro
            print('{}:{}'.format(word, pro))
        else:
            prev = word_list[i - 1]
            pro = bigram_prob((prev, word))
            product *= pro
            print('{},{}:{}'.format(prev, word, pro))
    return product

strings = ['这是一个比较常见的测试用例', '这是一个非常罕见的测试用例','今天中午我吃了晚饭','今天中午我吃了中饭', '下周一中午同事请客吃饭']
for string in strings:
    words = process(string)
    print('{} : {}'.format(string, prob_of_string_bigram(words)))