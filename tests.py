# from data.letter_priorities import lp
#
# list = ['Ігор', 'Анатолій', 'ААна', 'Євгеній']
#
# dc = {}
#
# #  делаем словарь: имя - приоритет
# for name in list:
#     dc[name] = lp[name[:1]]
#
# #  сортируем по прироритету и по алфавиту
# for i in sorted(dc.items(), key=lambda x: (x[1], x[0])):
#     print(i)

# from handlers.users.bonus_system.eSputnik import eSputnik
#
# api = eSputnik(esputnik_url='https://esputnik.com.ua', esputnik_user='khoruzhevskiyg@gmail.com', esputnik_password='Aa150288')
#
# info = {'first_name': 'Yan',
#         'email': 'moover1233@gmail.com',
#         'group': 'test'
#         }
#
# print(api.add_contact(info))
import re

from natsort import natsorted

def get_A(a, b):
    return b + a + 1

def get_B(a, b):
    return b - a + 2

test = [1, 2, 3, 4]
# print(zip(*[iter(test)] * 3))

for a, b in [
    [1, 3],
    [2, 4]
]:
    for func in (get_A, get_B):
        print(a, b)
        print(func(a, b))

text = "20-років Перемоги"

print(text[0].isdigit())
