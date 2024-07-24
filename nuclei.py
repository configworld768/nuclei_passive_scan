import json
import subprocess
import time
import requests
from mitmproxy import ctx
from redis.client import Redis
from multiprocessing import Process


#r = Redis(host='127.0.0.1', port=6379, db=0, password='ISFP')
r = Redis(host='127.0.0.1', port=6379, db=0)


class ReportAlert(object):
    ''' 
    企微告警、扫描结果csv文件发送到企微
    '''
    def __init__(self) -> None:
        #self.webhook = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=1c6'
        self.webhook = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=486'
        #self.webhook = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key='
        self.id_url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key=3e1c6&type=file'
        #self.id_url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key=086&type=file'
    
    def send_msg(self, content):
        ''' 企微告警 '''

        data1 = json.dumps({"msgtype": "text", "text": {"content": content, "mentioned_list": ["ISFP"]}})
        r = requests.post(self.webhook, data1, auth=('Content-Type', 'application/json'))
        print(r.json)
        print(r.status_code)
        return r.status_code
    
    def post_file(self, file):
        ''' 扫描结束发送扫描结果 csv 文件到企业微信群 '''

        data = {'file': open(file, 'rb')}
        response = requests.post(url=self.id_url, files=data)
        ctx.log.info(response.text)
        json_res = response.json()
        media_id = json_res['media_id']
        data = {"msgtype": "file",
                "file": {"media_id": media_id}
                }
        result = requests.post(url=self.webhook, json=data)
        return (result)
    
    
class NucleiScan(object):

    def __init__(self, name, alert) -> None:
        self.name = name
        self.qiwei_alert = qiwei_alert

    def nuclei_scan(self, name, qiwei_alert):
        ''' 
        消费 Counter put 到队列的 url
        '''
        print('Son process %s' % name)
        while True:
            try:
                b_value = r.rpop('int_queue')
                if b_value:
                    value = str(b_value, 'UTF-8')
                    print("Process getter get {}".format(value))
                    res = subprocess.getstatusoutput('/Users/bnbtomoon/Downloads/nuclei -u %s -t /Users/bnbtomoon/Documents/scan_poc -json -silent' % value )
                    if res[1]:
                        print(res[1])
                        print(type(res[1]))
                        for i in res[1].split('\n'):
                            vul = json.loads(i)
                            print("vul: %s" % vul)
                            #if vul['info']['severity'] == 'high':
                            qiwei_alert.send_msg(i)
                    else:
                        print("not found vul!")
                time.sleep(3)
            except Exception as e:
                print(e)

    
if __name__ == '__main__':
    qiwei_alert = ReportAlert()
    # 这里要启动几个nuclei进程可以自定义，修改 range 值即可
    for i in range(5):
        obj = 'nu' + str(i)
        obj = NucleiScan("Putter", 'alert')
        Process(target=obj.nuclei_scan, args=("Putter", qiwei_alert)).start()

