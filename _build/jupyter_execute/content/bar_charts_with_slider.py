#!/usr/bin/env python
# coding: utf-8

# ## Charts with a Slider
# 

# ### Introduction
# There are a host of software packages, libraries and frameworks that help us visualize data. Some of these tools are embedded in bigger statistical packages such as Stata and SPSS. A well-known Python library for visualizing data, Matplotlib, is also available at your service. Collaborative decision making in any business operation is an important element in situations where different departments of an organization have stakes in those decisions. In these collaborative environments, data visualization should be available to all of the stake holders and be updated simultaneously for instantaneous decision. 
# 
# While the above mentioned software packages have their own places in other areas of statistical analysis, they are not convenient to share visualizations and insights online and on different platforms. As a data scientist, if you produce data visualization you should be able to share them through a platform agnostic system to all of the concerned decision makers (usually non-technical people) so that they can interactively play with the graph. You need to have a tool for doing just this. Plotly Dash serves this purpose.

# ### Plotly Dash
# Dash is an open source Python library built on top of Plotly.js, React and Flask. Dash ties together modern UI elements like dropdowns, sliders, and graphs directly to your analytical Python code. It’s maintained by Plotly, another visualization library which helps building, scaling, and deploying data application in Python.
# 
# 

# Requirements
# This tutorial is based on dash version 2.6. This version supports Python 3. Versions of dash before 2.0.0 also supported Python 2. First, install dash.
# 
# 

# This also brings along the plotly graphing library ecosystem including plotly express which we are using in this hands-on. You need another package for handling and managing your data before sending your data to plotly express for visualization. While you have other alternatives, pandas is a convenient one for its easy-to-use dataframe. So, install pandas.
# 
# 

# <pre>
# <code>
# pip install jupyter-dash   # pip install dash if you are on non-Jupyter environment 
# pip install pandas
# </code>
# </pre>

# ### Working with Dash
# There are distinct steps you need to follow before getting your interactive chart from dash app. These steps are more or less the same irrespective of the types of project you may be working on. 
# 
# First let's import the necessary packages.

# In[1]:


from jupyter_dash import JupyterDash #from dash import Dash in non-Jupyter environment
from dash import html, dcc
import plotly.express as px
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input


# **Instantiate dash application**
# 
# Instantiate dash app is getting an object called app from Dash. You can simply use `__name__` inside the parenthesis and ignore what it is for now.

# In[2]:


app = JupyterDash(__name__)


# For the third step, we use the gapminder dataset from Plotly dataset.

# In[3]:


df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')


# You can use your own data but make sure it is structured in a way dash requires. The next step is preparing the layout and the figure to put on the layout.

# In[4]:


app.layout = html.Div([
    dcc.Graph(id='graph1'),
    dcc.Slider(
        df['year'].min(),
        df['year'].max(),
        step=None,
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        id='year-slider'
    )
])


# The first object in the `html.Div([...])` function is the `dcc.Graph(...)` which holds the figure with the given id. This id links to the call back function that I discuss below. The second object is `dcc.Slider(...)` which gives the figure interactivity (if you are not sure what it does, you can see the constructed figure below.).
# 
# The next block of code is the callback function. It takes inputs from the user (e.g. which year is need to displayed) and performs its task and returns it to the browser. The second argument of the callback function (`Input(...))`, itself a function, takes the value of year-slider. This is the id given to the `dcc.Slider(...)` in the above block of code. The first argument of the callback function (`Output(...))` takes graph1 the id given to the `dcc.Graph(..)` above. It is where the graph is displayed.
# 

# In[5]:


@app.callback(
Output('graph1', 'figure'),
Input('year-slider', 'value'))
def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]
    fig = px.scatter(filtered_df, 
                    x="gdpPercap", 
                    y="lifeExp",
                    size="pop", 
                    color="continent", 
                    hover_name="country",
                    log_x=True, size_max=55
                    )
    fig.update_layout(transition_duration=500)
    return fig


# The function `update_figure(...)` takes the values through `Input(...)` (i.e. year-slider). Based on the year chosen by the user, it filters the data for relevant for this year. Then it draws the graph using the plotly express package imported in the first step. Finnally, it regurns the chart through `Outout(...)` and throws it to the place where an id of graph1 is defined.
# 
# The last step is to run your application. If you are working on non-Jupyter environment, then run from the terminal like so.

# <pre>
# <code>
#  $ python app.py
#   ...Running on http://127.0.0.1:8050/ (Press CTRL+C to quit)
# </code>
# </pre>

# In my case, I am running on here on Jupyter, so the relevant code is in the following cell.

# In[6]:


if __name__ == '__main__':
    app.run_server(mode='inline', port=8053)

