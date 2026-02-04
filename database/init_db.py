import json
from datetime import datetime
import asyncio
import asyncpg
import os
import pathlib
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def init_database():
    logger.info("init_database")

    conn = None

    try:
        conn = await asyncpg.connect(
            user=os.getenv("POSTGRES_USER", "bot_user"),
            password=os.getenv("POSTGRES_PASSWORD", "bot_password"),
            database=os.getenv("POSTGRES_DB", "bot_db"),
            host="postgres",
            port=5432
        )

        logger.info("connect success")

        tables = await conn.fetch("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public';
        """)

        if tables:
            logger.info(f"Found tables: {[t['table_name'] for t in tables]}")
            return
        
        await create_tables(conn)
        logger.info("tables created")
        await load_data(conn)

    except Exception as e:
        logger.error(f"Error: {e}")
        raise
    finally:
        if conn:
            await conn.close()

async def create_tables(conn):
    logger.info("Creating tables")

    await conn.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
    
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS videos (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            creator_id VARCHAR(50) NOT NULL,
            video_created_at TIMESTAMP WITH TIME ZONE NOT NULL,
            views_count INTEGER DEFAULT 0,
            likes_count INTEGER DEFAULT 0,
            comments_count INTEGER DEFAULT 0,
            reports_count INTEGER DEFAULT 0,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
    """)

    await conn.execute("""
        CREATE TABLE IF NOT EXISTS video_snapshots (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            video_id UUID NOT NULL REFERENCES videos(id) ON DELETE CASCADE,
            views_count INTEGER DEFAULT 0,
            likes_count INTEGER DEFAULT 0,
            comments_count INTEGER DEFAULT 0,
            reports_count INTEGER DEFAULT 0,
            delta_views_count INTEGER DEFAULT 0,
            delta_likes_count INTEGER DEFAULT 0,
            delta_comments_count INTEGER DEFAULT 0,
            delta_reports_count INTEGER DEFAULT 0,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
    """)

    await conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_videos_creator_id ON videos(creator_id);
        CREATE INDEX IF NOT EXISTS idx_videos_video_created_at ON videos(video_created_at);
        
        CREATE INDEX IF NOT EXISTS idx_video_snapshots_video_id ON video_snapshots(video_id);
        CREATE INDEX IF NOT EXISTS idx_video_snapshots_created_at ON video_snapshots(created_at);
    """)

async def load_data(conn):
    logger.info("loading data")
    current_dir = pathlib.Path(__file__).parent
    fixtures_path = current_dir / "fixtures" / "videos.json"
    with open(fixtures_path, "r") as f:
        data = json.load(f)
        for video in data["videos"]:
            await conn.execute("""
                INSERT INTO videos (
                    id, creator_id, video_created_at, views_count, 
                    likes_count, comments_count, reports_count,
                    created_at, updated_at
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                ON CONFLICT (id) DO NOTHING
            """,
                video["id"],
                str(video['creator_id']),
                datetime.fromisoformat(video['video_created_at'].replace('Z', '+00:00')),
                video['views_count'],
                video['likes_count'],
                video['comments_count'],
                video['reports_count'],
                datetime.fromisoformat(video['created_at'].replace('Z', '+00:00')),
                datetime.fromisoformat(video['updated_at'].replace('Z', '+00:00'))
            )
            for snapshot in video["snapshots"]:
                await conn.execute("""
                INSERT INTO video_snapshots (
                    id, video_id, views_count, 
                    likes_count, comments_count, reports_count,
                    delta_views_count, delta_likes_count, 
                    delta_comments_count, delta_reports_count,     
                    created_at, updated_at
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
                ON CONFLICT (id) DO NOTHING
                """,
                    snapshot["id"],
                    snapshot["video_id"],
                    snapshot['views_count'],
                    snapshot['likes_count'],
                    snapshot['comments_count'],
                    snapshot['reports_count'],
                    snapshot['delta_views_count'],
                    snapshot['delta_likes_count'],
                    snapshot['delta_comments_count'],
                    snapshot['delta_reports_count'],
                    datetime.fromisoformat(snapshot['created_at'].replace('Z', '+00:00')),
                    datetime.fromisoformat(snapshot['updated_at'].replace('Z', '+00:00'))
                )
    logger.info("data loaded")

asyncio.run(init_database())