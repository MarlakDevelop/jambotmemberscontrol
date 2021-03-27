import requests
from time import sleep


API_SERVER = 'http://127.0.0.1:5000/api/v1'


class Bot:
    token = ''
    chats_with_members = {}

    def friendship_handler(self):
        friendship_offers_to_bot = requests.get(
            f'{API_SERVER}/friendship_offers_to_me',
            params={'search': ''},
            headers={'Authorization': f'Token {self.token}'}
        )
        friendship_offers_by_bot = requests.get(
            f'{API_SERVER}/friendship_offers_by_me',
            params={'search': ''},
            headers={'Authorization': f'Token {self.token}'}
        )
        for pk in list(map(lambda x: x['user']['id'], friendship_offers_to_bot.json()['users'])):
            requests.post(
                f'{API_SERVER}/friendship_offers/create/{pk}',
                data={},
                headers={'Authorization': f'Token {self.token}'}
            )
        for pk in list(map(lambda x: x['user']['id'], friendship_offers_by_bot.json()['users'])):
            requests.delete(
                f'{API_SERVER}/friendship_offers/delete/{pk}',
                headers={'Authorization': f'Token {self.token}'}
            )

    def chats_handler(self):
        chats_with_members = {}
        chats_ids = list(map(lambda x: x['chat']['id'], requests.get(
            f'{API_SERVER}/chats',
            params={'search': ''},
            headers={'Authorization': f'Token {self.token}'}
        ).json()['chats']))
        for pk in chats_ids:
            members = list(map(lambda x: {
                'id': x['member']['member']['user']['id'],
                'username': x['member']['member']['user']['username'],
            }, requests.get(
                f'{API_SERVER}/chat/{pk}/members',
                headers={'Authorization': f'Token {self.token}'}
            ).json()['members']))
            chats_with_members[str(pk)] = members
        for pk in list(filter(lambda x: x in list(self.chats_with_members), list(chats_with_members))):
            for member in chats_with_members[pk]:
                if str(member['id']) not in list(map(lambda x: str(x['id']), self.chats_with_members[pk])):
                    requests.post(
                        f'{API_SERVER}/chat/{pk}/send_message',
                        json={
                            'text': f'Поприветствуем {member["username"]}'
                        },
                        headers={'Authorization': f'Token {self.token}'}
                    )
            for member in self.chats_with_members[pk]:
                if str(member['id']) not in list(map(lambda x: str(x['id']), chats_with_members[pk])):
                    requests.post(
                        f'{API_SERVER}/chat/{pk}/send_message',
                        json={
                            'text': f'Попрощаемся с {member["username"]}'
                        },
                        headers={'Authorization': f'Token {self.token}'}
                    )
        self.chats_with_members = chats_with_members


bot = Bot()
bot.token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MTY4NDQ5MjUsIm5iZiI6MTYxNjg0NDkyNSwianRpIjoiN2IzNGFmOTAtNTdjMS00YWU3LTg2YTktNzc0ZjNkNGVkNjJjIiwiZXhwIjo4ODAxNjg0NDkyNSwiaWRlbnRpdHkiOjMsImZyZXNoIjp0cnVlLCJ0eXBlIjoiYWNjZXNzIn0.iM9sZHdyC83LCPoZsneYWFKDHX6JFR8vlWNRe9Rnfi0'
while True:
    try:
        bot.friendship_handler()
        bot.chats_handler()
    except Exception:
        pass
    sleep(5)
