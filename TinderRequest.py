import requests

GET_USER_API = 'https://api.gotinder.com/v2/recs/core?locale=en'
LIKE_USER_API = 'https://api.gotinder.com/like'


class TinderRequest:
    def __init__(self, tokenKey):
        self._session = requests.Session()
        headers = {'x-auth-token': tokenKey}
        self._session .headers.update(headers)

    @property
    def session(self):
        return self._session

    def get_user_list(self):
        return self.session.get(GET_USER_API)

    def user_like_req_log(self, response, message):
        if(response.status_code == 200):
            return message
        else:
            return "oops, can't seem to swipe"

    def send_and_log_user_like(self, user, message):
        print(f'sending: {user.id}, {user.s_number}, {message}')
        url = f'{LIKE_USER_API}/{user.id}?locale=en'
        postRes = self.session.post(url, data={'s_number': user.s_number})
        return self.user_like_req_log(postRes, message)
