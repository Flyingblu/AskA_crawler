import requests
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime


class Question:
    def __init__(self, q, date):
        self.title = q
        self.date = date
        self.body = None

    def __repr__(self):
        return '# ' + self.title + ' ' + self.date + '\n'


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
                q_list.append(Question(q_body, datetime.strptime(re.findall("\d{4}-\d{2}-\d{2}", piece.get_text())[0], "%Y-%m-%d")))
            else:
                answer = piece.find_all("div")
                ans_str = ""
                for div in answer:
                    ans_str += str(div)
                tmp_q = q_list.pop()
                tmp_q.body = re.sub(pattern="\(\/AskA\/", string=ans_str, repl="(https://app.xmu.edu.my/AskA/",
                                    flags=re.IGNORECASE).strip()
                q_list.append(tmp_q)

        cnt += 1
    return json.dumps(q_list, default=lambda o: o.__dict__, indent=4)


def to_markdown(q_list):
    file = open("out.md", 'w')
    for q in q_list:
        file.write('# ' + q.body + ' ' + q.date + '\n')
        file.write(q.ans + '\n')

    file.close()


def to_json_file(*json_obj):
    file = open("out.json", 'w')
    for j in json_obj:
        file.write(j)
    file.close()


if __name__ == "__main__":
    to_json_file(*get_qs())
