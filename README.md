# Py-BayAreaFastrak

## Background
Whenever we (Californians) drive past a Fastrak checkpoint during off hours or on the weekends, don't you always wonder 
if the Fastrak corporation actually turned off the sensors* and did not charge you or whether your Fastrack tag is 
actually registered. Finding Fastrak's backend and UI a bit antiquated? Well fear not, Py-BayAreaFastrak gives you
a python API to parse said transactions allowing you to hook into whatever notification system you want!

## How
To use the API, create a BayAreaFastrak client with your username and password and call the `get_transactions()` 
function. Example:
```
from fastrak import BayAreaFastrak
client = BayAreaFastrak(username="some_user", password="123456")
transactions = client.get_transactions()
```

## Notes
Given that the library is uses HTML parsing to achieve it's functionality, things are liable to 
break. Please file issues when things do.


## Contributions
Any contributions are welcome. Please make a PR with any proposed changes.

## TODO
### Relatively important
* Handle site session longevity
    * it's untested how long the authenticated sesion lasts for
* Make `get_transactions()` a generator to yield new results whenever they are loaded
* Replace some of the BeautifulSoup stuff with vanilla Python?

### Kinda important
* Publish to pypi while I still have a unique name
* Add a Dockerfile and HTTP server to expose this as an API
  
### Not important
* figure out how to use an asterick in markdown lol

## Footnotes
*: apparently newer Fastrak flex modules don't even beep anymore