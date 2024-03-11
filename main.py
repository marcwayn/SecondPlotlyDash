import pandas as pd
import plotly.express as px
from sklearn.datasets import load_wine # This is where the dataset comes from
from dash import Dash, html, dcc, callback # Dash for webapp, html for html components, dcc for charts/widgets, callback to link things
from dash.dependencies import Input, Output

### Loading dataset
def load_data():
    wine = load_wine()
    df = pd.DataFrame(wine.data, columns=wine.feature_names)
    df['WineType'] = [wine.target_names[t] for t in wine.target]
    return df

### Setting up DataFrame, ingredients list and averages of the DataFrame
df = load_data()
ingredients = df.drop(columns=['WineType']).columns
avg_df = df.groupby('WineType').mean().reset_index()


### Creating scatterplot
def create_scatterplot(x_axis='alcohol', y_axis='malic_acid', color_encode=True):
    scatter_fig = px.scatter(df, 
               x=x_axis, 
               y=y_axis, 
               color='WineType' if color_encode else None, 
               title = "{} vs {}".format(x_axis.capitalize(), y_axis.capitalize()))
    scatter_fig.update_layout(height=600)
    
    return scatter_fig

### Making a barchart
def create_barchart(ingredients=['alcohol', 'malic_acid', 'ash']):
    bar_fig=px.bar(avg_df, 
           x='WineType', 
           y=ingredients, 
           title="Average Ingredients per Wine Type")
    bar_fig.update_layout(height=600)

    return bar_fig

### Creating Widgets
x_axis = dcc.Dropdown(id='x_axis', options=ingredients, value='alcohol', clearable=False)
y_axis = dcc.Dropdown(id='y_axis', options=ingredients, value='malic_acid', clearable=False)

color_encode = dcc.Checklist(id='color_encode', options=['Color-Encode',])

multi_select = dcc.Dropdown(id='multi_select', options=ingredients, value=['alcohol', 'malic_acid', 'ash'], clearable=False, multi=True)

### Creating Web App Layout
app = Dash(title="Wine Analysis")

app.layout = html.Div(
    children=[
        html.H1("Wine Analysis Dataset", 
                style={'text-align': 'center'}
                ),
        html.Div("Exploring the relationship between various ingredients used in creating different wines(class_0, class_1, class_2)", 
                 style={'text-align': 'center'}
                 ),
        html.Br(),
        html.Div(  # Adding a scatterplot to the layout
            children=[
                x_axis, y_axis, color_encode, # These widgets are connected to this scatterplot
                dcc.Graph(id='scatter', figure=create_scatterplot())
            ],
            style={'display': 'inline-block', 'width': '50%'}, # Changing the component width and look
        ),
        html.Div(  # Adding a bar chart to the layout
            children=[
                multi_select, # Multi-select is connected to this chart
                html.Br(), # Makes it so they're side by side
                dcc.Graph(id='bar', figure=create_barchart())
            ],
            style={'display': 'inline-block', 'width': '50%'}, # Changing the component width and look
        )
    ],
    style={'padding': '50px'} # Add padding to all components
)

## Defining callbacks
# Decorator used to make the callback function. Updating ID and figure
@callback(Output('scatter', 'figure'), [Input('x_axis', 'value'), Input('y_axis', 'value'), Input('color_encode', 'value')])
def update_scatterplot(x_axis, y_axis, color_encode):
    return create_scatterplot(x_axis, y_axis, color_encode)

@callback(Output('bar', 'figure'), [Input('multi_select', 'value')])
def update_barchart(ingredients):
    return create_barchart(ingredients)

if __name__ == "__main__":
    app.run_server(debug=True)