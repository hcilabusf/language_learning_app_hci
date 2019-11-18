# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import collections
import flask
import logging
import time
import uuid
from _thread import start_new_thread
import threading

from datetime import datetime
from pages import PAGES, Page
from survey import SURVEY
from socketserver2 import SocketServer

from flask import flash, redirect, render_template, request, session, url_for
from SocketClass import Socket_Class # import the socket class to send markers
from simple_websocket_server import WebSocketServer, WebSocket

#from Data import User

app = flask.Flask(__name__)

app.config['DEBUG'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.debug = True

app.secret_key = 'dfasdfasdfasdf'

trialNum = 0
canSendMarker = False
sockett = None # socket variable created
#SOCKET_SERVER_IP = "127.0.0.1"
#SOCKET_SERVER_IP = "192.168.1.100"
SOCKET_SERVER_IP = "0.0.0.0"
SOCKET_SERVER_PORT = 8080
SERVER = None

def send_data(class_label):
    global trialNum
    print("sending!")

    milliSec = int(round(time.time() * 1000))  # Get current time in milliseconds
    data = "{};{};{};\n".format(trialNum, class_label, milliSec)
    #data = str(trialNum) +";"+classLabel+";" + str(milliSec) + ";\n"
    trialNum += 1 # increment trial number
    SERVER.broadcast(data)
    #SERVER.server.send(data.encode())
    #sockett.sendData(data)
    #sockett.sendData(data)

"""
A function that opens a socket with Matlab PC
"""
def openSocket():
    global sockett
    try:
        print("Opening socket!")
        #sockett = Socket_Class("192.168.2.201", 30000) # dor matlab server
        sockett = Socket_Class(SOCKET_SERVER_IP, SOCKET_SERVER_PORT) # for dummy server
        if sockett == None:
            return False
        return sockett.openSocket()
    except Exception as e:
        print(e)
        return False

def open_server(host, port):
    global sockett
    connected = openSocket()
    if connected:
        print("Connected sockett")
    t1 = threading.Thread(target=run_server, args=(SOCKET_SERVER_IP, SOCKET_SERVER_PORT))
    t1.start()

def run_server(host, port):
    print("Opening server")
    global SERVER
    SERVER = SocketServer(SOCKET_SERVER_IP, SOCKET_SERVER_PORT)
    SERVER.accept_connections()


'''
A function that sends the marker's data through socket class and increment trial number
'''
def sendData (classLabel):
    global sockett, trialNum

    milliSec = int(round(time.time() * 1000))  # Get current time in milliseconds
    data = str(trialNum) +";"+classLabel+";" + str(milliSec) + ";\n"
    sockett.sendData(data)
    trialNum += 1 # increment trial number

@app.route('/question/')
def question_start():
    #sendData('baselinestart')
    send_data('baselinestart')
    session['uid'] = uuid.uuid1()
    time.sleep(3)
    #sendData('baselineend')
    send_data('baselineend')
    time.sleep(0.5)
    #sendData('easystart')
    send_data('easystart')
    return redirect(url_for('question', page=0))

@app.route('/question/<int:page>', methods=['GET', 'POST'])
def question(page):
    global canSendMarker
    page_str = str(page)

    '''if page == 2:
        user = User(name=str(session['uid']), pageId=page, time=str(datetime.now()), message='begin easy test')
        user.put()

    if page == 10:
        user = User(name=str(session['uid']), pageId=page, time=str(datetime.now()),
                    message='end survey 1, begin med test')
        user.put()

    if page == 25:
        user = User(name=str(session['uid']), pageId=page, time=str(datetime.now()),
                    message='end survey 2, begin hard test')
        user.put()'''

    # this is called after I press next on the survey
    if canSendMarker:
        if page == 10: # I will start with hard tasks
            #sendData('hardstart')
            send_data('hardstart')
            canSendMarker = False # prevent from sending markers on wrong answers

    if page >= len(PAGES):
        session.pop('error_count')
        session.pop('uid')
        return render_template("cong.html")

    if request.method == 'POST':
        expect = PAGES[page].answer
        if expect == '':
            return redirect(url_for('question', page=page + 1))
        got = request.form['answer']
        if got != expect:
            session['error_count'][page_str] += 1
            flash('Wrong!')
            return redirect(url_for('question', page=page))
        else: # means the answer is correct
            canSendMarker = True
            if canSendMarker:
                if page == 9: # I finished the easy and will start survey so I will send easyend before starting the survey
                    #sendData('easyend')
                    send_data('easyend')
                    # I didn't change canSendMarker to false here because I need to send hard start when the new page 10 is loaded

                if page == len(PAGES) - 1: # I finished the hard and will start survey so I will send hardend before starting the survey
                    #sendData('hardend')
                    send_data('hardend')

            if PAGES[page].show_survey != 0:
                return redirect(url_for('survey', survey_num=PAGES[page].show_survey, next_page=page + 1))
            else:
                flash('Correct!')
                session['error_count'][page_str] = 0
                return redirect(url_for('question', page=page + 1))

    if 'error_count' not in session:
        session['error_count'] = {}
    if page_str not in session['error_count']:
        session['error_count'][page_str] = 0

    return render_template('question.html', page=PAGES[page], current_page=page_str)


@app.route('/')
def hello_world():
    #return render_template("welcomePage.html")
    open_server(SOCKET_SERVER_IP, SOCKET_SERVER_PORT)
    return render_template("welcomePage.html")

@app.route('/survey/<int:survey_num>')
def survey(survey_num):
    next_page = request.args.get('next_page')
    message = ''
    if survey_num == 1:
        message = 'end easy test, begin survey'
    if survey_num == 2:
        message = 'end med test, begin survey'
    if survey_num == 3:
        message = 'end hard test, begin survey'

    '''user = User(name=str(session['uid']), pageId=int(next_page), time=str(datetime.now()),
                message=message)
    user.put()'''

    return render_template('survey.html', survey_num=survey_num, next_page=next_page, url=SURVEY[survey_num - 1])

#if __name__ == "__main__":
#    t1 = threading.Thread(target=open_server, args=(SOCKET_SERVER_IP, SOCKET_SERVER_PORT))
#    t2 = threading.Thread(target=app.run)
#
#    t1.start()
#    t2.start()
