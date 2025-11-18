def queue():
	q = []
	def enqueue(v):
		q.append(v)
		
	def dequeue():
		if len(q) == 0:
			return None
		return q.pop(0)
	
	def size():
		return len(q)
		
	def is_not_empty():
		return len(q) > 0
		
	return { 
		'enqueue': enqueue, 
		'dequeue': dequeue, 
		'size': size, 
		'is_not_empty': is_not_empty
	}
		