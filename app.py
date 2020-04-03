from flask import Flask, render_template, jsonify, Response, request
import json
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def index_view():
    username = request.args.get('username')
    return render_template('index.html', username=username)


@app.route('/users')
def users_view():
    with open('./users.json', 'r') as f:
        users = json.loads(f.read())
    return render_template('users.html', users=users)


@app.route('/posts')
def posts_view():
    with open('./posts.json', 'r') as f:
        # read the json from posts.json
        posts = json.loads(f.read())
    return render_template('posts.html', posts=posts)

 # date sorting function from first to last according to date
def sort(data, name):
    return sorted(data[name], key=lambda x: datetime.strptime(x['time'], '%Y-%m-%dT%H:%M:%SZ'), reverse=False)

# implementing user timelines
@app.route('/timeline/<name>')
# pass in the name of the user we are
def timeline_view(name):
    with open('./posts.json', 'r') as f:
        data = json.loads(f.read())
        # grab the user data from the posts.json file
    return render_template('timelines.html', data={
        # implement the sort function on the user's post's
        'posts': sort(data, name),
        'user': name,
        # grab the length of the posts made
        'postsAmount': len(data[name])
    })


# enabled debug mode for refreshing
if __name__ == '__main__':
    app.run(debug=True)
