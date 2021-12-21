from flask import Flask, render_template, jsonify, Response, request
import json

app = Flask(__name__)

@app.route('/')
def index_view():
    username = request.args.get('username')
    return render_template('index.html', username = username)

@app.route('/users')
def users_view():
    with open('./users.json', 'r') as f:
        users = f.read()
    return Response(users, mimetype="application/json")

@app.route('/posts')
def posts_view():
    with open('./posts.json', 'r') as f:
        posts = json.load(f)
        users_posts = []

        # Add user to post content to make it easier to sort each post by time
        for user, content in posts.items():
            for post in content:
                post["user"] = user
                users_posts.append(post)

        # Sort the posts by time
        sorted_posts = sorted(users_posts, key = lambda x: x['time'], reverse=True)


    return Response(str(sorted_posts), mimetype="application/json")


# User timeline route
@app.route('/<username>')
def timeline_view(username):
    with open('./posts.json', 'r') as f:
        posts = json.load(f)

        # Sort user posts by time
        sorted_posts = sorted(posts[username], key = lambda x: x['time'], reverse=True)

    # Pass data to template
    return render_template('index.html', username = username, tweets = sorted_posts)

    
if __name__ == '__main__':
    app.run(host='127.0.0.1')