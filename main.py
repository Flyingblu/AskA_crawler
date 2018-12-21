import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re


class Question:
    def __init__(self, q, date):
        self.body = q
        self.date = date

    def __repr__(self):
        return self.body + ' ' + self.date


def get_qs():
    q_list = []
    cnt = 1
    while True:
        result = requests.get("https://app.xmu.edu.my/AskA/?p={0}&CategoryID=0".format(cnt))
        soup = BeautifulSoup(result.text, 'lxml')
        soup = soup.find_all(class_="table table-striped")
        tr_list = soup[0].find_all("tr")
        if not tr_list:
            break

        for piece in tr_list:
            if piece.find_all(id="showDetail"):
                q_body = piece.strong.get_text()
                if q_body[-1] == '\n':
                    q_body = q_body[:-2]
                q_list.append(Question(q_body, re.findall("\d{4}-\d{2}-\d{2}", piece.get_text())[0]))

        cnt += 1

    pprint(q_list)


if __name__ == "__main__":
    get_qs()
