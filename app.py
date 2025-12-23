from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

categories = ["fashion", "entertainment", "tech", "sports", "finance"]

users = [
    {"id": 1, "name": "pavan", "categories": ["fashion", "entertainment"]},
    {"id": 2, "name": "kalyan", "categories": ["tech", "finance"]},
    {"id": 3, "name": "krishna", "categories": ["sports"]},
    {"id": 4, "name": "manish", "categories": ["fashion"]},
    {"id": 5, "name": "rahul", "categories": ["entertainment", "tech"]},
]

posts = [
    {"id": 1, "title": "Summer Fashion Trends", "tag": "fashion"},
    {"id": 2, "title": "Latest Movie Review", "tag": "entertainment"},
    {"id": 3, "title": "New Smartphone Launch", "tag": "tech"},
    {"id": 4, "title": "IPL Match Highlights", "tag": "sports"},
    {"id": 5, "title": "Personal Finance Tips", "tag": "finance"},
    {"id": 6, "title": "Street Style Looks", "tag": "fashion"},
    {"id": 7, "title": "Celebrity Interview", "tag": "entertainment"},
    {"id": 8, "title": "AI in Daily Life", "tag": "tech"},
    {"id": 9, "title": "Home Workout Routine", "tag": "sports"},
    {"id": 10, "title": "Investment Basics", "tag": "finance"},
]

@app.route("/")
def health():
    return jsonify({"status": "API is running"})

@app.route("/users")
def list_users():
    return jsonify(users)

@app.route("/categories")
def list_categories():
    return jsonify(categories)

@app.route("/posts")
def list_posts():
    return jsonify(posts)

@app.route("/feed/<int:user_id>")
def user_feed(user_id):
    selected_user = None
    for user in users:
        if user["id"] == user_id:
            selected_user = user
            break

    if selected_user is None:
        return jsonify({"error": "User not found"}), 404

    result = []
    for post in posts:
        if post["tag"] in selected_user["categories"]:
            result.append(post)

    return jsonify({
        "user": selected_user["name"],
        "recommended_posts": result
    })

@app.route("/users", methods=["POST"])
def create_user():
    body = request.get_json()
    new_user = {
        "id": len(users) + 1,
        "name": body.get("name"),
        "categories": body.get("categories", [])
    }
    users.append(new_user)
    return jsonify(new_user), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
