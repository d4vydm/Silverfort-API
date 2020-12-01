## Silverfort
Silverfort protects organizations from data breaches by delivering strong authentication across entire corporate networks and cloud environments, without requiring any modifications to endpoints or servers. Using patent-pending technology, Silverfort's agentless approach enables multi-factor authentication and AI-driven adaptive authentication even for systems that don’t support it today, including proprietary systems, critical infrastructure, shared folders, IoT devices, and more.


## Goal
Use Silverfort API integration and log parsing to integratie with 3th party vendors.

One use case would be to trigger other systems based on the MFA information retrieved from the Silverfort logs.

Otherwise, we could insert risk indicators coming from 3th party vendors into Silverfort and update an entity risk. This feeds the risk-based engine in Silverfort and allows dynamic RBA behavior.


## Python code files
### sf_auth_api_wrapper.py
Silverfort authentication API wrapper provides a Python API wrapper for the Silverfort auth API

### sf_riskengine_api_wrapper.py
Silverfort risk engine API wrapper provides a Python API wrapper for the Silverfort risk engine API

### sf_log_parser.py
A Silverfort log parser which parses the output of a logstash instance. The logstash instance takes the Silverfort syslog and outputs a converted json.
Configuration for logstash can be found in the logstash directory. Deployment of logstash is out of scope of this code.


## Example config file
```
{
    "silverfort_logger": {
        "Threshold": 3,
        "TimeWindow": 60,
        "MFAResponse": ["Blocked", "Auto-Response"],
        "Action": "Denied"
    },
    "silverfort_api": {
        "admin_uri": "",
        "api_key": "",
        "node_uris": [ "", "" ],
        "mfa_api_user": "",
        "mfa_api_passw": ""
    },
    "sentinelone": {
        "uri": "",
        "api": "",
        "api_token": ""
    }
}
```


## Disclaimer
The code in this project tested with Silverfort version v3.5.11

