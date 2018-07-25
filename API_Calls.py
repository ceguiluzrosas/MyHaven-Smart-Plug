import Authorization_File as af
import traceback
import urllib2
import json


class API:

    def __init__(self):
        self.device_id = af.device_ids['Smart Plug']
        self.api_key = af.api["key"]
        self.url = "https://iot.peoplepowerco.com/cloud/json/"

    def get_data(self, startDate, endDate):
        headers = {'API_KEY': self.api_key}
        try:
            url = self.url + "devices/" + self.device_id + "/parametersByDate/" + startDate + "?endDate=" + endDate
            request = urllib2.Request(url, headers=headers)
            query = json.loads(urllib2.urlopen(request).read())
            if query["resultCode"] == 0:
                # Device on -- return query
                return [True, query]
            else:
                # Device not on -- return failure
                return [False, ("Unsuccessful Query: " + str(query['resultCode']))]
        except urllib2.HTTPError as e:
                return [False, 'HTTPError = ' + str(e.code)]
        except urllib2.URLError as e:
            return [False, 'URLError = ' + str(e.reason)]
        except Exception:
            return [False, 'Generic Exception: ' + traceback.format_exc()]

    def login(self):
        headers = {'Content-Type': 'application/json', 'API_KEY': self.api_key}
        try:
            url = self.url + "loginByKey"
            request = urllib2.Request(url, headers=headers)
            query = json.loads(urllib2.urlopen(request).read())
            if query['resultCode'] == 0:
                return [True, "We're In --- Commencing Script"]
            else:
                return [False, "Unsuccessful Login: "+str(query['resultCode'])]
        except urllib2.HTTPError as e:
            return [False, 'HTTPError = ' + str(e.code)]
        except urllib2.URLError as e:
            return [False, 'URLError = ' + str(e.reason)]
        except Exception:
            return [False, 'Generic Exception: ' + str(traceback.format_exc())]