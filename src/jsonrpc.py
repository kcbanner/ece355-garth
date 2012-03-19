import json
import string
import random
import urllib2

from event import EventEncoder

ID_LENGTH = 10

def _get_rpc_json(method, params, id=None):
    if id is None:
        id = ''
        for i in range(0, ID_LENGTH):
            id += random.choice(string.ascii_uppercase +
                                string.ascii_lowercase + 
                                string.digits)

    call = {'jsonrpc':'2.0', 
            'method':method,
            'params':params,
            'id':id}

    call_str = json.dumps(call, cls=EventEncoder)
    return call_str
    
def rpc(method, params, url, id=None):
    rpc_json = _get_rpc_json(method, params, id)
    req = urllib2.Request(url)
    req.add_header('Content-Type','application/json')
    f = urllib2.urlopen(req, rpc_json)

    response_json = f.read()
    response = json.loads(response_json)

    return response

    
