import requests, json, time

class _2Captcha:

    _default_params = lambda s: { "key": s.api_key, "json": 1 } 

    def __init__(self, api_key):
        self.api_url = "https://2captcha.com/"
        self.api_key = api_key

    def check(self, request_id):

        params = self._default_params()
        params["action"] = "get"
        params["id"] = request_id

        response = requests.post(self.api_url + "res.php", params)
        if response.status_code != 200:
            raise Exception("unexpected status code checking 2captcha request [{}]".format(response.status_code))

        data = json.loads(response.text)
        valid = data.get("status") == 1 or data.get("request") == "CAPCHA_NOT_READY"
        if not valid:
            raise Exception("captcha unsolved:\n" + json.dumps(data, indent = 4))

        return data["request"] if data["status"] == 1 else None

    def create(self, img):
        
        params = self._default_params()
        params["method"] = "base64"
        params["body"] = img

        response = requests.post(self.api_url + "in.php", params)
        if response.status_code != 200:
            raise Exception("unexpected status code creating 2captcha request [{}]".format(response.status_code))

        data = json.loads(response.text)
        valid = data.get("status") == 1 and "request" in data.keys()
        if not valid:
            raise Exception("failed to create 2captcha request:\n" + json.dumps(data, indent = 4))

        return data["request"]
    
    def solve(self, img):
        request_id = self.create(img)
        answer = None
        loops = 0
        time.sleep(10)
        while not answer and loops < 10:
            time.sleep(5)
            loops += 1
            answer = self.check(request_id)
        return answer
