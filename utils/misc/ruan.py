import requests


class Ruan:

    def __init__(self, ruan_url, ruan_user, ruan_password):
        self.url = ruan_url
        self.user = ruan_user
        self.password = ruan_password

    def check_card(self, card):
        r = requests.get("{0}:1809/DSUT/hs/FrontExchange/card/{1}"
                         .format(self.url, card), auth=(self.user, self.password))
        result = {"result": r.text, "status_code": r.status_code}

        return result['result']

    def check_balance(self, card):
        r = requests.get("{0}:1809/DSUT/hs/FrontExchange/card/{1}"
                         .format(self.url, card), auth=(self.user, self.password))
        result = {"result": r.text, "status_code": r.status_code}
        balance_code = result["result"].replace('"', '')

        r1 = requests.get("{0}:1809/apiservice/hs/api/cardbalance/{1}"
                               .format(self.url, balance_code), auth=(self.user, self.password))
        balance = {"result": r1.text}

        return balance['result']
