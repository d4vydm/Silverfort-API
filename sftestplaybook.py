import os
import sys

from sf_riskengine_api_wrapper import *
from sf_auth_api_wrapper import *
from sf_log_parser import *





##################################################
## Helper functions
def writeJsonToFile(filename, jsondata):
    with open(filename, 'w', encoding='utf-8') as outfile:
        json.dump(jsondata, outfile, indent=4)

    return 1

def printSep():
    i=os.get_terminal_size().columns
    while i > 0: i-=1; print("-", end = '')





##################################################
## Call functions
def executeCall(sfclient, command, resource, data):
    """
    Parse commands and call api function integrations
    """
    # print the command called
    print(f'Command {command} called\n')

    # Call the correct function
    try:
        if command == 'sf-get-user-risk':
            # Get a user risk
            resp = get_user_risk(sfclient, resource)
            return resp

        elif command == 'sf-update-user-risk':
            # Update user risk
            resp = update_user_risk(sfclient, data)
            return resp 

        elif command == 'sf-send-MFA-user':
            # Send MFA to user
            resp = send_mfa_user(sfclient, data)

        elif command == 'sf-update-resource-risk':
            # Update resource risk
            resp = update_resource_risk(sfclient, data)
            return resp

        else:
            errmsg = f'Command {command} not found'
            print(errmsg)
            raise ApiError(errmsg)

    # Log exceptions
    except Exception as e:
        error_message = f'Failed to execute {command} command. Error: '
        print(error_message + str(e.args[0]))

    return 0





##################################################
## SF risk engine playbook
def sf_risk_playbook(config):
    # Create Silverfort api client
    sf_risk_client = SFRiskClient(config["silverfort_risk_api"])

    # #1 Get the risk of user
    # print('\n\n#### Get the risk of user ####')
    # command = 'sf-get-user-risk'
    # resource = ''

    # resp = executeCall(sf_risk_client, command, resource, None)
    # if resp != 0:
    #     print("\nResult:\n" + resp)
    #     printSep()

    # #2 Update the risk of user
    # print('\n\n#### Update the risk of user ####')
    # command = 'sf-update-user-risk'
    # inputfile = './examples/in_update.json'

    # with open(inputfile, "r") as read_file:
    #     data = json.load(read_file)
    # print("Input:\n" + json.dumps(data, indent=4) + "\n")

    # resp = executeCall(sf_risk_client, command, None, data)
    # if resp != 0:
    #     print("\nResult:\n" + resp)
    #     printSep()


    #3 Reset some risks by sending in low risk indicators
    print('\n\n#### Reset risks ####')
    r = "Cortex XDR ..."
    u = "ezio@ddm.exn.local"
    data = """
    {{
        "user_principal_name": "{user}",
        "risks": {{
            "{reason}": {{
                "severity": "low",
                "valid_for": 1,
                "description": "{reason}"
            }}
        }}
    }}""".format(user=u, reason=r)

    resp = executeCall(sf_risk_client, command, None, data)
    if resp != 0:
        print("\nResult:\n" + resp)
        printSep()




##################################################
## SF authentication mfa playbook
def sf_auth_playbook(config):
    # Create Silverfort api client
    sf_auth_client = SFAuthClient(config["silverfort_auth_api"])

    #1 Send MFA to user
    print('\n\n#### Send MFA to user ')
    command = 'sf-send-MFA-user'
    username = ''
    domain = ''
    message = ''

    data = json.loads(json.dumps({"name": username, "domain": domain, "message": message}))
    resp = executeCall(sf_auth_client, command, None, data)
    if resp != 0:
        print("\nResult:\n" + resp)
        printSep()






##################################################
## SF logger playbook
def sf_logparser_playbook(logfile):
    # Create Silverfort logger
    sflogger = SFLogger()

    #1 Start log collector
    print("Starting log collector for logfile: ", logfile)
    startLogCollector(logfile, sflogger.sflogs)







##################################################
## SF main
if __name__ in ('__main__'):
    if len(sys.argv) < 3:
        print("Usage: python3 sftestplaybook.py <silverfort_config>.json <silverfort_json_logfile>.log")
        sys.exit()

    config_file = sys.argv[1]
    log_file = sys.argv[2]

    if not os.path.isfile(config_file):
        print('The specified config_file does not exist')
        sys.exit()

    if not os.path.isfile(log_file):
        print('The specified log_file does not exist')
        sys.exit()

    # Read config file
    with open(config_file, "r") as read_file:
        config = json.load(read_file)

    ## Run a test on the risk engine api
    sf_risk_playbook(config)

    # ## Run a test on the mfa api
    # sf_auth_playbook(config)

    # ## Run a test on log parsing
    # sf_logparser_playbook(log_file)
