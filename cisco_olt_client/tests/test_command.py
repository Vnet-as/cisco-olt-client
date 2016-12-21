from cisco_olt_client.command import arg2tuple
from cisco_olt_client.command import Command


def test_arg2tuple():
    assert arg2tuple('--onuID=23') == ('onuID', '23')




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
