import io
import os
import json
import pytest
import datetime

from pacu.main import Main
from pacu.core import lib
from pacu.core.models import PacuSession

from unittest import mock
from freezegun import freeze_time


@mock.patch('requests.get')
@mock.patch('pacu.core.lib.home_dir')
@mock.patch('pacu.core.lib.pacu_dir')
def test_fresh_install(pacu_dir, home_dir, get, tmp_path):
    pacu_dir.return_value = tmp_path
    home_dir.return_value = tmp_path
    get.return_value.text = '2021-01-01'
    (tmp_path/'pacu/').mkdir()
    with open(tmp_path/'pacu/last_update.txt','w') as f:
        f.write('2021-01-01')

    with freeze_time('2021-01-01'):
        assert  False == Main.check_for_updates(None)

    assert os.path.isfile(tmp_path/'update_info.json')
    with open(tmp_path/'update_info.json','r') as f:
        update_info = json.load(f)
    assert update_info['last_check'] == '2021-01-01'
    assert update_info['local_lastest'] == '2021-01-01'
    
@mock.patch('requests.get')
@mock.patch('pacu.core.lib.home_dir')
@mock.patch('pacu.core.lib.pacu_dir')
def test_one_month_no_update(pacu_dir, home_dir, get, tmp_path):
    pacu_dir.return_value = tmp_path
    home_dir.return_value = tmp_path
    get.return_value.text = '2021-01-01'
    (tmp_path/'pacu/').mkdir()
    with open(tmp_path/'pacu/last_update.txt','w') as f:
        f.write('2021-01-01')

    update_info = {
            'last_check':'2021-01-01',
            'local_lastest':'2021-01-01'
        }
    with open(tmp_path/'update_info.json','w') as f:
        json.dump(update_info, f)

    with freeze_time('2021-02-01'):
        assert  False == Main.check_for_updates(None)

@mock.patch('requests.get')
@mock.patch('pacu.core.lib.home_dir')
@mock.patch('pacu.core.lib.pacu_dir')
def test_one_month_updatable(pacu_dir, home_dir, get, tmp_path):
    pacu_dir.return_value = tmp_path
    home_dir.return_value = tmp_path
    get.return_value.text = '2021-02-01'
    (tmp_path/'pacu/').mkdir()
    with open(tmp_path/'pacu/last_update.txt','w') as f:
        f.write('2021-01-01')

    update_info = {
            'last_check':'2021-01-01',
            'local_lastest':'2021-01-01'
        }
    with open(tmp_path/'update_info.json','w') as f:
        json.dump(update_info, f)

    with freeze_time('2021-02-01'):
        assert  True == Main.check_for_updates(None)

    with open(tmp_path/'update_info.json','r') as f:
        update_info = json.load(f)
    assert update_info['last_check'] == '2021-02-01'
    assert update_info['local_lastest'] == '2021-02-01'

@mock.patch('pacu.core.lib.home_dir')
@mock.patch('pacu.core.lib.pacu_dir')
def test_local_updatable(pacu_dir, home_dir, tmp_path):
    pacu_dir.return_value = tmp_path
    home_dir.return_value = tmp_path
    (tmp_path/'pacu/').mkdir()
    with open(tmp_path/'pacu/last_update.txt','w') as f:
        f.write('2021-01-01')

    update_info = {
            'last_check':'2021-01-01',
            'local_lastest':'2021-02-01'
        }
    with open(tmp_path/'update_info.json','w') as f:
        json.dump(update_info, f)

    with freeze_time('2021-01-01'):
        assert  True == Main.check_for_updates(None)
