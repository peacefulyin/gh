import json
import string
import hashlib
import random
import time


class Sign:
    def __init__(self, jsapi_ticket, url):
        self.ret = {
            'nonceStr': self.__create_nonce_str(),
            'jsapi_ticket': jsapi_ticket,
            'timestamp': self.__create_timestamp(),
            'url': url,
        }
    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def __create_timestamp(self):
        return int(time.time())

    def sign(self):
        string = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])
        print("xxxxxx_string",string)
        self.ret['signature'] = hashlib.sha1(string.encode('utf-8')).hexdigest()
        return self.ret

# origin_string = "jsapi_ticket=LIKLckvwlJT9cWIhEQTwfBHFOKUvm4MRvL7Yz6YYekmfW4xvCRH2-dAsADbtifo20CBmSJigEt2VlOMVd9oDW&timestamp=1568086648&url=http://172.10.3.98/?code=061W0Rvq1Rc5Ki0h5uxq1B4Bvq1W0RvH&state=STATE"

def main():
    ticket = "LIKLckvwlJT9cWIhEQTwfBHFOKUvm4MRvL7Yz6YYekmfW4xvCRH2-dAsADbtifo20CBmSJigEt2VlOMVd9oDW"
    url = "http://172.10.3.98/?code=061W0Rvq1Rc5Ki0h5uxq1B4Bvq1W0RvH&state=STATE"
    sign = Sign(ticket,url)
    # print('origin_string',origin_string)
    print(sign.sign())

main()
