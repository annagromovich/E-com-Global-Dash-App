import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
from datetime import datetime, date

ecom_sales = pd.read_csv("https://raw.githubusercontent.com/annagromovich/E-com-Global-Dash-App/main/ecom_data_full.csv")
logo_link = 'https://assets.datacamp.com/production/repositories/5893/datasets/fdbe0accd2581a0c505dab4b29ebb66cf72a1803/e-comlogo.png'
color_scheme = px.colors.qualitative.T10
ecom_bar = ecom_sales.groupby('Country')['OrderValue'].agg('sum').reset_index(name='Total Sales ($)').sort_values(by='Total Sales ($)', ascending=False)
ecom_line = ecom_sales.groupby(['Year-Month','Country'])['OrderValue'].agg('sum').reset_index(name='Total Sales ($)')
line_graph = px.line(data_frame=ecom_line, x='Year-Month', y='Total Sales ($)', title='Total Sales by Month', color='Country')
bar_fig_country = px.bar(data_frame = ecom_bar, x='Total Sales ($)', y='Country', color='Country', orientation = 'h', title='Sales by Country', color_discrete_sequence=color_scheme)
bar_fig_country.update_layout(plot_bgcolor='#FFFFFF', showlegend=False, bargap=0.4)
bar_fig_country.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0, 0, 255, 0.1)')  # Blue grid with 10% opacity
bar_fig_country.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0, 0, 255, 0.1)', title_text='') 

external_stylesheets = ['styles.css']

