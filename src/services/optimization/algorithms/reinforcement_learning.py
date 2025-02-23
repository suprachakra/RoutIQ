"""
Contains RL-based models (e.g., DQN) for dynamic route adjustments.

This module provides an RLAgent class that:
- Builds a simple Deep Q-Network (DQN) using TensorFlow/Keras.
- Trains on provided state-action pairs to learn an optimal policy for route adjustments.
- Offers methods to predict actions and perform incremental training.

Assumptions:
- The environment provides states as numpy arrays.
- The action space is discrete (e.g., a set of possible route adjustments).
- This is a simplified DQN implementation for demonstration purposes.
"""

import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models, optimizers
from typing import Tuple

class RLAgent:
    def __init__(self, state_size: int, action_size: int, learning_rate: float = 0.001, gamma: float = 0.95):
        """
        Initialize the RLAgent with a simple DQN model.
        
        Args:
            state_size (int): Dimensionality of state space.
            action_size (int): Number of possible actions.
            learning_rate (float): Learning rate for the optimizer.
            gamma (float): Discount factor for future rewards.
        """
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.model = self._build_model()

    def _build_model(self) -> models.Model:
        """
        Build the DQN model.
        
        Returns:
            models.Model: Compiled Keras model.
        """
        model = models.Sequential()
        model.add(layers.Dense(64, input_dim=self.state_size, activation='relu'))
        model.add(layers.Dense(64, activation='relu'))
        model.add(layers.Dense(self.action_size, activation='linear'))
        model.compile(optimizer=optimizers.Adam(learning_rate=self.learning_rate), loss='mse')
        return model

    def act(self, state: np.ndarray) -> int:
        """
        Choose an action based on the current state.
        
        Args:
            state (np.ndarray): Current state.
        
        Returns:
            int: Selected action index.
        """
        state = np.reshape(state, [1, self.state_size])
        q_values = self.model.predict(state, verbose=0)
        return np.argmax(q_values[0])

    def train(self, state: np.ndarray, action: int, reward: float, next_state: np.ndarray, done: bool):
        """
        Train the model on a single experience tuple.
        
        Args:
            state (np.ndarray): Current state.
            action (int): Action taken.
            reward (float): Reward received.
            next_state (np.ndarray): Next state after the action.
            done (bool): Whether the episode is finished.
        """
        state = np.reshape(state, [1, self.state_size])
        next_state = np.reshape(next_state, [1, self.state_size])
        target = reward
        if not done:
            target += self.gamma * np.amax(self.model.predict(next_state, verbose=0)[0])
        target_f = self.model.predict(state, verbose=0)
        target_f[0][action] = target
        self.model.fit(state, target_f, epochs=1, verbose=0)

# Example usage:
if __name__ == "__main__":
    state_size = 10  # Example state dimension
    action_size = 4  # Example: 4 possible route adjustments
    agent = RLAgent(state_size, action_size)

    # Simulate a random state and perform a dummy training step.
    state = np.random.rand(state_size)
    action = agent.act(state)
    reward = 1.0  # Dummy reward
    next_state = np.random.rand(state_size)
    done = False
    agent.train(state, action, reward, next_state, done)

    print("Action taken:", action)
