from graia.application.message.elements.internal import App

def __set_data(d):
    result = '"data":[ '
    for key, content in d:
        result += "{"+f'"title":"{key}", "value":"{content}"'+"},"
    result = result[:-1] +' ]'
    return result

def __set_button(b):
    result = '"button":[ '
    for name in b:
        result += "{"+f'"name":"{name}", "action":""'+"},"
    result = result[:-1] +' ]'
    return result


u = 'https://static-s.aa-cdn.net/img/ios/1454663939/3359d0e7d8badb7f9a4ac0e2149ebb15?v=1'

def miniapp(prompt="咕咕", app_name="白咕咕", icon_url=u, title="咕咕咕~咕咕咕~", app_data=[], app_button=[]):
    data = __set_data(app_data)
    button = __set_button(app_button)
    content = '{"prompt":"['+prompt+']","app":"com.tencent.miniapp","appID":"","ver":"0.0.0.1","view":"notification","meta":{"notification":{"appInfo":{"appName":"'+app_name+'","appType":4,"iconUrl":"'+icon_url+'"},"title":"'+title+'",'+data+','+button+'} } }'
    return App(type='App', content=content)
