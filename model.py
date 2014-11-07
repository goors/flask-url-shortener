from DB import *
from flask import json, redirect
from UrlGenerator import encode_url
import time


class model:

    def is_safe(key, url):
        response = requests.get(URL.format(key=key, url=url))

        return response.text != 'malware'
    
    def get_url_stats(self, short_url):

        db = DB()

        parts = short_url.split("/",3)

        sql = '''SELECT clicks, short_url FROM links WHERE short_url=%s'''

        query = db.query(sql, (parts[3], ))

        link = query.fetchone()
        if link is not None:
            db.close()
            return self.format_result(link['clicks'], 1, "Clicks on link "+short_url)

        return self.format_result(None, 0, "Error"), 404


    def make_short_url(self, url):
    
        import requests

        key = 'AIzaSyBwCHhPcVAdwZJH-hlTU4WM_sHe8-_SGYU'
        URL = 'https://sb-ssl.google.com/safebrowsing/api/lookup?client=Safe&key={key}&appver=1.5.2&pver=3.1&url={url}'


        if(is_safe(key, url))

            db = DB()

            sql = '''SELECT id, short_url FROM links WHERE long_url=%s'''
            query = db.query(sql, (url, ))

            link = query.fetchone()

            if link is not None:
                db.close()
                return self.format_result("http://goo.rs/"+link['short_url'], 1, "Links already exists")

            else:

                sql = '''SELECT MAX(id) as id FROM links'''
                query = db.query(sql)
                id = query.fetchone()
                if id is not None:
                    short_url = encode_url(id['id'])
                else:
                    short_url = encode_url(1)
                sql = '''INSERT INTO links(id, long_url, short_url, clicks , u_id, created) VALUES (NULL, %s, %s, %s ,%s, %s )'''
                db.query(sql, (url, short_url, 0, 2, time.strftime('%Y-%m-%d %H:%M:%S') ))

            return self.format_result("http://goo.rs/"+short_url, 1, 'Url created')



    def format_result(self, result, status, message):
        response = {'response': result, 'status': status, 'message': message}
        return json.jsonify(response)

    def redirect(self, url):


        db = DB()

        sql = '''SELECT id, long_url FROM links WHERE short_url=%s'''

        query = db.query(sql, (url,))

        link = query.fetchone()
        if link is not None :

            sql = '''UPDATE links SET clicks=clicks+1 WHERE id=%s'''
            db.query(sql, (link['id'], ))
            db.close()


            return (link['long_url'])

        return False



