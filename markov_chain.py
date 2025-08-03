import numpy as np
class MarkovChain:
    def __init__(self, transition_matrix):
        """
        Initialize the Markov Chain with a transition matrix.
        :param transition_matrix: A square numpy array representing the transition probabilities.
        """
        self.transition_matrix = np.array(transition_matrix)
        self.state_count = self.transition_matrix.shape[0]
    
    def next_state(self, current_state):
        """
        Get the next state given the current state.
        :param current_state: The current state (integer index).
        :return: The next state (integer index).
        """
        return np.random.choice(self.state_count, p=self.transition_matrix[current_state])
    
    def generate_sequence(self, start_state, length):
        """
        Generate a sequence of states starting from a given state.
        :param start_state: The initial state (integer index).
        :param length: The length of the sequence to generate.
        :return: A list of states representing the generated sequence.
        """
        sequence = [start_state]
        for _ in range(length - 1):
            next_state = self.next_state(sequence[-1])
            sequence.append(next_state)
        return sequence

p = np.array([[0.3, 0.7], [0.2, 0.8]])
mc = MarkovChain(p)
start = 0  # Starting from state 0
sequence_length = 10
sequence = mc.generate_sequence(start, sequence_length)
print("Generated sequence:", sequence)
