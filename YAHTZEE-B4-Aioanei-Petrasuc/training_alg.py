import random
import numpy as np
from itertools import product

class YahtzeeTraining:
    def __init__(self, num_dice=5, sides=6, alpha=0.1, gamma=0.9, epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.995):
        """Inițializează parametrii pentru antrenarea Q-learning."""

        self.num_dice = num_dice
        self.sides = sides
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.q_table = {}  
        self.initialize_all_states()

    def initialize_all_states(self):
        """Inițializează toate stările posibile în tabelul Q. """

        for state in product(range(self.num_dice + 1), repeat=self.sides):
            if sum(state) == self.num_dice:
                self.q_table[state] = [0] * 13

    def initialize_state(self, dice_roll):
        """ Creează o stare pe baza aruncării zarurilor. """

        state = tuple(dice_roll.count(i) for i in range(1, self.sides + 1))
        return state

    def choose_action(self, state):
        """ Alege o acțiune bazată pe politica epsilon-greedy.
        - Dacă probabilitatea este mai mică decât epsilon, explorează (alege random).
        - Altfel, exploatează (alege acțiunea cu cea mai mare valoare Q).
        """
        if random.uniform(0, 1) < self.epsilon:
            return random.randint(0, len(self.q_table[state]) - 1)
        else:
            return np.argmax(self.q_table[state])

    def choose_next_action(self, state, last_games):
        """ Alege următoarea acțiune, evitând acțiunile deja selectate (`last_games`)."""

        if random.uniform(0, 1) < self.epsilon:
            available_actions = [i for i in range(len(self.q_table[state])) if i not in last_games]
            return random.choice(available_actions)
        else:
            available_actions = [i for i in range(len(self.q_table[state])) if i not in last_games]
            q_values_for_available_actions = [self.q_table[state][i] for i in available_actions]
            best_action = available_actions[np.argmax(q_values_for_available_actions)]
            return best_action

    def update_q_table(self, state, action, reward, next_state):
        """Actualizează valoarea Q pentru o stare și o acțiune dată folosind formula de actualizare Q-learning."""

        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward + self.gamma * self.q_table[next_state][best_next_action]
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] = reward

    def simulate_roll(self):
        """ Simulează o aruncare de zaruri. Există o probabilitate de 20% să obțină toate zarurile egale."""

        if random.randint(1, 100) <= 20:
            value = random.randint(1, self.sides)
            return [value] * self.num_dice
        else:
            return [random.randint(1, self.sides) for _ in range(self.num_dice)]

    def train(self, episodes):
        """Rulează antrenamentul pe un număr specificat de episoade. """

        for episode in range(episodes):
            dice_roll = self.simulate_roll()
            state = self.initialize_state(dice_roll)
            action = self.choose_action(state)
            next_state = self.initialize_state(dice_roll)
            reward = self.calculate_reward(action, dice_roll)
            self.update_q_table(state, action, reward, next_state)

            state = next_state
            if self.epsilon > self.epsilon_min:
                self.epsilon *= self.epsilon_decay

    def calculate_reward(self, action, dice_roll):
        """Calculează recompensa pentru o acțiune specifică pe baza zarurilor aruncate."""

        counts = [dice_roll.count(i) for i in range(1, self.sides + 1)]
        reward = 0

        max_rewards = {
            0: 5 * 1,  # Ones
            1: 5 * 2,  # Twos
            2: 5 * 3,  # Threes
            3: 5 * 4,  # Fours
            4: 5 * 5,  # Fives
            5: 5 * 6,  # Sixes
            6: 6 * 3,  # Three-of-a-kind
            7: 6 * 4,  # Four-of-a-kind
            8: 20,  # Full House
            9: 25,  # Small Straight
            10: 35,  # Large Straight
            11: 42,  # Chance
            12: 40  # Yahtzee
        }

        if action == 0:  # Ones
            reward = counts[0] * 1
        elif action == 1:  # Twos
            reward = counts[1] * 2
        elif action == 2:  # Threes
            reward = counts[2] * 3
        elif action == 3:  # Fours
            reward = counts[3] * 4
        elif action == 4:  # Fives
            reward = counts[4] * 5
        elif action == 5:  # Sixes
            reward = counts[5] * 6
        elif action == 6:  # Three-of-a-kind
            if any(count >= 3 for count in counts):
                for value, count in enumerate(counts, start=1):
                    if count >= 3:
                        reward = value * 3
                        break
        elif action == 7:  # Four-of-a-kind
            if any(count >= 4 for count in counts):
                for value, count in enumerate(counts, start=1):
                    if count >= 4:
                        reward = value * 4
                        break
        elif action == 8:  # Full House
            if sorted(counts) == [0, 0, 0, 0, 2, 3]:
                reward = 25
        elif action == 9:  # Small Straight
            small_straights = [[1, 1, 1, 1, 0, 0], [0, 1, 1, 1, 1, 0], [0, 0, 1, 1, 1, 1]]
            if any(counts == s for s in small_straights):
                reward = 30
        elif action == 10:  # Large Straight
            large_straights = [[1, 1, 1, 1, 1, 0], [0, 1, 1, 1, 1, 1]]
            if any(counts == s for s in large_straights):
                reward = 40
        elif action == 11:  # Chance
            reward = sum(dice_roll)
        elif action == 12:  # Yahtzee
            if any(count == 5 for count in counts):
                reward = 50

        max_reward = max_rewards[action]
        normalized_reward = (reward / max_reward) * 100

        return normalized_reward


if __name__ == "__main__":
    yahtzee_trainer = YahtzeeTraining()
    yahtzee_trainer.train(episodes=900000)

    for state, actions in list(yahtzee_trainer.q_table.items())[:]:
        print(f"State: {state}, Actions: {actions}")
