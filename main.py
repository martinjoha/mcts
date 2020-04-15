from games.nim import Nim
from games.ledge import Ledge
from agent.mcts import MCTS
from agent.node import *
from agent.state_manager import *
from config import *
import random

def main():
	state_manager = StateManager()
	wins = {
		'Player 1': 0,
		'Player 2': 0
	}

	for _ in range(mcts_config['G']):
		game = init_game()
		current_node = Node(game)
		agent = MCTS(current_node, state_manager, mcts_config['C'])
		while not state_manager.is_final_state(current_node.state):
			if game_config['verbose']:
				current_node.state.print_verbose()
			for _ in range(mcts_config['M']):
				agent.simulate()
			current_node = agent.choose_real_action(current_node)
			agent.set_root(current_node)
		current_node.state.print_verbose()
		wins[current_node.state.prev_player] += 1
		
	print(f'Player 1 wins {wins["Player 1"]} of {mcts_config["G"]} games ({wins["Player 1"]/mcts_config["G"]*100}%)')

def init_game():
	if game_config['game_type'] == 'nim':
		return Nim(nim_config['N'], nim_config['K'], init_player())
	else:
		return Ledge(ledge_config['board'], init_player())

def init_player():
	if game_config['P'] == 1:
		return 'Player 1'
	elif game_config['P'] == 2:
		return 'Player 2'
	else:
		return random.choice(['Player 1', 'Player 2'])

if __name__ == '__main__':
	main()