import requests

class Client:

    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0"

    def __init__(self, username, password):

        self.username = username
        self.password = password
        self.logged_in = False

        self.session = requests.Session()
        self.session.headers.update({"User-Agent": Client.USER_AGENT})

    def _require_login(func):
        def wrapper(self, *args, **kwargs):
            assert self.logged_in, func.__name__ + " requires client to be authenticated."
            func(self, *args, **kwargs)
        return wrapper

    def login(self):
        
        params = {
            "username": self.username,
            "password": self.password
        }
    
        response = self.session.post("https://ieddit.com/login/", params)
        cookies = self.session.cookies.get_dict()

        assert response.status_code == 200, "ieddit returned unexpected status code [{}]".format(response.status_code)
        assert "session" in cookies.keys(), "ieddit response missing session cookie"
        self.logged_in = True

    