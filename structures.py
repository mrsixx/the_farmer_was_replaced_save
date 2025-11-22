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
		
	def empty():
		return len(q) == 0
		
	return { 
		'enqueue': enqueue, 
		'dequeue': dequeue, 
		'size': size, 
		'empty': empty
	}


def priority_queue():
	q = []

	def _put(priority, item):
		q.append((priority, item))
		_sift_up(len(q) - 1)

	def _pop():
		if len(q) == 0:
			return None
		_swap(0, len(q) - 1)
		priority, item = q.pop(0)
		if len(q) > 0:
			_sift_down(0)
		return item

	def _empty():
		return len(q) == 0

	def _sift_up(index):
		parent = (index - 1) // 2
		if index > 0 and q[index][0] < q[parent][0]:
			_swap(index, parent)
			_sift_up(parent)
	def _sift_down(index):
		n = len(q)
		while True:
			smallest = index
			left = 2 * index + 1
			right = 2 * index + 2
			if left < n and q[left][0] < q[smallest][0]:
				smallest = left
			if right < n and q[right][0] < q[smallest][0]:
				smallest = right

			if smallest == index:
				break
			_swap(index, smallest)
			index = smallest

	def _swap(i, j):
		q[i], q[j] = q[j], q[i]
		
	return {
		'put': _put,
		'pop': _pop,
		'empty': _empty
	}