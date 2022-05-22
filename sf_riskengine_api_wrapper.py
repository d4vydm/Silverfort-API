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




## SFRiskClient
class SFRiskClient:
    def __init__(self, configfile):
        self.base_url = configfile['admin_uri']
        self.apikey = configfile['api_key']

    def get_general_http_request(self, function, param, resource):
        fulluri = self.base_url \
            + "/riskapi/" \
            + function \
            + "?apikey=" + self.apikey \
            + "&" + param + "=" + resource
        resp = requests.get(
            fulluri, 
            verify=False
        )

        if resp.status_code != 200:
            raise ApiError(f'GET {function} '.format(resp.status_code) + json.dumps(resp.json()))
        else:
            return resp

    def post_general_http_request(self, function, data):
        fulluri = self.base_url \
            + "/riskapi/" \
            + function \
            + "?apikey=" + self.apikey
        resp = requests.post(
            url=fulluri, 
            json=data, 
            verify=False, 
            headers={"Content-Type": "application/json"}
        )

        if resp.status_code != 200:
            raise ApiError(f'POST {function} '.format(resp.status_code) + json.dumps(resp.json()))
        else:
            return resp

    def get_user_entity_risk_http_request(self, resource):
        """
        initiates an http request to get the user entity's risk from Silverfort DB
        """
        function = "getEntityRisk"
        param = "user_principal_name"

        return self.get_general_http_request(function, param, resource)

    def update_user_entity_risk_http_request(self, data):
        """
        initiates an http request to update the user entity's risk in Silverfort DB
        """
        function = "updateEntityRisk"

        return self.post_general_http_request(function, data)

    def update_resource_entity_risk_http_request(self, data):
        """
        initiates an http request to update the resource entity's risk in Silverfort DB
        """
        function = "updateEntityRisk"

        return self.post_general_http_request(function, data)






## Wrapper functions
# Get User Risk
def get_user_risk(sfclient, resource):
    """
    Initiates http API request to the client base URL to get the resource risk score

    # Response content type: application/json
    # {
    #   "risk": "High",
    #   "reason": [
    #     "Suspicious activity",
    #     "Machine account",
    #     "Malware detected"
    #   ]
    # {

    """

    resp = sfclient.get_user_entity_risk_http_request(resource)

    name = 'SilverFort Get User Risk'
    output = json.dumps({"APICall": name, "Resource": resource, "Response": resp.json()}, indent=4)

    return output


# Update user risk
def update_user_risk(sfclient, data):
    """
    Request content type: application/json
    {
        "user_principal_name": "{{user_principal_name}}",
        "risks": {
            "activity_risk": {
                "severity": "critical",
                "valid_for": 1,
                "description": "Suspicious activity"
            },
            "malware_risk": {
                "severity": "high",
                "valid_for": 1,
                "description": "Malware detected"
            }
        }
    }

    Response content type: application/json
    {
    "result": "updated successfully"
    }
    """

    resp = sfclient.update_user_entity_risk_http_request(data)

    name = 'SilverFort Update User Risk'
    output = json.dumps({"APICall": name, "Resource": data["user_principal_name"], "Response": resp.json()}, indent=4)

    return output


# Update resource risk
def update_resource_risk(sfclient, data):
    """
    Request content type: application/json
    {
        "resource_name": "{{resource_name}}",
        "risks": {
            "activity_risk": {
                "severity": "critical",
                "valid_for": 1,
                "description": "Suspicious activity"
            },
            "malware_risk": {
                "severity": "high",
                "valid_for": 1,
                "description": "Malware detected"
            }
        }
    }

    Response content type: application/json
    {
    "result": "updated successfully"
    }
    """

    resp = sfclient.update_resource_entity_risk_http_request(data)

    name = 'SilverFort Update Resource Risk'
    output = json.dumps({"APICall": name, "Resource": data["resource_name"], "Response": resp.json()}, indent=4)

    return output


