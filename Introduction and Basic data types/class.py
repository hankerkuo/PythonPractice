class Account:
    def __init__(self, username, password, win, lose):
        self.username = username
        self.password = password
        self.win = win
        self.lose = lose
        self.winrate = self.win / (self.win + self.lose)

    def win_add(self, amount):
        self.win += amount
        self.winrate = self.win / (self.win + self.lose)

    def lose_add(self, amount):
        self.lose += amount
        self.winrate = self.win / (self.win + self.lose)

acct = Account('Hank', 'qwer123', 1, 1)
acct.win_add(100)
acct.lose_add(10)
print(acct.winrate)
print(Account.__dict__)
