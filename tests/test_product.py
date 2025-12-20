def test_home_page_loads(client):
    """Test that the home page loads successfully."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"EasePharma" in response.data

def test_search_function(client):
    """Test that search page loads without crashing."""
    response = client.get('/search?q=Vitamin')
    assert response.status_code == 200