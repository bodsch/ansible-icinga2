
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


@pytest.mark.parametrize("directories", [
    "/etc/ansible/facts.d",
    "/etc/icinga2",
    "/etc/icinga2/satellites.d",
    "/etc/icinga2/zones.d",
    "/etc/icinga2/features-enabled",
    "/etc/icinga2/features-available",
    "/etc/icinga2/scripts",
    "/usr/share/icinga2",
    "/usr/share/icinga2/include",
    "/usr/share/icinga2/include/plugins-contrib.d",
    "/var/log/icinga2",
    "/var/lib/icinga2",
    "/var/lib/icinga2/ca",
    "/var/lib/icinga2/certs",
    "/var/lib/icinga2/api",
    "/var/lib/icinga2/api/log",
    "/var/lib/icinga2/api/packages",
    "/var/lib/icinga2/api/packages/_api",
    "/var/lib/icinga2/api/zones",
    "/var/lib/icinga2/api/zones/global-templates",
    "/var/lib/icinga2/api/zones/master",
])
def test_directories(host, directories):
    d = host.file(directories)
    assert d.is_directory


@pytest.mark.parametrize("files", [
    "/etc/icinga2/icinga2.conf",
    "/etc/icinga2/api-users.conf",
    "/etc/icinga2/constants.conf",
    "/etc/icinga2/zones.conf",
    "/etc/icinga2/users.conf",
    "/usr/share/icinga2/include/command-icinga.conf",
    "/usr/share/icinga2/include/command-plugins.conf",
    "/usr/share/icinga2/include/command-plugins-windows.conf",
    "/usr/share/icinga2/include/plugins",
    "/usr/share/icinga2/include/plugins-contrib",
    "/var/log/icinga2/icinga2.log",
    "/var/lib/icinga2/icinga2.state",
    "/var/lib/icinga2/ca/ca.crt",
    "/var/lib/icinga2/ca/ca.key",
    "/var/lib/icinga2/certs/ca.crt",
    "/var/lib/icinga2/api/log/current",
    "/var/lib/icinga2/api/packages/_api/active.conf",
    "/var/lib/icinga2/api/packages/_api/active-stage",
    "/var/lib/icinga2/api/packages/_api/include.conf",
    "/var/lib/icinga2/api/zones/global-templates/_etc/services.conf",
])
def test_files(host, files):
    d = host.file(files)
    assert d.is_file


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

    service = host.socket("tcp://{}".format(ports))
    assert service.is_listening
