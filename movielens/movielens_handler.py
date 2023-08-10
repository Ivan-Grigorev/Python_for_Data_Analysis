import matplotlib.pyplot as plt
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

    def get_filtered_data(self):
        # Extract the release year from the title and add a new 'release_year' column as integer type
        self.data["release_year"] = (
            self.data["title"].str.extract(r"\((\d{4})\)").astype(int)
        )

        # Filter movies by release year from 1990 to 2000
        self.data = self.data.loc[
            (self.data["release_year"] >= 1990) & (self.data["release_year"] <= 2000)
        ]

        return self.data

    def movies_rating_count(self):
        # Invoke the get_filtered_data() function and get filtered DataFrame
        filtered_data = self.get_filtered_data()

        # Get average movies rating
        mean_rating = filtered_data.pivot_table(
            "rating", index="title", columns="gender", aggfunc="mean"
        ).dropna()

        # Count the number of ratings for each movie
        rating_by_title = filtered_data.groupby("title").size()

        # Select 20 movies with high ratings (at least 500 ratings)
        highly_rated_movies = mean_rating.loc[
            rating_by_title.index[rating_by_title >= 500]
        ].head(20)

        return highly_rated_movies

    def average_age_count(self):
        # Get movies titles from movies_rating_count() handled data
        movies_titles = self.movies_rating_count().reset_index()[["title"]]

        # Filter original DataFrame by movies titles
        users_age = self.data[self.data["title"].isin(movies_titles["title"])]

        # Get users average age
        mean_age = users_age.pivot_table(
            index="title", values="age", columns="gender", aggfunc="mean"
        )

        return mean_age

    def data_visualisation(self):
        # Create the single figure with two subplots stocked vertically.
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 10))

        # Invoke the movies_rating_count() function and retrieve the associated data
        movies_rating_data = self.movies_rating_count()

        # Rearrange movies_rating_count() data for plotting
        movies_rating_data = movies_rating_data.stack()
        movies_rating_data.name = "rating"
        movies_rating_data = movies_rating_data.reset_index()

        # Sort by highest rating
        movies_rating_data = movies_rating_data.sort_values(
            by="rating", ascending=False
        )

        # Plotting the first bar plot on the first subplot (ax1)
        ax1 = sns.barplot(
            y="title",
            x="rating",
            hue="gender",
            data=movies_rating_data,
            ax=ax1,
            palette={"F": "pink", "M": "blue"},
        )
        ax1.set_title("Average ratings by gender")

        # Add the final movie rating as plot label
        for container in ax1.containers:
            ax1.bar_label(container, fmt="%.2f", fontsize=6, fontweight="bold")

        # Set x-axis limits, ticks and tick labels
        ax1.set_xlim(0, 5)
        ax1.set_xticks(range(6))
        ax1.set_xticklabels(range(6))

        # Invoke the average_age_count() function and retrieve the associated data
        average_age_data = self.average_age_count()

        # Rearrange average_age_count() data for plotting
        average_age_data = average_age_data.stack()
        average_age_data.name = "average_age"
        average_age_data = average_age_data.reset_index()

        # Plotting the second bar plot for subplot (ax2)
        ax2 = sns.barplot(
            y="title",
            x="average_age",
            hue="gender",
            ax=ax2,
            data=average_age_data,
            palette={"F": "pink", "M": "blue"},
        )
        ax2.set_title("Users average age by gender")

        # Add average age as plot label
        for container in ax2.containers:
            ax2.bar_label(container, fmt="%.2f", fontsize=6, fontweight="bold")

        # Set x-axis limits, ticks and tick labels
        ax2.set_xlim(0, 35)
        ax2.set_xticks(range(36))
        ax2.set_xticklabels(range(36))

        plt.suptitle(
            "Data from MovieLens 1M for movies released between 1990 - 2000",
            fontsize=18,
            fontweight="bold",
        )
        plt.tight_layout()
        # Save figure to a file
        # plt.savefig("movielens_visualisation.png", dpi=300, bbox_inches="tight")
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
        movielens.data_visualisation()

    except FileNotFoundError as err:
        print(f"{err.strerror}: {err.filename}")
