#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json

from flask import Flask
from flask import render_template
from flask import request
from flask import g

from .manager import ydl_manger

app = Flask(__name__)

def invalid_request():
    return json.dumps({'status': 'error', 'errmsg': 'invalid_request'})


def success():
    return json.dumps({'status': 'success'})


@app.errorhandler(404)
def not_found(error):
    return '404 not found'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/task', methods=['POST'])
def add_task():
    manager = server.get_manager()

    tid = manager.create_task({'url': request.form['url']})
    manager.start_task(tid)
    return json.dumps({'tid': tid})


@app.route('/task/list', methods=['GET'])
def list_task():
    manager = server.get_manager()

    state = request.args.get('state', 'all')

    l = manager.list_tasks(state)
    return json.dumps(l)


@app.route('/task/state_coutner', methods=['GET'])
def list_state():
    manager = server.get_manager()
    l = manager.state_list()
    return json.dumps(l)


@app.route('/task/tid/<tid>', methods=['DELETE'])
def delete_task(tid):
    manager = server.get_manager()

    act = request.args.get('del_data', None)

    if act == 'true':
        manager.delete_task(tid, True)
    else:
        manager.delete_task(tid)

    return success()


@app.route('/task/tid/<tid>/status', methods=['GET'])
def query_task(tid):
    manager = server.get_manager()

    exerpt = request.args.get('exerpt', None)

    if exerpt == 'true':
        status = manager.query_task(tid, exerpt=True)
    else:
        status = manager.query_task(tid)

    return json.dumps(status)


@app.route('/task/tid/<tid>', methods=['PUT'])
def manipulate_task(tid):
    manager = server.get_manager()

    act = request.args.get('act', None)
    if act is None:
        return invalid_request()

    if act == 'pause':
        manager.pause_task(tid)
    elif act == 'resume':
        manager.resume_task(tid)
    else:
        return json.dumps({'status': 'error', 'errmsg': 'unknow action'})

    return success()


class server():
    manager = None
    def __init__(self, conf):
        global app
        self.app = app
        self.conf = conf
        self.manager = None


    def run(self):
        self.app.run(host=self.conf.host, port=self.conf.port)


    def bind_ydl_manager(self, ydl_manager):
        self.manager = ydl_manager
        server.manager = ydl_manager

    @staticmethod
    def get_manager():
        manager = getattr(g, 'manager', None)
        if manager is None:
            #  manager = g.manager = manager
            manager = g.manager = server.manager
        return manager


