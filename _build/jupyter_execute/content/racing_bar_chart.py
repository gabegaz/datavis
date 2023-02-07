#!/usr/bin/env python
# coding: utf-8

# ## Racing Bar Charts
# 
# ### Introduction
# 
# Analysis on temporal observations (aka time series data) can be made in several ways. One traditional and most commonly used time series charts is to draw time on the x-axis and values of variables on the y-axis. This provides us with the behavior of a variable (e.g. trend, variability, seasonality and a basic view of whether that variable exhibits stationarity). A relatively newer way of looking at the dynamics of changes in the units of analysis with respect to a given variable is a racing chart (i.e. animated charts based on changes in the values of a variable over time). Racing charts can be used for different types of plots such as scatter plots, bar charts etc. In this tutorial, we will see how we can construct a racing bar chart.

# There are different tools (libraries) out there that can help us draw a racing charts. One such tool is Python’s Plotly Dash, whose basic use was shown in section 1. This can be achieved by tweaking some of the arguments of the Figure object in Dash.

# ### Installation and setup
# I use Python 3.9 for this section tutorial and is based on dash version 2.6.1 (which supports Python 3). Versions of dash before 2.0.0 also support Python 2. But it is preferable to work with Python 3 as Python 2 is no more supported by the Python software foundation as of 2020. Working in a virtual environment is advisable as it will create a sandbox for our project without disturbing other environments in your machine. Creating a virtual environment is easy. You can implement one of the few approaches available. You can use venv which comes with Python. In linux systems, you can run the following commands to create a virtual environment.

# <pre>
# <code>
# cd Desktop                          #go to Desktop. You can be anywhere 
# mkdir NAME_OF_DIRECTORY             #create your folder anywhere you want your project to reside. 
#                                     #Replace NAME_OF_DIRECTORY with your own folder name
# python3 venv YOUR_VIRTUAL_ENV       #replace YOUR_VIRTUAL_ENV with your own name
# source venv/bin/activate            #This activates your environment
# </code>
# </pre>

# First, while you are in your virtual environment, install dash. Also install pandas for handling data and provide dataframe to plotly express (a package from Plotly) for visualization. But we don’t need to install plotly express separately as it is handled by dash. Installing dash will bring plotly express to our service.
# 

# <pre>
# <code>
# pip install jupyter-dash   # pip install dash if you are on non-Jupyter environment 
# pip install pandas
# </code>
# </pre>

# ### Start coding
# 
# **Importing packages**
# 
# Once your installation process went well, let’s start the actual coding. Open a file and name it whatever you want to call it. I called it app.py for this tutorial. I always consider the basic  seven step process, described in the first section, while working with Plotly Dash. First, import the packages that we need for instantiating our app, data handling, visualizing and interacting with our data. Each of these modules imported below will be explained in places they are used, so go run the following.

# In[1]:


from jupyter_dash import JupyterDash
from dash import html, dcc
import plotly.express as px
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input


# **Instantiate dash application**
# 
# We run `from jupyter_dash import JupyterDash` to have access to the Dash class to instantiate our application. So go run the following code. The `__name__` value for the name parameter is used to make it easy for Dash to locate static assets to be used in the app.
# 

# In[2]:


app = JupyterDash(__name__)


# **Work on your data**
# 
# Now, lets work on our data before going further coding with dash. We use pandas for this and the reason we imported `import pandas as pd`. You need pandas for reading our data, handling and managing it and sending the refined data to plotly express for visualization. While you have other alternatives, pandas is a convenient one for its easy-to-use dataframe.
# 
# At this point, I use data from National Bank of Ethiopia on total bank lending, collection of loans and outstanding loans. This information is available by bank (hence the reason for using it to show racing bar chart). If you want country data for example, you should have data of your interest from at least more than one country. The data I’m using is from my local machine, and is in comma separated values (csv), so I can use pandas’s `pd.read_csv(...)` method to get the data for our purpose.

# In[3]:


df = pd.read_csv('../data/bank_loan.csv')


# Let’s see the structure of the data we are using. Use `df.head()` to see the first five observations of the data set and `df.columns` to see the number and type of columns we will be working.

# In[4]:


#check data
df.head()


# At this point, you can work on preparing data suitable for visualization. I will not do much here because this data is already prepared for this purpose. Only one thing I do is to replace 0 with NA using the following code.
# 
# 

# In[5]:


#replace 0 with NA 
df.replace(0, np.nan, inplace=True)


# **Preparing dash layout**
# 
# Now that we are done with getting data, preparing it for our purpose, it’s time to start with the layout of the figure we are building. Everything in the following code snippet is inside `html.Div()` function of the `html` module imported above. This is translated to html's `div` component behind the scenes. Inside this div component, the title of the chart is put using `html.H2` which, in a similar manner, is translated to html's h2 component. 
# 
# 
# Next, we use `dcc` module to call a class Dropdown to select variables for visualization. `html.Br()` simply puts a vertical space. Our chart is put in the `html.Div()` with a `Graph` class coming with the same module. The `id='racing_bar_chart'` is a random name and can be changed, but a necessary construct to refer to the figure from a python callback function to be built in the next step.

# In[6]:


