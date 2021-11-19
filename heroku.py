from config_con import *
from module_wcapi_api import WOO_API
from module_mail import Mail
from module_fb_bot import Bot
from module_db_reg import DB_reg
from module_main_fuctions import MAIN_FUNC

import os
from flask import Flask, request
import requests
import apscheduler
from apscheduler.schedulers.background import BackgroundScheduler





mail1 = Mail()
wcapi1 = WOO_API()
db1 = DB_reg()
main3 = MAIN_FUNC()

app = Flask(__name__)
bot = Bot(PAGE_APP_TOKEN)



# def sensor():
#     main3.ping()
#
#     all_products = wcapi1.get_all_products()
#     for i in all_products:
#         all_products_list2 = []
#         name = str(i.get('name'))
#         all_products_list2.append(name)
#         woo_id = str(i.get('id'))
#         all_products_list2.append(woo_id)
#         price = str(i.get('regular_price'))
#         all_products_list2.append(price)
#         url = str(i.get('permalink'))
#         all_products_list2.append(url)
#         image2 = i['images'][0]
#         image = str(image2.get('src'))
#         all_products_list2.append(image)
#         stock_status = str(i.get('stock_status'))
#         all_products_list2.append(stock_status)
#         db1.insert_table_fb(all_products_list2)
#
# sched = BackgroundScheduler(daemon=True)
# sched.add_job(sensor, 'interval', minutes=10)
# sched.start()

@app.route('/customer_register', methods=['GET', 'POST'])
def customer_register():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    hook = 'CREATE NEW USER'
    texttosend = f'*** ALERTS FROM SITE ***\n\n ' \
                 f'- HOOK - \n' \
                 f'{hook}\n\n' \
                 f'*** DATA ***\n' \
                 f'1. USERNAME: {username}\n' \
                 f'2. MAIL: {email}\n'
    to = 'karenka@karenkashop.com'
    sbj = 'ALERT FROM SITE: ORDER CREATE'
    mail1.send_simple_text_mail(texttosend, to, sbj)


    return 'ok', 200

@app.route('/order_create', methods=['POST'])
def order_create():
    data = request.get_json()
    hook = 'Create order from site'
    order_user = data['shipping'].get('first_name')
    order_id = data.get('id')
    order_status = data.get('status')
    texttosend = f'*** ALERTS FROM SITE ***\n\n ' \
                 f'- HOOK - \n' \
                 f'{hook}\n\n' \
                 f'*** DATA ***\n' \
                 f'1. USER: {order_user}\n' \
                 f'2. ITEM ID: {order_id}\n' \
                 f'3. STATUS: {order_status}\n'
    to = 'karenka@karenkashop.com'
    sbj = 'ALERT FROM SITE: ORDER CREATE'
    mail1.send_simple_text_mail(texttosend, to, sbj)

    main3.printenumerate(data)
    return 'ok', 200

@app.route('/order_update', methods=['POST'])
def order_update():
    data = request.get_json()
    order_first_name = data['billing'].get('first_name')
    order_last_name = data['billing'].get('last_name')
    order_id = data.get('id')
    order_status = data.get('status')
    hook = 'Change order status'
    texttosend = f'*** ALERTS FROM SITE ***\n\n ' \
                 f'- HOOK - \n' \
                 f'{hook}\n\n' \
                 f'*** DATA ***\n' \
                 f'1. USER: {order_first_name + order_last_name}\n' \
                 f'2. ITEM ID: {order_id}\n' \
                 f'3. NEW STATUS: {order_status}\n'
    to = 'karenka@karenkashop.com'
    sbj = 'ALERT FROM SITE: ORDER UPDATE'
    mail1.send_simple_text_mail(texttosend, to, sbj)

    return 'ok', 200

