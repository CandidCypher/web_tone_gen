import time
import zmq
from flask import Flask

app = Flask(__name__)
ctx = zmq.Context()
pub = ctx.socket(zmq.PUB)

host = "127.0.0.10"
port = "5555"
url = "tcp://{}:{}".format(host, port)


def publish_msg(msg):
    try:
        pub.bind(url)
        time.sleep(1)
        print("Seding msg: {}".format(msg))
        pub.send(msg)
    except Exception as e:
        print("Error: {}".format(e))
    finally:
        pub.unbind(url)

@app.route("/print/", methods=['GET'])
def printNumber(number):
    response = 'Number %d' % number
    publish_msg('number %d' % number)
    return response


if __name__== '__main__':
    app.run(host='0.0.0.0', debug=True)
