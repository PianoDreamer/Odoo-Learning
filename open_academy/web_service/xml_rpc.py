import xmlrpc.client
import random

# Login Data
url = "http://localhost:8569"
db = 'o15-learn'
username = 'admin'
password = 'admin'


# Connect Database
def connect_db(common, url):
    result = True
    try:
        print("Description:", common.version())
    except Exception:
        result = False
    return result


# Login Database
def login_db(url, db, username, password):
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    if connect_db(common, url):
        uid = common.authenticate(db, username, password, {})
        return uid


# Records Read
def records_read(url, db, password, uid, model_name, fields_list):
    if uid != False:
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        records = models.execute_kw(db, uid, password, model_name, 'search_read', [[]], fields_list)
        for record in records:
            print(record)


# Records Create
def records_create(url, db, password, uid, model_name, records_list):
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    for record in records_list:
        new_record_id = models.execute_kw(db, uid, password, model_name, 'create', [record])
        print("New Session ID: ", new_record_id)



# Initial Data
uid = login_db(url, db, username, password)
model_name = 'open_academy.session'

if uid is not None:

    # Read Operation
    required_read_fields = ['name', 'number_of_seats']
    records_read(url, db, password, uid, model_name, {'fields': required_read_fields})

    # Create Operation
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

    records_list = [
        {'name': 'Session #' + str(random.randint(1, 9999)), 'course_id': random.randint(1, 3),
         'duration': random.randrange(5, 15, 5), 'number_of_seats': random.randrange(15, 25, 5)},
    ]
    domain_filter = [('isinstructor', '=', True)]
    instructor = models.execute_kw(db, uid, password, 'res.partner', 'search', [domain_filter], {'limit': 1})
    if len(instructor) > 0:
        for record in records_list:
            record['instructor_id'] = instructor[0]

    records_create(url, db, password, uid, model_name, records_list)

# Data Processor Finish Operation Log
else:
    print('Failure Connection')
print('Data Processor Executed')
