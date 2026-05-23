from sqlmodel import SQLModel, Session, create_engine

DATABASE_URL = "sqlite:///./database.db" # ./ => terminal current location(i.e., FAST_API)(relative path defined)

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session