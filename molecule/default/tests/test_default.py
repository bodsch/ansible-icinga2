import pytest
import os
import yaml
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

@pytest.fixture()
def AnsibleVars(host):
    all_vars = host.ansible.get_variables()
    return all_vars

@pytest.fixture()
def AnsibleDefaults():
    with open("../../defaults/main.yml", 'r') as stream:
        return yaml.load(stream)


def test_installation_directory(host, AnsibleVars):
    dir = host.file(AnsibleVars['monitoring_plugins_directory'])
    # result = host.ansible('debug','var=kafka_final_path')
    # dir = host.file(result['kafka_final_path'])
    assert dir.exists
    assert dir.is_directory
    assert dir.user == AnsibleVars['mariadb_log_file_group']
    assert dir.group == AnsibleVars['mariadb_log_file_group']


@pytest.mark.parametrize("dirs", [
    "/etc/ansible/facts.d",
    "/etc/icinga2",
    "/usr/share/icinga2",
    "/var/log/icinga2"
    "/var/lib/icinga2"
])
def test_directories(host, dirs):
    d = host.file(dirs)
    assert d.is_directory
    assert d.exists


# @pytest.mark.parametrize("files", [
#     "/opt/jolokia/jolokia-agent.jar"
# ])
# def test_files(host, files):
#     f = host.file(files)
#     assert f.exists
#     assert f.is_file


def test_user(host):
    assert host.group("nagios").exists
    assert host.user("nagios").exists
    assert "nagios" in host.user("nagios").groups
#    assert host.user("nagios").shell == "/sbin/nologin"
#    assert host.user("nagios").home == "/opt/jolokia"
