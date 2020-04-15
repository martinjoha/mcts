import math
import random
from agent.node import *

class MCTS:
	def __init__(self, root, state_manager, exploration_constant):
		self.state_manager = state_manager
		self.root = root
		self.exploration_constant = exploration_constant

	def tree_policy(self, current_node):
		current_player = self.state_manager.get_player(current_node.state)
		return self.get_tree_policy_for_p1(current_node) if current_player == 'Player 1' else self.get_tree_policy_for_p2(current_node)

	def get_tree_policy_for_p1(self, current_node):
		score = lambda node: node.value + self.exploration_constant * math.sqrt(math.log(current_node.count)/(1 + node.count))
		node_scores = [score(child) for child in current_node.children]
		best_node_index = node_scores.index(max(node_scores))
		return current_node.children[best_node_index] 

	def get_tree_policy_for_p2(self, current_node): # same as for p1 but choose the lowest score instead of highest
		score = lambda node: node.value - self.exploration_constant * math.sqrt(math.log(current_node.count)/(1 + node.count))
		node_scores = [score(child) for child in current_node.children]
		best_node_index = node_scores.index(min(node_scores))
		return current_node.children[best_node_index] 

	def default_policy(self, current_node):
		random_child = random.choice(self.state_manager.get_children(current_node.state))
		return Node(random_child, current_node)

	def traverse_search_tree(self):
		current_node = self.root
		while current_node.children and not self.state_manager.is_final_state(current_node.state):
			current_node = self.tree_policy(current_node)
		return current_node

	def rollout(self, current_node):
		self.expand(current_node)
		while not self.state_manager.is_final_state(current_node.state):
			current_node = self.default_policy(current_node)
		return current_node

	def backpropagate(self, current_node, reward):
		current_node.count += 1 # final state node needs to add a count before starting the loop
		while current_node.parent:
			current_node.parent.count += 1
			current_node.value += (reward - current_node.value) / current_node.count
			current_node = current_node.parent

	def set_root(self, node): # for setting new root when simulation is finished and an actual move has been picked.
		self.root = node

	def simulate(self):
		leaf_node = self.traverse_search_tree()
		final_node = self.rollout(leaf_node)
		reward = self.state_manager.evaluate_state(final_node.state)
		self.backpropagate(final_node, reward)

	def choose_real_action(self, current_node):
		counts = [child.count for child in current_node.children]
		chosen_node_index = counts.index(max(counts))
		return current_node.children[chosen_node_index]
		
	def expand(self, current_node):
		children = self.state_manager.get_children(current_node.state)
		for child in children:
			child_node = Node(child, current_node)
			current_node.children.append(child_node)