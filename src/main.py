from data import model

mm = model()
data = [i for i in range(0,10)]

for i in data:
	_data = ((i,),)
	_next = ((i+1,),)
	_context = {"back": (i-1,)}
	mm.add(_data)
	mm.update(_data, _next, _context)

#print(data)
#print(mm)

#data = ((1,),)
#x = mm.match_datapoint(data, partial=True).exact()
x = mm.model[((2,),)].match_next_dp({"back": (1,)}, exact=True)
print(x)