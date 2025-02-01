from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    # Get the new post data from the client
    new_post = request.get_json()

    # Check if both 'title' and 'content' are provided
    if not new_post.get('title') or not new_post.get('content'):
        missing_fields = []
        if not new_post.get('title'):
            missing_fields.append('title')
        if not new_post.get('content'):
            missing_fields.append('content')

        # Return a 400 error with a message about the missing fields
        return jsonify({"error": "Missing fields", "missing_fields": missing_fields}), 400

    # Generate a new ID for the post
    new_id = max(post['id'] for post in POSTS) + 1 if POSTS else 1
    new_post['id'] = new_id

    # Add the new post to our list
    POSTS.append(new_post)

    # Return the new post data to the client
    return jsonify(new_post), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
