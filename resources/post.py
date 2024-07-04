from flask_restful import Resource, reqparse
from models import Post, Comment
from app import db

class PostListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, required=True, help="Title is required")
    parser.add_argument('body', type=str, required=True, help="Body is required")
    parser.add_argument('tags', type=str)
    parser.add_argument('is_draft', type=bool)

    def get(self):
        posts = Post.query.filter_by(is_draft=False).all()
        return [{"id": post.id, "title": post.title, "body": post.body, "tags": post.tags, "created_at": post.created_at} for post in posts], 200

    def post(self):
        data = PostListResource.parser.parse_args()
        post = Post(title=data['title'], body=data['body'], tags=data['tags'], is_draft=data['is_draft'], user_id=1) # Assuming user_id=1 for simplicity
        db.session.add(post)
        db.session.commit()
        return {"message": "Post created successfully", "post_id": post.id}, 201

class PostResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str)
    parser.add_argument('body', type=str)
    parser.add_argument('tags', type=str)
    parser.add_argument('is_draft', type=bool)

    def get(self, post_id):
        post = Post.query.get_or_404(post_id)
        if post.is_draft:
            return {"message": "Post not found"}, 404
        return {"id": post.id, "title": post.title, "body": post.body, "tags": post.tags, "created_at": post.created_at}, 200

    def put(self, post_id):
        post = Post.query.get_or_404(post_id)
        data = PostResource.parser.parse_args()
        if data['title']:
            post.title = data['title']
        if data['body']:
            post.body = data['body']
        if data['tags']:
            post.tags = data['tags']
        if data['is_draft'] is not None:
            post.is_draft = data['is_draft']
        db.session.commit()
        return {"message": "Post updated successfully"}, 200

    def delete(self, post_id):
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return {"message": "Post deleted successfully"}, 200
