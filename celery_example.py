from flask import Flask
import time
from flask_celery import make_celery

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://127.0.0.1:6379'
app.config['CELERY_BACKEND'] = 'redis://127.0.0.1:6379/0'

celery = make_celery(app)

@app.route('/process/<name>')
def process(name):
    reverse.delay(name)
    return '<h1>I sent an async request!</h1>'

@celery.task(name = 'celery_example.reverse')
def reverse(string):
    time.sleep(5)
    return string[::-1]

if __name__ == '__main__':
	app.run(host = '0.0.0.0', port = '5000', debug = True)



