# -*- coding: utf-8 -*-

import commands
import json

from sqlite3worker import Sqlite3Worker
from boardlist import ADD_lIST

SQLITE_PATH = '/var/lib/grafana/grafana.db'

if __name__ == '__main__':
    sql_worker = Sqlite3Worker(SQLITE_PATH)

    for list in ADD_lIST:
        sql_worker.server_ip = list['add_ip']
        folder_id = sql_worker.select_dir(list['folder_name'])
        if folder_id == None:
            print('{dir} Not Found Create Start IP={ip}'.format(dir=list['folder_name'], ip=list['add_ip']))
            sql_worker.create_dir(list['folder_name'])
            folder_id = sql_worker.select_dir(list['folder_name'])
        else:
            print('Dir Id = {id} IP={ip}'.format(id=folder_id[0], ip=list['add_ip']))

        print('Create Board IP={ip}'.format(ip=list['add_ip']))
        sql_worker.create_board(list['board_name'], folder_id[0])
