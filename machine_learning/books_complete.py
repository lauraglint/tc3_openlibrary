import pandas as pd
from sqlalchemy import create_engine

# Database
DATABASE_URL = "postgresql://postgres:VpJkyKPDSDUtTXwOTSlyyZvjUBPsLGdo@maglev.proxy.rlwy.net:46115/railway"
engine = create_engine(DATABASE_URL)

books = pd.read_sql("SELECT * FROM books", engine)
topics = pd.read_sql("SELECT id, topic FROM books_with_topics", engine)
clusters = pd.read_sql("SELECT id, cluster FROM books_with_clusters", engine)
predictions = pd.read_sql("SELECT id, predicted_edition_count FROM books_with_ed_pred", engine)

df = books.merge(topics, on="id", how="left")
df = df.merge(clusters, on="id", how="left")
df = df.merge(predictions, on="id", how="left")

df_final = df[[
    'id', 'title', 'authors', 'first_publish_year', 'subject',
    'edition_count', 'cluster', 'topic', 'predicted_edition_count'
]]

# Save
df_final.to_sql('books_complete', engine, if_exists='replace', index=False)