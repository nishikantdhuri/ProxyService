from flask import Flask,request,Response,Blueprint,redirect,url_for
import time
from flask_login import current_user,login_required,fresh_login_required
import requests
import os
from app import login_manager
SITE_NAME1 = os.environ['SITE1']#'http://127.0.0.1:81'
SITE_NAME2 = os.environ['SITE2']#'http://127.0.0.1:82'
curr_req=''
count=0
map_port={'81':SITE_NAME1,'82':SITE_NAME2}
states={'81':['CLOSED',0,0],'82':['CLOSED',0,0]}
general_bp=Blueprint('general_bp',__name__,url_prefix='/home')

def check_if_running(url):
    try:
        resp = requests.get(url)
        if resp.status_code != 200:
            return False
        return True
    except Exception as ex:
        return False


def circuit_breaker(url):
    if states[url.split(':')[2][0:2]][0] == 'CLOSED':
        if check_if_running(url):
            states[url.split(':')[2][0:2]] = ['CLOSED', 0, 0]
            return (url, True)
        else:
            while states[url.split(':')[2][0:2]][1] <= 5:
                states[url.split(':')[2][0:2]][1] = int(states[url.split(':')[2][0:2]][1]) + 1
                if check_if_running(url):
                    states[url.split(':')[2][0:2]] = ['CLOSED', 0, 0]
                    break
            if states[url.split(':')[2][0:2]][1] != 0:
                states[url.split(':')[2][0:2]][0] = 'OPEN'
                circuit_breaker(url)
            else:
                return (url, True)
    elif states[url.split(':')[2][0:2]][0] == 'OPEN':
        states[url.split(':')[2][0:2]][2] = int(states[url.split(':')[2][0:2]][2]) + 1
        if states[url.split(':')[2][0:2]][2] > 3:
            states[url.split(':')[2][0:2]][0] = 'HALF-OPEN'
            circuit_breaker(url)
        else:
            return (url, False)
    else:
        if check_if_running(url):
            states[url.split(':')[2][0:2]] = ['CLOSED', 0, 0]
        else:
            states[url.split(':')[2][0:2]] = ['OPEN', 0, 0]
        circuit_breaker(url)


# ath:path>',methods=['GET','POST','DELETE'])
@general_bp.route('/<path:path>', methods=['GET', 'POST', 'DELETE'])
#@login_manager.login_required
@login_required
#@fresh_login_required
def proxy(path):
    if current_user.is_authenticated:

        global SITE_NAME1, curr_req, SITE_NAME2
        if curr_req == '':
            curr_req = SITE_NAME1
        elif curr_req == SITE_NAME1:
            curr_req = SITE_NAME2
        else:
            curr_req = SITE_NAME1

        curr_req1 = circuit_breaker(curr_req)
        if curr_req1 and curr_req1[1]:
            curr_req1 = curr_req1[0]
            if request.method == 'GET':
                resp = requests.get(str(curr_req1) + '/' + str(path))
                excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
                headers = [(name, value) for (name, value) in resp.raw.headers.items() if
                           name.lower() not in excluded_headers]
                response = Response(resp.content, resp.status_code, headers)
                return response
            elif request.method == 'POST':
                resp = requests.post(str(curr_req1) + '/' + str(path), json=request.get_json())
                excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
                headers = [(name, value) for (name, value) in resp.raw.headers.items() if
                           name.lower() not in excluded_headers]
                response = Response(resp.content, resp.status_code, headers)
                return response
            elif request.method == 'DELETE':
                resp = requests.delete(str(curr_req1) + '/' + str(path)).content
                response = Response(resp.content, resp.status_code, '')
                return response
        else:
            return 'Error'
    else:
        redirect(url_for('auth_bp.login_page'))