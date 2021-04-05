import requests
import json


class eSputnik:

    def __init__(self, esputnik_url, esputnik_user, esputnik_password,
                 esputnik_address_book_id=None, esputnik_prefix=None):
        self.url = esputnik_url
        self.user = esputnik_user
        self.password = esputnik_password
        self.address_book_id = esputnik_address_book_id
        self.prefix = esputnik_prefix
        self.headers = {"content-type": "application/json"}

    def info(self):
        r = requests.get("{0}/api/v1/version".format(self.url), auth=(self.user, self.password))
        result = {"result": r.text, "status_code": r.status_code}

        return result

    def address_books(self):
        r = requests.get("{0}/api/v1/addressbooks".format(self.url), auth=(self.user, self.password))
        result = {"result": r.text, "status_code": r.status_code}

        return result

    def balance(self):
        r = requests.get("{0}/api/v1/balance".format(self.url), auth=(self.user, self.password))
        result = {"result": r.text, "status_code": r.status_code}

        return result

    def is_contact(self, data):
        r = requests.get("{0}/api/v1/contacts".format(self.url), params=data, auth=(self.user, self.password), headers=self.headers)
        if not r.text:
            return True
        else:
            return False

    def add_contact(self, info):
        data = {"addressBookId": self.address_book_id, "firstName": info["first_name"],
                "channels": {"type": "email", "value": info["email"]},
                "groups": {"name": "{0}{1}".format(info["group"], self.prefix)}}
        if not self.is_contact(data):
            r = requests.post("{0}/api/v1/contact".format(self.url), data=json.dumps(data), auth=(self.user, self.password), headers=self.headers)
            result = {"result": r.text, "status_code": r.status_code}

            return result

    def remove_contact(self, id):
        r = requests.delete("{0}/api/v1/contact/{1}".format(self.url, id), auth=(self.user, self.password), headers=self.headers)
        result = {"result": r.text, "status_code": r.status_code}

        return result

    def get_contact(self, id):
        r = requests.get("{0}/api/v1/contact/{1}".format(self.url, id), auth=(self.user, self.password), headers=self.headers)
        result = {"result": r.text, "status_code": r.status_code}

        return result

    def update_contact(self, id, info):
        data = {"addressBookId": self.address_book_id, "firstName": info["first_name"],
                "channels": {"type": "email", "value": info["email"]},
                "groups": {"name": "{0}{1}".format(info["group"], self.prefix)}}
        requests.put("{0}/api/v1/contact/{1}".format(self.url, id), data=json.dumps(data), auth=(self.user, self.password), headers=self.headers)

        return True
