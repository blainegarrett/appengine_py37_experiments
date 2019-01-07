import json
from flask import Flask
from google.cloud import datastore


# Setup the WSGI application
app = Flask(__name__)


def batch_upsert(client):
    task1 = datastore.Entity(client.key('Task', 'test1'))

    task1.update({
        'category': 'Personal',
        'done': False,
        'priority': 4,
        'description': 'Learn Cloud Datastore'
    })

    task2 = datastore.Entity(client.key('Task', 'test2'))

    task2.update({
        'category': 'Work',
        'done': False,
        'priority': 8,
        'description': 'Integrate Cloud Datastore'
    })

    # [START datastore_batch_upsert]
    client.put_multi([task1, task2])
    # [END datastore_batch_upsert]

    return task1, task2


@app.route('/')
def hello():
    """
    Simple Hellow world route
    """
    return 'Hello World!'


@app.route('/upsert')
def upsert():
    """
    Update or Insert two tasks
    """
    datastore_client = datastore.Client()
    task1, task2 = batch_upsert(datastore_client)
    return 'Created 2 Tasks'



@app.route('/datastore')
def ds():
    import os
    # raise Exception(os.environ['DATASTORE_PROJECT_ID'])

    # Instantiates a client
    datastore_client = datastore.Client()

    #batch_upsert(datastore_client)


    keys = [
        datastore_client.key('Task', 1),
        datastore_client.key('Task', 2)
    ]

    # [START datastore_batch_lookup]
    tasks = datastore_client.get_multi(keys)

    return json.dumps(tasks)





if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
