# Celery Example

This code is to demonstrate how to use celery in python and in flask. There will be two functions, the first one is using celery in python, which is a easy-known coding; the second is a combination between flask and celery, a preview of SFCS and GPM integration system.



## What is Celery?

Our program may need to execute complex tasks that cost a lot of time. The three key elements of Celery is broker, worker, and backend. Once the tasks has been assigned, broker will dispatch the tasks to workers, after workers completed the tasks, it returns the result to backend which we usually use Redis or RabbitMQ. 

Celery allows Python applications to quickly implement task queues for mamy workers. It takes care of the hard part of receiving tasks and assigning them appropriately to workers. There are some goals that can be accomplish by Celery.

1. Define independent tasks that your workers can do as a Python function
2. Listen to a message broker to get new tasks queue
3. Assign those requests to workers to complete the task
4. Monitor the progress and status of tasks and workers

(https://medium.com/swlh/python-developers-celery-is-a-must-learn-technology-heres-how-to-get-started-578f5d63fab3)

There are several parameters for celery. Ex. `celery -A tasks worker --loglevel=info `

​	-A: which application to run  

​	worker: parameters after "worker" are for worker

​		--loglevel: what type of worker information to display

​		--concurrency: how many workers at the same time, max = CPU number

​	queue: which queue to work



## Python Celery

#### 	tasks.py:

​		This program contains tow functions, which adds and multiplies the two input integers x and y. In order to simulate the complex tasks in real-world, the system will sleep for 10 seconds.

##### 		Without Celery:

​			`$ source virtualenv/bin/activate`

​			`$ python`

​				>>> from tasks import add

​				>>> from tasks import multi

​				>>> add(5, 6)

​				11

​				>>> multi(6, 2)

​				12

​			You can see that when you call the functions, the system will pause for 10 seconds, which makes the whole program waiting, this is time-consuming.

##### 		With Celery:

###### 			Terminal 1 (celery):

​				`$ source virtualenv/bin/activate`

​				`$ celery -A tasks worker --loglevel=info `

###### 			Terminal 2 (python):

​				`$ source virtualenv/bin/activate`

​				`$ python`

​					>>> from tasks import add

​					>>> from tasks import multi

​					>>> add.delay(5, 6)

​					<AsyncResult: 1c13fe24-f0c6-440b-9608-af219c60d975>

​					>>> multi.delay(6, 2)

​					<AsyncResult: 75bf2fb2-8a79-4dba-a85a-edddcc2e974e>

​				As you can see whenever you call the function, the program returns the task's worker ID. Also, celery will show the progress time and final result. As a result, with the assist of celery, our program may continue to function even though there are tasks that takes time to process.



## Flask Celery

#### 	celery_example.py:

​		This programs shows the corporation between Flask and Celery, it reverses whatever you typed in the URL.

##### 		Without Celery:

​			`$ source virtualenv/bin/activate`

​			`$ python celery_example.py` 

```python
from flask import Flask
import time

app = Flask(__name__)

@app.route('/celery_example/<name>')
def process(name):
    time.sleep(10)
    print(name[::-1])
    return '<h1> Request Received!</h1>'

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = '5000', debug = True)
```

​		Open your brower and type your IP address (`192.xx.xx.xx:5000/process/testing`), the website will then return "Request Received!", whereas the terminal when have a 10 seconds delay before the result "gnitset".



##### 		With Celery:

```python
from flask import Flask
import time
from flask_celery import make_celery

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://127.0.0.1:6379'
app.config['CELERY_BACKEND'] = 'redis://127.0.0.1:6379/0'

celery = make_celery(app)

@app.route('/celery_example/<name>')
def process(name):
    reverse.delay(name)
    return '<h1>Request Received!</h1>'

@celery.task(name = 'celery_example.reverse')
def reverse(string):
    time.sleep(10)
    return string[::-1]

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = '5000', debug = True)
```

###### 		Terminal 1 (celery):

​				`$ source virtualenv/bin/activate`

​				`$ celery -A celery_example.celery worker --loglevel=info `

###### 		Terminal 2 (python):

​				`$ source virtualenv/bin/activate`

​				`$ python celery_example.py` 

​			Open your browser and type in the address(`192.xx.xx.xx:5000/process/flask_celery`). Though the website will return "Request Received!" immediately, the terminal for celery will wait 10 seconds before returning the result "yrelec_ksalf". You can try changing the URL and the website will still be able to function, whereas celery will output each result after 10 seconds.

###### flask_celery.py:

​	This code is a class that combines flask configuration with celery configuration, also it uses flask application context so that we can call celery tasks within flask.





































