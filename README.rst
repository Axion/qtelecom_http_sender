Реализация HTTP протокола для отправки СМС посредством http://www.qtelecom.ru/

Применение::

    from qtelecom import QTSMS

    username = 'your_username'
    password = 'your_password'
    phone = '80000000000'
    sms_body = 'some text'

    sender = QTSMS(username, password)
    sender.post_sms([phone], sms_body)

При некорректных входных параметрах будет вызвано исключение SMSLengthException

При ошибке отправки будет вызвано исключение ServerException