from pattern_match import pattern_match

import random

rules = {
	'*X hello *Y': ['How do you do . Please state your problem .'],
	'*X I want *Y': ['What would it mean if you got *Y ?', 'Why do you want *Y ?', 'Suppose you got *Y soon .'],
	'*X if *Y': ['Do you really think its likely that *Y ?', 'Do you wish that *Y ?', 'What do you think about *Y ?', 'Really-- if *Y .'],
	'*X no *Y': ['Why not ?', 'You are being a bit negative .', 'Are you saying "NO" just to be negative ?'],
	'*X I was *Y': ['Were you really ?', 'Perhaps I already knew you were *Y', 'Why do you tell me you were *Y now ?'],
	'*X I feel *Y': ['Do you often feel *Y ?'],
	'*X I felt *Y': ['What other feelings do you have ?'],
}

notmatch_responses = [
	'I didn\'t get what you say .', 
	'Sorry ?', 
	'I cannot understand .',
]

words_to_sub = {
	'I': 'you',
	'you': 'I',
	'me': 'you',
	'am': 'are',
	'my': 'your',
	'your': 'my',
}

def choose_accurate_rule(rules):
	return random.choice(rules)

def flatten(l):
	r = []
	for i in l:
		if isinstance(i, list):
			r += flatten(i)
		else:
			r.append(i)
	return r

def switch_viewpoint(dic):
	for variable in dic:
		value = dic[variable]
		if isinstance(value, str):
			if value in words_to_sub:
				dic[variable] = words_to_sub[value]
		if isinstance(value, list):
			for i, each in enumerate(value):
				if each in words_to_sub:
					value[i] = words_to_sub[each]

def make_response(input):
	responses = {}
	for rule in rules:
		dic = pattern_match(rule.split(), input.split())
		if dic != None:
			switch_viewpoint(dic)
			response = random.choice(rules[rule])
			words = response.split()
			for i, word in enumerate(words):
				if word in dic:
					words[i] = dic[word]
			responses[rule] = ' '.join(flatten(words))
	return responses

def start_conversation(inputs):
	for input in inputs:
		print('You  : ', input)
		res = make_response(input)
		print('Eliza: ', end=' ')
		if res:
			chosen = choose_accurate_rule(list(res.keys()))
			print(res[chosen])
		else:
			print(random.choice(notmatch_responses))