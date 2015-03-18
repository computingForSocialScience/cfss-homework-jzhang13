import matplotlib.pyplot as plt
import networkx as nx
import json
import pymysql
from flask import Flask, request, render_template, redirect
from create_tables import *
import tempfile

db = pymysql.connect(db='fb_networks', host = 'localhost', user = 'root', passwd = '', charset='utf8')

app = Flask(__name__)

@app.route('/')
def index():
    cur = db.cursor()
    cur.execute('SELECT uid, name FROM friend_attributes;')
    friendlist = cur.fetchall()[:100]
    return render_template('index.html', friends = friendlist)

@app.route('/profile/<userid>')
def profile(userid):
    cur = db.cursor()
    cur.execute('SELECT name, pic, sex, birthday_date, profile_url FROM friend_attributes WHERE uid = %s;', userid)
    atr = cur.fetchall()[:100] 
    a = atr[0] #a[0-4] are name/pic/sex/birthday/profile_url
    cur.execute('SELECT uid1, uid2 FROM friend_edges WHERE uid1 = %s;', a[0])
    friends = cur.fetchall()[:100]
    G = nx.Graph()
    G.add_edges_from(friends)
    friends_with_id = []
    for f in friends: 
        cur.execute('SELECT uid FROM friend_attributes WHERE name = %s LIMIT 1;', f[1])
        uid = cur.fetchall()
        if uid != ():
            friends_with_id.append((uid[0][0], f[1]))
        #testing
    nx.draw(G)
    f = tempfile.NamedTemporaryFile(dir='static/temp',suffix='.png',delete=False)
    plt.savefig(f)
    f.close()
    graph_url = f.name.split('\\')[-1]
    #testing

    return render_template('profile.html', name = a[0], pic = a[1], sex = a[2], birthday = a[3], profile_url = a[4], friends_with_id = friends_with_id, graph_url = graph_url)
        
@app.route('/upload/', methods = ['GET', 'POST'])
def upload():
    if request.method == 'POST':
        friend_attributes = []
        f = request.form['friend_attributes']
        data = json.load(f)
        fr_atr = data
        for atr in fr_atr:
            friend_attributes.append((atr['uid'], atr['first_name'],atr['middle_name'],atr['last_name'],atr['name'], atr['pic'],atr['religion'],atr['birthday_date'],atr['sex'],json.dumps(atr['hometown_location']),json.dumps(atr['current_location']),atr['relationship_status'],atr['significant_other_id'],atr['political'],atr['locale'],atr['profile_url'],atr['website']))
        friend_edges = []
        f = request.form['friend_edges']
        data = json.load(f)
        edges = data
        for e in edges:
            friend_edges.append((e['uid1'], e['uid2']))
        cur = db.cursor()
        cur.execute('DROP TABLE IF EXISTS friend_attributes;')
        cur.execute('DROP TABLE IF EXISTS friend_edges;')
        initialize()
        ins = '''INSERT INTO friend_attributes (uid, first_name, middle_name, last_name, name, pic, religion, birthday_date, sex, hometown_location, current_location, relationship_status, significant_other_id, political, locale, profile_url, website) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
        cur.executemany(ins, friend_attributes)
        ins = '''INSERT INTO friend_edges (uid1, uid2) VALUES (%s, %s);'''
        cur.executemany(ins, friend_edges)
        db.commit()
        return redirect('/')
    else:
        return render_template('upload.html')

if __name__ == '__main__':
    cur = db.cursor()
    cur.execute('DROP TABLE IF EXISTS friend_attributes;')
    cur.execute('DROP TABLE IF EXISTS friend_edges;')
    initialize()
    app.debug = True
    app.run()