@app.route('/jotform', methods=['POST'])
def jotform():
    data1 = request.form.to_dict()
    submissionID = data1.get('submissionID')
    response = requests.get(f'https://eu-api.jotform.com/submission/{submissionID}?apiKey={JOT_API_KEY}')
    data2 = response.json()
    data3 = data2.get('content')
    data4 = data3.get('answers')
    keys = ['name', 'categories', 'sku', 'description', 'short_description', 'tags', 'stock_quantity', 'regular_price', 'material', 'size', 'length', 'color', 'main_image', 'additional_image', 'comments']
    new_product = {}
    for i in keys:
        new_product[i] = None
    for index, (key, value) in enumerate(data4.items()):
        print(f'{index}) {key}: {value}')
        if key == '23':
            data5 = data4.get('23')
            jot_regular_price = data5.get('answer')
            new_price = jot_regular_price
        if key == '41':
            data5 = data4.get('41')
            jot_name = data5.get('answer')
            new_name = jot_name
            new_external_link = jot_name.replace(" ", "-").lower()
        if key == '301':
            data5 = data4.get('301')
            jot_categories_id = data5.get('answer')
            new_categories = jot_categories_id
        if key == '163':
            data5 = data4.get('163')
            jot_stock_quantity = data5.get('answer')
            new_stock = jot_stock_quantity
        if key == '257':
            data5 = data4.get('257')
            jot_sku = data5.get('answer')
            new_sku = jot_sku
        if key == '36':
            data5 = data4.get('36')
            jot_tags = data5.get('answer')
            tags = jot_tags.split(',')
            tags_list = []
            for i in tags:
                tags_list.append({'name': i})
            new_tags = tags_list
        if key == '278':
            data5 = data4.get('278')
            jot_description = data5.get('answer')
            new_description = jot_description
        if key == '279':
            data5 = data4.get('279')
            jot_short_description = data5.get('answer')
            new_short_description = jot_short_description
        if key == '81':
            data5 = data4.get('81')
            jot_main_image = data5.get('answer')
            new_main_image = jot_main_image
        if key == '300':
            data5 = data4.get('300')
            jot_additional_image = data5.get('answer')
            new_additional_image = jot_additional_image
        if key == '362':
            data5 = data4.get('362')
            jot_size = data5.get('answer')
            new_size = str(jot_size)
        if key == '90':
            data5 = data4.get('90')
            jot_length = data5.get('answer')
            new_length = str(jot_length)
        if key == '375':
            data5 = data4.get('375')
            jot_material = data5.get('answer')
            jot_material = jot_material.split(":")[0]
            new_material = jot_material
        if key == '376':
            data5 = data4.get('376')
            jot_color = data5.get('answer')
            jot_color = jot_color.split(":")[0]
            new_color = jot_color
        if key == '352':
            data5 = data4.get('352')
            jot_comments = data5.get('answer')
            new_comments = jot_comments

    text = f'New product ({new_name}) & SKU({new_sku}) & Stock quantity ({new_stock}) successfully added! \n\nExternal link to product: \n\nhttps://karenkashop.com/product/{new_external_link} \n'
    to = 'karenka@karenkashop.com'
    sbj = 'ALERT FROM SITE: CREATE NEW PRODUCT'
    mail1.send_simple_text_mail(text, to, sbj)

    wcapi1.product_create(new_name, new_description, new_short_description, new_comments, new_sku, new_price,
                          new_stock, new_tags, new_color, new_length, new_size, new_material, new_categories,
                          new_main_image, new_additional_image)
    return 'ok', 200

@app.route("/product_updated", methods=["GET", "POST"])
def product_updated():
    data = request.get_json()
    product_name = data.get('name')
    hook = 'PRODUCT UPDATED'
    texttosend = f'*** ALERTS FROM SITE ***\n\n ' \
                 f'- HOOK - \n' \
                 f'{hook}\n\n' \
                 f'*** DATA ***\n' \
                 f'1. PRODUCT NAME: {product_name}\n'
    to = 'karenka@karenkashop.com'
    sbj = 'ALERT FROM SITE: PRODUCT UPDATE'
    mail1.send_simple_text_mail(texttosend, to, sbj)

    return 'ok', 200

@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == FB_VERIFY_TOKEN:
            return 'Invalid verification token', 403
        return request.args["hub.challenge"], 200
    return "Hello, Solstice!", 200


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if messaging_event.get("message"):
                    bot.message(messaging_event)
                elif messaging_event.get("delivery"):
                    pass
                elif messaging_event.get("read"):
                    pass
                elif messaging_event.get("optin"):
                    pass
                elif messaging_event.get("postback"):
                    bot.postback(messaging_event)
                else:
                    print(f' unknown messaging_event: {messaging_event}')
    return 'ok', 200

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))


