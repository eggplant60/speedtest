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

    print(conf)

    # DATABASE 作成
    try:
        subprocess.check_call(['createdb', conf['dbname'],
                               '--owner='+conf['user'], '--template=template0'])
    except subprocess.CalledProcessError:
        print('Warn: {}はすでにあります'.format(conf['dbname']))

    """
    # speedtest のヘッダを得る
    header = subprocess.check_output(['./speedtest-cli', '--csv-header'], stdout=f).decode()
    # カラム名はheaderから生成
    columns = [c.lower().replace(' ', '_') for c in header.strip().split(',')]
    """

    # TABLE 作成   
    with psycopg2.connect(
            host = conf['host'],
            port = conf['port'],
            database = conf['dbname'],
            user = conf['user'],
            password = conf['password']) as conn:        
        with conn.cursor() as cur:
            sql = """
            CREATE TABLE IF NOT EXISTS result (
                server_id integer,
                sponsor varchar,    
                server_name varchar,
                timestamp timestamp PRIMARY KEY,
                distance decimal(10,6),
                ping decimal(10,6),
                download decimal(18,6),
                upload decimal(18,6),
                share varchar,
                ip_address varchar
            );
            """
            cur.execute(sql)
            conn.commit()

print('create table')
