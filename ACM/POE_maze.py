# # #
#   #
# # #
import random


class POEMaze:
    question = []
    push_list = []
    final_result = []

    def random_question(self):
        l = [1, 1, 1, 1, 1, 1, 1, 1]
        for j in range(10):
            a = random.randrange(-1, 7)
            for i in range(a - 1, a + 2):
                l[i] = 0 if l[i] else 1
        return l

    # question = [1, 1, 1, 1, 1, 1, 0, 1]
    # recursion version
    def solve_question_recur(self, ques, start_pt=-1, first_recur=True):
        if first_recur is True:
            self.question = ques[:]
        # print('push', start_pt)
        self.push_list.append(start_pt)
        for i in range(start_pt - 1, start_pt + 2):
            ques[i] = 0 if ques[i] else 1
        if ques == [1, 1, 1, 1, 1, 1, 1, 1]:
            for i in range(-1, 7):
                if self.push_list.count(i) % 2 == 1:
                    self.final_result.append(i)
            print('For solving', self.question, 'solution:', self.final_result)
        else:
            try:
                self.solve_question_recur(ques, random.randrange(-1, 7), first_recur=False)
            except RecursionError:
                print('finding solution failed, recursion exceed, please try again')
        return self.final_result

    # iteration version
    def solve_question_iteration(self, ques):
        self.question = ques[:]
        while True:
            start_pt = random.randrange(-1, 7)
            self.push_list.append(start_pt)
            for i in range(start_pt - 1, start_pt + 2):
                ques[i] = 0 if ques[i] else 1
            if ques == [1, 1, 1, 1, 1, 1, 1, 1]:
                for i in range(-1, 7):
                    if self.push_list.count(i) % 2 == 1:
                        self.final_result.append(i)
                print('For solving', self.question, 'solution:', self.final_result)
                break

# lst = random_question()
# question = lst
# x = POEMaze()
# x.solve_question(x.random_question())
POEMaze().solve_question_iteration(POEMaze().random_question())