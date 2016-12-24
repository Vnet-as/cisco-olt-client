import socket
try:
    from io import BytesIO as StringIO
except ImportError:
    from StringIo import StringIO

from paramiko.client import SSHClient, AutoAddPolicy

from cisco_olt_client.command import Command
from cisco_olt_client.exceptions import ConnectionError


class OltClient:

    def __init__(
        self,
        hostname,
        username,
        password,
        auto_connect=True,
        recv_timeout=1,
        recv_chunk_size=4096,
        missing_host_key_policy_cls=AutoAddPolicy,
        ssh_connection_options=None
    ):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.auto_connect = auto_connect
        self.recv_timeout = recv_timeout
        self.recv_chunk_size = recv_chunk_size
        self.missing_host_key_policy_cls = missing_host_key_policy_cls
        self.shell = None
        self.ssh_client = None
        self.ssh_connection_options = dict(
            look_for_keys=False,
            allow_agent=False,
            timeout=5
        ) if ssh_connection_options is None else ssh_connection_options

    def get_ssh_client(self):
        '''Prepare default ssh client and set missing host key policy'''
        ssh_client = SSHClient()
        ssh_client.set_missing_host_key_policy(
            self.missing_host_key_policy_cls())
        return ssh_client

    def get_olt_shell(self, ssh_client, recv_msg=True):
        '''
        Initiate OLT interactive cli interface

        :param bool recv_msg: Indicates that the login message (everything that
            is printed by OLT on login) should be read so it will not appear in
            output of subsequent command.

        :return: OLT interactive cli interface in form of paramiko's channel
        :rtype: :class:`paramiko.Channel`
        :raises paramiko.AuthenticationException:
        '''
        ssh_client.connect(
            self.hostname,
            username=self.username,
            password=self.password,
            **self.ssh_connection_options
        )
        shell = ssh_client.invoke_shell()
        shell.settimeout(self.recv_timeout)
        if recv_msg:
            exec_command(shell, '')
        return shell

    def connect(self):
        '''Initialize interactive shell'''
        # the ssh_client reference is needed otherwise it will get garbage
        # collected and causing the shell to close immediately
        self.ssh_client = self.get_ssh_client()
        self.shell = self.get_olt_shell(self.ssh_client)

    def disconnect(self):
        '''Close interactive shell channel and ssh client as well'''
        self.shell.close()
        self.ssh_client.close()

    def execute(self, cmd, args=None):
        '''
        Use the client to execute given command

        If given `cmd` is already instance of
        :class:`~cisco_olt_client.command.Command` it'll be executed using the
        client, otherwise `cmd` and `args` will be used to create an instance
        for you.

        :param cmd: Command to execute
        :type cmd: :class:`~cisco_olt_client.command.Command` or str

        :param args: Additional command arguments. In python2, if you need to
            preserve order of arguments use ordered dict or list of 2-tuples
        :type args: list or dict
        '''
        if not instance(cmd, Command):
            cmd = Command(cmd, args=args)
        return cmd.execute(self)

    def raw_exec_command(self, cmd, **exec_options):
        if self.shell is None:
            if self.auto_connect:
                self.connect()
            else:
                raise ConnectionError(
                    'Connectio not ready and auto_connect flag is False')
        return exec_command(self.shell, cmd, **exec_options)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()


def exec_command(
    shell,
    cmd,
    buffer=None,
    recv_chunk_size=4096,
    output_as_file=False,
    new_line=True,
    new_line_char='\n'
):
    '''
    Use `shell` to execute given command command string `cmd`

    Receiving or rather determining commands output via interactive shell is a
    bit tricky. This function reads from the shell channel until
    :exc:`socket.timeout` is raised, then check if channel is still open, if
    so, received data is considered command's output. If on
    :exc:`socket.timeout` channel is closed, most probably connection error
    occured. Anyway, this is not deterministic.

    Timeout on receiving socket is set with :meth:`Channel.settimeout`.
    `More info <http://docs.paramiko.org/en/2.0/api/channel.html#paramiko.channel.Channel.settimeout>`_.


    :param shell: :class:`~parmiko.channel.Channel` representation of OLT linux
	interactive shell, for more information see
	`paramiko' documentation <http://docs.paramiko.org/en/stable/api/client.html>`_
    :type shell: :class:`~parmiko.channel.Channel`

    :param cmd: Command with arguments to execute
    :type cmd: str

    :param buffer: File-like object where command output is written, if `None`,
        `StringIO` is used by default
    :type buffer: file-like object or None

    :param recv_chunk_size: Reads from `shell` by chunks of the size
        `recv_chunk_size`, default is 4096
    :type recv_chunk_size: int

    :param output_as_file: If set to `True`, result will be file-like object
        used as a buffer for command's output
    :type output_as_file: bool

    :param new_line: If set to `True`, `new_line_char` is appended to given
        command string, carriage return
    :type new_line: bool

    :param new_line_char: What character is appended to given command if
        `new_line` is `True`
    :type new_line_char: str

    :returns: Command's output either as a string or as file-like object if
        `output_as_file` is `True`
    '''
    buffer = StringIO() if buffer is None else buffer
    if new_line and not cmd.endswith(new_line_char):
        cmd += new_line_char
    shell.send(cmd)
    while True:
        try:
            buffer.write(shell.recv(recv_chunk_size))
        except socket.timeout:
            if shell.closed:
                raise ConnectionError('Connection to OTL failed')
            break
    return buffer if output_as_file else buffer.getvalue()
