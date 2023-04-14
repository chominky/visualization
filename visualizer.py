import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import os


def draw_graph(file_path: str, x: str, y: str, file_format: str, title: str, save: bool) -> None:
    """Draw graph from csv file

    Args:
        file_path (str): file path to draw graph
        x (str): column to x
        y (str): column to y
        format (str): file format. png, html
        title (str): title of plot
        save (bool): whether save or not
    """
    df = pd.read_csv(file_path)
    assert x in df.columns, f"{x} column is not in {file_path}"
    assert y in df.columns, f"{y} column is not in {file_path}"

    if x == "date":
        df["date"] = pd.to_datetime(df['date'])
    if file_format == "png":
        plt.figure(figsize=(14,5))
        sns.set_style("ticks")
        sns.lineplot(data=df,x=x,y=y,color='firebrick')
        sns.despine()
        plt.title(title,size='x-large',color='blue')
        plt.grid()
        if save:
            os.makedirs("./plots", exist_ok=True)
            plt.savefig(f"./plots/{title}.png")


if __name__ == "__main__":
    draw_graph(file_path="./AAPL.csv", x="date", y="close", file_format="png",
               title="The Stock Price of AAPL", save=True)