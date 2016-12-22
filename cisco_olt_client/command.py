import shlex
import collections

try:
    str_t = basestring
except NameError:
    str_t = str


def args2mapping(args, mapping_cls=collections.OrderedDict):
    '''
    Parse list of command line arguments into mapping (ordered by default)
    '''
    return mapping_cls([arg2tuple(arg) for arg in args])


def arg2tuple(arg):
    '''
    Parse string command line argument into name, value tuple
    '''
    arg_parts = arg.split('=', 1)
    if len(arg_parts) == 2:
        name, value = arg_parts
    else:
        name, value = arg_parts[0], None

    if name.startswith('--'):
        name = name[2:]

    # try to normalize string that's quoted
    if value is not None:
        _value = shlex.split(value)
        # other length than 1 means that the value string was either not properly
        # quoted or is empty, in both cases we're not touching it
        if len(_value) == 1:
            value = _value[0]

    return name, value


class Command:

    def __init__(self, cmd, args=None):
        '''
        Single command and it's output representation

        >>> c = Command('/remote-eq/status', ['--onuID=23', '--port=pon.7'])
        >>> c.compile()
        '/remote-eq/status --onuID=23 --port=pon.7'

        :param cmd: Full path to the command.
        :type cmd: str

        :param args: Additional command arguments. In python2, if you need to
            preserve order of arguments use ordered dict or list of 2-tuples
        :type args: list or dict
        '''
        # save original cmd and args just in case of dragons
        self._cmd = cmd
        self._args = args
        # assumption is there's no space in cmd path
        # if there's space in cmd path and args is None, parse the rest after space as arguments
        if ' ' in cmd and args is None:
            self.cmd, args = cmd.split(' ', 1)
        else:
            self.cmd = cmd

        # if original args is mapping use it directly
        if isinstance(args, collections.Mapping):
            self.args = args
        # process string types before any other iterables
        elif isinstance(args, str_t):
            self.args = args2mapping(shlex.split(args))
        # we assume it's list of strings
        elif isinstance(args, collections.Iterable):
            if args and len(args[0]) == 2:
                self.args = collections.OrderedDict(args)
            else:
                self.args = args2mapping(args)
        elif args is None:
            self.args = collections.OrderedDict()

    def get_arg_strs(self):
        return [
            "--%s" % arg if value is None else "--%s=%s" % (arg, value)
            for arg, value in self.args.items()
        ]

    def compile(self):
        return " ".join([self.cmd] + self.get_arg_strs())
