class Node:
	def __init__(self, state, parent=None):
		self.parent = parent
		self.state = state
		self.children = []
		self.value = 0
		self.count = 0

	def __repr__(self):
		return str(self.state)
