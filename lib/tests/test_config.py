# Copyright 2014 Muchos authors (see AUTHORS)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from muchos.config import DeployConfig


def test_defaults():
    c = DeployConfig("muchos", '../conf/muchos.props.example', '../conf/hosts/example/example_cluster',
                     '../conf/checksums', 'mycluster')
    assert c.checksum_ver('accumulo', '1.9.0') == 'f68a6145029a9ea843b0305c90a7f5f0334d8a8ceeea94734267ec36421fe7fe'
    assert c.checksum('accumulo') == 'baa5e0929248ff0d96355bc7fb42a5b75d183a83364519296e07b0adbb089180'
    assert c.get('ec2', 'default_instance_type') == 'm5d.large'
    assert c.get('ec2', 'worker_instance_type') == 'm5d.large'
    assert c.get('ec2', 'aws_ami') == 'ami-9887c6e7'
    assert c.max_ephemeral() == 1
    assert c.mounts(2) == ['/media/ephemeral0', '/media/ephemeral1']
    assert c.node_type_map() == {'default': {'mounts': ['/media/ephemeral0', ], 'devices': ['/dev/nvme1n1', ]},
                                 'worker': {'mounts': ['/media/ephemeral0', ], 'devices': ['/dev/nvme1n1', ]}}
    assert c.node_type('worker1') == 'worker'
    assert c.node_type('leader1') == 'default'
    assert not c.has_option('ec2', 'vpc_id')
    assert not c.has_option('ec2', 'subnet_id')
    assert c.get('ec2', 'key_name') == 'my_aws_key'
    assert c.instance_tags() == {}
    assert len(c.nodes()) == 6
    assert c.get_node('leader1') == ['namenode', 'resourcemanager', 'accumulomaster', 'zookeeper']
    assert c.get_node('worker1') == ['worker']
    assert c.get_node('worker2') == ['worker']
    assert c.get_node('worker3') == ['worker']
    assert c.has_service('accumulomaster')
    assert not c.has_service('fluo')
    assert c.get_service_hostnames('worker') == ['worker1', 'worker2', 'worker3', 'worker4']
    assert c.get_service_hostnames('zookeeper') == ['leader1']
    assert c.get_hosts() == {'leader2': ('10.0.0.1', None), 'leader1': ('10.0.0.0', '23.0.0.0'), 'worker1': ('10.0.0.2', None), 'worker3': ('10.0.0.4', None), 'worker2': ('10.0.0.3', None), 'worker4': ('10.0.0.5', None)}
    assert c.get_public_ip('leader1') == '23.0.0.0'
    assert c.get_private_ip('leader1') == '10.0.0.0'
    assert c.cluster_name == 'mycluster'
    assert c.version("accumulo").startswith('2.')
    assert c.version("fluo").startswith('1.')
    assert c.version("hadoop").startswith('3.')
    assert c.version("zookeeper").startswith('3.')
    assert c.get_service_private_ips("worker") == ['10.0.0.2', '10.0.0.3', '10.0.0.4', '10.0.0.5']
    assert c.get('general', 'proxy_hostname') == "leader1"
    assert c.proxy_public_ip() == "23.0.0.0"
    assert c.proxy_private_ip() == "10.0.0.0"
    assert c.get('general', 'cluster_basedir') == "/home/centos"
    assert c.get('general', 'cluster_user') == "centos"
    assert c.get_non_proxy() == [('10.0.0.1', 'leader2'), ('10.0.0.2', 'worker1'), ('10.0.0.3', 'worker2'),
                                 ('10.0.0.4', 'worker3'), ('10.0.0.5', 'worker4')]
    assert c.get_host_services() == [('leader1', 'namenode resourcemanager accumulomaster zookeeper'), ('leader2', 'metrics'),
            ('worker1', 'worker'), ('worker2', 'worker'), ('worker3', 'worker'), ('worker4', 'worker')]

def test_case_sensitive():
    c = DeployConfig("muchos", '../conf/muchos.props.example', '../conf/hosts/example/example_cluster',
                     '../conf/checksums', 'mycluster')
    assert c.has_option('ec2', 'default_instance_type') == True
    assert c.has_option('ec2', 'Default_instance_type') == False
    c.set('nodes', 'CamelCaseWorker', 'worker,fluo')
    c.init_nodes()
    assert c.get_node('CamelCaseWorker') == ['worker', 'fluo']
