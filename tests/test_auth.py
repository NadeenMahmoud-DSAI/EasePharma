import unittest

def test_register_and_login(client):
    """Test that a user can register and then login."""
    
    # 1. Register
    response = client.post('/auth/register', data={
        'email': 'test@test.com',
        'password': 'password123',
        'full_name': 'Test User'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Registration successful" in response.data or b"Login" in response.data

    # 2. Login
    response = client.post('/auth/login', data={
        'email': 'test@test.com',
        'password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome back" in response.data or b"EasePharma" in response.data