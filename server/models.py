from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
import re
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, name):
        if not name or name.strip() == '':
            raise ValueError('Author must have a name')
        # Check for unique name
        try:
            existing = Author.query.filter(Author.name == name).first()
            if existing and (self.id is None or existing.id != self.id):
                raise ValueError('Author name must be unique')
        except Exception as e:
            # Table might not exist yet during tests
            # Check if this is an OperationalError (table doesn't exist)
            if 'no such table' in str(e):
                pass
            else:
                raise
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if phone_number and not re.match(r'^\d{10}$', phone_number):
            raise ValueError('Phone number must be exactly ten digits')
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    CLICKBAIT_PATTERNS = ["Won't Believe", "Secret", "Top", "Guess"]

    @validates('title')
    def validate_title(self, key, title):
        if not any(pattern in title for pattern in self.CLICKBAIT_PATTERNS):
            raise ValueError('Title must contain clickbait phrases')
        return title

    @validates('content')
    def validate_content(self, key, content):
        if content and len(content) < 250:
            raise ValueError('Content must be at least 250 characters')
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if summary and len(summary) > 250:
            raise ValueError('Summary must be a maximum of 250 characters')
        return summary

    @validates('category')
    def validate_category(self, key, category):
        if category and category not in ['Fiction', 'Non-Fiction']:
            raise ValueError('Category must be either Fiction or Non-Fiction')
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
