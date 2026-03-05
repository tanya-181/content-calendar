from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
from hashtag_engine import suggest_hashtags

app = Flask(__name__)
CORS(app)

DB_PATH = os.path.join("/tmp", "database.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            caption TEXT,
            platform TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'to_write',
            scheduled_date TEXT,
            hashtags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


# ── POSTS ──────────────────────────────────────────────────────────────────

@app.route("/api/posts", methods=["GET"])
def get_posts():
    platform = request.args.get("platform")
    conn = get_db()
    if platform and platform != "all":
        posts = conn.execute(
            "SELECT * FROM posts WHERE platform = ? ORDER BY created_at DESC", (platform,)
        ).fetchall()
    else:
        posts = conn.execute("SELECT * FROM posts ORDER BY created_at DESC").fetchall()
    conn.close()
    return jsonify([dict(p) for p in posts])


@app.route("/api/posts", methods=["POST"])
def create_post():
    data = request.json
    conn = get_db()
    cursor = conn.execute(
        """INSERT INTO posts (title, caption, platform, status, scheduled_date, hashtags)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (
            data["title"],
            data.get("caption", ""),
            data["platform"],
            data.get("status", "to_write"),
            data.get("scheduled_date", ""),
            data.get("hashtags", ""),
        ),
    )
    conn.commit()
    post = conn.execute("SELECT * FROM posts WHERE id = ?", (cursor.lastrowid,)).fetchone()
    conn.close()
    return jsonify(dict(post)), 201


@app.route("/api/posts/<int:post_id>", methods=["PUT"])
def update_post(post_id):
    data = request.json
    conn = get_db()
    conn.execute(
        """UPDATE posts SET title=?, caption=?, platform=?, status=?, scheduled_date=?, hashtags=?
           WHERE id=?""",
        (
            data["title"],
            data.get("caption", ""),
            data["platform"],
            data["status"],
            data.get("scheduled_date", ""),
            data.get("hashtags", ""),
            post_id,
        ),
    )
    conn.commit()
    post = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    conn.close()
    return jsonify(dict(post))


@app.route("/api/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    conn = get_db()
    conn.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Post deleted"}), 200


@app.route("/api/posts/<int:post_id>/status", methods=["PATCH"])
def update_status(post_id):
    data = request.json
    conn = get_db()
    conn.execute("UPDATE posts SET status=? WHERE id=?", (data["status"], post_id))
    conn.commit()
    post = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    conn.close()
    return jsonify(dict(post))


# ── HASHTAG SUGGESTER ──────────────────────────────────────────────────────

@app.route("/api/hashtags", methods=["POST"])
def get_hashtags():
    data = request.json
    topic = data.get("topic", "")
    platform = data.get("platform", "instagram")
    hashtags = suggest_hashtags(topic, platform)
    return jsonify({"hashtags": hashtags})


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
