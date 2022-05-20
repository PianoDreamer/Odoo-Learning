import json
import random
import urllib.request

# Login Data
HOST = 'localhost'
PORT = 8569
DB = 'o15-learn'
USER = 'admin'
PASS = 'admin'


def json_rpc(url, method, params):
    data = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": random.randint(0, 1000000000),
    }
    req = urllib.request.Request(url=url, data=json.dumps(data).encode(), headers={
        "Content-Type": "application/json",
    })
    reply = json.loads(urllib.request.urlopen(req).read().decode('UTF-8'))
    if reply.get("error"):
        raise Exception(reply["error"])
    return reply["result"]


def call(url, service, method, *args):
    return json_rpc(url, "call", {"service": service, "method": method, "args": args})


# log in the given database
url = "http://%s:%s/jsonrpc" % (HOST, PORT)
uid = call(url, "common", "login", DB, USER, PASS)


# Initial Data
model_name = 'open_academy.session'

if uid != False:
    # Read Operation
    record_ids = call(url, "object", "execute", DB, uid, PASS, model_name, 'search', [])
    records_list = call(url, "object", "execute", DB, uid, PASS, 'open_academy.session', 'read', record_ids)
    for record in records_list:
        print("Name:", record['name'], "|", "Number of Seats:", record['number_of_seats'])

    # Create Operation
    new_record = {
        'name': 'Session #' + str(random.randint(1, 9999)),
        'course_id': random.randint(1, 3),
        'duration': random.randrange(5, 15, 5),
        'number_of_seats': random.randrange(15, 25, 5),
        'instructor_id': 1,
    }

    new_record_id = call(url, "object", "execute", DB, uid, PASS, model_name, 'create', new_record)
    print("New Session ID: ", new_record_id)

# Data Processor Finish Operation Log
else:
    print('Failure Connection')
print('Data Processor Executed')
