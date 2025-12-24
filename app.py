from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)



CATEGORIES = ["fashion", "entertainment", "tech", "sports", "finance"]

users = [
    {"id": 1, "name": "Pavan", "interests": ["fashion", "entertainment"]},
    {"id": 2, "name": "Kalyan", "interests": ["tech", "finance"]},
    {"id": 3, "name": "Krishna", "interests": ["sports"]},
    {"id": 4, "name": "Manish", "interests": ["fashion"]},
    {"id": 5, "name": "Rahul", "interests": ["entertainment", "tech"]},
]

posts = [
    {"id": 1, "title": "Summer Fashion Trends", "tag": "fashion", "views": 120, "created_at": 1},
    {"id": 2, "title": "Latest Movie Review", "tag": "entertainment", "views": 300, "created_at": 2},
    {"id": 3, "title": "New Smartphone Launch", "tag": "tech", "views": 500, "created_at": 3},
    {"id": 4, "title": "IPL Match Highlights", "tag": "sports", "views": 700, "created_at": 4},
    {"id": 5, "title": "Personal Finance Tips", "tag": "finance", "views": 250, "created_at": 5},
    {"id": 6, "title": "Street Style Looks", "tag": "fashion", "views": 400, "created_at": 6},
    {"id": 7, "title": "Celebrity Interview", "tag": "entertainment", "views": 150, "created_at": 7},
    {"id": 8, "title": "AI in Daily Life", "tag": "tech", "views": 900, "created_at": 8},
    {"id": 9, "title": "Home Workout Routine", "tag": "sports", "views": 200, "created_at": 9},
    {"id": 10, "title": "Investment Basics", "tag": "finance", "views": 600, "created_at": 10},
]



def get_user_by_id(user_id):
    for user in users:
        if user["id"] == user_id:
            return user
    return None


@app.route("/")
def health():
    return jsonify({"status": "Recommendation API running"})

@app.route("/categories")
def get_categories():
    return jsonify(CATEGORIES)

@app.route("/users")
def get_users():
    return jsonify(users)

@app.route("/posts")
def get_posts():
    return jsonify(posts)



@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({"error": "User name is required"}), 400

    interests = data.get("interests", [])

    for interest in interests:
        if interest not in CATEGORIES:
            return jsonify({"error": f"Invalid category: {interest}"}), 400

    new_user = {
        "id": len(users) + 1,
        "name": data["name"],
        "interests": interests
    }

    users.append(new_user)
    return jsonify(new_user), 201



@app.route("/feed/<int:user_id>")
def get_feed(user_id):

    # Safe pagination parsing
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 5))
    except:
        return jsonify({"error": "Invalid pagination parameters"}), 400

    # Safety limits
    page = max(page, 1)
    limit = min(max(limit, 1), 20)

    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    interests = user["interests"]

    # 1. Interest-based posts
    interest_posts = [p for p in posts if p["tag"] in interests]
    interest_posts.sort(key=lambda x: x["created_at"], reverse=True)

    # 2. Fallback to trending
    if len(interest_posts) < limit:
        trending = sorted(posts, key=lambda x: x["views"], reverse=True)
        for post in trending:
            if post not in interest_posts:
                interest_posts.append(post)
            if len(interest_posts) >= limit:
                break

    total = len(interest_posts)

    # 3. Pagination
    start = (page - 1) * limit
    end = start + limit
    paginated_feed = interest_posts[start:end]

    return jsonify({
        "user": user["name"],
        "page": page,
        "limit": limit,
        "total": total,
        "feed": paginated_feed
    })



if __name__ == "__main__":
    app.run(debug=True)
