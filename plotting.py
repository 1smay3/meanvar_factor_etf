import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from config import factor_names


def line_chart(dataframe: pd.DataFrame, x_col_name: str, y_col_name: str, title: str):
    fig = px.line(dataframe, x=x_col_name, y=y_col_name, title=title)
    return fig


def distribution_dashboard(source_data):
    # Set up plotly dashboard page (Aggregated, then days of week)
    labels_tuple = tuple(source_data.columns)

    fig = make_subplots(
        rows=3,
        cols=3,
        specs=[
            [{}, {}, {}],
            [{}, {}, {}],
            [{"rowspan": 1, "colspan": 3, "type": "table"}, None, None],
        ],
        print_grid=False,
        subplot_titles=labels_tuple,
    )

    # Make list of values for table
    mean = []
    median = []
    std = []
    skew = []
    kurt = []
    sample_size_list = []

    i = 0
    for ticker in source_data.columns:
        # Get position of subplot
        i += 1
        if i < 4:
            row = 1
            col = i
        else:
            row = 2
            col = i - 3

        rel_source_data = source_data[ticker]
        source_data_no_idx = rel_source_data.reset_index()

        factor_mean = source_data_no_idx.mean(numeric_only=True)
        factor_median = source_data_no_idx.median(numeric_only=True)
        factor_std = source_data_no_idx.std(numeric_only=True)
        factor_skew = source_data_no_idx.skew(numeric_only=True)
        factor_kurt = source_data_no_idx.kurtosis(numeric_only=True)
        sample_size = len(source_data_no_idx)

        # Histogram each dist on one page
        fig.append_trace(
            go.Histogram(x=rel_source_data, histnorm="probability"), row=row, col=col
        )

        # Add to lists for table
        mean.append("{:.2%}".format(factor_mean[0]))
        median.append("{:.2%}".format(factor_median[0]))
        std.append("{:.2%}".format(factor_std[0]))
        skew.append("{:.3}".format(factor_skew[0]))
        kurt.append("{:.3}".format(factor_kurt[0]))
        sample_size_list.append("{:1}".format(sample_size))

    # Create table to add at bottom from df

    sample_stats = pd.DataFrame(
        {
            "Mean": mean,
            "Median": median,
            "Standard Deviation": std,
            "Skew": skew,
            "Kurtosis": kurt,
            "Sample Size": sample_size_list,
        },
        index=source_data.columns,
    )

    sample_stats_labeled = sample_stats.reset_index()
    sample_stats_labeled = sample_stats_labeled.rename({"index": "Day of Week"}, axis=1)

    fig.add_trace(
        go.Table(
            header=dict(values=list(sample_stats_labeled.columns), align="center"),
            cells=dict(
                values=[
                    sample_stats_labeled["Day of Week"],
                    sample_stats_labeled["Mean"],
                    sample_stats_labeled["Median"],
                    sample_stats_labeled["Standard Deviation"],
                    sample_stats_labeled["Skew"],
                    sample_stats_labeled["Kurtosis"],
                    sample_stats_labeled["Sample Size"],
                ],
                align="center",
            ),
        ),
        row=3,
        col=1,
    )

    fig.update_layout(title_text="Factor Return Distributions", showlegend=False)
    fig.write_html("outputs/distributions.html")
    return fig


def correlation_plot(returns):
    renamed_ret = returns.set_axis(factor_names, axis=1, inplace=False)
    plt.figure(figsize=(10, 4))
    correlation_matrix = sns.heatmap(
        renamed_ret.corr(), vmin=-1, vmax=1, annot=True, cmap=cmap
    )
    # Give a title to the heatmap. Pad defines the distance of the title from the top of the heatmap.
    correlation_matrix.set_title(
        "Correlation Heatmap", fontdict={"fontsize": 12}, pad=12
    )
    plt.savefig("outputs/corrmatrix.png", dpi=300, bbox_inches="tight")
    return plt


def create_color(r, g, b):
    return [r / 256, g / 256, b / 256]


def frontier_scatter(mean_var_output, alL_factor_tickers):
    # Build annotations for hover text
    pre_text = "Portfolio Weights: <br>"
    post_text = ""
    for ticker in alL_factor_tickers:
        item = ticker + ": " + mean_var_output[ticker].map("{:.2%}".format) + "<br>"
        post_text += item

    # Max sharpe
    max_sharpe_portfolio = mean_var_output.loc[mean_var_output['sharpe'].idxmax()]
    max_sharpe_vol = max_sharpe_portfolio['volatility']
    max_sharpe_rets = max_sharpe_portfolio['returns']

    # Init figure
    fig = go.Figure()

    # Add plots for all simulated portfolios, with colour gradient for Sharpe
    fig.add_trace(
        go.Scatter(
            x=mean_var_output["volatility"],
            y=mean_var_output["returns"],
            text=pre_text + post_text,
            marker=dict(
                color=(mean_var_output["sharpe"]),
                showscale=True,
                size=7,
                line=dict(width=1),
                colorscale="aggrnyl",
                colorbar=dict(title="Sharpe<br>Ratio"),
            ),
            mode="markers",
        )
    )

    # Add market for max sharpe
    fig.add_annotation(dict(font=dict(color='rgba(0,0,200,0.8)', size=12),
                            x=max_sharpe_vol,
                            # x = xStart
                            y=max_sharpe_rets,
                            text='Max Sharpe Portfolio',
                            # ax = -10,
                            textangle=0,
                            xanchor='right',
                            xref="x",
                            yref="y"))

    fig.update_layout(
        template="plotly_white",
        xaxis=dict(title="Annualised Risk (Volatility)"),
        yaxis=dict(title="Annualised Return"),
        title="Sample of Random Portfolios",
        coloraxis_colorbar=dict(title="Sharpe Ratio"),
    )
    fig.write_html("outputs/frontier.html")
    return fig
