import os
from fastapi import FastAPI, Query
from sqlalchemy import create_engine, text
import pandas as pd
import requests

app = FastAPI(title="OpenLibrary Books API")

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("no DATABASE_URL")

engine = create_engine(DATABASE_URL)


# fetch data from Open Library
def fetch_books(subject: str, limit: int = 100, batch_size: int = 50) -> pd.DataFrame:
    dfs = []
    for offset in range(0, limit, batch_size):
        url = f"https://openlibrary.org/subjects/{subject}.json?limit={batch_size}&offset={offset}"
        response = requests.get(url)
        if response.status_code != 200:
            continue
        data = response.json()

        books = []
        for book in data.get('works', []):
            books.append({
                'title': book.get('title'),
                'authors': ', '.join([a['name'] for a in book.get('authors', [])]),
                'first_publish_year': book.get('first_publish_year'),
                'subject': subject,
                'edition_count': book.get('edition_count'),
                'key': book.get('key')
            })
        df = pd.DataFrame(books)
        dfs.append(df)

    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()


@app.post("/fetch-books")
def fetch_and_store_books(subject: str = Query(...), limit: int = Query(100)):
    df = fetch_books(subject=subject, limit=limit)

    if df.empty:
        return {"message": f"couldn't fetch {subject}"}

    df.to_sql('books', con=engine, if_exists='append', index=False)
    return {"message": f"{len(df)} {subject} books fetched"}


@app.get("/list-books")
def list_books(limit: int = 100):
    query = text(f"SELECT * FROM books LIMIT {limit}")
    with engine.connect() as conn:
        result = conn.execute(query)
        books = [dict(row) for row in result]
    return books


@app.get("/list-books/{subject}")
def list_books_by_subject(subject: str, limit: int = 100):
    query = text(f"SELECT * FROM books WHERE subject = :subject LIMIT {limit}")
    with engine.connect() as conn:
        result = conn.execute(query, {'subject': subject})
        books = [dict(row) for row in result]
    return books
