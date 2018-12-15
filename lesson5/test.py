from gensim.models import word2vec

model = word2vec.Word2Vec.load('./word2vecModel/WikiCHModel')

# print(model.wv.similarity('奥运会','金牌')) #两个词的相关性

# print(model.wv.most_similar(['英国','上海'],['中国']))

print(model.most_similar('宝马', topn=10))

print(model.most_similar('腾讯', topn=10))
