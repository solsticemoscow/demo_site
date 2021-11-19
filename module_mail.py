import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime


class Mail(object):

    def __init__(self):
        self.REG_MAIL_SMTP = 'mail.karenkashop.com'
        self.REG_MAIL_PORT = 587
        self.REG_MAIL_USER = 'smtp@karenkashop.com'
        self.REG_MAIL_PASS = '************'

        self.REG_MAIL_FROM = 'info@karenkashop.com'
        self.REG_MAIL_SUBJECT = 'TEST'
        self.REG_MAIL_TO = 'alexander.tsyrkun@gmail.com'
        self.REG_MAIL_TEXT = 'TEST'

    def send_simple_text_mail(self, text='Default from KarenkaShop.', to='karenka@karenkashop.com', sbj='ALERT FROM KARENKASHOP'):
        try:
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

            me = self.REG_MAIL_USER
            you = to
            mail_pass = self.REG_MAIL_PASS
            msg = MIMEMultipart()
            msg['Subject'] = sbj
            msg['From'] = me
            msg['To'] = you
            message_text = MIMEText(text)
            msg.attach(message_text)

            s = smtplib.SMTP('mail.karenkashop.com', 587)
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(me, mail_pass)
            s.sendmail(me, you, msg.as_string())
            s.quit()
            print('Send mail successfully.')
        except Exception as error:
            print(f'Send mail error! Text: {error}')
            return error

    # def send_html_mail(self, text='Default from KarenkaShop.', to='alexander.tsyrkun@gmail.com'):
    #     try:
    #         now = datetime.now()
    #         dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    #         me = 'smtp@karenkashop.com'
    #         you = to
    #         mail_pass = 'E8RRSeM4XATKVgQ'
    #         msg = MIMEMultipart()
    #         msg['Subject'] = 'FROM KARENKASHOP INFO'
    #         msg['From'] = me
    #         msg['To'] = you
    #         message_text = text
    #
    #         html = codecs.open("email_trackship.html", 'r')
    #         html = html.read()
    #         part1 = MIMEText(message_text, 'plain')
    #         part2 = MIMEText(html, 'html')
    #
    #         msg.attach(part1)
    #         msg.attach(part2)
    #
    #         s = smtplib.SMTP('mail.karenkashop.com', 587)
    #         s.ehlo()
    #         s.starttls()
    #         s.ehlo()
    #         s.login(me, mail_pass)
    #         s.sendmail(me, you, msg.as_string())
    #         s.quit()
    #         print('Send mail successfully.')
    #     except Exception as error:
    #         print(f'Send mail error! {error}')
    #         return error
    #
    # def replace_html(self, order_id, track_id):
    #
    #     order_id = str(order_id)
    #     track_id = str(track_id)
    #     # html = codecs.open("email_trackship.html", 'r')
    #     # html = html.read()
    #     base = os.path.dirname(os.path.abspath(__file__))
    #     html = open(os.path.join(base, "email_trackship.html"))
    #
    #     soup = bs(html, 'html.parser')
    #
    #     old_order_id_text = soup.find("h3").get_text()
    #     o = old_order_id_text[13:23]
    #
    #
    #     # href = "http://{track_ship}"
    #     #
    #     #
    #     old_track_id = soup.find("a", {'class': "mcnButton"})
    #
    #
    #     # print(f' old_order_id: {old_order_id}')
    #     # print(f' old_track_id: {old_track_id}')
    #
    #     # new_order_id = old_order_id_text.find(text=re.compile(('{order_id}')).replace_with(order_id)
    #     #
    #     # new_track_id = old_track_id.find(text=re.compile('{track_ship}')).replace_with(track_id)
    #     # print(new_order_id, new_track_id)
    #     #
    #     # with open("email_trackship.html", "wb") as f_output:
    #     #     f_output.write(soup.prettify("utf-8"))






# mail1 = Mail()
# #
# texttosend = f'User  request live agent.'
# #
# mail1.send_simple_text_mail()










