import requests
import dotenv
import os
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()




def get_user_info(token):

    headers = {
        'Authorization': f'Bearer {token}',
    }
    

    response = requests.get('https://api-ssl.bitly.com/v4/user', headers=headers)
    response.raise_for_status()

    return response.json()

def short_link(token):

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }

    data = {"long_url": example}
    response = requests.post('https://api-ssl.bitly.com/v4/bitlinks', headers=headers, json=data)
    slovar_otvet = response.json()
    return slovar_otvet["link"]


token = os.getenv("TOKEN_BITLY")

print('''Программа для работы с ссылками Bitly
      1.Узнать информацию о пользователе
      2.Получить сокращенную ссылку''')

am = input("Введите цифру выбранного варианта: ")

if am == "1":
    pprint(get_user_info())
elif am == "2":
    example = input("Введите вашу ссылку для сокращения: ")
    pprint(short_link())
else:
    print("Ошибка! Вы должны ввести 1 или 2")



