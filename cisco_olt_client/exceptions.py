
class CiscoOltClientException(Exception):
    '''Base class for all ``cisco_olt_client`` exceptions'''


class ConnectionError(CiscoOltClientException):
    '''Raised for unhandled / perceived connection errors'''


class CommandError(CiscoOltClientException):
    '''Command related errors base exception'''


class CommandNotExecuted(CommandError):
    '''
    Command was not executed yet

    Raised when attributes are requested that are usable only after the
    command was executed. e.g. error, warning state
    '''
