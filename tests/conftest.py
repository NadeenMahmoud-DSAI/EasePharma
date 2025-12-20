import sys
import os
import pytest
import shutil


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from app import create_app

@pytest.fixture
def client():
    test_data_dir = "tests_data"
    os.makedirs(test_data_dir, exist_ok=True)
    
    app = create_app()
    app.config['TESTING'] = True
    app.config['DATA_PATH'] = test_data_dir
    app.config['WTF_CSRF_ENABLED'] = False  

    with app.test_client() as client:
        yield client

    if os.path.exists(test_data_dir):
        shutil.rmtree(test_data_dir)