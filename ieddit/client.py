from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote_plus
from ._2captcha import _2Captcha
import re, requests

class Client:

    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0"
    IEDDIT = lambda e: urljoin("https://ieddit.com/", e)

    def __init__(self, username, password, _2captcha_api_key, do_login = True):

        self.username = username
        self.password = password
        self.logged_in = False

        self._2captcha = _2Captcha(_2captcha_api_key)

        self.session = requests.Session()
        self.session.headers.update({"User-Agent": Client.USER_AGENT})

        if do_login:
            self.login()

    def _require_login(func):
        def wrapper(self, *args, **kwargs):
            assert self.logged_in, func.__name__ + " requires client to be authenticated."
            return func(self, *args, **kwargs)
        return wrapper

    def login(self):
        
        params = {
            "username": self.username,
            "password": self.password
        }

        response = self.session.get(Client.IEDDIT("/login/"))
        response = self.session.post(Client.IEDDIT("/login/"), params)
        cookies = self.session.cookies.get_dict()

        assert response.status_code == 200, "ieddit returned unexpected status code [{}]".format(response.status_code)
        assert not response.url.endswith("/login/"), "login failed :(\n" + response.text
        self.logged_in = True

    @_require_login
    def create_post(self, title, sub, url = "", text = "", nsfw = False):

        # send get request and create html parser
        response = self.session.get(Client.IEDDIT("/create_post"))
        parser = BeautifulSoup(response.text, "html.parser")

        # find base64 captcha data and solve
        img = parser.select_one(".captcha-div img")
        base64 = img["src"].split()[1]       
        answer = self._2captcha.solve(base64)
        assert answer, "failed to solve captcha :("

        params = {
            "url": url,
            "self_post_text": text,
            "title": title,
            "sub": sub,
            "captcha": answer
        }

        response = self.session.post(Client.IEDDIT("/create_post"), params)
        post_url = response.url

        pattern = r"\/i\/{}\/(\d+)\/".format(sub)
        match = re.search(pattern, post_url)

        assert match, "failed to create post: [{}] => {}".format(response.status_code, response.text)
        post_id = int(match.group(1))

        if nsfw:
            params = { "post_id": post_id }
            self.session.post(Client.IEDDIT("/user/nsfw"), params)
            
        return post_id, post_url