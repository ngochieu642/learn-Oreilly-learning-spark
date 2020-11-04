import urllib3
import json


def processCallSigns(signs):
    http = urllib3.PoolManager()
    urls = map(lambda x: 'http://73s/com/qsos/%.json' % x, signs)
    requests = map(lambda x: (x, http.request('GET', x)), urls)
    result = map(lambda x: (x[0], json.loads(x[1].data)), requests)
    return filter(lambda x: x[1] is not None, result)


def fetchCallSigns(input):
    return input.mapPartitions(lambda callSigns: processCallSigns(callSigns))


contactsContactList = fetchCallSigns(validSigns)
