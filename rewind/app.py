from flask import Flask, request, jsonify

app = Flask(__name__) 
app.idNum = 1
app.users = {}

@app.route("/sign-up", methods=['POST'])
def sign_up():
    newUser = request.json
    newUser["idNum"] = app.idNum
    app.users[app.idNum] = newUser
    app.idNum = app.idNum + 1
    return jsonify(newUser)



@app.route("/check-users", methods=['GET'])
def check_users():
    return app.users

app.tweets = []

@app.route("/tweet", methods=['POST'])
def tweet():
    payload = request.json
    userID = int(payload['id'])
    tweet = payload['tweet']

    if userID not in app.users:
        return "사용자가 존재하지 않습니다.", 400

    if len(tweet) > 300:
        return "300자를 초과했습니다.", 400

    app.tweets.append({
        'user_id': userID,
        'tweet': tweet
    })
    return '', 200

@app.route("/check-tweet", methods=['POST'])
def check_tweet():
    return app.tweets

@app.route("/follow", methods=['POST'])
def follow():
    payload = request.json
    userID = int(payload['id'])
    userIDtoFollow = int(payload['follow'])

    if(userID or userIDtoFollow) not in app.users:
        return '사용자가 존재하지 않습니다.', 400
    
    user = app.users[userID]
    if user.get('follow'):
        user['follow'].append(userIDtoFollow)
        user['follow'] = list(set(user['follow']))
    else:
        user['follow'] = [userIDtoFollow]
    return jsonify(user)

@app.route("/unfollow", methods=['POST'])
def unfollow():
    payload = request.json
    userID = int(payload['id'])
    userIDtoUnfollow = int(payload['unfollow'])
    if (userID or userIDtoUnfollow) not in app.users:
        return '사용자가 존재하지 않습니다.'
    user = app.users[userID]
    if user.get('follow'):
        user['follow'].remove(userIDtoUnfollow)

    return jsonify(user)

if '__main__' == __name__:
    app.run()