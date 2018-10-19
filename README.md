# spyderlab
learn&amp;test code for my spyder

import urllib.request
import urllib.error

#urllib.urlopen的基本使用方式
response = urllib.request.urlopen('http://python.org/')
result = response.read().decode('utf-8')
print(result)

#带有试错和head的健壮代码
try:
    headers ={'User_Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
    response = urllib.request.Request('http://python.org/', headers = headers)
    html = urllib.request.urlopen(response)
    result = html.read().decode('utf-8')
except utllib.error.URLError as e:
    if hasattr(e, 'reason'):
        print('错误原因是' + str(e.reason))
except urllib.error.HTTPError as e:
    if hasattr(e, 'code'):
        print('错误状态码是' + str(e.code))
else:
    print('请求成功通过')
