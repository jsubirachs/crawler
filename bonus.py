#!/usr/bin/env python3


from bottle import route, request
import sqlite3 as lite
import json
from urllib import request as urlrequest
from lxml import etree


DB = 'ara.db'


@route('/bonus1', method='GET')
def bonus1_tables():
    '''
    RestAPI Bonus1 exercice.
    url: http://localhost:8080/bonus1
    method: GET
    data received: json with db table names
    '''
    db = lite.connect(DB)
    with db:
        cursor = db.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        return {
            'days': [i[0] for i in tables if i[0] != "sqlite_sequence"]
            }


@route('/bonus1/<date>', method='GET')
def bonus1_date(date):
    '''
    RestAPI Bonus1 exercice.
    url: http://localhost:8080/bonus1/<date>
    method: GET
    data received: json with db table name items by id
    '''
    db = lite.connect(DB)
    with db:
        cursor = db.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'"
                       " and name=?",(date,))
        table = cursor.fetchall()
        if len(table) != 0:
            cursor.execute("SELECT * FROM " + table[0][0])
            items = cursor.fetchall()
            return {
                'urls': [{'id': i[0], 'web': i[1]} for i in items]
            }
        else:
            return "Table name doesn't exists!\n"


@route('/bonus1/<date>/<id>', method='GET')
def bonus1_date(date, id):
    '''
    RestAPI Bonus1 exercice.
    url: http://localhost:8080/bonus1/<date>/<id>
    method: GET
    data received: json with id item information
    '''
    db = lite.connect(DB)
    with db:
        cursor = db.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'"
                       " and name=?",(date,))
        table = cursor.fetchall()
        if len(table) != 0:
            cursor.execute("SELECT web,vowels FROM " + table[0][0] +
                           " WHERE id=?",(id,))
            item = cursor.fetchall()
            if len(item) != 0:
                return {
                    'item': [{
                        'id': id,
                        'web': item[0][0],
                        'vowels': item[0][1]
                        }]
                    }
            else:
                return "ID number doesn't exists!\n"
        else:
            return "Table name doesn't exists!\n"


@route('/bonus3', method='POST')
def bonus3_url():
    '''
    RestAPI endpoint Bonus3 exercice.
    url: http://localhost:8080/bonus3
    method: POST
    data send: json {"url":"", "xpath":""}
    '''
    data = request.body.readline()
    if not data:
        return 'No data received\n'
    crawler = json.loads(data.decode('utf-8'))
    for i in ('url', 'xpath'):
        if i not in crawler.keys():
            return "JSON POST need 'url' and 'xpath' keys!\n"
    url = crawler['url']
    xpath = crawler['xpath']
    try:        
        page = urlrequest.urlopen(url)
    except:
        return "Invalid Url or server down!\n"
    htmlparser = etree.HTMLParser()
    source = etree.parse(page, htmlparser)
    try:
        data = ' '.join(source.xpath(xpath))
    except:
        return "Invalid xpath expression!\n"
    return {
        'url': url,
        'xpath': xpath,
        'data': data,
        }


if __name__ == "__main__":
    from bottle import run


    run(host='localhost', port=8080)
