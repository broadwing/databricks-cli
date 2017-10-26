# Databricks CLI
# Copyright 2017 Databricks, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"), except
# that the use of services to which certain application programming
# interfaces (each, an "API") connect requires that the user first obtain
# a license for the use of the APIs from Databricks, Inc. ("Databricks"),
# by creating an account at www.databricks.com and agreeing to either (a)
# the Community Edition Terms of Service, (b) the Databricks Terms of
# Service, or (c) another written agreement between Licensee and Databricks
# for the use of the APIs.
#
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import mock
from tabulate import tabulate

import databricks_cli.clusters.cli as cli
from databricks_cli.utils import pretty_format
from tests.utils import get_callback

CREATE_RETURN = {'cluster_id': 'test'}
CREATE_JSON = '{"name": "test_cluster"}'


def test_create_cli_json():
    with mock.patch('databricks_cli.clusters.cli.create_cluster') as create_cluster_mock:
        with mock.patch('databricks_cli.jobs.cli.click.echo') as echo_mock:
            create_cluster_mock.return_value = CREATE_RETURN
            get_callback(cli.create_cli)(None, CREATE_JSON)
            assert create_cluster_mock.call_args[0][0] == json.loads(CREATE_JSON)
            assert echo_mock.call_args[0][0] == pretty_format(CREATE_RETURN)


CLUSTER_ID = 'test'


def test_start_cli():
    with mock.patch('databricks_cli.clusters.cli.start_cluster') as start_cluster_mock:
        get_callback(cli.start_cli)(CLUSTER_ID)
        assert start_cluster_mock.call_args[0][0] == CLUSTER_ID


def test_restart_cli():
    with mock.patch('databricks_cli.clusters.cli.restart_cluster') as restart_cluster_mock:
        get_callback(cli.restart_cli)(CLUSTER_ID)
        assert restart_cluster_mock.call_args[0][0] == CLUSTER_ID


def test_delete_cli():
    with mock.patch('databricks_cli.clusters.cli.delete_cluster') as delete_cluster_mock:
        get_callback(cli.delete_cli)(CLUSTER_ID)
        assert delete_cluster_mock.call_args[0][0] == CLUSTER_ID


def test_get_cli():
    with mock.patch('databricks_cli.clusters.cli.get_cluster') as get_cluster_mock:
        get_cluster_mock.return_value = '{}'
        get_callback(cli.get_cli)(CLUSTER_ID)
        assert get_cluster_mock.call_args[0][0] == CLUSTER_ID


LIST_RETURN = {
    'clusters': [{
        'cluster_id': 'test_id',
        'cluster_name': 'test_name',
        'state': 'PENDING'
    }]
}


def test_list_jobs():
    with mock.patch('databricks_cli.clusters.cli.list_clusters') as list_clusters_mock:
        with mock.patch('databricks_cli.clusters.cli.click.echo') as echo_mock:
            list_clusters_mock.return_value = LIST_RETURN
            get_callback(cli.list_cli)(None)
            assert echo_mock.call_args[0][0] == \
                tabulate([('test_id', 'test_name', 'PENDING')], tablefmt='plain')


def test_list_clusters_output_json():
    with mock.patch('databricks_cli.clusters.cli.list_clusters') as list_clusters_mock:
        with mock.patch('databricks_cli.clusters.cli.click.echo') as echo_mock:
            list_clusters_mock.return_value = LIST_RETURN
            get_callback(cli.list_cli)('json')
            assert echo_mock.call_args[0][0] == pretty_format(LIST_RETURN)
