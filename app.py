import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

# --- Configuration ---
app = Flask(__name__)
# Enable CORS for all domains (allows frontend to talk to backend)
CORS(app)

# Database Configuration (SQLite)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'recipes.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Models ---

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)  # Stored as newline-separated string
    instructions = db.Column(db.Text, nullable=False) # Stored as newline-separated string
    cooking_time = db.Column(db.Integer, nullable=False) # In minutes
    difficulty = db.Column(db.String(20), nullable=False) # Easy, Medium, Hard
    cuisine = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'ingredients': self.ingredients,
            'instructions': self.instructions,
            'cooking_time': self.cooking_time,
            'difficulty': self.difficulty,
            'cuisine': self.cuisine,
            'created_at': self.created_at.isoformat()
        }

# --- Routes ---

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}), 200

@app.route('/stats', methods=['GET'])
def get_stats():
    total_recipes = Recipe.query.count()
    cuisines = db.session.query(Recipe.cuisine).distinct().count()
    return jsonify({
        'total_recipes': total_recipes,
        'unique_cuisines': cuisines
    })

@app.route('/recipes', methods=['GET'])
def get_recipes():
    query = request.args.get('search')
    cuisine_filter = request.args.get('cuisine')
    difficulty_filter = request.args.get('difficulty')

    sql_query = Recipe.query

    if query:
        search = f"%{query}%"
        sql_query = sql_query.filter(
            (Recipe.title.like(search)) | 
            (Recipe.description.like(search))
        )
    
    if cuisine_filter and cuisine_filter != 'All':
        sql_query = sql_query.filter(Recipe.cuisine == cuisine_filter)
        
    if difficulty_filter and difficulty_filter != 'All':
        sql_query = sql_query.filter(Recipe.difficulty == difficulty_filter)

    recipes = sql_query.order_by(Recipe.created_at.desc()).all()
    return jsonify([r.to_dict() for r in recipes])

@app.route('/recipes/<int:id>', methods=['GET'])
def get_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    return jsonify(recipe.to_dict())

@app.route('/recipes', methods=['POST'])
def create_recipe():
    data = request.get_json()
    
    # Basic Validation
    required_fields = ['title', 'description', 'ingredients', 'instructions', 'cooking_time', 'difficulty', 'cuisine']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    new_recipe = Recipe(
        title=data['title'],
        description=data['description'],
        ingredients=data['ingredients'],
        instructions=data['instructions'],
        cooking_time=int(data['cooking_time']),
        difficulty=data['difficulty'],
        cuisine=data['cuisine']
    )
    
    db.session.add(new_recipe)
    db.session.commit()
    return jsonify(new_recipe.to_dict()), 201

@app.route('/recipes/<int:id>', methods=['PUT'])
def update_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    data = request.get_json()

    recipe.title = data.get('title', recipe.title)
    recipe.description = data.get('description', recipe.description)
    recipe.ingredients = data.get('ingredients', recipe.ingredients)
    recipe.instructions = data.get('instructions', recipe.instructions)
    recipe.cooking_time = int(data.get('cooking_time', recipe.cooking_time))
    recipe.difficulty = data.get('difficulty', recipe.difficulty)
    recipe.cuisine = data.get('cuisine', recipe.cuisine)

    db.session.commit()
    return jsonify(recipe.to_dict())

@app.route('/recipes/<int:id>', methods=['DELETE'])
def delete_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    db.session.delete(recipe)
    db.session.commit()
    return jsonify({'message': 'Recipe deleted successfully'})

# --- Initialization ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database initialized successfully.")
    app.run(debug=True, port=5000)
