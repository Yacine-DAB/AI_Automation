from sqlalchemy import (
     Column,
     Integer,
     String,
     DateTime,
     ForeignKey,
     JSON,
     Boolean,
)
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class Video(Base):
     __tablename__ = 'videos'
     
     id = Column(Integer, primary_key=True, index=True)
     url = Column(String, index=True)
     created_at = Column(DateTime, default=datetime.now)
     status = Column(String, default='pending')
     
     video_metadata = relationship('Metadata',
                                   back_populates='video',
                                   uselist=False)
     summary = relationship('VideoSummary',
                            back_populates='video',
                            uselist=False)
     sponsor = relationship('VideoSponsor',
                            back_populates='video',
                            uselist=False)
     
     
class metadata(Base):
     __tablename__ = 'metadata'
     
     id = Column(Integer, primary_key=True, index=True)
     video_id = Column(Integer, ForeignKey('videos.id'))
     created_at = Column(DateTime, default=datetime.now)
     status = Column(String, default='pending')
     creator = Column(String, index=True, nullable=True)
     metadata_json = Column(JSON, nullable=True)
     
     video = relationship('Video', 
                          back_populates='video_metadata')
     
class VideoSummary(Base):
     __tablename__ = 'video_summaries'
     
     id = Column(Integer, primary_key=True, index=True)
     video_id = Column(Integer, ForeignKey('videos.id'))
     sumamry = Column(String)
     created_at = Column(DateTime, default=datetime.now)
     status = Column(String, default='pending')
     
     video = relationship('Video',
                          back_populates='sumamry')
     
class VideoSponsor(Base):
     __tablename__ = 'video_sponsors'
     
     id = Column(Integer, primary_key=True, index=True)
     video_id = Column(Integer, ForeignKey('videos.id'))
     is_sponsored = Column(Boolean, default=False)
     brands_mentioned = Column(DateTime, default=datetime.now)
     status = Column(String, default='pending')
     
     video = relationship('Video', back_populates='sponsor')
     
     
class Channel(Base):
     __tablename__ = 'chennels'
     
     id = Column(Integer, primary_key=True, index=True)
     url = Column(String, index=True)
     created_at = Column(DateTime, default=datetime.now)
     status = Column(String, default='pending')
     channel_metadata = Column(JSON, nullable=False)
     
     