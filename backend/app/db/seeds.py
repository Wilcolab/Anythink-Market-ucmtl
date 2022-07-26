import asyncio
import asyncpg

from app.api.dependencies.database import get_repository
from app.db.repositories.comments import CommentsRepository
from app.db.repositories.items import ItemsRepository
from app.db.repositories.users import UsersRepository
from app.core.config import get_app_settings

async def add_x(x):
    SETTINGS = get_app_settings()
    DATABASE_URL = SETTINGS.database_url.replace("postgres://", "postgresql://")
    conn = await asyncpg.connect(DATABASE_URL)
    itemsRepository = ItemsRepository(conn=conn)
    usersRepository = UsersRepository(conn=conn)
    commentsRepository = CommentsRepository(conn=conn)

    for i in range(x):
        user = await usersRepository.create_user(username=f"aviad{i}", password=f"{x}", email=f"{i}@{i}.com")
        item = await itemsRepository.create_item(slug=f"item{i}", seller=user, title=f"title{i}", description=f"description{i}")
        comment = await commentsRepository.create_comment_for_item(body=f"great!", item=item, user=user)
    
    await conn.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(add_x(100))
