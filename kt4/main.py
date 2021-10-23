#вариант 2 - https://habr.com/ru/all/
#   .tm-articles-list>article
#   .tm-articles-list>article h2
#   .tm-articles-list>article .tm-votes-meter__value
#   tm-articles-list__item

from requests import get
import re
import bs4
from flask import Flask, render_template


#с помощью специальной библиотеки
def parseBibl(txt):
    result = []
    soup = bs4.BeautifulSoup(txt, features="html.parser")
    divs = soup.find_all("article",class_="tm-articles-list__item")
    if not divs:
        raise Exception("По данному запросу ничего не найдено на странице")
    for item in divs:
        h2 = item.find("h2")
        span = item.find("span", class_="tm-votes-meter__value")
        result.append(f"Статья: '{h2.get_text()}' Рейтинг ({span.get_text()})")
    return result



# с помощью регулярных выражений
def parseRegex(txt):
    headers = re.findall("class=\"tm-article-snippet__title-link\"><span>(.+?)</span>",txt)
    rating = re.findall("class=\"tm-votes-meter__value.+?\">(.+?)</span>",txt)
    if not headers or not rating:
        raise Exception("По данному запросу ничего не найдено на странице")
    result = []
    c = 0
    for h in headers:
        result.append(f"Статья: '{h}' (Рейтинг {rating[c]})")
        c += 1
    return result



def main2():
    try:
        resp = get('https://habr.com/ru/all/')
        if not resp:
            raise Exception(f"Сервер вернул код статуса HTTP: {resp.status_code}")
    except Exception as e:
        print(e)
        return False
    return resp

app = Flask(__name__)


@app.route('/')
def mainpage():
    return render_template('index.html')


@app.route('/bs4')
def parsbs4():
    try:
        resp = main2()
        res = parseBibl(resp.text)
    except Exception as e:
        print(e)
    return render_template('bs4.html', data=res)


@app.route('/regex')
def parsregex():
    try:
        resp = main2()
        res = parseRegex(resp.text)
    except Exception as e:
        print(e)
    return render_template('regex.html', data=res)


if __name__ == "__main__":
    try:
        resp = get('https://habr.com/ru/all/')
        if not resp:
            raise Exception(f"Сервер вернул код статуса HTTP: {resp.status_code}")
    except Exception as e:
        print(e)

    app.run(debug=False)
