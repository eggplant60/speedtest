#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2   # handle PostgreSQL
import json
import subprocess

if __name__ == '__main__':
    # 設定の読み込み
    conf_path = 'db_conf.json'
    with open(conf_path, 'r') as f:
        conf = json.load(f)

    #print(conf)
    
    with psycopg2.connect(
            host = conf['host'],
            port = conf['port'],
            database = conf['dbname'],
            user = conf['user'],
            password = conf['password']) as conn:
        
        with conn.cursor() as cur:

            row = subprocess.check_output(['./speedtest-cli', '--csv']).decode()            
            data = tuple([c.lower().replace(' ', '_') for c in row.strip().split(',')])

            #import pdb; pdb.set_trace()
            cur.execute("INSERT INTO result VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", data)
            conn.commit()



print('complete!')
