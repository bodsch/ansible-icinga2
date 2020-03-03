import pytest
import os
#import yaml
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.fixture()
def get_vars(host):
    defaults_files = "file=../../defaults/main.yml name=role_defaults"
    vars_files = "file=../../vars/main.yml name=role_vars"

    ansible_vars = host.ansible(
        "include_vars",
        defaults_files)["ansible_facts"]["role_defaults"]

    ansible_vars.update(host.ansible(
        "include_vars",
        vars_files)["ansible_facts"]["role_vars"])

    # print(ansible_vars)

    return ansible_vars


# def test_installation_directory(host, get_vars):
#     dir = host.file(get_vars['monitoring_plugins_directory'])
#     assert dir.exists
#     assert dir.is_directory
#     assert dir.user == get_vars['mariadb_log_file_group']
#     assert dir.group == get_vars['mariadb_log_file_group']


@pytest.mark.parametrize("dirs", [
    "/etc/ansible/facts.d",
    "/etc/icinga2",
    "/usr/share/icinga2",
    "/var/log/icinga2",
    "/var/lib/icinga2"
])
def test_directories(host, dirs):
    d = host.file(dirs)
    assert d.is_directory
    assert d.exists


def test_user(host):
    assert host.group("nagios").exists
    assert host.user("nagios").exists
    assert "nagios" in host.user("nagios").groups
#    assert host.user("nagios").shell == "/sbin/nologin"
#    assert host.user("nagios").home == "/opt/jolokia"


def test_service(host):
    service = host.service("icinga2")
    assert service.is_enabled
    assert service.is_running


@pytest.mark.parametrize("ports", [
    '0.0.0.0:5665',
])
def test_open_port(host, ports):

    for i in host.socket.get_listening_sockets():
        print( i )

    solr = host.socket("tcp://{}".format(ports))
    assert solr.is_listening
