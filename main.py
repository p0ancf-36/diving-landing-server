from fastapi import Depends, FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import text
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession

import uvicorn

engine = create_async_engine("sqlite+aiosqlite:///test_database.sqlite3")
async_session = sessionmaker(
	engine,
	class_=AsyncSession,
	expire_on_commit=False
)
async def get_session() -> AsyncSession:
	async with async_session() as session:
		yield session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/add_user")
async def add_user(req: Request, session: AsyncSession = Depends(get_session)):
	req_body = await req.json()

	surname: str = req_body["surname"]
	fname: str = req_body["fname"]
	sname: str = req_body["sname"]
	phone: str = req_body["phone"]
	email: str = req_body["email"]

	await session.execute(text(
		f"""
		INSERT INTO users (surname, fname, sname, phone, email) VALUES {(surname, fname, sname, phone, email)}
		"""
	))
	await session.commit()

	return Response()

if __name__ == "__main__":
	uvicorn.run("main:app", port=5000, reload=True)