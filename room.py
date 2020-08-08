class Room:
    def __init__(self, room_id):
        self.id = room_id
        self.players = []

    def add_player(self, player):
        if player not in self.players:
            self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)

    def play(self):
        room_size = len(self.players)
        roles = {}
        for player in self.players:
            roles[player] = 'Citizen'
            
        return roles