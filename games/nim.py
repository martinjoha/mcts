class Nim:
	def __init__(self, N, K, player, prev_N=None):
		self.N = N
		self.K = K
		self.player = player
		self.prev_player = 'Player 2' if player == 'Player 1' else 'Player 1'
		self.prev_N = prev_N

	def get_children(self):
		children = []
		for i in range(1, self.K + 1):
			if i > self.N:
				break
			children.append(Nim(self.N-i, self.K, self.prev_player, self.N))
		return children

	def get_player(self):
		return self.player

	def is_final_state(self):
		return self.N == 0

	def print_verbose(self):
		if not self.prev_N:
			print(f'Start pile: {self.N} stones, {self.player} begins')
		elif self.is_final_state():
			print(f'{self.prev_player} wins')
		else:
			print(f'{self.prev_player} selects {self.prev_N - self.N} stone(s): Remaining stones = {self.N}')

	def __repr__(self):
		return f'N = {self.N}, K = {self.K}, {self.player}\'s turn'