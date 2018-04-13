class Account:
    class win_data:
        def __init__(self, win, lose):
            self.win = win
            self.lose = lose
            self.winrate = self.win / (self.win + self.lose)

        def win_add(self, amount):
            self.win += amount
            self.winrate = self.win / (self.win + self.lose)

        def lose_add(self, amount):
            self.lose += amount
            self.winrate = self.win / (self.win + self.lose)

acct = Account.win_data(1, 1)
acct.win_add(100)
acct.lose_add(100)
print(acct.winrate)
