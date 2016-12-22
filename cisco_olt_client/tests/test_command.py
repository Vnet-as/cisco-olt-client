import pytest
import shlex
from cisco_olt_client.exceptions import CommandNotExecuted
from cisco_olt_client.command import arg2tuple, args2mapping
from cisco_olt_client.command import Command, NEWLINE_SEP


def test_args2mapping():
    assert args2mapping(['--onuID=23'])['onuID'] == '23'
    args = shlex.split('--onuID=23 --arg="string with spaces" --noval')
    args_mapping = args2mapping(args)
    assert args_mapping['onuID'] == '23'
    assert args_mapping['arg'] == 'string with spaces'
    assert args_mapping['noval'] is None
    assert list(args_mapping.keys())[1] == 'arg'


def test_arg2tuple():
    assert arg2tuple('--onuID') == ('onuID', None)
    assert arg2tuple('--onuID=23') == ('onuID', '23')
    assert arg2tuple('--onuID="this is a string with spaces"') == ('onuID', "this is a string with spaces") # noqa


def test_args_none():
    cmd = Command('/path/cmd')
    assert not cmd.args

def test_compile_arg_no_value():
    cmd = Command('/path/cmd', dict(arg=None))
    assert cmd.compile() == '/path/cmd --arg'

    cmd = Command('/path/cmd --arg')
    assert cmd.args['arg'] is None
    assert cmd.compile() == '/path/cmd --arg'


def test_simple_compile():
    cmd_str = 'cmd --arg1=val1 --arg2=val2'
    cmd = Command('cmd', (('arg1', 'val1'), ('arg2', 'val2')))
    assert cmd.compile() == cmd_str

    cmd = Command('cmd', {'arg1': 'val1', 'arg2': 'val2'})
    # order is not guaranteed
    assert '--arg1=val1' in cmd.compile()
    assert '--arg2=val2' in cmd.compile()
    assert cmd.compile().startswith('cmd ')

    cmd = Command('cmd', ['--arg1=val1', '--arg2=val2'])
    assert cmd.compile() == cmd_str


def test_execute_error():
    class ClientMock:
        def raw_exec_command(self, *args, **kwargs):
            return b'\r\nError\r\n'
    cmd = Command('cmd')
    cmd.execute(ClientMock())
    assert cmd.error
    assert not cmd.warning

def test_execute_warrning():
    class ClientMock:
        def raw_exec_command(self, *args, **kwargs):
            return b'\r\nWarning\r\n'
    cmd = Command('cmd')
    cmd.execute(ClientMock())
    assert not cmd.error
    assert cmd.warning

def test_raise_not_executed():
    cmd = Command('cmd')
    with pytest.raises(CommandNotExecuted):
        cmd.error
    with pytest.raises(CommandNotExecuted):
        cmd.warning
