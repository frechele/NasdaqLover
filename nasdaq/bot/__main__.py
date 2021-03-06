from datetime import datetime
import pandas_market_calendars as mcal

from nasdaq.bot.slack import SlackAPI
from nasdaq.core.database import Database


class Bot:
    def __init__(self):
        self.api = SlackAPI()
        self.db = Database()

        self.table_name_map = {
            'nasdaq': '나스닥',
            'nasdaqFut': '나스닥(선물)',
            'vix': 'VIX 지수',
            'krw': '원화 환율',
            'wti': 'WTI 선물',
        }

    def __call__(self):
        if not self.market_open_check():
            self.alert_holiday()
            return

        self.review_previous_market()


    def market_open_check(self) -> bool:
        nasdaq = mcal.get_calendar('NASDAQ')
        today = datetime.today().strftime('%Y-%m-%d')

        return len(nasdaq.schedule(start_date=today, end_date=today)) != 0


    def alert_holiday(self):
        blocks = [
            {
                'type': 'header',
                'text': {
                    'type': 'plain_text',
                    'text': '휴장 알림'
                }
            },
            {
                'type': 'section',
                'text': {
                    'type': 'plain_text',
                    'text': '금일은 미국 증시 휴장일입니다.'
                }
            }
        ]
        self.api.send_message(blocks)


    def review_previous_market(self):
        blocks = []

        blocks.append({
            'type': 'header',
            'text': {
                'type': 'plain_text',
                'text': '지난 시장 현황'
            }
        })

        for table_name in self.db.table_names:
            df = self.db.get_daily_price(table_name).tail(2)

            prev_close = df.iloc[0]['close']

            today_open = df.iloc[-1]['open']
            today_high = df.iloc[-1]['high']
            today_low = df.iloc[-1]['low']
            today_close = df.iloc[-1]['close']

            today_open_return = (today_open - prev_close) / prev_close * 100
            today_high_return = (today_high - prev_close) / prev_close * 100
            today_low_return = (today_low - prev_close) / prev_close * 100
            today_close_return = (today_close - prev_close) / prev_close * 100

            blocks.append({
                'type': 'section',
                'fields': [
                    {
                        'type': 'mrkdwn',
                        'text': f'*{self.table_name_map[table_name]}*'
                    },
                    {
                        'type': 'mrkdwn',
                        'text': ' '
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f'시가: {today_open:.2f} ({today_open_return:+.2f}%)'
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f'고가: {today_high:.2f} ({today_high_return:+.2f}%)'
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f'저가: {today_low:.2f} ({today_low_return:+.2f}%)'
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f'종가: {today_close:.2f} ({today_close_return:+.2f}%)'
                    }
                ]
            })

        self.api.send_message(blocks)


if __name__ == '__main__':
    bot = Bot()
    bot()
