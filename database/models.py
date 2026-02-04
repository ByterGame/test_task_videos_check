from datetime import datetime
from dataclasses import dataclass
from typing import Optional
import uuid


@dataclass
class Video:
    id: uuid.UUID
    creator_id: str
    video_created_at: datetime
    views_count: int = 0
    likes_count: int = 0
    comments_count: int = 0
    reports_count: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Video':
        return cls(
            id=uuid.UUID(str(data['id'])) if isinstance(data.get('id'), str) else data.get('id'),
            creator_id=str(data.get('creator_id')),
            video_created_at=data.get('video_created_at'),
            views_count=data.get('views_count', 0),
            likes_count=data.get('likes_count', 0),
            comments_count=data.get('comments_count', 0),
            reports_count=data.get('reports_count', 0),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def to_dict(self) -> dict:
        return {
            'id': str(self.id),
            'creator_id': self.creator_id,
            'video_created_at': self.video_created_at.isoformat() if self.video_created_at else None,
            'views_count': self.views_count,
            'likes_count': self.likes_count,
            'comments_count': self.comments_count,
            'reports_count': self.reports_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


@dataclass
class VideoSnapshot:
    id: uuid.UUID
    video_id: uuid.UUID
    views_count: int = 0
    likes_count: int = 0
    comments_count: int = 0
    reports_count: int = 0
    delta_views_count: int = 0
    delta_likes_count: int = 0
    delta_comments_count: int = 0
    delta_reports_count: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> 'VideoSnapshot':
        return cls(
            id=uuid.UUID(str(data['id'])) if isinstance(data.get('id'), str) else data.get('id'),
            video_id=uuid.UUID(str(data['video_id'])) if isinstance(data.get('video_id'), str) else data.get('video_id'),
            views_count=data.get('views_count', 0),
            likes_count=data.get('likes_count', 0),
            comments_count=data.get('comments_count', 0),
            reports_count=data.get('reports_count', 0),
            delta_views_count=data.get('delta_views_count', 0),
            delta_likes_count=data.get('delta_likes_count', 0),
            delta_comments_count=data.get('delta_comments_count', 0),
            delta_reports_count=data.get('delta_reports_count', 0),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def to_dict(self) -> dict:
        return {
            'id': str(self.id),
            'video_id': str(self.video_id),
            'views_count': self.views_count,
            'likes_count': self.likes_count,
            'comments_count': self.comments_count,
            'reports_count': self.reports_count,
            'delta_views_count': self.delta_views_count,
            'delta_likes_count': self.delta_likes_count,
            'delta_comments_count': self.delta_comments_count,
            'delta_reports_count': self.delta_reports_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }