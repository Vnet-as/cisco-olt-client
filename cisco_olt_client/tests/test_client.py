
from cisco_olt_client.client import OltClient
from cisco_olt_client.client import exec_command, socket


def test_init():
    client = OltClient('hostname', 'username', 'password')
    assert client.hostname == 'hostname'
    assert client.username == 'username'
    assert client.password == 'password'


def test_get_ssh_client():
    client = OltClient('hostname', 'username', 'password')
    ssh_client = client.get_ssh_client()
    assert isinstance(ssh_client._policy, client.missing_host_key_policy_cls)


def test_get_shell(mocker):
    client = OltClient('hostname', 'username', 'password')
    ssh_client = client.get_ssh_client()
    mocker.patch.object(ssh_client, 'connect')
    mocker.patch.object(ssh_client, 'invoke_shell')
    mocker.patch('cisco_olt_client.client.exec_command')
    shell = client.get_olt_shell(ssh_client)
    assert shell


def test_exec_command(mocker):
    shell = mocker.Mock()
    shell.closed = False
    shell.send = mocker.Mock()
    shell.recv = mocker.Mock()
    cmd_out = b'Vesele Vianoce'
    shell.recv.side_effect = [cmd_out, socket.timeout]
    cmd = '/remote-wq/onu/showconfig'
    assert exec_command(shell, cmd) == cmd_out
    shell.send.assert_called_with(cmd + '\n')

    shell.recv.side_effect = [cmd_out, socket.timeout]
    exec_command(shell, cmd, new_line=False)
    shell.send.assert_called_with(cmd)
