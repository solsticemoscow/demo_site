import os, re
from enum import Enum
from module_db_reg import DB_reg
from module_mail import Mail
from module_wcapi_api import WOO_API
from module_main_fuctions import *
from config_con import *
import time
import requests, json
from requests_toolbelt import MultipartEncoder
from pymessenger import utils


mail1 = Mail()
db1 = DB_reg()
wcapi2 = WOO_API()
m1 = MAIN_FUNC()


class NotificationType(Enum):
    regular = "REGULAR"
    silent_push = "SILENT_PUSH"
    no_push = "NO_PUSH"

class Bot(object):

    def __init__(self, access_token, **kwargs):
        self.api_version = kwargs.get('api_version') or DEFAULT_API_VERSION
        self.app_secret = kwargs.get('app_secret')
        self.graph_url = 'https://graph.facebook.com/v{0}'.format(self.api_version)
        self.access_token = access_token

        self.fb_list = []
        self.counter = 0
        self.tag = None
        self.user_name = None


        self.main_menu_payload = ['ok', 'shop_start', 'main', 'go']
        self.getstarted_payload = ['GET_STARTED', '<GET_STARTED_PAYLOAD>']
        self.shop_payload = ['shopping', 'shopping_again']


        self.image_stock = 'https://karenkashop.com/wp-content/uploads/2021/07/59873E5FEF9740DBA44B7DA16E3F4CD3.jpeg'
        self.image_custom = 'https://karenkashop.com/wp-content/uploads/2021/07/kq1n6hzsahy.jpg'
        self.image_outofstock = 'https://karenkashop.com/wp-content/uploads/2021/07/pngtree-sold-out-banner-with-red-ribbon-and-stars-png-image_1531226.jpg'

        self.text_event = "Do you want to know about Sveta's next event?"
        self.text_all_shown = 'All items shown. Tap Back to continue.'

        self.quick_reply_show_more = {
            "content_type": "text",
            "title": "Show more",
            "payload": "show_more"}

        self.quick_reply_show_next = {
            "content_type": "text",
            "title": "Show next",
            "payload": "show_next"}

        self.quick_reply_back = {
            "content_type": "text",
            "title": "All items shown.Tap to continue.",
            "payload": "shop_start"}

        self.quick_reply_stock = {
            "content_type": "text",
            "title": "Stock",
            "payload": "instock"}

        self.quick_reply_outstock = {
            "content_type": "text",
            "title": "Out Stock: Notify me",
            "payload": "outstock"}

        self.quick_reply_back_to_main = {
            "content_type": "text",
            "title": "Back to main",
            "payload": "back"}


        self.message_menu = {
                            "attachment":
                                {
                                    "type": "template",
                                    "payload":
                                        {
                                            "template_type": "generic",
                                            "elements": [
                                                {
                                                    "title": "Shop",
                                                    "image_url": self.image_stock,
                                                    "subtitle": "Buy online items",
                                                    "buttons": [{
                                                        "type": "postback",
                                                        "title": "SHOW ITEMS NOW!",
                                                        "payload": "shopping"}]
                                                 },
                                                {
                                                    "title": "Custom order",
                                                    "image_url": self.image_custom,
                                                    "subtitle": "CUSTOM ORDER FROM OWNER",
                                                    "buttons": [{
                                                        "type": "postback",
                                                        "title": "CREATE CUSTOM ORDER",
                                                        "payload": "custom"}]
                                                }
                                            ]
                                        }
                                }
                        }

        self.message_human = {
        "recipient": {},
        "message": {'text': 'message'},
        "messaging_type": "MESSAGE_TAG",
        "tag": "HUMAN_AGENT"
        }

        self.elements = []


    @property
    def auth_args(self):
        if not hasattr(self, '_auth_args'):
            auth = {
                'access_token': self.access_token
            }
            if self.app_secret is not None:
                appsecret_proof = utils.generate_appsecret_proof(self.access_token, self.app_secret)
                auth['appsecret_proof'] = appsecret_proof
            self._auth_args = auth
        return self._auth_args



    def send_recipient(self, recipient_id, payload, notification_type=NotificationType.regular):
        payload['recipient'] = {
            'id': recipient_id
        }
        payload['notification_type'] = notification_type.value
        return self.send_raw(payload)

    def send_message(self, recipient_id, message, notification_type=NotificationType.regular):
        return self.send_recipient(
            recipient_id,
            {
                'message': message

            },
            notification_type)

    def send_attachment(self, recipient_id, attachment_type, attachment_path,
                        notification_type=NotificationType.regular):
        payload = {
            'recipient': {
                {
                    'id': recipient_id
                }
            },
            'notification_type': notification_type,
            'message': {
                {
                    'attachment': {
                        'type': attachment_type,
                        'payload': {}
                    }
                }
            },
            'filedata': (os.path.basename(attachment_path), open(attachment_path, 'rb'))
        }
        multipart_data = MultipartEncoder(payload)
        multipart_header = {
            'Content-Type': multipart_data.content_type
        }
        return requests.post(self.graph_url, data=multipart_data,
                             params=self.auth_args, headers=multipart_header).json()

    def send_attachment_url(self, recipient_id, attachment_type, attachment_url,
                            notification_type=NotificationType.regular):
        return self.send_message(recipient_id, {
            'attachment': {
                'type': attachment_type,
                'payload': {
                    'url': attachment_url
                }
            }
        }, notification_type)


    def send_text_message(self, recipient_id, message, notification_type=NotificationType.regular):
        return self.send_message(recipient_id, {
            'text': message
        }, notification_type)

    def send_generic_message1(self, recipient_id, elements, notification_type=NotificationType.regular):
        return self.send_message(recipient_id, {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": elements
                }}},
            notification_type)

    def send_generic_message2(self, recipient_id, elements, notification_type=NotificationType.regular):
        return self.send_message(recipient_id,
                                 {"attachment": {
                "type": "template",
                "payload":{
                    "template_type": "generic",
                    "elements": elements
                    }},
                "quick_replies": [{
            "content_type": "text",
            "title": "Show next",
            "payload": "show_next"}]},
                notification_type)

    def send_generic_message3(self, recipient_id, elements, notification_type=NotificationType.regular):
        return self.send_message(recipient_id,
                                 {"attachment": {
                "type": "template",
                "payload":{
                    "template_type": "generic",
                    "image_aspect_ratio": "SQUARE",
                    "elements": elements
                    }}}, notification_type)

    def send_button_message(self, recipient_id, text, buttons, notification_type=NotificationType.regular):
        """

        """
        return self.send_message(recipient_id, {"attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": text,
                    "buttons": buttons
                }
            }}, notification_type)

    def send_action(self, recipient_id, action, notification_type=NotificationType.regular):
        """
        :param recipient_id:
        :param action: [mark_seen : typing_on : typing_off]
        :param notification_type:
        :return:

        """
        return self.send_recipient(recipient_id, {
            'sender_action': action
        }, notification_type)

    def send_image(self, recipient_id, image_path, notification_type=NotificationType.regular):
        return self.send_attachment(recipient_id, "image", image_path, notification_type)

    def send_image_url(self, recipient_id, image_url, notification_type=NotificationType.regular):
        return self.send_attachment_url(recipient_id, "image", image_url, notification_type)

    def send_audio(self, recipient_id, audio_path, notification_type=NotificationType.regular):
        return self.send_attachment(recipient_id, "audio", audio_path, notification_type)

    def send_audio_url(self, recipient_id, audio_url, notification_type=NotificationType.regular):
        return self.send_attachment_url(recipient_id, "audio", audio_url, notification_type)

    def send_video(self, recipient_id, video_path, notification_type=NotificationType.regular):
        return self.send_attachment(recipient_id, "video", video_path, notification_type)

    def send_video_url(self, recipient_id, video_url, notification_type=NotificationType.regular):
        return self.send_attachment_url(recipient_id, "video", video_url, notification_type)

    def send_file(self, recipient_id, file_path, notification_type=NotificationType.regular):
        return self.send_attachment(recipient_id, "file", file_path, notification_type)

    def send_file_url(self, recipient_id, file_url, notification_type=NotificationType.regular):
        return self.send_attachment_url(recipient_id, "file", file_url, notification_type)

    def get_user_info(self, recipient_id, fields=['name']):
        """Getting information about the user
        https://developers.facebook.com/docs/messenger-platform/user-profile
        Input:
          recipient_id: recipient id to send to
        Output:
          Response from API as <dict>
        """
        params = {}
        if fields is not None and isinstance(fields, (list, tuple)):
            params['fields'] = ",".join(fields)

        params.update(self.auth_args)

        request_endpoint = '{0}/{1}'.format(self.graph_url, recipient_id)
        response = requests.get(request_endpoint, params=params)
        if response.status_code == 200:
            return response.json()

        return None

    def send_raw(self, payload):
        request_endpoint = '{0}/me/messages'.format(self.graph_url)
        # print(f'PAYLOAD {payload}')
        response = requests.post(
            request_endpoint,
            params=self.auth_args,
            json=payload
        )
        result = response.json()
        # print(f'PAYLOAD2 {result}')
        return result

    def _send_payload(self, payload):
        """ Deprecated, use send_raw instead """
        return self.send_raw(payload)

    def set_get_started(self, gs_obj):
        request_endpoint = '{0}/me/messenger_profile'.format(self.graph_url)
        response = requests.post(
            request_endpoint,
            params = self.auth_args,
            json = gs_obj
        )
        result = response.json()
        return result

    def set_persistent_menu(self, pm_obj):
        """Set a persistent_menu that stays same for every user. Before you can use this, make sure to have set a get started button.
        https://developers.facebook.com/docs/messenger-platform/reference/messenger-profile-api/persistent-menu
        Input:
          pm_obj: Your formatted persistent menu object as described by the API docs
        Output:
          Response from API as <dict>
        """
        request_endpoint = '{0}/me/messenger_profile'.format(self.graph_url)
        response = requests.post(
            request_endpoint,
            params = self.auth_args,
            json = pm_obj
        )
        result = response.json()
        return result

    def remove_get_started(self):
            delete_obj = {"fields": ["get_started"]}
            request_endpoint = '{0}/me/messenger_profile'.format(self.graph_url)
            response = requests.delete(
                request_endpoint,
                params = self.auth_args,
                json = delete_obj
            )
            result = response.json()
            return result

    def remove_persistent_menu(self):
            delete_obj = {"fields": ["persistent_menu"]}
            request_endpoint = '{0}/me/messenger_profile'.format(self.graph_url)
            response = requests.delete(
                request_endpoint,
                params = self.auth_args,
                json = delete_obj
            )
            result = response.json()
            return result

    def products(self, fields=None):
        sveta_cat_id = '1316392885406065'
        params = {}
        if fields is not None and isinstance(fields, (list, tuple)):
            params['fields'] = ",".join(fields)
        params.update(self.auth_args)
        request_endpoint = '{0}/{1}/products'.format(self.graph_url, sveta_cat_id)
        response = requests.get(request_endpoint, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def attachments(self, attachments):
        print(f'3: ATT {attachments}')

    def tags(self, sender_id, tags):
        source = tags.get('source')
        print(f' TAGS {source}')
        if source == 'customer_chat_plugin':
            user_data = self.get_user_info(sender_id, fields=['id', 'name', 'first_name', 'last_name'])
            # for user_data:
            # print(f' UD = {user_data}')
            # print(f' TAGS {source}')
            # db_mid.insert_guests(guest_id, guest_name, guest_firstname, guest_lastname)

    def read(self, read):
        pass

    def quick_reply(self, sender_id, quick_reply):
        print(f' QUICK {quick_reply}')

    def referral(self, messaging_event):
        pass
        # referral = messaging_event['postback'].get('referral')
        # sender_id = messaging_event['sender'].get('id')
        # for index, (key, value) in enumerate(referral.items()):
        #     # referer_uri = referral.get('referer_uri')
        #     if referral.get('source') == 'CUSTOMER_CHAT_PLUGIN':
        #         texttosend = f'Guest user via Site Chat Plugin ({sender_id}) with referer_uri {referral.get("referer_uri")} request live agent.'
        #         self.mail1.send_simple_text_mail(texttosend)

    def delivery(self, delivery):
        pass
        # print(f' DEL {delivery}')

    def optin(self, sender_id, messaging_event):
        opt = messaging_event.get('optin')
        for i in opt:
            print(f' OPT_field: {i}')

# ----------------------- MAIN -----------------------------------

    def text(self, sender_id, sender_text):
        if sender_text == 'YES':
            pass
        elif sender_text == 'Back to main':
            self.send_message(sender_id, self.message_menu)
        elif sender_text == 'OK, i understand':
            self.send_message(sender_id, self.message_menu)
        elif sender_text == 'Jewelry':
            self.tag = 'Talk with human'
            message1 = {
                "text": "Pick category",
                "quick_replies": [
                    {
                        "content_type": "text",
                        "title": "Bracelets",
                        "payload": "custom_bracelets",
                    },
                    {
                        "content_type": "text",
                        "title": "Rings",
                        "payload": "custom_rings"
                    },
                    {
                        "content_type": "text",
                        "title": "Earrings",
                        "payload": "custom_earrings"
                    },
                    {
                        "content_type": "Necklaces",
                        "title": "Rings",
                        "payload": "custom_necklaces"
                    }
                ]

            }
            self.send_message(sender_id, message1)

        else:
            pass

    def message(self, messaging_event):
        print(f' NA message: {messaging_event}')
        sender_id = messaging_event['sender'].get('id')
        sender_text = messaging_event['message'].get('text')
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if (re.fullmatch(regex, sender_text)):
            customer_email = sender_text
            name = self.user_name.get("name")
            customer_inbox_page = f'https://business.facebook.com/latest/inbox/all?asset_id=101362591603442&business_id=656443424789457&mailbox_id=101362591603442&selected_item_id={sender_id}'
            texttosend = f'*** ALERTS FROM FACEBOOK ***\n\n ' \
                         f'- HOOK - \n' \
                         f'{self.tag}\n\n' \
                         f'*** DATA ***\n' \
                         f'1. USER ID: {sender_id}\n' \
                         f'2. USER EMAIL: {customer_email}\n' \
                         f'3. USER NAME: {name}\n' \
                         f'4. LINK TO MESSAGES: {customer_inbox_page}\n'
            sbj = f'ALERT FROM FACEBOOK: {self.tag}'
            to = 'karenka@karenkashop.com'
            mail1.send_simple_text_mail(texttosend, to, sbj)
            # m1.telegram_send_message(texttosend)



            message = {
                "text": "Success! Waiting for response, you get feedback via email or messenger.",
            }
            self.send_message(sender_id, message)
        elif sender_text == 'Show items again':
            self.show_products(sender_id)
        elif sender_text == 'Back to main menu':
            self.send_message(sender_id, self.message_menu)
        # elif sender_text == 'Jewelry' or 'Home decor':
        #     customer_email = sender_text
        #     customer_inbox_page = f'https://business.facebook.com/latest/inbox/all?asset_id=101362591603442&business_id=656443424789457&mailbox_id=101362591603442&selected_item_id={sender_id}'
        #     texttosend = f'*** ALERTS FROM FACEBOOK ***\n\n ' \
        #                  f'- HOOK - \n' \
        #                  f'{self.tag}\n\n' \
        #                  f'*** DATA ***\n' \
        #                  f'1. USER ID: {sender_id}\n' \
        #                  f'2. USER EMAIL: {customer_email}\n' \
        #                  f'3. USER NAME: {self.user_name}\n' \
        #                  f'4. LINK TO MESSAGES: {customer_inbox_page}\n'
        #     to = 'solstice@karenkashop.com'
        #     mail1.send_simple_text_mail(texttosend, to)
        #
        #     # t1.send_msg_to_whatsup(texttosend)
        #     # to = TWILIO_NUM_KARENKA
        #     # t1.send_msg_to_whatsup(texttosend, to)
        #
        #     message = {
        #         "text": "Success! Waiting for response, you get feedback via email or messenger.",
        #     }
        #     self.send_message(sender_id, message)
        #     # message1 = {
        #     #     "text": "Pick category",
        #     #     "quick_replies": [
        #     #         {
        #     #             "content_type": "text",
        #     #             "title": "Bracelets",
        #     #             "payload": "custom_bracelets",
        #     #         },
        #     #         {
        #     #             "content_type": "text",
        #     #             "title": "Rings",
        #     #             "payload": "custom_rings"
        #     #         },
        #     #         {
        #     #             "content_type": "text",
        #     #             "title": "Earrings",
        #     #             "payload": "custom_earrings"
        #     #         },
        #     #         {
        #     #             "content_type": "text",
        #     #             "title": "Necklaces",
        #     #             "payload": "custom_necklaces"
        #     #         }
        #     #     ]
        #     #
        #     # }
        #     # self.send_message(sender_id, message1)
        # elif sender_text == 'Rings' or 'Earrings' or 'Necklaces' or 'Bracelets':

        else:
            print(f' NA TEXT: {sender_text}')

    def show_products(self, sender_id):
        products_count = db1.max_element()
        all_products = db1.select_table_fb()
        self.fb_list = []
        self.counter = 0
        for index, item in enumerate(all_products):
            if item.get('stock_status') == "instock":
                gen_template = {"title": item.get('name'),
                                "image_url": item.get('image'),
                                "subtitle": item.get('price') + ' $ per item',
                                "buttons": [
                                    {
                                        "type": "web_url",
                                        "url": f'https://karenkashop.com/?add-to-cart={item.get("woo_id")}',
                                        "title": "BUY",
                                        "webview_height_ratio": "tall"}, {
                                        "type": "web_url",
                                        "url": item.get('url'),
                                        "webview_height_ratio": "tall",
                                        "title": "VIEW INFO"}]}
                current_item = gen_template.copy()
                self.fb_list.append(current_item)
            if item.get('stock_status') == "outofstock":
                gen_template = {"title": item.get('name'),
                                "image_url": item.get('image'),
                                "subtitle": f'ITEM OUT OF STOCK',
                                "buttons": [
                                    {
                                        "type": "web_url",
                                        "url": item.get('url'),
                                        "webview_height_ratio": "tall",
                                        "title": "GET NOTIFY"}]}
                current_item = gen_template.copy()
                self.fb_list.append(current_item)
            products_count = products_count - 1
            self.counter = self.counter + 1
            if products_count == 0:
                self.send_generic_message1(sender_id, self.fb_list)
                message1 = {
                    "text": "All products shown. Tap to continue.",
                    "quick_replies": [
                        {
                            "content_type": "text",
                            "title": "Show items again",
                            "payload": "shopping_again",
                        },
                        {
                            "content_type": "text",
                            "title": "Back to main menu",
                            "payload": "main",
                        }
                    ]

                }
                self.send_message(sender_id, message1)
                self.fb_list = []
                self.counter = 0
                break
            if self.counter == 5:
                self.send_generic_message1(sender_id, self.fb_list)
                time.sleep(2)
                message1 = {
                    "text": "Next 5:"}
                self.send_message(sender_id, message1)
                self.fb_list = []
                self.counter = 0

    def postback(self, messaging_event):
        print(f' NA postback: {messaging_event}')
        payload = messaging_event['postback'].get('payload')
        sender_id = messaging_event['sender'].get('id')
        GreetingText = [
            {'locale': "default",
             'text': 'Welcome to KarenkaShop {{user_first_name}}! All actions in this shop you will be taped on images or text. If you want talk with human you can send request. Enjoy!', },
            {'locale': "en_US",
             'text': 'Welcome to KarenkaShop {{user_first_name}}! All actions in this shop you will be taped on images or text. If you want talk with human you can send request. Enjoy!'}]
        get_st = {"payload": "GET_STARTED"}
        menu = {"greeting": GreetingText,
                "get_started": get_st,
                "composer_input_disabled": True,
                "persistent_menu": [
                    {
                        "locale": "default",
                        "composer_input_disabled": True,
                        "call_to_actions": [
                            {
                                "type": "postback",
                                "title": "Shop now",
                                "payload": "shopping"
                            },
                            # {
                            #     "type": "web_url",
                            #     "title": "Upcoming Events",
                            #     "url": "https://karenkashop.com/events",
                            #     "webview_height_ratio": "tall"
                            # },
                            {"type": "postback",
                             "title": "Send request to shop manager",
                             "payload": "human"}
                        ]
                    }
                ]}
        self.set_get_started(get_st)
        self.set_persistent_menu(menu)
        if payload in self.getstarted_payload:
            self.send_message(sender_id, self.message_menu)
        elif payload in self.main_menu_payload:
            self.send_message(sender_id, self.message_menu)
        elif payload in self.shop_payload:
            self.show_products(sender_id)
        elif payload == 'human':
            self.user_name = self.get_user_info(sender_id)
            self.tag = 'Talk with human'
            message = {
                "text": "Tap your mailbox below to send data",
                "quick_replies": [
                    {
                        "content_type": "user_email",

                    }
                ]

            }
            self.send_message(sender_id, message)
        elif payload == 'custom':
            self.user_name = self.get_user_info(sender_id)
            self.tag = 'Create custom request'
            message = {
                "text": "Tap your mailbox below to send data",
                "quick_replies": [
                    {
                        "content_type": "user_email",

                    }
                ]

            }
            self.send_message(sender_id, message)

        else:
            print(f' NA postback: {messaging_event}')


