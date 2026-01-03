import pytest
import json
from app import app, db, Recipe

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_health_check(client):
    rv = client.get('/health')
    assert rv.status_code == 200
    assert b'healthy' in rv.data

def test_create_recipe(client):
    data = {
        'title': 'Test Pancake',
        'description': 'Fluffy pancakes',
        'ingredients': 'Flour\nMilk\nEggs',
        'instructions': 'Mix\nFry',
        'cooking_time': 15,
        'difficulty': 'Easy',
        'cuisine': 'American'
    }
    rv = client.post('/recipes', json=data)
    assert rv.status_code == 201
    assert b'Test Pancake' in rv.data

def test_get_recipes(client):
    # Create one first
    client.post('/recipes', json={
        'title': 'Salad', 'description': 'Green', 'ingredients': 'Lettuce', 
        'instructions': 'Toss', 'cooking_time': 5, 'difficulty': 'Easy', 'cuisine': 'French'
    })
    
    rv = client.get('/recipes')
    assert rv.status_code == 200
    data = json.loads(rv.data)
    assert len(data) == 1
    assert data[0]['title'] == 'Salad'

def test_filter_recipes(client):
    client.post('/recipes', json={
        'title': 'Pasta', 'description': 'Yum', 'ingredients': 'Pasta', 
        'instructions': 'Boil', 'cooking_time': 10, 'difficulty': 'Easy', 'cuisine': 'Italian'
    })
    
    # Filter by cuisine
    rv = client.get('/recipes?cuisine=Italian')
    assert len(json.loads(rv.data)) == 1
    
    # Filter by wrong cuisine
    rv = client.get('/recipes?cuisine=Mexican')
    assert len(json.loads(rv.data)) == 0

def test_validation_error(client):
    # Missing fields
    rv = client.post('/recipes', json={'title': 'Incomplete'})
    assert rv.status_code == 400
