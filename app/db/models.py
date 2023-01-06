from sqlalchemy import Column, Boolean, Integer, String, DateTime
from db.sql import Base
from datetime import datetime

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    time_created = Column(DateTime, default=datetime.utcnow)
    email = Column(String, unique=True)
    discord_id = Column(Integer, unique=True)
    twitch_id = Column(String, unique=True)
    youtube_id = Column(String, unique=True)
    bb_bills = Column(Integer, default=0)
    exp = Column(Integer, default=0)