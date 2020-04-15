class StateManager:

	def get_children(self, node):
		return node.get_children()

	def get_player(self, node):
		return node.get_player()

	def evaluate_state(self, node):
		if not node.is_final_state():
			return
		return 1 if node.prev_player == 'Player 1' else -1

	def is_final_state(self, node):
		return node.is_final_state()

	