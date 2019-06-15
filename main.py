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
    def __init__(self, chinese, answer, hint='', error_count_before_hint=2, show_survey=0,
                is_test=False, marker_data = ''):
        self.chinese = chinese
        self.answer = answer
        self.error_count_before_hint = error_count_before_hint
        self.hint = hint
        self.show_survey = show_survey
        self.is_test = is_test
        self.marker_data = marker_data


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
    Page('红', 'red'),
    Page('黄', 'yellow'),

    Page('红', 'red', is_test = True, marker_data = 'easystart'),
    Page('黄', 'yellow', is_test = True),
    Page('红', 'red', is_test = True),
    Page('红', 'red', is_test = True),
    Page('黄', 'yellow', is_test = True),

    Page('黄', 'yellow', is_test = True, marker_data='easyend'),

    Page('黑', 'black', hint='黑 = black'),
    Page('橙', 'orange', hint='橙 = orange'),
    Page('棕', 'brown', hint='棕 = brown'),
    Page('粉', 'pink', hint='粉 = pink'),
    Page('白', 'white', hint='白 = white'),
    Page('白 棕 粉', 'white brown pink'),
    Page('橙 绿 蓝', 'orange green blue'),
    Page('黑 红 粉', 'black red pink'),
    Page('黄 棕 蓝', 'yellow brown blue'),

    Page('橙 红 蓝', 'orange red blue', is_test=True, marker_data = 'hardstart'),
    Page('黑 红 粉', 'black red pink', is_test=True),
    Page('黄 棕 白', 'yellow brown white', is_test=True),
    Page('橙 粉 黑', 'orange pink black', is_test=True),
    Page('黑 红 粉', 'black red pink', is_test=True),

    Page('绿 黄 白', 'green yellow white', is_test=True,
    marker_data='hardend'),

    Page('食', 'food', hint='食 = food'),
    Page('水', 'water', hint='水 = water'),
    Page('奶', 'milk', hint='奶 = milk'),
    Page('食', 'food'),
    Page('奶', 'milk'),
    Page('水', 'water'),
    Page('食', 'food'),
    Page('水', 'water'),
    Page('奶', 'milk'),

    Page('水', 'water', is_test=True, marker_data = 'easystart'),
    Page('食', 'food', is_test=True),
    Page('奶', 'milk', is_test=True),
    Page('水', 'water', is_test=True),
    Page('奶', 'milk', is_test=True),
    Page('食', 'food', is_test=True,
    marker_data='easyend'),

    Page('菠', 'spinach', hint='菠 = spinach'),
    Page('茶', 'tea', hint='茶 = tea'),
    Page('渴', 'thirsty', hint='渴 = thirsty'),
    Page('菠', 'spinach', hint='菠 = spinach'),
    Page('饺', 'dumpling', hint='饺 = dumpling'),
    Page('菠 茶 奶', 'spinach tea milk'),
    Page('食 水 渴', 'food water thirsty'),
    Page('饺 茶 菠', 'dumpling tea spinach'),
    Page('茶 茶 渴', 'tea tea thirsty'),

    Page('饺 茶 菠', 'dumpling tea spinach', is_test=True, marker_data = 'hardstart'),
    Page('菠 茶 奶', 'spinach tea milk', is_test=True),
    Page('食 水 渴', 'food water thirsty', is_test=True),
    Page('茶 茶 渴', 'tea tea thirsty', is_test=True),
    Page('水 茶 饺', 'water tea dumpling', is_test=True),
    Page('黑 水 茶', 'black water tea', is_test=True, marker_data='hardend'),

    Page('狗', 'dog', hint='狗 = dog'),
    Page('猫', 'cat', hint='猫 = cat'),
    Page('龟', 'turtle', hint='龟 = turtle'),
    Page('猫', 'cat'),
    Page('龟', 'turtle'),
    Page('狗', 'dog'),
    Page('龟', 'turtle'),

    Page('狗', 'dog', is_test=True, marker_data = 'easystart'),
    Page('龟', 'turtle', is_test=True),
    Page('狗', 'dog', is_test=True),
    Page('猫', 'cat', is_test=True),
    Page('龟', 'turtle', is_test=True),
    Page('猫', 'cat', is_test=True, marker_data='easyend'),

    Page('山', 'mountain', hint='山 = mountain'),
    Page('河', 'river', hint='河 = river'),
    Page('云', 'cloud', hint='云 = cloud'),
    Page('雨', 'rain', hint='雨 = rain'),
    Page('海', 'sea', hint='海 = sea'),
    Page('雨 河 云', ' rain river cloud'),
    Page('山 河 海', 'mountain river sea'),
    Page('云 海 雨', 'cloud sea rain'),
    Page('山 云 雨', 'mountain cloud rain'),

    Page('雨 河 云', 'rain river cloud', is_test=True, marker_data = 'hardstart'),
    Page('云 海 雨', 'cloud sea rain', is_test=True),
    Page('云 雨 河', 'cloud rain river', is_test=True),
    Page('山 河 海', 'mountain river sea', is_test=True),
    Page('河 云 山', 'river cloud mountain', is_test=True),

    Page('山 云 雨', 'mountain cloud rain', is_test=True, marker_data='hardend')

    # Page('', '', hint=''),
    # Page('', '', hint=''),
    # Page('', '', hint=''),
    # Page('', '', hint=''),
    # Page('', '', hint=''),
    # Page('', ''),
    # Page('', ''),
    # Page('', ''),
    # Page('', ''),
    #
    # Page('', '', is_test=True, marker_data = 'hardstart'),
    # Page('', '', is_test=True),
    # Page('', '', is_test=True),
    # Page('', '', is_test=True),
    # Page('', '', is_test=True),
    #
    # Page('', '', is_test=True,
    # marker_data='hardend'),
    #
    # Page('', '', hint=''),
    # Page('', '', hint=''),
    # Page('', '', hint=''),
    # Page('', '', hint=''),
    # Page('', '', hint=''),
    # Page('', ''),
    # Page('', ''),
    # Page('', ''),
    # Page('', ''),
    #
    # Page('', '', is_test=True, marker_data = 'hardstart'),
    # Page('', '', is_test=True),
    # Page('', '', is_test=True),
    # Page('', '', is_test=True),
    # Page('', '', is_test=True),
    #
    # Page('', '', is_test=True,
    # marker_data='hardend'),
    #
    # Page('', '', hint=''),
    # Page('', '', hint=''),
    # Page('', '', hint=''),
    # Page('', '', hint=''),
    # Page('', '', hint=''),
    # Page('', ''),
    # Page('', ''),
    # Page('', ''),
    # Page('', ''),
    #
    # Page('', '', is_test=True, marker_data = 'hardstart'),
    # Page('', '', is_test=True),
    # Page('', '', is_test=True),
    # Page('', '', is_test=True),
    # Page('', '', is_test=True),
    #
    # Page('', '', is_test=True,
    # marker_data='hardend'),
    #
    # Page('', '', hint=''),
    # Page('', '', hint=''),
    # Page('', '', hint=''),
    # Page('', '', hint=''),
    # Page('', '', hint=''),
    # Page('', ''),
    # Page('', ''),
    # Page('', ''),
    # Page('', ''),
    #
    # Page('', '', is_test=True, marker_data = 'hardstart'),
    # Page('', '', is_test=True),
    # Page('', '', is_test=True),
    # Page('', '', is_test=True),
    # Page('', '', is_test=True),
    #
    # Page('', '', is_test=True,
    # marker_data='hardend'),
    #
    # Page('', '', hint=''),
    # Page('', '', hint=''),
    # Page('', '', hint=''),
    # Page('', '', hint=''),
    # Page('', '', hint=''),
    # Page('', ''),
    # Page('', ''),
    # Page('', ''),
    # Page('', ''),
    #
    # Page('', '', is_test=True, marker_data = 'hardstart'),
    # Page('', '', is_test=True),
    # Page('', '', is_test=True),
    # Page('', '', is_test=True),
    # Page('', '', is_test=True),
    #
    # Page('', '', is_test=True,
    # marker_data='hardend')
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
    if "end" in classLabel:
        trialNum += 1 # increment trial number only after an end trial.

