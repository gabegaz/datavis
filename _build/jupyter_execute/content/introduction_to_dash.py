#!/usr/bin/env python
# coding: utf-8

# ### Introduction
# 
# We will start off our journey of data visualization with the basics using Plotly Dash. Dash is an open source Python library built on top of Plotly.js, React and Flask, Dash ties modern UI elements like dropdowns, sliders, and graphs directly to your analytical Python code. It’s maintained by Plotly, another visualization library which helps building, scaling, and deploying data apps in Python. To introduce you to what a simple Dash app looks like, let's create a simple visualization app with a small data set.

# ### A six step process to visualize data
# 
# To simplify how Plotly Dash works, we will break down the process into six distinct steps. These steps are what you need to have before getting your interactive chart from dash app.
# 
# The steps are more or less the same irrispective of the types of project you may be working on; and we will follow all of the hands-on in this project based on these steps. Steps 3-5 might be a little involved and might suddenly increase in complexity depending on the size of the application.
# 
# 
# | #   | <p style="text-align: left;">Steps </p>                  | <p style="text-align: left;"> app </p> |
# | :-- | :------------------------------------------------------: | ----:|
# | 1   | <p style="text-align: left;">Imports (boiler plate) </p> | <p style="text-align: left;"> from dash import Dash, html, dcc</p> <p style="text-align: left;"> import plotly.express as px </p> <p style="text-align: left;"> import pandas as pd </p> |
# | 2   |<p style="text-align: left;"> App Instantiation <p> | <p style="text-align: left;">app = Dash(`__name__`) </p> |
# | 3   |<p style="text-align: left;"> Extract data to be visualized</p>                            |<p style="text-align: left;"> df = pd.read_csv(...) </p>|
# | 4   |<p style="text-align: left;"> Visualize the data</p> |<p style="text-align: left;"> fig = px.bar(...) </p>|
# | 5   |<p style="text-align: left;"> App layout: a list of HTMl and/or interactive components </p> |<p style="text-align: left;"> app.layout = html.Div([<br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;dcc.Dropdown() <br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; dcc.Graph()<br>...]) </p>|
# | 6   |<p style="text-align: left;"> Call back functions</p>	                                     |<p style="text-align: left;"> app.callback(...) </p>|
# | 7   |<p style="text-align: left;"> Running the app </p>	                                         |<p style="text-align: left;"> if __name__ = "__main__":<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  app.run_server() </p> |
# 

# As you can see from the above table, the first step imports all the available libraries. The second step is instantiating the app making Dash available for using its powerful methods/objects. In the third step, we get data to be visualized. We can get data from anywhere you can imagine (local file system, local and remote databases, cloud resources, APIs etc.) In the fourth step, we visualize the data that we extracted in the previous step. The fifth step constructs the layout where the figure is displayed on. The sixth step is what powers dash for its interactivity. The seventh step prepares the app for running it. The actual execution of the app will be made from the terminal.

# Now we will follow these steps to visualize a crop production data into bar graph so that we can apply it to more advanced charts in the upcoming sections.
# 
# This section is based on dash version 2.6. This version supports Python 3. Versions of dash before 2.0.0 also supported Python 2. 
# First create a Python environment. 

# <pre>
# <code>
# cd Desktop                          #go to Desktop. You can be anywhere 
# mkdir NAME_OF_DIRECTORY             #create your folder anywhere you want your project to reside. 
#                                     #Replace NAME_OF_DIRECTORY with your own folder name
# python3 venv YOUR_VIRTUAL_ENV       #replace YOUR_VIRTUAL_ENV with your own name
# source venv/bin/activate            #This activates your environment
# </code>
# </pre>

# Next, install dash and pandas, while you are in your environment.

# <pre>
# <code>
# pip install dash
# pip install pandas
# </code>
# </pre>

# 
# ### Step 1: Import the necessary libraries
# 
# Importing dash and its ecosystem is no different from importing other python library. The first line needs some explanation, however. There are two flavours of dash(Python): Dash and JupyterDash. JupyterDash is usually used to work with Jupyter Notebook as we are doing now. For script based python files, you can use `from dash import Dash`.

# In[1]:


from jupyter_dash import JupyterDash
from dash import html, dcc
import plotly.express as px
import pandas as pd


# The second line imports two important components `html` and `dcc`. In the third line, we are importing plotly express that does the actualization visualization task. Finally, we are importing pandas to extract, handle and prepare data so that it will be in a format that plotly express requires.

# ### Step 2: Instantiate app
# 
# Instantiating dash app is getting an object called app from Dash. You can simply use __name__ inside the parenthesis and ignore what it is for now.
# 
# We use JupyterDash here. As explained above, you can use Dash proper (so that this will be `app = Dash(__name__)` if you want to work in a different environment from Jupyter notebook.

# In[2]:


app = JupyterDash(__name__)


# ### Step 3: Extract and prepare data
# 
# In the third step, we use data from the World Bank on exports of goods and services for three countries: Ethiopia, Uganda and Kenya. The values are expressed in millions of USD. To extract this data, we use pandas's `pd.read_excel(...)` function.

# In[3]:


df = pd.read_excel('../data/exports.xlsx')


# You can see the structure of the data by using the data frame. Just run the following cell, you will find the data in long form.

# In[4]:


df


# ### Step 4: Generate the figure
# 
# Dash graphs are drawn separately and will be appended in the layout (that we will build in teh next step). There are a couple of important functions in the Plotly ecosystem that we can use to draw graphs for Dash. The first of these is [plotly express](https://plotly.com/python/plotly-express/). Plotly express was imported as px above. We can use its inbuilt fuction `px.line(...)` to draw our graph based on the export data like so.

# In[5]:


fig = px.line(df, x="year", 
             y="Exports of goods and services (Million US$)", 
             color="Country")


# We are drawing a line graph. It has four basic arguments. The function takes data using the first argument `df`. The second and third arguments are the `x-axis`, and the `y-axis` respectively. Finally, want to differenciate which lines are for which country. Thus, the last argument (i.e. `color`) serves this purpose.

# ### Step 5: Now the layout
# 
# Once we draw the graph (which was captured in the object `fig`), we can prepare a layout for putting it properly. This leads us to `layouts`. Dash layouts are simply html components with some additional Dash components.
# 
# The function`html.Div(...)` (which translates to html's `Div`) holds everything including the graph and some text(such as title or a summary of the graph). The first object in the `html.Div(...)` is the title of the graph with html header. The second argument of the function is the `dcc.Graph(...)` which holds the figure with the given id. The id links to the call back function which doesn't exist here. We will cover callbacks in a later article.

# In[6]:


app.layout = html.Div(children=[
    html.H1(children='Exports of goods and services (Million US$)'),
    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])


# ### Step 6: Callback functions
# 
# We are not using callbacks here (we will deal with them in a latter section in this project).

# ### Step 7: Run the app
# 
# Finnaly, we prepare the application to run from the terminal. `mode='inline'` is an argument that you might not use for Dash (it is used only for JupyterDash to help run on Jupyter Notebook)

# In[7]:


if __name__ == '__main__':
    app.run_server(mode='inline', port=8051)


# You can click the link and see your app running. Even at this lavel of infance, Dash plots can exhibit some interactivity. Moving the cursor accross the lines show as values for the correspoending axis. Furthermore, once can click country name in the legend to hid plots on main graph, and so on.
