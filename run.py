
from robot import myrobot
from werobot.contrib.flask import make_view
from flask import Flask,request,abort
import hashlib
import config as cfg

app = Flask(__name__)
app.add_url_rule(rule='/', # WeRoBot 挂载地址
                 endpoint='werobot', # Flask 的 endpoint
                 view_func=make_view(myrobot),
                 methods=['GET', 'POST'])



@app.route('/',methods=['GET','POST'])
def wechat():
    '''对接微信公众号'''
    #参数是在请求链接后携带的
    #微信的签名
    signature = request.args.get("signature")
    #我们签名所需的两个参数
    timestamp = request.args.get("timestamp")
    nonce = request.args.get("nonce")
    #签名校验成功后需返回给微信的
    echostr = request.args.get("echostr")
    #参数校验
    if not all([signature, timestamp, nonce]):
        abort(400)

    #开始签名
    #将数据添加进数组
    li = [cfg.token, timestamp, nonce]

    #排序
    li.sort()

    #拼接字符串
    #不编码的话python会报错
    tmp_str = "".join(li).encode('utf-8')

    #进行sha1加密
    sign = hashlib.sha1(tmp_str).hexdigest()

    #将自己的签名与微信进行对比
    if signature != sign:
        abort(403)
    #如果签名与微信的一致需返回echostr给微信
    else:
        return echostr

if(__name__=="__main__"):
    app.run()