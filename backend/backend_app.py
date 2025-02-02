from flask import Flask, jsonify, request
from flask_cors import CORS

from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


SWAGGER_URL="/api/docs"  # (1) swagger endpoint e.g. HTTP://localhost:5002/api/docs
API_URL="/static/masterblog.json" # (2) ensure you create this dir and file

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Masterblog API' # (3) You can change this if you like
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]
def find_post_by_id(post_id):
    """ Find post with the id `post_id`.
    If there is no post with this id, return None. """
    for post in POSTS:
        if post['id'] == post_id:
            return post
    return None

@app.route('/api/posts', methods=['GET'])
def get_posts():
    sort_field = request.args.get('sort')
    direction = request.args.get('direction', 'asc').lower()

    # If sort_field is provided, we need to sort the posts
    if sort_field:
        # Check if the sort field is valid (either 'title' or 'content')
        if sort_field not in ['title', 'content']:
            return jsonify({"error": "Invalid sort field. Choose 'title' or 'content'."}), 400

        # Sort based on the direction
        reverse = direction == 'desc'

        # Sort the posts by the specified field and direction
        POSTS_sorted = sorted(POSTS, key=lambda post: post.get(sort_field, ''), reverse=reverse)

        return jsonify(POSTS_sorted)

    # If no sorting is provided, return posts in the original order
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

@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    # Find the post with the given ID
    post = find_post_by_id(id)

    # If the post wasn't found, return a 404 error
    if post is None:
        return jsonify("Not Found"), 404

    # Remove the post from the list
    for post in POSTS:
        if post['id'] == id:
            POSTS.remove(post)

    # Return the deleted message
    message = {
    "message": f"Post with id {post['id']} has been deleted successfully."
}
    return jsonify(message),200

@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    # Find the post with the given ID
    post = find_post_by_id(id)

    # If the post wasn't found, return a 404 error
    if post is None:
        return 'Not Found', 404

    # Update the post with the new data
    new_data = request.get_json()
    post.update(new_data)

    # Return the updated post
    return jsonify(post)

@app.route('/api/posts/search', methods=['GET'])
def search_post():
    # Handle GET request (with title)
    title = request.args.get('title')
    if title:
        filtered_posts = [post for post in POSTS if title.lower() in post.get('title', '').lower()]
        return jsonify(filtered_posts)

    # Handle GET request (with content)
    content = request.args.get('content')
    if content:
        filtered_posts = [post for post in POSTS if content.lower() in post.get('content', '').lower()]
        return jsonify(filtered_posts)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
