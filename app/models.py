# backend/app/models.py
from sqlalchemy import Table, Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import metadata

words = Table(
    "words",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("word", String(100), nullable=False),
    Column("pos", String(50)),          
    Column("meaning", Text),
    Column("created_at", DateTime, server_default=func.now()))

attempts = Table(
    "attempts",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("word_id", Integer, ForeignKey("words.id")),
    Column("original_sentence", Text),
    Column("corrected_sentence", Text),
    Column("score", Float),
    Column("level", String(50)),
    Column("suggestion", Text),
    Column("created_at", DateTime, server_default=func.now()))
