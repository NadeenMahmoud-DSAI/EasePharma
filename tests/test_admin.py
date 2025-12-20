import pytest
from flask import session

def test_admin_dashboard_access_authorized(client):
    """Test that an Admin user can access the dashboard."""
    with client.session_transaction() as sess:
        sess['user_id'] = '999'
        sess['role'] = 'Admin'
        sess['user_name'] = 'Test Admin'

    response = client.get('/admin/dashboard', follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Admin Dashboard" in response.data
    assert b"Total Revenue" in response.data

def test_admin_dashboard_access_denied_customer(client):
    """Test that a standard Customer CANNOT access the dashboard."""
    with client.session_transaction() as sess:
        sess['user_id'] = '100'
        sess['role'] = 'Customer'
        sess['user_name'] = 'Test Customer'

    response = client.get('/admin/dashboard', follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Access Denied" in response.data or b"Login" in response.data

def test_admin_dashboard_access_denied_guest(client):
    """Test that a generic Guest (not logged in) cannot access the dashboard."""
    response = client.get('/admin/dashboard', follow_redirects=True)
    
    assert b"Login" in response.data