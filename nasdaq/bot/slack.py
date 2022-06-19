from slack_sdk import WebClient

from nasdaq.core.config import CONFIG


class SlackAPI:
    def __init__(self):
        self.config = CONFIG['slack']

        self.client = WebClient(self.config['token'])

    def send_message(self, blocks):
        self.client.chat_postMessage(channel='stock-bot',
            blocks=blocks,
            text='StockBot alert'
        )

if __name__ == '__main__':
    api = SlackAPI()
    api.send_message('asdf')
