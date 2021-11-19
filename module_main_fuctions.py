import os, json, re
from config_con import *
import ftplib
from pythonping import ping


class MAIN_FUNC(object):

    def __init__(self):
        self.first = ''
        self.json_filename = ''


    def cut_spaces(self, s):
        i = 0
        if s.find(" ") > -1:
            while s[i] == ' ':
                s = s[1:]
            while s[len(s)-1] == ' ':
                s = s[:-1]
                i = 1
            while i < len(s)-1:
                if s[i] == ' ' and s[i+1] == ' ':
                    s = s[:i+1] + s[i+2:]
                else:
                    i += 1
        return s


    def save_json_data(self, data, name):
        with open(name, "w") as data_file:
            json.dump(data, data_file, indent=2)
        data_file.close()

    def load_json_data(self, filename):
        DATA = None
        if os.path.exists(filename):
            with open(filename, "r") as cfile:
                str1 = cfile.read()
                DATA = json.loads(str1)
            cfile.close()
        return DATA

    def delete_item_from_list(self, list):
        i = len(list) - 1
        while i > -1:
            if list[i]['name'] == 'Material':
                del list[i]
            i -= 1

    def regex_mail(self, text):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if (re.fullmatch(regex, text)):
            mail = text
            return mail

    def version(self, package):
        print(package.__version__)

    def reg_ftp(self):
        host = REG_FTP_HOST
        user = REG_FTP_USER
        passwd = REG_FTP_PASS
        port = int(REG_FTP_PORT)

        server = ftplib.FTP()
        try:
            server.connect(host, port)
            print('Success!')
        except Exception as error:
            print(f' Error: {error}')
        try:
            server.login(user, passwd)
            server.dir()
            print('Success!')
        except Exception as error:
            print(f' Error: {error}')

    def printenumerate(self, dict):
        try:
            for index, (key, value) in enumerate(dict.items()):
                print(f'{index}){key}: {value}')
            return 'Success!', 200
        except Exception as error:
            print(f' Error: {error}')

    def ping(self, site='karenkashop.com'):
        try:
            ping(site, verbose=True)
            return 'Success!', 200
        except Exception as error:
            print(f' Error: {error}')




#
# m1 = MAIN_FUNC()
# texttosend = f'*** ALERTS FROM SITE ***\n\n ' \
#              f'- HOOK - \n' \
#              f'*** DATA ***\n' \
#              f'1. USERNAME: username\n' \
#              f'2. MAIL: email\n'
# m1.telegram_send_message(texttosend)










