from flask import Flask, jsonify, request

app = Flask(__name__)

posts = []


# Endpoint for creating a new post
@app.route('/posts', methods=['POST'])
def create_post():

    data = request.get_json()
    id = data.get('id')
    username = data.get('username')
    caption = data.get('caption')

    post = {
        'id': id,
        'username': username,
        'caption': caption
    }


    # Add the post to the list
    posts.append(post)

    return jsonify(post), 201

# Endpoint for listing all posts
@app.route('/posts', methods=['GET'])
def list_posts():
    return jsonify(posts)

# Endpoint for deleting a post
@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    # Find the post with the given ID
    for post in posts:
        if post['id'] == post_id:
            # Remove the post from the list
            posts.remove(post)
            return jsonify({'message': 'Post deleted'})

    # If the post ID is not found, return an error message
    return jsonify({'error': 'Post not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
