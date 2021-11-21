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