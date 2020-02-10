class Agent:
    def __init__(self, value, position):
        self.value = value
        self.position = position

    def __str__(self):
        return 'Value: {} Pos: {}'.format(self.value, self.position)

    # neighbors[0] left neighbor
    # neighbor[1] right neighbor
    def update(self, neighbors):
        # Check left first, because we want
        # to sort in ascending order
        # -1 means there's no neighbor
        if neighbors[0] != None:
            if neighbors[0].value > self.value:
                # swap position
                neighbors[0].position, self.position = self.position, neighbors[0].position
        elif neighbors[1] != None:
            if neighbors[1].value < self.value:
                # swap position
                neighbors[1].position, self.position = self.position, neighbors[1].position
