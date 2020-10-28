import requests
import smtplib
from bs4 import BeautifulSoup
from re import sub
from decimal import Decimal
import time

URL = 'https://www.amazon.com/Sony-Full-frame-Mirrorless-Interchangeable-Lens-ILCE7M3K/dp/B07B45D8WV/ref=sr_1_3?dchild=1&keywords=sony+a7&qid=1596669454&sr=8-3'

headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}

def check_price():
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find(id="productTitle").get_text()
    price = soup.find(id="priceblock_saleprice").get_text()
    priceDec = Decimal(sub(r'[^\d.]', '', price)) #convert price string into decimal

    print(title.strip())
    print('Price:')
    print(priceDec)

    if(priceDec < 1700.00):
        send_mail()
    else:
        print('Price still above buy limit')


def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('slimbotV1@gmail.com','tnpsynbwzdrstsic')

    subject = 'Price went down!'
    body = 'Check the amazon link: https://www.amazon.com/Sony-Full-frame-Mirrorless-Interchangeable-Lens-ILCE7M3K/dp/B07B45D8WV/ref=sr_1_3?dchild=1&keywords=sony+a7&qid=1596669454&sr=8-3'

    msg = f"Subject:{subject}\n\n{body}"

    server.sendmail(
        'slimbotV1@gmail.com', #from
        'spencer.m.lim@gmail.com', #to
        msg
    )

    print('email has been sent')

    server.quit()

'''
#loop to run once a day (adjustable)
while(True):
    check_price()
    time.sleep(60 * 60 * 24)
'''
