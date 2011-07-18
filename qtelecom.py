# -*- coding: utf-8 -*-
"""Отправка СМС сообщений посредством HTTP API qtelecom.ru"""
# pylint: disable=R0902,W0142,R0903,R0201,R0914,R0912,R0915,R0913
import urllib
import urllib2
import StringIO
import gzip
from xml.dom.minidom import parseString


class SMSLengthException(Exception):
    """Maximum length is 480 characters"""
    pass

class ServerException(Exception):
    """Maximum length is 480 characters"""
    pass


class QTSMS:

    def __init__(self, username, password):

        self.__username = username
        self.__password = password
        self.__opener = urllib2.build_opener()

        headers = [
            ('User-Agent', 'qtelecom.ru python API client'),
            ('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
        ]
        self.__opener.addheaders = headers

    def post_sms(self, targets, message, sender = ""):
        if len(message) > 480:
            raise SMSLengthException("SMS length exceed 480 charactes")

        if len(message) < 1:
            raise SMSLengthException("SMS is empty")

        post_data = urllib.urlencode({
            'action': 'post_sms',
            'target': ','.join(targets),
            'sms_type': '',
            'sender': sender,
            'user': self.__username,
            'pass': self.__password,
            'message': message.encode("utf-8")
        })

        data = self.__opener.open("http://service.qtelecom.ru/public/http/", post_data).read()
        data = StringIO.StringIO(data)
        gzipper = gzip.GzipFile(fileobj=data)
        data = gzipper.read()
        response =  parseString(data)

        if len(response.getElementsByTagName('errors')) > 0:
            error = "\n".join([node.childNodes[0].childNodes[0].data
                for node in response.getElementsByTagName('errors')])

            print error
            raise ServerException(error)