import pymysql
import json

db = pymysql.connect(db='fb_networks',host='localhost',user='root',passwd='', charset = 'utf8')

def initialize():
    cur = db.cursor()
    table = '''CREATE TABLE IF NOT EXISTS friend_attributes (uid VARCHAR(255), first_name VARCHAR(255),middle_name VARCHAR(255),last_name VARCHAR(255),name VARCHAR(255),pic VARCHAR(255),religion VARCHAR(255),birthday_date VARCHAR(255),sex VARCHAR(255), hometown_location VARCHAR(255),current_location VARCHAR(255),relationship_status VARCHAR(255),significant_other_id VARCHAR(255),political VARCHAR(255),locale VARCHAR(255), profile_url VARCHAR(255),website VARCHAR(255));'''
    cur.execute(table)
    edges = '''CREATE TABLE IF NOT EXISTS friend_edges (uid1 VARCHAR(255),uid2 VARCHAR(255));'''
    cur.execute(edges)
    #put data
    friend_attributes = []
    f = open('friend_attributes.json')
    data = json.load(f)
    fr_atr = data
    f.close()
    for atr in fr_atr:
        friend_attributes.append((atr['uid'], atr['first_name'],atr['middle_name'],atr['last_name'],atr['name'], atr['pic'],atr['religion'],atr['birthday_date'],atr['sex'],json.dumps(atr['hometown_location']),json.dumps(atr['current_location']),atr['relationship_status'],atr['significant_other_id'],atr['political'],atr['locale'],atr['profile_url'],atr['website']))
    friend_edges = []
    f = open('friend_edges.json')
    data = json.load(f)
    edges = data
    f.close()
    for e in edges:
        friend_edges.append((e['uid1'], e['uid2']))
    ins = '''INSERT INTO friend_attributes (uid, first_name, middle_name, last_name, name, pic, religion, birthday_date, sex, hometown_location, current_location, relationship_status, significant_other_id, political, locale, profile_url, website) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
    cur.executemany(ins, friend_attributes)
    ins = '''INSERT INTO friend_edges (uid1, uid2) VALUES (%s, %s);'''
    cur.executemany(ins, friend_edges)
    db.commit()

