import urllib.request
import urllib.response
import http.client
import http.cookiejar
import hashlib
import random
import time


def hex_md5(strIn):
    md5 = hashlib.md5()
    md5.update(strIn.encode('utf-8'))
    return md5.hexdigest()


def request_ajax_url(url, body, referer=None, cookie=None, **headers):
    req = urllib.request.Request(url)
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Requested-With', 'XMLHttpRequest')

    if cookie:
        req.add_header('Cookie', cookie)

    if referer:
        req.add_header('Referer', referer)

    if headers:
        for k in headers.keys():
            req.add_header(k, headers[k])

    # postBody = json.dumps(body)
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    urllib.request.install_opener(opener)
    response = urllib.request.urlopen(req, body)

    if response:
        return response, cj


data = {'username': 'admin', 'password': hex_md5("12344321")}
result, cj = request_ajax_url("http://tendawifi.com/login/Auth",
                              "username=admin&password=00a1f187721c63501356bf791e69382c".encode('utf-8'))
print(result.getcode())
print(result.getheaders())
if result.getcode() != 200:
    exit(0)

cookiePassword = None
for cookie in cj:
    if cookie.name == "password":
        cookiePassword = cookie.value

if cookiePassword == None:
    exit(0)

while True:
    data = "%f&_=%d" % (random.random(), int(time.time()))

    print("data:" + data)
    result = request_ajax_url("http://tendawifi.com/goform/GetRouterStatus", data.encode('utf-8'), None,
                              "password=%s" % cookiePassword)
    print(result[0].read())
    result = request_ajax_url("http://tendawifi.com/goform/WifiApScan", data.encode('utf-8'), None,
                              "password=%s" % cookiePassword)
    print(result[0].read())
    time.sleep(1)
