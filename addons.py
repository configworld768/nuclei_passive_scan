import mitmproxy.http
from mitmproxy import ctx
from redis.client import Redis


class Counter:
    def __init__(self):
        self.num = 0

    def request(self, flow: mitmproxy.http.HTTPFlow):
        self.num = self.num + 1
        if 'firefox' not in flow.request.host and 'mozilla' not in flow.request.host and "google" not in flow.request.host and 'png' not in flow.request.path and 'ico' not in flow.request.path:
            ctx.log.info("We've seen %d flows" % self.num)
            res_cookies = dict(flow.request.cookies)
            ctx.log.info(res_cookies)
            str_cookie = str(res_cookies)
            str_cookie_1 = str_cookie.replace(':','=').replace("'","")
            ctx.log.info(str_cookie_1)
            scan_url1 = '{}://{}:{}{}'.format(flow.request.scheme,flow.request.host,flow.request.port,flow.request.path)
            scan_url = '\"%s\"' % scan_url1
            cookies =  " " + "-H" + " "  + "\"cookie:%s\"" % str_cookie_1
            url = scan_url + cookies
            ctx.log.info(url)
            if url not in has_scan_url:
                if 'png' not in url and 'html' not in url:
                    r.lpush('int_queue', url)
                    ctx.log.info("%s 已加入redis 队列" % url)
                    has_scan_url.append(url)
                
has_scan_url = []
#r = Redis(host='127.0.0.1', port=6379, db=0, password='**************')
r = Redis(host='127.0.0.1', port=6379, db=0)
addons = [
    Counter()
]
