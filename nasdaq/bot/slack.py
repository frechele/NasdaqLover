from slack_sdk import WebClient

from nasdaq.core.config import CONFIG


class SlackAPI:
    def __init__(self):
        self.config = CONFIG['slack']

        self.client = WebClient(self.config['token'])

    def send_message(self, message: str):
        self.client.chat_postMessage(channel='stock-bot',
            blocks=[
                {
                    'type': 'section',
                    'text': {
                        'type': 'mrkdwn',
                        'text': '답이 없는 장세입니다. 존버하세요.'
                    }
                }
            ],
            text='StockBot alert'
        )

if __name__ == '__main__':
    api = SlackAPI()
    api.send_message('asdf')
