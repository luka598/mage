from tools import correct_data, correct_context

class match():
	def __init__(self) -> None:
		self.matches = {1: []}
		return

	def add_match(self, match_p, data):
		assert match_p <= 1, 'match_p not a percentage, (match_p > 1)'
		try:
			self.matches[match_p].append(data)
		except KeyError:
			self.matches[match_p] = [data]
		return False

	def exact(self):
		if 1 > len(self.matches[1]):
			return None
		else:
			return self.matches[1][0]

	def max(self):
		return max(self.matches.keys())

class model():
	def __init__(self) -> None:
		self.model = {}

	def match_datapoint(self, data, return_first = True):
		data = correct_data(data)

		matches = match()
		if data in self.model.keys():
			matches.add_match(1, data)
			if return_first:
				return matches

	def rank_dp(self):
		assert False, "Not implemented"

	def add(self, data):
		data = correct_data(data)
		assert self.match_datapoint(data) is not None, "That data alredy exsists"
		self.model[data] = datapoint(data)
		return

	def update(self, data, next_data, context):
		data = correct_data(data)
		assert self.match_datapoint(data) is None, "That data does not exsists"
		self.model[data].update(next_data, context)
		return


class datapoint():
	def __init__(self, data) -> None:
		self.data = correct_data(data)
		self.next_dps = {}
		self.count = 0
		return

	def match_next_dp(self, data, return_first=True):
		matches = match()
		if data in self.next_dps.keys():
			matches.add_match(1, data)
			if return_first:
				return matches
		return matches

	def rank_next_dp(self, context):
		assert False, "Not implemented"
		return

	def update(self, next_data, context):
		next_data = correct_data(next_data)
		if self.match_next_dp(next_data) is None:
			self.next_dps[next_data] = next_datapoint(next_data)
		self.next_dps[next_data].update(context)
		return

class next_datapoint():
	def __init__(self, data) -> None:
		self.data = correct_data(data)
		self.context = {}
		self.count = 0

	def match(self):
		assert False, "Not implemented"

	def match_contexts(self):
		assert False, "Not implemented"

	def update(self, context):
		context = correct_context(context)
		for context_id in context:
			if context_id in self.context:
				self.context[context_id].update(context)
			else:
				self.context[context_id] = context_datapoint(context_id, context)

class context_datapoint():
	def __init__(self, id, context) -> None:
		self.id = id
		self.data = [tuple(context[id])]
		self.count = 0
		return

	def match_contexts(self, context):
		match = match()
		if context[self.id] in self.data:
			match.add_match(1, context[self.id])
		return match

	def update(self, context):
		context = correct_context(context)
		if context[self.id] not in self.data:
			self.data.append(context[self.id])
		return