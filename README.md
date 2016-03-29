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
First, is recommended to use a virtual environtment. With python3 its easy:
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
 - I use an OrderedDict() for save the data in order because is more easy to verify thats crawl ok.
 - I use 'COOKIES_ENABLED': False settings because without this not all the urls loading well.

## Bonus:
1. Persist the results in a database (e.g., SQLite) and expose a ReST API to access some statistics (by article, by day, etc);
2. Implement another statistic that returns the average size of images in a article;
3. Create a ReST API end-point that receives an URL and crawls in on-demand;
4. Use of a Continuous Integration system (Hint: TravisCI)
5. 

## Bonus resolution:
### Bonus 1:
For persist the results I decided to use SQLite database without any ORM because are few operations. The database is structured with a nametable type date (i.e., date29032016) and columns of Id, Web, Vowels.
For the ReST API are many options in the market. For big projects and good performance are big frameworks like Django, CherryPY, Tornado, etc., but also can do it very well with little framekorks o microframeworks like webpy, web2py, eve, falcon, flask, bottle, etc. For this exercice I decided to use bottle because carry on a webserver (others like falcon need install gunicorn) and is faster than flask (falcon web-benchmarks).

### Installing:
You need install bottle:
```
(venv)$ pip install bottle
```
