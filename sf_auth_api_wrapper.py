import requests
import json


# Suppress SSL warning
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)




## APIError
class ApiError(Exception):
    """An API Error Exception"""
    def __init__(self, status):
        self.status = status

    def __str__(self):
        return "ApiError: status={}".format(self.status)




## SFAuthClient
class SFAuthClient:
    def __init__(self, configfile):
        self.base_url = configfile['node_uris'][0] #Trigger to the first node
        self.api_user = configfile["mfa_api_user"]
        self.api_passw = configfile["mfa_api_passw"]

    def send_mfa_user_http_request(self, data):
        fulluri = self.base_url \
            + "/api/v1/authentication/mfa" \
            + "?username=%s&client_domain=%s&display=%s" %(data["name"],data["domain"],data["message"])
        resp = requests.post(
            fulluri, 
            auth=(self.api_user, self.api_passw),
            verify=False
        )

        if resp.status_code != 200:
            raise ApiError(f'POST MFA '.format(resp.status_code) + json.dumps(resp.json()))
        else:
            print("Call ok. User MFA feedback: ",resp.json()['result'])
            return resp



## Wrapper functions
# Send MFA to user
def send_mfa_user(sfclient, data):
    resp = sfclient.send_mfa_user_http_request(data)

    name = 'SilverFort send MFA to user'
    output = json.dumps({"APICall": name, "Resource": data["name"], "Response": resp.json()}, indent=4)

    return output