@app.route('/question/')
def question_start():
    sendData('baselinestart')
    session['uid'] = uuid.uuid1()
    time.sleep(3)
    sendData('baselineend')
    time.sleep(0.5)
    # sendData('easystart')
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
    # if canSendMarker:
    #     if page == 10: # I will start with hard tasks
    #         sendData('hardstart')
    #         canSendMarker = False # prevent from sending markers on wrong answers

    if page >= len(PAGES):
        session.pop('error_count')
        session.pop('uid')
        return render_template("cong.html")

    # Adding condition for method!=POST so, we only send marker when page loads,
    # not twice, for when page loads, and when the user submits an answer.
    if PAGES[page].marker_data!='' and request.method!='POST':
        sendData(PAGES[page].marker_data)

    if request.method == 'POST':
        expect = PAGES[page].answer

        if expect == '':
            return redirect(url_for('question', page=page + 1))
        got = request.form['answer']
        if got != expect:
            if PAGES[page].is_test:
                return redirect(url_for('question', page=page+1))
            else:
                session['error_count'][page_str] += 1
                flash('Wrong!')
                return redirect(url_for('question', page=page))
        else: # means the answer is correct
            # canSendMarker = True
            # if canSendMarker:
            #     if page == 9: # I finished the easy and will start survey so I will send easyend before starting the survey
            #         sendData('easyend')
            #         # I didn't change canSendMarker to false here because I need to send hard start when the new page 10 is loaded
            #
            #     if page == len(PAGES) - 1: # I finished the hard and will start survey so I will send hardend before starting the survey
            #         sendData('hardend')

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
