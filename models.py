from datetime import date
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import validates, Mapped, mapped_column, relationship
import re
EMAIL_REGEX = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'



class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(db.String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(db.String(50), nullable=False)
    email: Mapped[str] = mapped_column(db.String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(db.String(256), nullable=False)
    hobbies: Mapped[list["Hobby"]] = relationship(back_populates="user")
    projects: Mapped[list["Project"]] = relationship(back_populates="user")

    @validates('first_name')
    def validate_first_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("First name cannot be empty")
        if len(value) > 50:
            raise ValueError("First name cannot exceed 50 characters")
        return value

    @validates('last_name')
    def validate_last_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Last name cannot be empty")
        if len(value) > 50:
            raise ValueError("Last name cannot exceed 50 characters")
        return value

    @validates('email')
    def validate_email(self, key, value):
        if not value or not value.strip():
            raise ValueError("Email cannot be empty")
        if not re.match(EMAIL_REGEX, value):
            raise ValueError("Invalid email address")
        if len(value) > 120:
            raise ValueError("Email cannot exceed 120 characters")
        return value

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Category(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    hobbies: Mapped[list["Hobby"]] = relationship(back_populates="category")
    
class Hobby(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    category_id: Mapped[int] = mapped_column(db.ForeignKey('category.id'), nullable=False)
    category: Mapped["Category"] = relationship(back_populates="hobbies")
    projects: Mapped[list["Project"]] = relationship(back_populates="hobby")

	

class Project(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(nullable=True)
    start_date: Mapped[date] = mapped_column(default=date.today, nullable=False)
    end_date: Mapped[Optional[date]] = mapped_column(nullable=True)
    project_link: Mapped[Optional[str]] = mapped_column(nullable=True)
    hobby_id: Mapped[int] = mapped_column(db.ForeignKey('hobby.id'), nullable=False)
    hobby: Mapped["Hobby"] = relationship(back_populates="projects")
    user_id: Mapped[int] = mapped_column(db.ForeignKey('user.id'), nullable=False)
    user: Mapped["User"] = relationship(back_populates="projects")