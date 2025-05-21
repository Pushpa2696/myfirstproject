from sqlalchemy import create_engine
import pandas as pd
import streamlit as st
import plotly.express as px

# Secure Database Connection with SSL
DATABASE_URL = r"mysql+pymysql://4DqqoiZXMnHx5MN.root:3wJPqKRiThuBOBDz@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/IMDB?ssl_ca=C:\Users\vishn\OneDrive\Desktop\Project1\isrgrootx1 .pem"


# Create SQLAlchemy Engine
engine = create_engine(DATABASE_URL)

# Fetch Data
query = "SELECT * FROM movies"
df= pd.read_sql(query, engine)

# Streamlit App Title
st.title("IMDb 2024 Movie Analysis")

# Sidebar Filters
st.sidebar.header("Filter Movies")
selected_genre = st.sidebar.selectbox("Select Genre", ["All"] + sorted(df["genre"].unique()))
min_rating = st.sidebar.slider("Minimum Rating", min_value=0.0, max_value=10.0, value=5.0, step=0.1)
min_votes = st.sidebar.slider("Minimum Votes", min_value=int(df["votes"].min()), max_value=int(df["votes"].max()), value=int(df["votes"].min()))

# Apply Filters
filtered_df = df.copy()
if selected_genre != "All":
    filtered_df = filtered_df[filtered_df["genre"] == selected_genre]
filtered_df = filtered_df[(filtered_df["rating"] >= min_rating) & (filtered_df["votes"] >= min_votes)]

# Display Filtered Data
st.subheader("Filtered Movies")
st.dataframe(filtered_df)

# Top 10 Movies by Rating & Votes
st.subheader("Top 10 Movies by Rating & Votes")
top_movies = df.nlargest(10, ["rating", "votes"])
fig_top_movies = px.bar(top_movies, x="movie_name", y="rating", color="votes", title="Top 10 Movies")
st.plotly_chart(fig_top_movies)

# Genre Distribution
st.subheader("Genre Distribution")
genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["Genre", "Count"]
fig_genre = px.bar(genre_counts, x="Genre", y="Count", title="Movie Count by Genre")
st.plotly_chart(fig_genre)

# Average Duration by Genre
st.subheader("Average Duration by Genre")
avg_duration = df.groupby("genre")["duration"].mean().reset_index()
fig_duration = px.bar(avg_duration, x="duration", y="genre", orientation="h", title="Average Duration per Genre")
st.plotly_chart(fig_duration)

# Voting Trends by Genre
st.subheader("Voting Trends by Genre")
avg_votes = df.groupby("genre")["votes"].mean().reset_index()
fig_votes = px.bar(avg_votes, x="genre", y="votes", title="Average Votes per Genre")
st.plotly_chart(fig_votes)

# Rating Distribution (Box Plot)
st.subheader("Rating Distribution")
fig_rating_dist = px.box(df, y="rating", title="Rating Distribution Box Plot")
st.plotly_chart(fig_rating_dist)

# Top-rated movie per genre (Table)
st.subheader("Top-Rated Movie Per Genre")
top_movies_per_genre = df.loc[df.groupby("genre")["rating"].idxmax()]
st.dataframe(top_movies_per_genre)

# Popular Genres by Votes (Pie Chart)
st.subheader("Popular Genres by Votes")
genre_votes = df.groupby("genre")["votes"].sum().reset_index()
fig_genre_votes = px.pie(genre_votes, names="genre", values="votes", title="Popular Genres by Votes")
st.plotly_chart(fig_genre_votes)

# Shortest & Longest Movies (Table)
st.subheader("Shortest & Longest Movies")
shortest_movie = df.nsmallest(1, "duration")
longest_movie = df.nlargest(1, "duration")
st.write("### Shortest Movie")
st.dataframe(shortest_movie)
st.write("### Longest Movie")
st.dataframe(longest_movie)

# Ratings vs. Votes Correlation (Scatter Plot)
st.subheader("Ratings vs. Votes Correlation")
fig_corr = px.scatter(df, x="votes", y="rating", title="Ratings vs. Votes Correlation", trendline="ols")
st.plotly_chart(fig_corr)


