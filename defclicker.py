import requests
import dotenv
import os
from pprint import pprint
from dotenv import load_dotenv
import customtkinter
load_dotenv()

app = customtkinter.CTk()
app.geometry("540x350")
app.title("DefClicker")


app.iconbitmap("./click.ico")
customtkinter.set_appearance_mode("dark")

def short_link(entry_long_url,token):

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }

    data = {"long_url": entry_long_url.get()}
    response = requests.post('https://api-ssl.bitly.com/v4/bitlinks', headers=headers, json=data)
    slovar_otvet = response.json()
    print(data)
    print(slovar_otvet)
    return slovar_otvet["link"]
    
token = os.getenv("TOKEN_BITLY")

def forlabel(entry_long_url,token,label4):
    a = short_link(entry_long_url,token)
    label4.configure(text=f"Ваша ссылка: {a}")
    
    
label = customtkinter.CTkLabel(app, text="DefClicker", fg_color="transparent", font=('Times 30',35))
label2 = customtkinter.CTkLabel(app, text="Введите ссылку,которую нужно сократить", fg_color="transparent")
label2.place(x=150,y=170)
label3 = customtkinter.CTkLabel(app, text="Пример: http://dzen.ru/example1/example2/", fg_color="transparent",font=('Times 30',12))
label3.place(x=160,y=230)
label.place(x=200,y=100)
entry_long_url = customtkinter.CTkEntry(app)
entry_long_url.place(x=200,y=200)
button = customtkinter.CTkButton(app, text="Сократить ссылку", command=lambda: forlabel(entry_long_url,token,label4))
button.place(x=200,y=280)
label4 = customtkinter.CTkLabel(app, text=f"Ваша ссылка: ", fg_color="transparent", font=('Times 30',20))
label4.place(x=20,y=50)



app.mainloop()