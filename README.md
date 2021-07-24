# Py-BayAreaFastrak

## Background
Py-BayAreaFastrak gives you a python API for your transactions on bayareafastrak.org allowing you to process the data or
hook into whatever notification system you want.

## How
To use the API, create a BayAreaFastrak client with your username and password and call the `get_transactions()` 
function. 

Example:
```
from fastrak import BayAreaFastrak
client = BayAreaFastrak(username="some_user", password="123456")
transactions = client.get_transactions()
print(transactions[0])
# {'post_date': '01/01/1970', 'transaction_date': '01/01/1970', 'transaction_time': '00:00:00 AM', 
'tag_id': '12345678', 'description': 'Bay Bridge', 'debit': 6.0, 'credit': 0, 'net': 6.0, 'balance': 100}
```

### Requirements
* Beautifulsoup4 
```
pip install beautifulsoup4
```
Note: For better or for worse, I plan to remove this dependency in the future and use my own parser so that there are 
no external dependencies. Might be a bad idea, but bs4 seems a bit bloated for what I need to do and I've already 
implemented a simple HTML parser for extracting the form token

## Notes
Given that the library parses HTML to achieve its functionality, things are liable to break if and when Bayareafastrak 
changes their interface so please file issues if something is not working as expected

## Contributions
Any contributions are welcome. Please make a PR with any proposed changes.

## TODO
### Relatively important
* Handle site session longevity
  * It's untested how long the authenticated session lasts for
* Convert transaction date to Python timestamp
* Add date filtering functionality
* Make `get_transactions()` a generator to yield new results whenever transactions show up
* Replace BeautifulSoup stuff with vanilla Python?
  * Maybe use HtmlElParser
    * slower and less pretty but fewer dependencies

### Kinda important
* Publish to pypi while I still have a unique name for the repo
* Add a Dockerfile
* Add a HTTP server to expose this as an API
  
### Not important
* Figure out how to use an asterisk in markdown lol

## Footnotes
*: apparently newer Fastrak flex modules don't even beep anymore