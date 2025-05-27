import streamlit as st
import pandas as pd
import sqlalchemy
import matplotlib.pyplot as plt
import seaborn as sns

# Database
DATABASE_URL = 'postgresql://postgres:VpJkyKPDSDUtTXwOTSlyyZvjUBPsLGdo@maglev.proxy.rlwy.net:46115/railway'

# Page
st.set_page_config(page_title="Books Dashboard", layout="wide")

st.title("Books Dashboard — Built with OpenLibrary and Machine Learning")

st.markdown("""
This dashboard displays a simple analysis on data sourced by OpenLibrary via API, complemented with features created with Machine Learning.
            
Here you can find:
            - A clusterization analysis by the books subjects;
            - A prediction on how many adition a book has or can have;
            - Books by decade, subject and topic.

You can interact with the dashboard by using the filters on the left and narrow your view.
            
This project was created as part of my post graduation course on machine learning. You can reach out via GitHub @lauraglint
            """)

@st.cache_data
def load_data():
    engine = sqlalchemy.create_engine(DATABASE_URL)
    query = "SELECT * FROM books_complete"
    df = pd.read_sql(query, engine)
    return df

df = load_data()

st.success("Data loaded")

# Filters
st.sidebar.header("Filters")

subject = st.sidebar.multiselect("Subject", options=df['subject'].unique(), default=df['subject'].unique())
cluster = st.sidebar.multiselect("Cluster", options=sorted(df['cluster'].dropna().unique()), default=sorted(df['cluster'].dropna().unique()))
topic = st.sidebar.multiselect("Topic", options=sorted(df['topic'].dropna().unique()), default=sorted(df['topic'].dropna().unique()))

df_filtered = df[
    (df['subject'].isin(subject)) &
    (df['cluster'].isin(cluster)) &
    (df['topic'].isin(topic))
]

st.subheader(f"{len(df_filtered)} Books Available")

st.dataframe(df_filtered)

# Graphs
st.subheader("Actual Edition Count vs. Predicted")

fig1, ax = plt.subplots(figsize=(10,6))
sns.scatterplot(
    data=df_filtered,
    x='edition_count',
    y='predicted_edition_count',
    hue='cluster',
    palette='tab10',
    ax=ax
)
ax.set_xlabel("Actual Edition Count")
ax.set_ylabel("Predicted Edition Count")
ax.set_title("Actual Edition Count vs. Predicted")
st.pyplot(fig1)


st.subheader("Books by Subject")

fig2, ax = plt.subplots(figsize=(8,5))
sns.countplot(data=df_filtered, y='subject', order=df_filtered['subject'].value_counts().index, palette="viridis", ax=ax)
ax.set_title("Books by Subject")
st.pyplot(fig2)


st.subheader("Books Published Count Evolution")

df_filtered['decade'] = (df_filtered['first_publish_year'] // 10) * 10

fig3, ax = plt.subplots(figsize=(10,6))
sns.countplot(data=df_filtered, x='decade', hue='subject', palette='tab20', ax=ax)
ax.set_title("Published Books by Decade")
plt.xticks(rotation=45)
st.pyplot(fig3)


st.subheader("Correlation Heatmap")

fig4, ax = plt.subplots(figsize=(8,6))
sns.heatmap(df_filtered.corr(numeric_only=True), annot=True, cmap="YlGnBu", ax=ax)
ax.set_title("Correlation")
st.pyplot(fig4)


st.subheader("Books Clusters by Decade")

df_filtered['decade'] = (df_filtered['first_publish_year'] // 10) * 10

fig5, ax = plt.subplots(figsize=(10,6))
sns.countplot(data=df_filtered, x='decade', hue='cluster', palette='tab20', ax=ax)
plt.xticks(rotation=45)
ax.set_title("Books Clusters by Decade")
st.pyplot(fig5)


st.subheader("Books by Cluster")

fig6, ax = plt.subplots(figsize=(8,5))
sns.countplot(data=df_filtered, x='cluster', palette="tab10", ax=ax)
ax.set_title("Books by Cluster")
st.pyplot(fig6)


# Data download
st.subheader("Export Data")
st.download_button(
    label="Download CSV",
    data=df_filtered.to_csv(index=False).encode('utf-8'),
    file_name='books_filtered.csv',
    mime='text/csv',
)
