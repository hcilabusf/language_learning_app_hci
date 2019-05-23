# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import collections
import logging

import uuid
from datetime import datetime
import time

import flask

from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from SocketClass import Socket_Class # import the socket class to send markers

#from Data import User

app = flask.Flask(__name__)

app.config['DEBUG'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.debug = True

app.secret_key = 'dfasdfasdfasdf'


class Page(object):
    def __init__(self, chinese, answer, hint='', error_count_before_hint=2, show_survey=0):
        self.chinese = chinese
        self.answer = answer
        self.error_count_before_hint = error_count_before_hint
        self.hint = hint
        self.show_survey = show_survey


SURVEY = [
    'https://docs.google.com/forms/d/e/1FAIpQLSeSlLSn8VEeDRvt5S1orlTDUd-Io0N8WNHhobFihuTOqvEoTA/viewform?embedded=true',
    'https://docs.google.com/forms/d/e/1FAIpQLSc7KVv-Csr8IqZWqWF_5TMfvLUz9A2tNwaZ-V4eafoAMdMxwQ/viewform?embedded=true',
    'https://docs.google.com/forms/d/e/1FAIpQLSfqjfzXdnizoZ3voFvV9zHJGwFI8lmSXWSjtuDCQibD4fY1Aw/viewform?embedded=true']

PAGES = [
    Page('红', 'red', hint='红 = red'),
    Page('黄', 'yellow', hint='黄 = yellow'),
    Page('红', 'red'),
    Page('黄', 'yellow'),
    Page('红', 'red'),
    Page('黄', 'yellow'),
    Page('红', 'red'),
    Page('黄', 'yellow'),
    Page('红', 'red'),
    Page('黄', 'yellow', show_survey=1),

    Page('黑', 'black', hint='黑 = black'),
    Page('橙', 'orange', hint='橙 = orange'),
    Page('棕', 'brown', hint='棕 = brown'),
    Page('粉', 'pink', hint='粉 = pink'),
    Page('白', 'white', hint='白 = white'),
    Page('白 棕 粉', 'white brown pink'),
    Page('橙 绿 蓝', 'orange green blue'),
    Page('黑 红 粉', 'black red pink'),
    Page('紫 棕 蓝', 'purple brown blue'),
    Page('绿 黄 白', 'green yellow white', show_survey=3),
]

'''Page('绿', 'green', hint='绿 = green'),
    Page('绿', 'green'),
    Page('紫', 'purple', hint='紫 = purple'),
    Page('紫', 'purple'),
    Page('绿 紫', 'green purple'),
    Page('紫 绿', 'purple green'),
    Page('蓝', 'blue', hint='蓝 = blue'),
    Page('蓝', 'blue'),
    Page('蓝 绿', 'blue green'),
    Page('紫 蓝', 'purple blue', show_survey=2),'''

trialNum = 0
canSendMarker = False
sockett = None # socket variable created

"""
A function that opens a socket with Matlab PC
"""
def openSocket ():
    global sockett
    try:
        #sockett = Socket_Class("192.168.2.201", 30000) # dor matlab server
        sockett = Socket_Class("127.0.0.1", 8080) # for dummy server
        if sockett == None:
            return False
        return sockett.openSocket()
    except Exception as e:
        print(e)
        return False

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
    sendData('baselinestart')
    session['uid'] = uuid.uuid1()
    time.sleep(3)
    sendData('baselineend')
    time.sleep(0.5)
    sendData('easystart')
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
            sendData('hardstart')
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
                    sendData('easyend')
                    # I didn't change canSendMarker to false here because I need to send hard start when the new page 10 is loaded

                if page == len(PAGES) - 1: # I finished the hard and will start survey so I will send hardend before starting the survey
                    sendData('hardend')

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
    if openSocket():
        session.pop('error_count', None)
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
