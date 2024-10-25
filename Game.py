class Game:
    def __init__(self, datetime):
        self.datetime = datetime
        self.home = ""
        self.away = ""
        self.home_score = 0
        self.away_score = 0
        self.preseason = False
        self.playoffs = False


    def __str__(self):
        return f"{self.away}@{self.home}, " + str(self.datetime)