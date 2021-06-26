
from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar
import pytest
import os
import testinfra.utils.ansible_runner

# import pprint
# pp = pprint.PrettyPrinter()

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('instance')


@pytest.fixture()
def get_vars(host):
    """

    """
    cwd = os.getcwd()

    file_defaults = "file={}/defaults/main.yml name=role_defaults".format(cwd)
    file_vars = "file={}/vars/main.yml name=role_vars".format(cwd)
    file_molecule = "file=molecule/default/group_vars/all/vars.yml name=test_vars"

    defaults_vars = host.ansible("include_vars", file_defaults).get("ansible_facts").get("role_defaults")
    vars_vars = host.ansible("include_vars", file_vars).get("ansible_facts").get("role_vars")
    molecule_vars = host.ansible("include_vars", file_molecule).get("ansible_facts").get("test_vars")

    ansible_vars = defaults_vars
    ansible_vars.update(vars_vars)
    ansible_vars.update(molecule_vars)

    templar = Templar(loader=DataLoader(), variables=ansible_vars)
    result = templar.template(ansible_vars, fail_on_undefined=False)

    return result


def local_facts(host):
    return host.ansible("setup").get("ansible_facts").get("ansible_local").get("icinga2")


@pytest.mark.parametrize("dirs", [
    "/etc/ansible/facts.d",
    "/etc/icinga2",
    "/usr/share/icinga2",
    "/var/log/icinga2",
    "/var/lib/icinga2"
])
def test_directories(host, dirs):
    d = host.file(dirs)
    # major_version = host.ansible("setup").get("ansible_facts").get("ansible_local").get("sqlplus").get("version").get("major")
    # content = host.file('/etc/profile.d/sqlplus.sh').content_string
    # user_name = get_vars.get('sqlplus_oracle_user').get('name')
    #
    assert d.is_directory
    assert d.exists


def test_user(host):

    user = local_facts(host).get("icinga2_user")
    group = local_facts(host).get("icinga2_group")

    assert host.group(group).exists
    assert host.user(user).exists
    assert group in host.user(user).groups


def test_service(host):
    service = host.service("icinga2")
    assert service.is_enabled
    assert service.is_running


@pytest.mark.parametrize("ports", [
    '0.0.0.0:5665',
])
def test_open_port(host, ports):

    for i in host.socket.get_listening_sockets():
        print(i)

    solr = host.socket("tcp://{}".format(ports))
    assert solr.is_listening
