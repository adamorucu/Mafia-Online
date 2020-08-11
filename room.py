import math
from random import shuffle

class Room:
    def __init__(self, room_id, host):
        self.id = room_id
        self.sessids = []
        self.player_names = []
        self.host = host

    def add_player(self, sessid, player_name):
        if sessid not in self.sessids:
            self.sessids.append(sessid)
        if player_name not in self.player_names:
            self.player_names.append(player_name)

    def assign_roles(self):
        room_size = len(self.sessids)
        roles = []
        roles += ['Mafia'] * (room_size // 3)
        roles += ['Police']
        roles += ['Priest']
        roles += ['Citizen'] * (room_size - 2 - (room_size // 3))
        print(roles)
        shuffle(roles)
        self.roles = roles
        return self.roles
        # return dict(set(self.players, roles))

    def expl(self, role):
        return 'role explanation'