from data import model

mm = model()
data = [i for i in range(0,10)]

for i in data:
	_data = ((i,),)
	_next = ((i+1,),)
	_context = {"back": (i-1,)}
	mm.add(_data)
	mm.update(_data, _next, _context)

print(data)
print(mm)