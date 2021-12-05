#pyright: reportGeneralTypeIssues=false
from tools import correct_data, correct_context, make_mutable, partial_ordered_match
from copy import deepcopy, copy

class match():
	def __init__(self) -> None:
		self.matches = {0:[]}
		return

	def add_match(self, match_p, data):
		assert match_p <= 1, 'match_p not a percentage, (match_p > 1)'
		try:
			self.matches[match_p].append(data)
		except KeyError:
			self.matches[match_p] = [data]
		return False

	def exact(self):
		if 1 in self.matches.keys():
			if 1 > len(self.matches[1]):
				return None
			else:
				return self.matches[1][0]
		else:
			return None

	def max(self):
		return max(self.matches.keys())

	def positive(self):
		matches = deepcopy(self.matches)
		return matches.remove(0)


	def __str__(self):
		return str(self.matches)

	def __repr__(self) -> str:
	    return self.__str__()

class model():
	def __init__(self) -> None:
		self.model = {}

	def _exact_match(self, data, return_first=True):
		matches = match()
		if data in self.model.keys():
			matches.add_match(1, data)
			if return_first:
				return matches
		return matches

	def _partial_match(self, data):
		matches = match()
		for key in self.model.keys():
			match_p = partial_ordered_match(key, data)
			matches.add_match(match_p, key)
		return matches

	def match_datapoint(self, data, first=False, partial=False):
		data = correct_data(data)
		matches = match()
		if first:
			matches = self._exact_match(data)
		if partial:
			matches = self._partial_match(data)
		return matches

	def rank_dp(self, matches):
		assert False, "Not implemented"

	def add(self, data):
		data = correct_data(data)
		assert self.match_datapoint(data, first=True).exact() is None, f"Can't add {data}, that data alredy exsists"
		self.model[data] = datapoint(data)
		return

	def update(self, data, next_data, context):
		data = correct_data(data)
		assert self.match_datapoint(data, first=True).exact() is not None, "That data does not exsists"
		self.model[data].update(next_data, context)
		return

	def json(self):
		json = '{'
		for key in self.model:
			json += f'"{str(key)}":{self.model[key].json()},'
		json = json[:-1]
		json += '}'

		return json

	def __str__(self):
		return self.json()


class datapoint():
	def __init__(self, data) -> None:
		self.data = correct_data(data)
		self.next_dps = {}
		self.count = 0
		return

	def _exact_match(self, context):
		matches = match()
		for next_dp in self.next_dps:
			match_p = self.next_dps[next_dp].match_contexts(context, exact=True)
			matches.add_match(match_p, next_dp)
		return matches

	def match_next_dp(self, context, exact=False, partial=False):
		matches = match()
		if exact:
			matches = self._exact_match(context)
		return matches

	def rank_next_dp(self, context):
		assert False, "Not implemented"
		return

	def update(self, next_data, context):
		next_data = correct_data(next_data)
		if self.match_next_dp(next_data).exact() is None:
			self.next_dps[next_data] = next_datapoint(next_data)
		self.next_dps[next_data].update(context)
		return

	def json(self):
		next_dps = '{'
		for key in self.next_dps:
			next_dps += f'"{str(key)}":{self.next_dps[key].json()},'
		next_dps = next_dps[:-1]
		next_dps += '}'
		return f'{{"data":{str(make_mutable(self.data))},"next_dps":{next_dps},"count":{self.count}}}'

	def __str__(self):
		return self.json()

	def __repr__(self):
		return self.__str__()

class next_datapoint():
	def __init__(self, data) -> None:
		self.data = correct_data(data)
		self.context = {}
		self.count = 0

	def match(self):
		assert False, "Not implemented"

	def match_contexts(self, context, exact):
		matches = 0
		n = 0
		for context_id in self.context:
			matches += self.context[context_id].match(context, exact=exact).max()
			n += 1
		if n == 0:
			return 0
		else:
			return matches/n

	def update(self, context):
		context = correct_context(context)
		for context_id in context:
			if context_id in self.context:
				self.context[context_id].update(context)
			else:
				self.context[context_id] = context_datapoint(context_id, context)

	def json(self):
		context = '{'
		for key in self.context:
			context += f'"{str(key)}":{self.context[key].json()},'
		context = context[:-1]
		context += '}'
		json = f'{{"data":{str(make_mutable(self.data))},"context":{context},"count":{self.count}}}'
		return json

	def __str__(self):
		return self.json()

	def __repr__(self):
		return self.__str__()

class context_datapoint():
	def __init__(self, id, context) -> None:
		self.id = id
		self.data = [tuple(context[id])]
		self.count = 0
		return

	def _exact_match(self, context):
		matches = match()
		if context[self.id] in self.data:
			matches.add_match(1, context[self.id])
		return matches

	def match(self, context, exact=False, partial=False):
		matches = match()
		if exact:
			matches = self._exact_match(context)
		return matches

	def update(self, context):
		context = correct_context(context)
		if context[self.id] not in self.data:
			self.data.append(context[self.id])
		return

	def json(self):
		data = '['
		for dp in self.data:
			data += f'"{str(dp)}",'
		data = data[:-1]
		data += ']'
		json = f'{{"id":"{str(self.id)}","data":{data},"count":{self.count}}}'
		return json

	def __str__(self):
		return self.json()

	def __repr__(self):
		return self.__str__()