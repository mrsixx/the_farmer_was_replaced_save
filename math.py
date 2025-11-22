def point(x,y):
	return {'X': x, 'Y': y }
	
def round_positive(x):
	return (x // 1) + (x % 1 != 0)

def sqrt(x):
	return x ** 0.5