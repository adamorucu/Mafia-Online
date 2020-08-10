import numpy as np
import math

class Room:
    def __init__(self, room_id):
        self.id = room_id
        self.players = []

    def add_player(self, player):
        if player not in self.players:
            self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)

    def assign_roles(self):
        room_size = len(self.players)
        roles = []
        roles += ['Mafia'] * room_size // 3
        roles += ['Police']
        roles += ['Priest']
        roles += ['Citizen'] * room_size - 2 - room_size // 3
        self.roles = np.random.shuffle(roles)
        return dict(set(self.players, roles))