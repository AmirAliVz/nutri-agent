import uuid

from sqlalchemy import Column, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Meal(Base):
    __tablename__ = "meals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    raw_input = Column(Text, nullable=False)  # what user typed
    meal_type = Column(String)  # breakfast, lunch, dinner
    logged_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class FoodItem(Base):
    __tablename__ = "food_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    meal_id = Column(UUID(as_uuid=True), ForeignKey("meals.id"))
    name = Column(String, nullable=False)
    brand = Column(String, nullable=True)
    quantity = Column(Float)
    unit = Column(String)
    nutrition_id = Column(UUID(as_uuid=True), ForeignKey("nutrition_facts.id"))


class NutritionFacts(Base):
    __tablename__ = "nutrition_facts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    food_name = Column(String, nullable=False)
    brand = Column(String, nullable=True)
    source = Column(String)  # usda, nutritionix, web_search

    # Macros
    calories = Column(Float)
    protein = Column(Float)
    fat = Column(Float)
    carbohydrates = Column(Float)
    fiber = Column(Float)
    sugar = Column(Float)

    # Micros
    sodium = Column(Float)
    potassium = Column(Float)
    calcium = Column(Float)
    iron = Column(Float)
    vitamin_a = Column(Float)
    vitamin_c = Column(Float)
    vitamin_d = Column(Float)
    vitamin_b12 = Column(Float)
    magnesium = Column(Float)
    zinc = Column(Float)

    # Fat breakdown
    saturated_fat = Column(Float)
    unsaturated_fat = Column(Float)
    omega_3 = Column(Float)

    cached_at = Column(DateTime(timezone=True), server_default=func.now())


class Insight(Base):
    __tablename__ = "insights"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    meal_id = Column(UUID(as_uuid=True), ForeignKey("meals.id"))
    content = Column(Text, nullable=False)
    insight_type = Column(String)  # meal, daily, weekly
    created_at = Column(DateTime(timezone=True), server_default=func.now())
