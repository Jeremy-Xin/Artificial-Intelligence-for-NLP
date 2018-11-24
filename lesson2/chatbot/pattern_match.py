import re

def pattern_match(pattern, input):
	context = {}
	r = match_list(pattern, 0, input, 0, context)
	if r:
		return context
	return None

def is_variable(word):
	if not isinstance(word, str):
		return False
	pattern = r"^\?[a-zA-Z]+\w*$"
	r = re.match(pattern, word)
	return r != None

def is_scope_variable(word):
	if not isinstance(word, str):
		return False
	pattern = r"^\*[a-zA-Z]+\w*$"
	r = re.match(pattern, word)
	return r != None

def no_more(lst, index):
	return index > len(lst) - 1

def has_more(lst, index):
	return index <= len(lst) - 1

def match_list(p_list, p_index, i_list, i_index, context):
	if no_more(p_list, p_index) and no_more(i_list, i_index):
		return True

	if has_more(p_list, p_index) and has_more(i_list, i_index):
		pattern = p_list[p_index]
		if is_variable(pattern):
			return handle_variable(p_list, p_index, i_list, i_index, context)

		if is_scope_variable(pattern):
			return handle_scope_variable(p_list, p_index, i_list, i_index, context)

		return handle_word(p_list, p_index, i_list, i_index, context)

	if has_more(p_list, p_index) and no_more(i_list, i_index):
		pattern = p_list[p_index]
		if is_scope_variable(pattern):
			return handle_scope_variable(p_list, p_index, i_list, i_index, context)
		else:
			return False

	return False

def handle_word(p_list, p_index, i_list, i_index, context):
	if p_list[p_index] != i_list[i_index]:
		return False
	return match_list(p_list, p_index + 1, i_list, i_index + 1, context)


def handle_variable(p_list, p_index, i_list, i_index, context):
	variable = p_list[p_index]
	value = i_list[i_index]
	if variable in context and context[variable] != value:
		return False
	context[variable] = value
	return match_list(p_list, p_index + 1, i_list, i_index + 1, context)


def handle_scope_variable(p_list, p_index, i_list, i_index, context):
	variable = p_list[p_index]
	if variable in context:
		context_value = context[variable]
		for i, v in enumerate(context_value):
			if v != i_list[i_index + i]:
				return False
		return match_list(p_list, p_index + len(context_value), i_list, i_index + len(context_value), context)

	value = []
	for idx in range(i_index - 1, len(i_list)):
		# the first iteration is to match no-word for a scope variable
		if idx >= i_index:
			value.append(i_list[idx])
		new_context = dict(context)
		new_context[variable] = value
		result = match_list(p_list, p_index + 1, i_list, i_index + len(value), new_context)
		if result:
			context.update(new_context)
			return result
	return False

