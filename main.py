# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import flask
import time
import uuid
import threading

from pages import PAGES, Page
from survey import SURVEY
from simple_server import SocketServer

from flask import flash, redirect, render_template, request, session, url_for

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
SOCKET_SERVER_IP = "0.0.0.0" # Might require change
SOCKET_SERVER_PORT = 8080 # Might require change
SERVER = None

def send_data(class_label):
    global trialNum
    print("sending!")

    milliSec = int(round(time.time() * 1000))  # Get current time in milliseconds
    data = "{};{};{};\n".format(trialNum, class_label, milliSec)
    trialNum += 1 # increment trial number
    SERVER.broadcast(data)

""" Runs the server in a separate thread
    :param host: Server ip address
    :param port: Server port
"""
def open_server(host, port):
    global sockett
    connected = openSocket()
    if connected:
        print("Connected sockett")
    t1 = threading.Thread(target=run_server, args=(SOCKET_SERVER_IP, SOCKET_SERVER_PORT))
    t1.start()

""" Initiate the server
    :param host: Server ip address
    :param port: Server port
"""
def run_server(host, port):
    print("Opening server")
    global SERVER
    SERVER = SocketServer(SOCKET_SERVER_IP, SOCKET_SERVER_PORT)
    SERVER.accept_connections()

@app.route('/question/')
def question_start():
    send_data('baselinestart')
    session['uid'] = uuid.uuid1()
    time.sleep(3)
    send_data('baselineend')
    time.sleep(0.5)
    send_data('easystart')
    return redirect(url_for('question', page=0))

@app.route('/question/<int:page>', methods=['GET', 'POST'])
def question(page):
    global canSendMarker
    page_str = str(page)

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
                    send_data('easyend')
                    # I didn't change canSendMarker to false here because I need to send hard start when the new page 10 is loaded

                if page == len(PAGES) - 1: # I finished the hard and will start survey so I will send hardend before starting the survey
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

    return render_template('survey.html', survey_num=survey_num, next_page=next_page, url=SURVEY[survey_num - 1])

