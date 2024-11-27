import pytest
import requests

def test_get_user_endpoint():
    # Replace 'http://localhost:5000' with the actual URL where your Flask app is running
    url = "http://localhost:5000/api/user-ranks?player=wens-890"
    
    response = requests.get(url)
    
    # Assert that the response status code is 200
    assert response.status_code == 200