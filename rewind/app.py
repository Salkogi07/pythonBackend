from flask import Flask, jsonify, request

app = Flask(__name__) 
app.users = {}
app.posts = []
app.idCnt = 1

@app.route("/sign-up", methods=['POST'])
def sign_up():
    newUser = request.json
    newUser["id"] = app.idCnt
    app.users[app.idCnt] = newUser
    app.idCnt = app.idCnt + 1
    return jsonify(newUser)

@app.route("/post", methods=['POST'])
def post():
    payload = request.json
    userID = int(payload['id'])
    msg = payload['msg']

    if userID not in app.users:
        return '사용자가 존재하지 않습니다', 400
    if len(msg) > 300:
        return '300자를 초과했습니다', 400
    
    app.posts.append({
        'user_id' : userID,
        'post' : msg
    })
    return '성공', 200

@app.route("/follow", methods=['POST'])
def follow():
    payload = request.json
    userID = int(payload['id'])
    userIDtoFollow = int(payload['follow'])

    if userID not in app.users or userIDtoFollow not in app.users:
        return '사용자가 존재하지 않습니다.', 400
    
    user = app.users[userID]
    if user.get('follow'):
        user['follow'].append(userIDtoFollow)
        user['follow'] = list(set(user['follow']))
    else:
        user['follow'] = [userIDtoFollow]
    return jsonify(user)

@app.route("/follow", methods=['POST'])
def follow():
    payload = request.json
    userID = int(payload['id'])
    userIDtoFollow = int(payload['follow'])

    if userID not in app.users or userIDtoFollow not in app.users:
        return '사용자가 존재하지 않습니다.', 400
    
    user = app.users[userID]
    if user.get('follow'):
        try: user['follow'].remove(userIDtoFollow)
        except: pass
    else:
        user['follow'] = []
    return jsonify(user)


if '__main__' == __name__:
    app.run()

# @app.route("/check-users", methods=['GET'])
# def check_users():
#     return app.users

# app.tweets = []

# @app.route("/tweet", methods=['POST'])
# def tweet():
#     payload = request.json
#     userID = int(payload['id'])
#     tweet = payload['tweet']

#     if userID not in app.users:
#         return "사용자가 존재하지 않습니다.", 400

#     if len(tweet) > 300:
#         return "300자를 초과했습니다.", 400

#     app.tweets.append({
#         'user_id': userID,
#         'tweet': tweet
#     })
#     return '', 200

# @app.route("/check-tweet", methods=['POST'])
# def check_tweet():
#     return app.tweets

# @app.route("/unfollow", methods=['POST'])
# def unfollow():
#     payload = request.json
#     userID = int(payload['id'])
#     userIDtoUnfollow = int(payload['unfollow'])
#     if (userID or userIDtoUnfollow) not in app.users:
#         return '사용자가 존재하지 않습니다.'
#     user = app.users[userID]
#     if user.get('follow'):
#         user['follow'].remove(userIDtoUnfollow)

#     return jsonify(user)
