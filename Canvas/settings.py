class Settings():
    def __init__(self, fill=None, stroke=None):
        self.fill = fill
        self.stroke = stroke

    def __hash__(self):
        return hash((hash(self.fill), hash(self.stroke)))
