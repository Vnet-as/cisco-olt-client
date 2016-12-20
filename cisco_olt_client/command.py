import collections


class Command:

    def __init__(self, cmd, args=None):
        '''
        Single command and it's output representation

        >>> c = Command('/remote-eq/status/show', ['--onuID=23', '--port=pon.7'])
        >>> c.compile()
        '/remote-eq/status/show --onuID=23 --port=pon.7'

        :param args: Additional command arguments. In python2, if you need to
            preserve order of arguments use ordered dict or list of 2-tuples
        :type args: list or dict
        '''
        self.cmd = cmd
        self.args = args or {}

    def _get_arg_strs(self):
        if not isinstance(self.args, collections.Mapping):
            if len(self.args) and isinstance(self.args[0], str):
                return list(self.args)
        return [
            "--%s=%s" % (arg, value)
            for arg, value in (
                self.args.items()
                if isinstance(self.args, collections.Mapping) else
                self.args
            )
        ]

    def compile(self):
        return " ".join([self.cmd] + self._get_arg_strs())
