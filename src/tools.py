def mutable(data):
	if type(data) != type(tuple()):
		return False
	return True

def make_immutable(data):
	new_data = []
	for i in data:
		new_data.append(tuple(i))
	new_data = tuple(new_data)
	return new_data

def make_mutable(data):
	new_data = []
	for i in data:
		new_data.append(list(i))
	new_data = list(new_data)
	return new_data

def valid_data(data):
	if type(data) != type(tuple()):
		return False
	for i in data:
		if type(i) != type(tuple()):
			return False
	return True

def correct_data(data):
	#Checks if data is mutable, if it is than make it immutable
	if mutable(data):
		data = make_immutable(data)
	#Checks if data structure is valid to add in model
	assert valid_data(data), 'Data structure invalid'
	return data

def correct_context(context):
	assert type(context) == type(dict()), "Context not a dictionary"
	for context_id in context:
		context_id = tuple(context[context_id])
	return context

def partial_ordered_match(a, b):
	matched = 0
	n = 0
	for aa, bb in zip(a,b):
		temp_matched = 0
		temp_n = 0
		for aaa, bbb in zip(aa, bb):
			if aaa == bbb:
				temp_matched += 1
			temp_n += 1
		matched += temp_matched/temp_n
		n += 1
	
	if n == 0:
		return 0
	else:
		return matched/n