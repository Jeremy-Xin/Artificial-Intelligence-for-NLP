import random

def adj():
    return random.choice('漂亮 | 蓝色 | 好看'.split('|'))

def noun():
    return random.choice('猫 | 女人 | 男人'.split('|'))

def verb():
    return random.choice('看着 | 坐着 '.split('|'))

def noun2():
    return random.choice('桌子 | 皮球'.split('|'))

def sentence():
    return ''.join([adj(), noun(), verb(), noun2()])

print(sentence())