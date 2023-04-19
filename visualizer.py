import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import os
import plotly.graph_objects as go
from typing import List


def draw_single_graph(stock: str, x: str, y: str, file_format: str, title: str, save: bool) -> None:
    """Draw graph from csv file

    Args:
        stock (str): stock to draw graph
        x (str): column to x
        y (str): column to y
        format (str): file format. png, html
        title (str): title of plot
        save (bool): whether save or not
    """
    df = pd.read_csv(f"./data/{stock}.csv")
    assert x in df.columns, f"{x} column is not in {stock}"
    assert y in df.columns, f"{y} column is not in {stock}"

    if x == "date":
        df["date"] = pd.to_datetime(df['date'])
    if file_format == "png":
        plt.figure(figsize=(14,5))
        sns.set_style("ticks")
        sns.lineplot(data=df, x=x, y=y, color='firebrick')
        sns.despine()
        plt.title(title,size='x-large',color='blue')
        plt.grid()
        if save:
            os.makedirs("./plots", exist_ok=True)
            plt.savefig(f"./plots/{title}.png")
    elif file_format == "html":
        fig = go.Figure()
        fig.add_trace(go.Scatter(name="close",
                         x=df["date"],
                         y=df["close"],
                         mode="lines"))
        fig.update_layout(title_text="The Stock Price of AAPL",
                          title_x=0.5)
        fig.update_xaxes(title='date')
        fig.update_yaxes(title='close')
        fig.show()
        if save:
            os.makedirs("./plots", exist_ok=True)
            fig.write_html(f"./plots/{title}.html")

def draw_multiple_graph(stock_list: List[str], x: str, y: str, file_format: str, save: bool) -> None:
    """Draw multiple graph from csv files

    Args:
        stock_list (List[str]): stock list to draw graph
        x (str): column to x
        y (str): column to y
        format (str): file format. png, html. if html, draw with animation bar
        save (bool): whether save or not
    """
    if file_format == "png":
        nrows = len(stock_list)
        fig, axs = plt.subplots(figsize=(14,int(nrows*5)), nrows=nrows)
        sns.set(style="ticks")
        sns.despine()
        for i, stock in enumerate(stock_list):
            df = pd.read_csv(f"./data/{stock}.csv")
            assert x in df.columns, f"{x} column is not in {stock}"
            assert y in df.columns, f"{y} column is not in {stock}"

            if x == "date":
                df["date"] = pd.to_datetime(df['date'])
            sns.lineplot(data=df,x="date",y='close',color='firebrick', ax=axs[i])
            axs[i].set_title(f"The Stock Price of {stock}",size='x-large',color='blue')
            axs[i].grid()
        plt.tight_layout(pad=1)
        plt.show()
        if save:
            os.makedirs("./plots", exist_ok=True)
            fig.savefig(f"./plots/{', '.join(stock_list)}.png")
    elif file_format == "html":
        start_visible = [True] + [False for _ in range(len(stock_list)-1)]
        stock_df_list = [pd.read_csv(f"./data/{stock}.csv") for stock in stock_list]
        trace_list = [go.Scatter(name=stock,x=df["date"],y=df["close"],mode="lines",visible=vis)
                    for stock, df, vis in zip(stock_list, stock_df_list, start_visible)]
        fig = go.Figure(data=trace_list)

        steps = []
        for stock in stock_list:
            # Hide all traces
            step = dict(
                        method='update',
                        args=[{'visible': [True if stock in data['name'] else False for data in fig.data]},
                            {'title.text': f'The Stock Price of {stock}'}],
                        label=stock
                    )
            # Add step to step list
            steps.append(step)
        sliders = [dict(steps=steps)]
        fig.layout.sliders = sliders
        fig.update_layout(title_text=f'The Stock Price of {stock_list[0]}',
                        title_x=0.5)
        fig.update_xaxes(title='date')
        fig.update_yaxes(title='close')
        fig.show()
        if save:
            os.makedirs("./plots", exist_ok=True)
            fig.write_html(f"./plots/{', '.join(stock_list)}.html")

if __name__ == "__main__":
    company_name = "AAPL"
    draw_single_graph(stock=company_name, x="date", y="close",
                      file_format="png",
                      title=f"The Stock Price of {company_name}", save=True)
    # company_list = ["AAPL", "MSFT"]
    # draw_multiple_graph(stock_list=company_list, x="date", y="close",
    #                     file_format="png", save=True)
