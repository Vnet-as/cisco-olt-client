
from cisco_olt_client.client import OltClient


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