app = dash.Dash(__name__, meta_tags=[{'name': 'viewport',
                            'content': 'width = device-width, initial-scale=0.8, maximum-scale=0.8, minumum-scale=0.8'}],
                 external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(
    children=[
        html.Img(src=logo_link, style={'float':'left'}),
        html.H1('The Sales Dashboard for E-com Global', style={'text-align': 'center', 'color': '#1f77b4'}),
        html.Div([
           dcc.Graph(id='bar_graph', figure=bar_fig_country, className='custom-graph', style={'display': 'inline-block', 'vertical-align': 'middle'}),
            html.Span(["In 2011, ", html.B("Australia"), " emerged as E-com Global's top customer, driving total sales volume surpassing $6,000, constituting a substantial ", html.B("29%"), " of the company's overall sales. ", html.B("France and the United Kingdom"), " closely followed, each contributing just over $5,500 in sales. Meanwhile, sales volumes with ", html.B("Germany"), " hovered around $3,150, while transactions with ", html.B("Hong Kong"), " amounted to approximately $1,660."],
                      style={'display': 'inline-block', 'font-size': '18px', 'line-height': '1.5', 'text-align': 'justify', 'background-color': 'rgba(173, 216, 230, 0.5)', 'padding': '10px', 'border-radius': '5px', 'margin': '0', 'box-sizing': 'border-box', 'vertical-align': 'middle'},
                      className='custom-span'),
            ]),
        html.Br(),
        html.Br(),
        html.Div([
                html.H3('Select a Country to Update All the Following Graphs Accordingly'),
                html.Div([
                    dcc.Dropdown(
                        id='country_dd',
                        options=[
                            {'label': 'UK', 'value': 'United Kingdom'},
                            {'label': 'GM', 'value': 'Germany'},
                            {'label': 'FR', 'value': 'France'},
                            {'label': 'AUS', 'value': 'Australia'},
                            {'label': 'HK', 'value': 'Hong Kong'}
                        ],
                        style={'width': '150px', 'margin': '0 auto'}
                    ),
                ])], style={ 'display': 'flex', 'align-items': 'center', 'gap': '20px' }),
            html.Div([
                html.Br(),
                dcc.Graph(id='graph_1', style={'display': 'inline-block', 'vertical-align': 'middle'},
                          className = 'custom-graph'),
                html.Span(["E-com Global's customer countries experience sales peaks at different times of the year. The ", html.B("UK and France"), " typically see their highest sales towards the end of the year, during the holiday season. In contrast, ", html.B("Germany and Australia"), " enjoy sales peaks in the spring months, specifically in May and March, respectively. Meanwhile, ", html.B("Hong Kong"), " stands out with two sales peaks annually, occurring in January and late summer."],
                          style={'display': 'inline-block', 'vertical-align': 'middle', 'font-size': '18px', 'line-height': '1.5', 'text-align': 'justify', 'background-color': 'rgba(173, 216, 230, 0.5)', 'padding': '10px', 'border-radius': '5px'},
                          className='custom-span'),
                html.Br(),
                html.Br(),
                html.Span([html.B("Australia"), ", E-com Global's largest customer, favors goods in the Kitchen category. Meanwhile, European nations such as ", html.B("the UK, Germany, and France"), " tend to purchase items primarily from the Garden category. In contrast, Clothes stand out as the top goods category for ", html.B("Hong Kong.")],
                          style={'display': 'inline-block', 'vertical-align': 'middle', 'font-size': '18px', 'line-height': '1.5', 'text-align': 'justify', 'background-color': 'rgba(173, 216, 230, 0.5)', 'padding': '10px', 'border-radius': '5px'},
                          className = 'custom-span'),
                dcc.Graph(id='graph_2', style={'display': 'inline-block', 'vertical-align': 'middle'},
                          className='custom-graph')
            ]),
            html.Div([
                html.H3('Select a Goods Category to Update the Graph Accordingly'),
                dcc.Dropdown(id='category_dd',
                             options=[
                                 {'label': 'Kitchen', 'value': 'Kitchen'},
                                 {'label': 'Garden', 'value': 'Garden'},
                                 {'label': 'Household', 'value': 'Household'},
                                 {'label': 'Clothes', 'value': 'Clothes'}
                             ],
                             style={'width': '150px'}
                             ),
            ],
            style={ 'display': 'flex', 'align-items': 'center', 'gap': '20px' }),

            html.Div([
                dcc.Graph(id='categories', style={'display': 'inline-block', 'vertical-align': 'middle'},
                          className='custom-graph'),
                html.Span(["Scales stand out as the top pick in the ", html.B("Kitchen"), " goods category worldwide, while Seeds dominate as the preferred choice in the ", html.B("Garden"), " category. Across households globally, Rugs emerge as the favored item in the ", html.B("Household"), " category, whereas Hats take the lead in the ", html.B("Clothes"), " category. To delve into country-specific preferences, simply select your desired country from the dropdown menu above."],
                          style={'display': 'inline-block', 'vertical-align': 'middle', 'font-size': '18px', 'line-height': '1.5', 'text-align': 'justify', 'background-color': 'rgba(173, 216, 230, 0.5)', 'padding': '10px', 'border-radius': '5px'},
                          className='custom-span')
            ])
    ]
)


@app.callback(
    [Output(component_id='graph_1', component_property='figure'),
     Output(component_id='graph_2', component_property='figure')],
    Input(component_id='country_dd', component_property='value')
)
def update_plots(input_country):
    # Set a default value
    country_filter = 'All Countries'
    # Ensure the DataFrame is not overwritten
    sales = ecom_sales.copy(deep=True)
    if input_country:
        country_filter = input_country
        sales = sales[sales['Country'] == country_filter]
    ecom_line = sales.groupby(['Year-Month','Country'])['OrderValue'].agg('sum').reset_index(name='Total Sales ($)')
    graph_1 = px.line(data_frame=ecom_line, x='Year-Month', y='Total Sales ($)', title=f'Total Sales by Month in {country_filter}', color='Country', color_discrete_sequence=color_scheme)
    graph_1.update_xaxes(title_text = '')
    graph_1.update_yaxes(title_text = '')
    graph_1.update_layout(legend=dict(font=dict(size=10)))
    ecom_bar_major_cat = sales.groupby('Major Category')['OrderValue'].agg('sum').reset_index(name='Total Sales ($)').sort_values(by='Total Sales ($)', ascending=False)
    graph_2 = px.bar(
        title=f'Sales in {country_filter} by Major Category', data_frame=ecom_bar_major_cat, x='Total Sales ($)', y='Major Category',
        color='Major Category', color_discrete_sequence=color_scheme
    )
    graph_2.update_yaxes(title_text='')
    graph_2.update_layout(showlegend = False)
    graphs = [graph_1, graph_2]
    
    # Loop through the graphs and customize the layout
    for graph in graphs:
        graph.update_layout(
            plot_bgcolor='#FFFFFF',  # Set background color to white
            xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(0, 0, 255, 0.1)'),  # Customize x-axis grid
            yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(0, 0, 255, 0.1)')
        )
    # Return the figure
    return graphs

@app.callback(
    Output(component_id='categories', component_property='figure'),
    [Input(component_id='category_dd', component_property='value'),
    Input(component_id='country_dd', component_property='value')]
)
def update_categories_graph(input_category, input_country):
    default_category = 'Kitchen'
    category_filter = input_category if input_category else default_category
    country_filter = input_country if input_country else 'All Countries'
    sales = ecom_sales.copy(deep=True)
    if input_country:
        sales = sales[sales['Country'] == input_country]
    if not input_category:
        sales = sales[sales['Major Category'] == default_category]
    else:
        sales = sales[sales['Major Category'] == input_category]
    major_minor = sales.groupby(['Major Category', 'Minor Category'])['OrderValue'].agg('sum').reset_index(name='Total Sales ($)').sort_values(by='Total Sales ($)', ascending = False)
    title = f'Sales of Minor Categories in {category_filter} Category in {country_filter}'
    categories = px.bar(
        title=title,
        data_frame=major_minor,
        x='Total Sales ($)',
        y='Minor Category',
        color='Minor Category',
        color_discrete_sequence=color_scheme
    )
    categories.update_layout(
        plot_bgcolor='#FFFFFF',
        showlegend=False,
        title = {
            'text': title,
            'font': {'size': 14}
        },  
            xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(0, 0, 255, 0.1)'), 
            yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(0, 0, 255, 0.1)')
    )
    categories.update_yaxes(title_text='')
    return categories
    
if __name__ == '__main__':
    app.run_server(debug=True)
    
