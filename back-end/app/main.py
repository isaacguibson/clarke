from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from app.database.connection import engine, Base
from app.database.seed import seed_database
from app.database.connection import SessionLocal
from app.graphql.schema import schema

Base.metadata.create_all(bind=engine)

db = SessionLocal()
try:
    from app.models import State
    if db.query(State).count() == 0:
        seed_database(db)
finally:
    db.close()

app = FastAPI(
    title="Clarke Energia API",
    description="GraphQL API for Clarke Energia challenge",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graphql_router = GraphQLRouter(schema, path="/graphql")
app.include_router(graphql_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
