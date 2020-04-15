import copy

class Ledge:
	def __init__(self, board, player, prev_board=None):
		assert board.count(2) <= 1, 'The board can only contain one gold coin'
		self.board = board
		self.player = player
		self.prev_player = 'Player 2' if player == 'Player 1' else 'Player 1'
		self.prev_board = prev_board

	def get_children(self):
		children = []
		if self.board[0] != 0:
			new_board = copy.deepcopy(self.board)
			new_board[0] = 0
			children.append(Ledge(new_board, self.prev_player, self.board))
		for i in range(1,len(self.board)):
			if self.board[i] == 0:
				continue
			for j in range(i - 1, -1, -1):
				if self.board[j] != 0:
					break
				new_board = copy.deepcopy(self.board)
				new_board[i], new_board[j] = new_board[j], new_board[i]
				children.append(Ledge(new_board, self.prev_player, self.board))
		return children

	def is_final_state(self):
		return self.board.count(2) == 0

	def get_player(self):
		return self.player

	def print_verbose(self):
		if not self.prev_board:
			print(f'Start board: {str(self.board)}, {self.player} starts')
			return 

		changed_cell1, changed_cell2 = -1, -1
		for i in range(len(self.board)):
			if self.board[i] != self.prev_board[i]:
				changed_cell1 = i
				for j in range(i + 1, len(self.board)):
					if self.board[j] != self.prev_board[j]:
						changed_cell2 = j
						break
				break
		
		if changed_cell1 == 0 and self.prev_board[0] != 0:
			cell_value = self.encode_cell_value(self.prev_board[0])
			print(f'{self.prev_player} picks up {cell_value}: {str(self.board)}')
			if self.is_final_state():
				print(f'{self.prev_player} wins.')
		else:
			cell_value = self.encode_cell_value(self.board[changed_cell1])
			print(f'{self.prev_player} moves {cell_value} from cell {changed_cell2} to {changed_cell1}: {str(self.board)}') 

	def encode_cell_value(self, value):
		if value == 1:
			return 'copper'
		else:
			return 'gold'

	def __repr__(self):
		return str(self.board)