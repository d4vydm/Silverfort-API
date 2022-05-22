import sys
import json
import time
import threading



class SFLog:
    """
    SFLog class contains a log dictionary representing a single Silverfort log
    The log is a json formatted Silverfort log
    """
    log = {}

    def __init__(self, s):
        self.log = s

    def getDestinationServiceName(self):
        return self.log["destinationServiceName"]

    def getDeviceVendor(self):
        return self.log["deviceVendor"]

    def getSilverfortPolicyAction(self):
        return self.log["SilverfortPolicyAction"]

    def getSourceUserName(self):
        return self.log["sourceUserName"]

    def getDestinationNtDomain(self):
        return self.log["destinationNtDomain"]

    def getDeviceProduct(self):
        return self.log["deviceProduct"]

    def getDeviceEventClassId(self):
        return self.log["deviceEventClassId"]

    def getDeviceReceiptTime(self):
        return self.log["deviceReceiptTime"]

    def getSeverityLabel(self):
        return self.log["severity_label"]

    def getSilverfortMfaResponse(self):
        return self.log["SilverfortMfaResponse"]

    def getSilverfortPolicy(self):
        return self.log["SilverfortPolicy"] 

    def getApplicationProtocol(self):
        return self.log["applicationProtocol"] 

    def getLogTimeStamp(self):
        return self.log["@timestamp"] 

    def getSilverfortMfaResponseTime(self):
        return self.log["SilverfortMfaResponseTime"] 

    def getSourceAddress(self):
        return self.log["sourceAddress"] 

    def getHost(self):
        return self.log["host"] 

    def getSilverfortReqResult(self):
        return self.log["SilverfortReqResult"] 

    def getSilverfortReqRisk(self):
        return self.log["SilverfortReqRisk"] 

    def getSourceNtDomain(self):
        return self.log["sourceNtDomain"] 

    def getSourceHostName(self):
        return self.log["sourceHostName"]

    def getLogType(self):
        return self.log["name"] 

    def getDestinationHostName(self):
        return self.log["destinationHostName"] 



class SFLogger:
    """
    SFLogger class contains a list of logs and function to work on that list of logs.
    The logs list is a list of json formatted Silverfort logs
    """
    sflogs = []

    def appendLog(self, s):
        l = SFLog(s)
        self.sflogs.append(l)

    def getLog(self, index):
        return self.sflogs[index]

    def getLastLog(self):
        l = len(self.sflogs)
        if (l > 1):
            return self.sflogs[l-1]
        else:
            return None

    def getAllLogs(self):
        return self.sflogs

    def getNumberOfLogs(self):
        return len(self.sflogs)



def followSFJSONLog(filepath):
    """
    followSFJSONLog tails the given file. Each new line yields out of the function and returns the current line
    """
    f = open(filepath, 'r')
    while True:
        line = f.readline()
        if line:
            yield line
        else:
            time.sleep(0.5)


def collectSFLogs(filepath, sflogger):
    """
    collectSFLogs reads the given log file via a call to a log follow function. 
    Each log line the file is added to the given logs list
    """
    gen = followSFJSONLog(filepath)
    for line in gen:
        if (line != '\n'):
            s = json.loads(line)
            sflogger.appendLog(s)


def startLogCollector(filepath, sflogger):
    """
    startLogCollector starts a log collector thread
    filepath is a string containing the os path of the log file
    logs is a list
    """
    # Run the log file collector in a thread, it keeps looking for new lines in the log file
    x = threading.Thread(target=collectSFLogs, args=(filepath, sflogger,))
    x.start()

