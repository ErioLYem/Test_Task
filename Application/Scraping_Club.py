from bs4 import BeautifulSoup
import requests
from requests import Session
from time import sleep
import json

global TITLE
global MENU
list_card = []
headers = {"User-Agent": "CrookedHands/2.0 (EVM x8), CurlyFingers20/1;p"}
#Блок для авторизации
work = Session()
work.get("https://quotes.toscrape.com/", headers=headers)
response1 = work.get("https://quotes.toscrape.com/login", headers=headers)
soup4 = BeautifulSoup(response1.text, "lxml")
token = soup4.find("form").find("input").get("value")
data = {"csrf_token": token, "username": "noname", "password": "pass"}
result1 = work.post("https://quotes.toscrape.com/login", headers=headers, data=data, allow_redirects=True)

#Блок для нахождения имени сайта и тегов навигации
url2 = "https://quotes.toscrape.com"
response2 = requests.get(url2)
soup2 = BeautifulSoup(response2.text, "lxml")
MENU = soup2.find("div", class_="col-md-4 tags-box").find("h2").text
TITLE = soup2.find("title").text
#print(head)
#print(menu)
data = soup2.find_all("span", class_="tag-item")
#print(data)
for i in data:
    tag1 = i.find("a", class_="tag").text
    list_card.append(tag1)

#Блок для нахождения данных карточек
st = str(input("Куда сохранить?"))
dt = [
               {
                    "Heading": TITLE,
                    "Menu": MENU,
                    "Tags_to_menu": list_card
                }
]
with open(st +'\otchet.json', 'a+') as f:
    f.write(json.dumps(dt))
n=1
while True:
    url = f"https://quotes.toscrape.com/page/{n}/"
    response9 = requests.get(url)
    soup9 = BeautifulSoup(response9.text, "lxml")
    result = soup9.find_all("span", class_="text")
    if len(result) != 0:
        url = f"https://quotes.toscrape.com/page/{n}/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        data = soup.find_all("div", class_="quote")
        for i in data:
            text = i.find("span", class_="text").text
            name = i.find("small", class_="author").text
            tags_cart = i.find("div", class_="tags").text
            card_url = "https://quotes.toscrape.com" + i.find("a").get("href")
            response = requests.get(card_url)
            soup = BeautifulSoup(response.text, "lxml")
            data = soup.find("div", class_="author-details")
            name_autors = data.find("h3", class_="author-title").text
            british_date = data.find("span", class_="author-born-date").text
            british_location = data.find("span", class_="author-born-location").text
            descript_autors = data.find("div", class_="author-description").text
            print(text + "\n" + name + "\n" + tags_cart + "\n"+ name_autors + "\n"+ "Родился:" + british_date + british_location + "\n"+ "Описание:"+" \n" + descript_autors)
            data_json = [
                {
                    "Quote": text,
                    "First_Name_Second_Name": name,
                    "Tags": tags_cart
                },
                {
                    "Name_Autors": name_autors,
                    "Date_of_birth": british_date,
                    "Place_of_birth": british_location,
                    "Description": descript_autors
                }
            ]
            with open(st+'\otchet.json', 'a+') as f:
                f.write(json.dumps(data_json))
        n+=1
        sleep(3)
    else:
        break
