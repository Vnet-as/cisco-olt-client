
class CiscoOltClientException(Exception):
    '''Base class for all ``cisco_olt_client`` exceptions'''


class ConnectionError(CiscoOltClientException):
    '''Raised for unhandled / perceived connection errors'''
