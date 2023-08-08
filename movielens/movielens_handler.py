import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Set pandas display options for DataFrame output
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)


class MovieLens:
    def __init__(self, users_file, movies_file, ratings_file):
        # Create DataFrame from the users table
        self.users = pd.read_table(
            users_file,
            sep="::",
            header=None,
            names=["user_id", "gender", "age", "occupation", "zip"],
            engine="python",
        )

        # Create DataFrame from the movies table
        self.movies = pd.read_table(
            movies_file,
            sep="::",
            header=None,
            names=["movie_id", "title", "genres"],
            engine="python",
        )

        # Create DataFrame from the ratings table
        self.ratings = pd.read_table(
            ratings_file,
            sep="::",
            header=None,
            names=["user_id", "movie_id", "rating", "timestamp"],
            engine="python",
        )

        # Merge the three DataFrames into one consolidated DataFrame
        self.data = pd.merge(pd.merge(self.ratings, self.users), self.movies)

    def movies_rating_count(self):
        # Extract the release year from the title and add a new 'release_year' column as integer type
        self.data["release_year"] = (
            self.data["title"].str.extract(r"\((\d{4})\)").astype(int)
        )

        # Filter movies by release year from 1990 to 2000
        self.data = self.data.loc[
            (self.data["release_year"] >= 1990) & (self.data["release_year"] <= 2000)
        ]

        # Get average movies rating
        mean_rating = self.data.pivot_table(
            "rating", index="title", columns="gender", aggfunc="mean"
        ).dropna()

        # Count the number of ratings for each movie
        rating_by_title = self.data.groupby("title").size()

        # Select 20 movies with high ratings (at least 500 ratings)
        highly_rated_movies = mean_rating.loc[
            rating_by_title.index[rating_by_title >= 500]
        ].head(20)

        return highly_rated_movies

    def data_visualisation(self):
        # Create the single figure with two subplots stocked vertically.
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 10))

        # Rearrange data for plotting
        mvc = self.movies_rating_count()
        mvc = mvc.stack()
        mvc.name = "rating"
        mvc = mvc.reset_index()

        # Plotting the first bar plot on the first subplot (ax1)
        ax1 = sns.barplot(
            y="title",
            x="rating",
            hue="gender",
            data=mvc,
            ax=ax1,
            palette={"F": "pink", "M": "blue"},
        )
        ax1.set_title("Average ratings by gender for movies released between 1990 - 2000")

        # Add the final movie rating as plot label
        for container in ax1.containers:
            ax1.bar_label(container, fmt="%.2f", fontsize=6, fontweight="bold")

        # Set x-axis limits, ticks, and tick labels
        ax1.set_xlim(0, 5)
        ax1.set_xticks(range(6))
        ax1.set_xticklabels(range(6))

        plt.suptitle("Data from MovieLens 1M", fontsize=18, fontweight="bold")
        plt.tight_layout()
        plt.show()

    def __repr__(self):
        return self.data


if __name__ == "__main__":
    try:
        movielens = MovieLens(
            users_file="/Users/a1/PythonProjects/Python_for_Data_Analysis/datasets/movielens/users.dat",
            movies_file="/Users/a1/PythonProjects/Python_for_Data_Analysis/datasets/movielens/movies.dat",
            ratings_file="/Users/a1/PythonProjects/Python_for_Data_Analysis/datasets/movielens/ratings.dat",
        )
        # print(movielens.__repr__())
        movielens.movies_rating_count()
        movielens.data_visualisation()
    except FileNotFoundError as err:
        print(f"{err.strerror}: {err.filename}")
