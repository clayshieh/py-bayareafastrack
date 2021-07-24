from datetime import datetime
from html.parser import HTMLParser
import logging
import re
import requests

from bs4 import BeautifulSoup

logging.basicConfig()
logger = logging.getLogger(__name__)


class HtmlEl(object):
    """HtmlEl is a structure that holds the raw information from HtmlElParser"""

    def __init__(self, tag, attrs=None):
        self.tag = tag
        self.attrs = attrs
        self.data = None


class HtmlElParser(HTMLParser):
    """
    HtmlElParser is a basic python html parser that implements some search functionality to find the correct element
    """

    def __init__(self, tag, key=None):
        super().__init__()
        self.toi = tag
        self.key = key  # lambda function for checking

        self.results = list()
        self.el = None

    def handle_starttag(self, tag, attrs) -> None:
        if tag == self.toi:
            self.el = HtmlEl(tag, attrs)

    def handle_endtag(self, tag) -> None:
        if tag == self.toi and self.el:
            # either no check or check passes
            if self.key is None or self.key is not None and self.key(self.el):
                self.results.append(self.el)
            self.el = None

    def handle_data(self, data) -> None:
        if self.el:
            self.el.data = data


class BayAreaFastrak(object):
    """BayAreaFastrak implements a client for other libraries to query the transaction records"""

    class Transaction(object):
        post_datetime_format = "%m/%d/%Y"
        transaction_datetime_format = "%m/%d/%Y %I:%M:%S %p"

        def __init__(self, post_date, transaction_date, transaction_time, tag_id, description, debit, credit, balance):
            self.post_datetime = datetime.strptime(post_date, BayAreaFastrak.Transaction.post_datetime_format)
            self.transaction_datetime = datetime.strptime(f"{transaction_date} {transaction_time}",
                                                          BayAreaFastrak.Transaction.transaction_datetime_format)
            self.tag_id = tag_id
            self.description = description
            self.debit = format_currency(debit) if debit else 0.0
            self.credit = format_currency(credit) if credit else 0.0
            self.net = self.debit - self.credit
            self.balance = format_currency(balance)

        def __repr__(self):
            return str(self.__dict__)

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()

        # init functions
        self.login()

    def login(self, remember_me=False) -> None:
        logger.info("Attempting to login to bayareafastrak.org...")
        url = "https://www.bayareafastrak.org/vector/account/home/accountLogin.do"
        params = {
            "btnLogin.x": 1,
            "btnLogin.y": 1,
            "formid": "frmLogin"
        }
        data = {
            "formid": "frmLogin",
            "login": self.username,
            "loginPassword": self.password,
            "rememberMe": remember_me,
            "btnLogin": "",
            "ctokenElem": self.get_login_token()
        }
        resp = self.session.post(url, params=params, data=data)
        if resp.status_code != 200:
            raise Exception("failed to login")
        logger.info("successfully logged in")

    def get_login_token(self) -> str:
        url = "https://www.bayareafastrak.org/vector/account/home/accountLogin.do"
        resp = self.session.get(url)
        if resp.status_code != 200:
            raise Exception("failed to get login page")

        # low effort
        parser = HtmlElParser("script", key=lambda el: el.data and "ctokenElem" in el.data)
        parser.feed(resp.text)
        if len(parser.results) != 1:
            raise Exception("failed to find token script element")
        token_el = parser.results[0]

        results = re.search("value=\"(.*)\" name=\"ctokenElem\"", token_el.data).groups()
        if len(results) != 1:
            raise Exception(f"did not find token in script element, results: {results}")
        logger.info("got login token")
        return results[0]

    def get_transactions(self):
        url = "https://www.bayareafastrak.org/vector/account/transactions/batatransactionSearch.do"
        resp = self.session.get(url)
        if resp.status_code != 200:
            raise Exception("failed to get transactions")
        return self.extract_transactions(resp.text)

    @staticmethod
    def extract_transactions(data):
        ret = list()
        soup = BeautifulSoup(data, 'html.parser')
        transaction_table_el = soup.find("table", id="transactionItem")
        transaction_table_body = transaction_table_el.find("tbody")
        transaction_table_rows = transaction_table_body.find_all("tr")
        for transaction_table_row in transaction_table_rows:
            row_data = [data.get_text().strip() for data in transaction_table_row.find_all("td")]
            ret.append(BayAreaFastrak.Transaction(*row_data))
        return ret


# Helper functions
def format_currency(currency_data: str) -> float:
    remove_characters = ["$", "(", ")"]
    ret = ""
    for c in currency_data:
        if c not in remove_characters:
            ret += c
    return float(ret)
