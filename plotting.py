from efficientFrontier import mean_variance_pairs
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import math

# Plot the risk vs. return of randomly generated portfolios
# Manipulate mean_variance_pairs to plot
mvp = pd.DataFrame.from_records(mean_variance_pairs)
mvp.rename({0:'mean', 1:'variance'}, axis=1, inplace=True)

# sqrt variance for std
mvp['std'] = mvp['variance'].apply(math.sqrt)

# Risk free rate for sharpe ratio
rf =0



print("Debug")
# Create Plot
# fig = go.Figure()
# fig.add_trace(go.Scatter(x=mean_variance_pairs[:,1]**0.5,
#                          y=mean_variance_pairs[:,0],
#                       #- Add color scale for sharpe ratio
#                       marker=dict(color=(mean_variance_pairs[:,0]-rf)/(mean_variance_pairs[:,1]**0.5),
#                                   showscale=True,
#                                   size=7,
#                                   line=dict(width=1),
#                                   colorscale="RdBu",
#                                   colorbar=dict(title="Sharpe<br>Ratio")
#                                  ),
#                       mode='markers'))
#
#
#
# # Add title/labels
# fig.update_layout(template='plotly_white',
#                   xaxis=dict(title='Annualised Risk (Volatility)'),
#                   yaxis=dict(title='Annualised Return'),
#                   title='Sample of Random Portfolios',
#                   coloraxis_colorbar=dict(title="Sharpe Ratio"))
#
# fig.show()
