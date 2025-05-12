from sqlalchemy import create_engine, Column, Integer, Numeric, String, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Nutrient(Base):
    __tablename__ = "NUTRIENT"
    nutrient_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    unit = Column(String(20), nullable=False)

class Age(Base):
    __tablename__ = "AGE"
    age_id = Column(Integer, primary_key=True)
    age_min = Column(Integer, nullable=False)
    age_max = Column(Integer, nullable=False)
    label = Column(String(20), nullable=False)

class Sex(Base):
    __tablename__ = "SEX"
    sex_id = Column(Integer, primary_key=True)
    sex_code = Column(String(10), nullable=False, unique=True)

class NutrientRef(Base):
    __tablename__ = "NUTRIENT_REFERENCE"
    nutrient_id  = Column(Integer, ForeignKey("NUTRIENT.nutrient_id"), primary_key=True)
    age_id       = Column(Integer, ForeignKey("AGE.age_id"), primary_key=True)
    sex_id       = Column(Integer, ForeignKey("SEX.sex_id"), primary_key=True)
    rda_amount   = Column(Numeric(10, 3))
    ul_amount    = Column(Numeric(10, 3))
    ai_amount   = Column(Numeric(10, 3))

class CalorieRef(Base):
    __tablename__ = "CALORIE_REFERENCE"
    age_id       = Column(Integer, ForeignKey("AGE.age_id"), primary_key=True)
    sex_id       = Column(Integer, ForeignKey("SEX.sex_id"), primary_key=True)
    kcal         = Column(Integer, nullable=False)