app.layout = html.Div([
        html.H2("A racing bar chart: Ethiopian banks"),

        dcc.Dropdown(id= 'dropdown_var_input',
                options=[{'label': var, 
                                'value': var} for var in ['collection', 'disbursement', 'outstanding']]),
        html.Br(),
        html.Div(
            dcc.Graph(id='racing_bar_chart_output',
                ),
            ),
        html.Br()
    ])


# **Callback functions for interactivity**
# 
# The first part of the following code snippet is the callbacks. [This](https://stackoverflow.com/questions/824234/what-is-a-callback-function) stackoverflow thread has a good resource on this. A callback function is a function you provide to another piece of code, allowing it to be called by that code. The `@app.callback(...)` function is put above the normal python function so that the later calls the former. The dash callback functions have a specific structure. The `Output` and `Input` modules imported above are used here to transfer arguments to the user defined fucntion (in this case `racing_bar_chart()`. 
# 
# The callback function works as follows.The first argument of the `Output`, racing_bar_chart_output, refers to the id of the graph inside `dcc.Graph()` above in the layout. This tells the function, that calls it, (i.e. called by the user defined function below the callback) to put the figure in the place with the relevant id. The second argument is just an optional argument (can be safely ignored for now). In the `Input`, the first argument is the id of the `dcc.Dropdown(...)` function in the layout section above. This tells the function, that calls it, (i.e. `racing_bar_chart()`) to take inputs and use that input. This is indicated by the argument of the user defined funciton (i.e. `racing_bar_chart()`. The argument selected_var is a parameter that expects some input from the callback above it. The second argument of `Input` tells which part of the `dcc.Dropdown()` function with the id of drop_down_input is taken as input.

# In[7]:


@app.callback(
    Output('racing_bar_chart_output', 'figure'),
    Input('dropdown_var_input', 'value'))
def racing_bar_chart(selected_var):
    range_y=[]

    #determine the range of the y-axis for each of the variables
    if selected_var=='collection':
        range_y = [0, 54]
    if selected_var=='disbursement':
        range_y =  [0, 111]
    if selected_var=='outstanding':
        range_y = [0, 708]

    #construct the image        
    fig_bar = px.bar(df, x="bank", y=selected_var, color="bank",
                animation_frame="year", animation_group="bank",
                    range_y= range_y,
                    color_discrete_sequence=px.colors.qualitative.T10)    
    fig_bar.update_yaxes(showgrid=True),
    fig_bar.update_xaxes(categoryorder='total descending')
    fig_bar.update_traces(hovertemplate=None)
    fig_bar.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 500
    fig_bar.update_layout(margin=dict(t=70, b=0, l=70, r=40),
                            hovermode="x unified",
                            xaxis_tickangle=360,
                            xaxis_title='Banks in Ethiopia', yaxis_title=selected_var,
                            title_font=dict(size=25, color='#a5a7ab', family="Lato, sans-serif"),
                            font=dict(color='#8a8d93'),
                            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                            )
    #returns the constructed figure to the space with the id=racing_bar_chart_output
    return fig_bar


# Let’s examine the user defined function racing_bar_chart. It is a normal python function. It starts with the key word `def`, have a user-defined name, expects some value through the variable inside the parenthesis, and returns something return fig_bar. The only difference is the value that this function expects comes from another function (the callback function.) There are three sections inside this function. Lets see each of them. The first one is determining the range of values in the y-axis. This is because, the relative size of loan disbursement, collection and outstanding values are different. Because we are drawing the bar charts on the same plot, huge differences in the range of the y-axis values distorts the charts. The code is pretty simple: if the column transferred through the callback function to this function is, for e.g. "collection", then set the range of values for this variable accordingly. Then, this information will be used to customize the graph yet to be constructed.
# 
# The second section of the code snippet in the function is the actual construction of the figure. The method `px.bar()` is the method used to accept some inputs and draw the chart. Remember that plotly.express was imported as px above. The first argument to this function is the the data frame df. It then sets the y-axis and the x-axis. Please note that the selected_var the function accepts from the callback is used here to set the y-axis.
# 
# **Running the app**
# 
# At the end of your file, you should have the following code. This checks if this file ( `__name__` ) is the same as `__main__` and runs the dash app.

# In[8]:


if __name__ == '__main__':
    app.run_server(mode='inline', port=8052)


# Once you run your app from your machine. Make sure you have got a similar chart from your own browser like the one shown above.
# 
# At first appearance, you will see an empty grid. You will see a dropdown menu just above the figure with a place holder that says “Select”. Select the variable of interest. As soon as you selected a variable to draw, a year slider appears below the chart. Press the `play` sign and see the year slider move. Because private banks joined the Ethiopian financial sector starting the late 1990’s, you won’t see any significant racing up until then. Furthermore, because there are several banks displayed on the legend, you may not see the chart very clearly on small devices (if, for e.g., you are reading this tutorial on mobile devices). Have a try on larger devices.
# 
# There is one big bank (CBE short for Commercial Bank of Ethiopia) which dampened the relative importance of other banks. You can hide CBE from the race and try with the rest of the banks. You can easily do this by using the legend above the chart. You can click “CBE” once and its color fades away and you will not see “CBE” in the chart making the racing clearer. You can also use the control buttons at the top right of the chart. 
# As you put the cursor closor to the controls, you can read their purpose such as reseting axis, zooming in and out. You can also download images it to your local machine.
