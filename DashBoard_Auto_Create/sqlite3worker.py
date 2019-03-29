# -*- coding: utf-8 -*-

import pprint
import commands
import time
import sqlite3
import json
import random
import string

from jsonbase import FOLDER_JSON, BOARD_SKEL, BOARD_BODY


class Sqlite3Worker:
    server_ip = ''

    def __init__(self, file_path):
        self.sqlite3_conn = sqlite3.connect(file_path)
        self.sqlite3_conn.text_factory = str
        self.sqlite3_cursor = self.sqlite3_conn.cursor()

    def _db_insert(self, value):
        sql = """INSERT INTO dashboard (version, slug, title, data, org_id, 
             created, updated, updated_by, created_by, gnet_id, 
             plugin_id, folder_id, is_folder, has_acl, uid)
              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        try:
            self.sqlite3_cursor.execute(sql, value)
            self.sqlite3_conn.commit()
        except sqlite3.IntegrityError as e:
            print('Insert  Error: {err} IP={ip} '.format(err=e.args[0], ip=self.server_ip))

    def _get_iface(self):
        cmd = 'curl -s -G \'http://localhost:8086/query?pretty=true\' --data-urlencode "db=scouterCounter" --data-urlencode "q=SHOW TAG VALUES FROM "traffic_test"  WITH KEY = "InterFace" WHERE ("IP" = \'{ip}\')"'.format(
            ip=self.server_ip)
        (exitstatus, outtext) = commands.getstatusoutput(cmd)
        if exitstatus == 0:
            data = json.loads(outtext)
            return data['results'][0]['series'][0]['values']
        else:
            print(exitstatus)
            print('\n_get_iface Function Check')
            exit(1)

    def _get_random(self):
        uid_length = random.randint(8, 20)
        string_pool = string.ascii_letters + string.digits  # string.punctuation 에러발생하여 사용 중단
        result = ""
        for i in range(uid_length):
            result += random.choice(string_pool)
        return result

    def create_dir(self, title):
        uid = self._get_random()
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        load = json.loads(FOLDER_JSON)
        load['title'] = title.decode('utf-8')
        load['uid'] = uid
        json_data = json.dumps(load, ensure_ascii=False)
        value = [1, title, title, json_data, 1, date, date, 1, 1, 0, '', 0, 1, 0, uid]
        self._db_insert(value)

    def create_board(self, title, folder_id):
        uid = self._get_random()
        iface_list = self._get_iface()
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        skel = json.loads(BOARD_SKEL)
        skel['title'] = title.decode('utf-8')
        skel['uid'] = uid
        num = 0
        x = 0
        y = 0

        for list in iface_list:
            body = json.loads(BOARD_BODY)
            body['id'] = num
            body['title'] = self.server_ip + '-' + list[0]      # InfluxDB 1.7 버전은 response 데이터 가 달라 list[1]이다
            body['targets'][0]['tags'][0]['value'] = self.server_ip
            body['targets'][0]['tags'][1]['value'] = list[0]
            num += 1
            if x == 0:
                body['gridPos']['x'] = 0
                body['gridPos']['y'] = y
                x += 1
            elif x == 1:
                body['gridPos']['x'] = body['gridPos']['w']
                body['gridPos']['y'] = y
                x -= 1
                y += body['gridPos']['h']
            skel['panels'].append(body)
        json_data = json.dumps(skel, ensure_ascii=False)
        value = [1, title, title, json_data, 1, date, date, 1, 1, 0, '', folder_id, 0, 0, uid]
        self._db_insert(value)

    def select_dir(self, title):
        sql = "SELECT id FROM dashboard WHERE title = ? AND is_folder = 1"
        try:
            self.sqlite3_cursor.execute(sql, [title])
            return self.sqlite3_cursor.fetchone()
        except sqlite3.IntegrityError as e:
            print('select  error: ', e.args[0])

    def close(self):
        self.sqlite3_cursor.close()
        self.sqlite3_conn.close()
