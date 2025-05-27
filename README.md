# OpenLibrary Books — API, Machine Learning and Dashboard

A complete end-to-end project that collects data from the OpenLibrary API, stores it in a PostgreSQL database, enriches it with Machine Learning models (Topic Modeling, Clustering, and Regression), and visualizes insights through a dynamic dashboard.

This project was developed as part of a Machine Learning challenge, focusing on data pipeline automation, model deployment, and business storytelling.


## 🔗 Project Structure

api/ → FastAPI project for data collection and query
machine_learning/ → Machine Learning notebooks (Topic Modeling, Clustering, Regression)
dashboard.py → Streamlit dashboard for data visualization
requirements.txt → Python dependencies
README.md → Project documentation


## Features

### API — Data Collection and Query

- Fetch books data from OpenLibrary by subject.
- Store data into PostgreSQL.
- Endpoints to fetch, query, and list books.
- Built with **FastAPI** and **SQLAlchemy**.


### Machine Learning Pipeline

- **Topic Modeling:** Generated from book titles using BERTopic (NLP).
- **Clustering:** Groups books into clusters based on features like subject and title topic.
- **Regression Model:** Predicts the number of editions (`edition_count`) a book is likely to have based on:
  - Title topic
  - Subject
  - First publish year


### Dashboard

- Built with **Streamlit**.
- Interactive:
  - Filters by subject, cluster, and topic.
- Includes:
  - Real vs. Predicted Edition Count scatterplot.
  - Books distribution by decade, subject, and clusters.
  - Topic and cluster analysis.
- Data export feature in CSV.


## Clone the repository:

```bash
git clone https://github.com/lauraglint/tc3_openlibrary
cd tc3_openlibrary