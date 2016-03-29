# Crawler Exercice
## Goals:
The main goal of this tech task is to write a news crawler. In order to simply the requirements you should only crawl the "ARA.cat" news site. Your script should work as follows:

1. Go into "ARA.cat" website;
2. Gather all news URLs;
3. Count the number of vowels for each article;
4. Return the number of vowels for each resource (key-value representation)

## Goals resolution:
For the tech task to write a news crawler I decided to use the [scrapy](http://scrapy.org/) framework because is so powerful (based in Twisted, then asynchronous fast requests), well documented and very confortable using xpath or css. Plus benefit the port to python3 in the last months, I wanted to try it. With other options, getting the source with any library like urllib, using parsers like Beautifulsoup or lxml, are great for few urls, but if you have a lot of urls and want to do it quicky then need some asynchronous, multiprocess or threat library.

### Installing:
First, is recommended to use a virtual environment. With python3 it's easy:
```
$ python3 -m venv venv
$ . venv/bin/activate
(venv)$
```
Then you can proceed to intall scrapy for python3:
```
(env)$ pip install scrapy==1.1.0rc1
```
### Comments:
 - I used RSS feed (xml file) for obtain the urls.
 - I used an OrderedDict() for save the data in order because is more easy to verify all ok.
 - I used 'COOKIES_ENABLED': False settings because without this not all the urls loading well.

## Bonus:
1. Persist the results in a database (e.g., SQLite) and expose a ReST API to access some statistics (by article, by day, etc);
2. Implement another statistic that returns the average size of images in a article;
3. Create a ReST API end-point that receives an URL and crawls in on-demand;
4. Use of a Continuous Integration system (Hint: TravisCI)

## Bonus resolution:
### Bonus 1:
For persist the results I decided to use SQLite database without any ORM because are few operations. The database is structured with a nametable type date (i.e., date29032016) and columns of Id, Web, Vowels.
For the ReST API are many options in the market. For big projects and good performance exists big frameworks like Django, CherryPY, Tornado, etc., but also can do it very well with little frameworks o microframeworks like webpy, web2py, eve, falcon, flask, bottle, etc. For this exercice I decided to use bottle because carry on a webserver (others like falcon needs install gunicorn) and is faster than flask (falcon web-benchmarks).

### Installing:
You need install bottle:
```
(venv)$ pip install bottle
```
### Bonus 1 Comments:
 - This ReST API use only method='GET'
     - url: http://localhost:8080/bonus1
       - data received: json with db table names
     - url: http://localhost:8080/bonus1/<date>
       - data received: json with db table name items by id
     - url: http://localhost:8080/bonus1/<date>/<id>
       - data received: json with id item information

### Bonus 2:
Don't implemented because the images are loaded through javascript and scrapy by default doesn't run it. The unique visible images in the article are always the same, static images in the header and footer. The solution to this problem is add more libraries to execute javascript and extract 'height' and 'width' attributes and calculate the average.

### Bonus 3:
Another ReST API with bottle, but this case using another method (POST) with format json. You need to send 'url' and 'xpath' for the crawler. This time the crawler isn't scrapy. I decided to use urllib for the request and lxml for the parser (installed automatically when install scrapy) because is only one url and the speed and code is optimum.

### Bonus 3 Comments:
  - This ReST API use only method='POST'
      - url: http://localhost:8080/bonus3
        - data send: json {"url":"", "xpath":""}

### Bonus 4:
Don't implemented because when I had read the exercice I didn't know the Continuous Integration concept and let this question for the last. So I didn't update my git branche in every successful code test like CI says.

## Last Comments:
 - I prefer to separate in diferent modules the principal exercice and the bonus for better maintainability and test.
 - I created a Ctrl-C KeyboardInterrupt signal for bottle server because seems that maybe Twisted reactor block this exception and then bottle server doesn't respond to this keys.

## Run:
For run the program execute:
```
(venv)$ python3 crawler.py
```
