from webwhatsapi import WhatsAPIDriver
from webwhatsapi import WhatsAPIDriverStatus
from webwhatsapi.objects.message import Message
import os
import time
import subprocess
# os.environ["PATH"] += os.pathsep + \
'D:\\Programming\\Python\\WebDriver\\geckodriver.exe'


class NewMessageObserver:
    def on_message_received(self, new_messages):
        for message in new_messages:
            if message.type == "chat":
                print(
                    "New message '{}' received from number {}".format(
                        message.content, message.sender.id
                    )
                )
            else:
                print(
                    "New message of type '{}' received from number {}".format(
                        message.type, message.sender.id
                    )
                )


class whatsapp:
    def __init__(self):
        self.driver = WhatsAPIDriver(username='Fabian')
        WhatsAPIDriver._SELECTORS = {
            'firstrun': "#wrapper",
            'qrCode': "canvas[aria-label='Scan me!']",
            'qrCodePlain': "div[data-ref]",
            'mainPage': ".two",
            'chatList': ".infinite-list-viewport",
            'messageList': "#main > div > div:nth-child(1) > div > div.message-list",
            'unreadMessageBar': "#main > div > div:nth-child(1) > div > div.message-list > div.msg-unread",
            'searchBar': ".input",
            'searchCancel': ".icon-search-morph",
            'chats': ".infinite-list-item",
            'chatBar': 'div.input',
            'sendButton': 'button.icon:nth-child(3)',
            'LoadHistory': '.btn-more',
            'UnreadBadge': '.icon-meta',
            'UnreadChatBanner': '.message-list',
            'ReconnectLink': '.action',
            'WhatsappQrIcon': 'span.icon:nth-child(2)',
            'QRReloader': 'div[data-ref] > span > div'
        }

        self.driver.get_qr('qr.png')
        subprocess.call(r'qr.png', shell=True)

        print("Waiting for QR")
        self.driver.wait_for_login()
        print("Bot started")

    def getMessages(self):
        self.driver.get_all_chats()


wa = whatsapp()
wa.getMessages()
wa.driver.get_battery_level()
