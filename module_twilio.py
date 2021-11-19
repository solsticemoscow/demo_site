from config_con import *

from twilio.twiml.messaging_response import MessagingResponse
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

client = Client(TWILIO_ACCOUNT, TWILIO_TOKEN)


class TWILIO(object):

    def __init__(self):
        self.first = ''
        self.json_filename = ''
        self.number = TWILIO_NUM_SOL
        # self.authy_api = AuthyApiClient(TWILIO_AUTHY_API_KEY)

    def send_msg_to_whatsup(self, body='TEST!', from_number=TWILIO_NUM_SANDBOX, to_number=TWILIO_NUM_KARENKA):
        client.messages.create(body=body,
                           from_=f'whatsapp:{from_number}',
                           to=f'whatsapp:{to_number}')
        print('Success!')
        return 200


    def send_sms_to_number_sid(self, body='TEST!', number=TWILIO_NUM_SOL):
        try:
            message = client.messages.create(
                messaging_service_sid='MGff06cf854baa65409e0a193bcf5883d6',
                body=body,
                to=number
            )
            print('Success!')
        except Exception as error:
            print(f' Error: {error}')

    def send_sms_to_number(self, body='TEST SMS!', from_number=TWILIO_NUM_SERVICE1, to_number=TWILIO_NUM_SOL):
        try:
            message = client.messages \
                .create(
                body=body,
                from_=from_number,
                to=to_number
            )
            print('Success!')
            print(message.sid)
        except Exception as error:
            print(f' Error: {error}')

    def verification_send(self, to_number=TWILIO_NUM_SOL):
        try:
            verification = client.verify \
                .services('VAc670b528137bc65b301c0dd63f51839c') \
                .verifications \
                .create(to=to_number, channel='sms')
            print(verification.status, verification.sid)
            return verification.sid
        except Exception as error:
            print(f' Error: {error}')

    def verification_check(self, to_number=TWILIO_NUM_SOL, user_code='123456'):
        try:
            verification_check = client.verify \
                .services('VAc670b528137bc65b301c0dd63f51839c') \
                .verification_checks \
                .create(to=to_number, code=user_code)
            print(verification_check.status)
            return verification_check.status
        except Exception as error:
            print(f' Error: {error}')

    # def authy_app(self):
    #     sms = self.authy_api.users.request_sms(self.authy_api)
    #     if sms.ok():
    #         print(sms.content)
    #         print('Success!')
    #     else:
    #         print(f' Error')






#
#
# w1 = TWILIO()
# w1.send_msg_to_whatsup(body='TEST!', from_number=TWILIO_NUM_SANDBOX, to_number=TWILIO_NUM_KARENKA)
# # w1.verification_send()
# w1.verification_check(to_number=TWILIO_NUM_SOL, user_code='8785')



