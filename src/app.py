from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import plotly.io as pio   #plotly.io (pio): Graph templates ko customize karne ke liye
import plotly.colors as colors 
import plotly.graph_objects as go
pio.templates.default = "plotly_white" 
import pandas as pd

# Load and clean data
df = pd.read_csv("Sample - Superstore.csv", encoding='latin-1')
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])
df['Order Month'] = df['Order Date'].dt.month.astype('category')
df['Order Year'] = df['Order Date'].dt.year
df['Order Day of Week'] = df['Order Date'].dt.dayofweek

# Initialize Dash app
app = Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])
server = app.server  # Expose the server for deployment


app.layout = html.Div([
    html.H1(
        children='E-Commerce Data Analysis Dashboard in Python',
        style={
            'textAlign': 'center',
            'color': '#fff'
        }
    ),
    html.Div([
        html.Div([
            dcc.Slider(
            df['Order Year'].min(),
            df['Order Year'].max(),
            step=None,
            value=df['Order Year'].min(),
            marks={str(year): str(year) for year in df['Order Year'].unique()},
            id='year-slider'
        ),
        ], className="top_right"),
        html.Div([
            dcc.Dropdown(
            id='region-dropdown',
            options=[
                {'label': region, 'value': region} for region in df['Region'].unique()
            ],
            value=df['Region'].unique()[0],  # Default value
            placeholder="Select a Region",
            style={
            'width': '100%',              # Adjust the dropdown width
            'backgroundColor': '#1f2c56', # Background color of the dropdown
            'color': '#000',             # Text color
            'border': '1px solid #ccc',  # Border styling
            'padding': '10px',           # Padding inside the dropdown
            'borderRadius': '5px',       # Rounded corners
        }  # Adjust the dropdown width
        ),
        ], className="top_left")
    ], className="top_filter"),
    
    html.Div([
        html.Div([
            dcc.Graph(id='graph-with-slider')],className="montly_train"
        ),
        html.Div([
            dcc.Graph(id='pie-with-slider')], className="category_pie"
        )
    ], className="top_chart"),
    html.Div([
        html.Div([
            dcc.Graph(id='graph-bar-slider')],className="sub_category_bar"
        ),
        html.Div([
            dcc.Graph(id='time-with-slider')], className="time_profit")
    ],className="mid_chart"),
    html.Div([
        html.Div([
            dcc.Graph(id='profit-bar-slider')],className="profit_category_bar"
        ),
        html.Div([
            dcc.Graph(id='profit-with-slider')], className="bottom_time_profit"
        ),
        html.Div([
            dcc.Graph(id='salse-with-slider')], className="bottom_time_profit_salse"
        )
    ],className="bottom_chart")
])

@callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value'),
     Input('region-dropdown', 'value')]
)
def update_figure_time(selected_year,selected_region):
    filtered_df = df[(df['Order Year'] == selected_year) & (df['Region'] == selected_region)]
    sales_by_month = filtered_df.groupby('Order Month')['Sales'].sum().reset_index()
    fig = px.line(sales_by_month, 
                  x='Order Month', 
                  y='Sales')
    fig.update_layout(title_text=f'Monthly Sales Analysis for {selected_year}',title_x=0.5, title_font=dict(size=24))
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot area
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent outer area
        font=dict(color='white'),  # Ensure text is visible
        height=350 #height 200px 
    )
    return fig

@callback(
    Output('pie-with-slider', 'figure'),
    [Input('year-slider', 'value'),
     Input('region-dropdown', 'value')]
)
def update_figure_pie(selected_year,selected_region):
    filtered_df = df[(df['Order Year'] == selected_year) & (df['Region'] == selected_region)]
    sales_by_category = filtered_df.groupby('Category')['Sales'].sum().reset_index()


    fig = px.pie(sales_by_category, 
                values='Sales', 
                names='Category', 
                hole=0.5, 
                color_discrete_sequence=px.colors.qualitative.Pastel)

    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(title_text='Sales Analysis by Category',title_x=0.5, title_font=dict(size=24))
    # Update layout to make background transparent
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot area
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent outer area
        font=dict(color='white'),  # Ensure text is visible
        height=350 #height 200px 
    )
    return fig
@callback(
    Output('graph-bar-slider', 'figure'),
    [Input('year-slider', 'value'),
     Input('region-dropdown', 'value')]
)
def update_figure_bar(selected_year,selected_region):
    filtered_df = df[(df['Order Year'] == selected_year) & (df['Region'] == selected_region)]
    sales_by_subcategory = filtered_df.groupby('Sub-Category')['Sales'].sum().reset_index()
    fig = px.bar(sales_by_subcategory, 
                x='Sub-Category', 
                y='Sales')
    fig.update_layout(title_text='Sales Analysis by Sub-Category',title_x=0.5, title_font=dict(size=24))
    # Update layout to make background transparent
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot area
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent outer area
        font=dict(color='white'),  # Ensure text is visible
        height=350 #height 200px 
    )
    return fig
@callback(
    Output('time-with-slider', 'figure'),
    [Input('year-slider', 'value'),
     Input('region-dropdown', 'value')]
)
def update_figure_profit(selected_year,selected_region):
    filtered_df = df[(df['Order Year'] == selected_year) & (df['Region'] == selected_region)]
    profit_by_month = filtered_df.groupby('Order Month')['Profit'].sum().reset_index()
    fig = px.line(profit_by_month, 
                x='Order Month', 
                y='Profit')

    fig.update_layout(title_text='Monthly Profit Analysis', title_x=0.5,title_font=dict(size=24))
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot area
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent outer area
        font=dict(color='white'),  # Ensure text is visible
        height=350 #height 200px 
    )
    return fig


@callback(
    Output('profit-bar-slider', 'figure'),
    [Input('year-slider', 'value'),
     Input('region-dropdown', 'value')]
)
def update_figure_profit(selected_year,selected_region):
    filtered_df = df[(df['Order Year'] == selected_year) & (df['Region'] == selected_region)]
    profit_by_category = filtered_df.groupby('Category')['Profit'].sum().reset_index()

    fig = px.pie(profit_by_category, 
                values='Profit', 
                names='Category', 
                hole=0.5, 
                color_discrete_sequence=px.colors.qualitative.Pastel)

    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(title_text='Profit Analysis by Category', title_x=0.5,title_font=dict(size=20))
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot area
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent outer area
        font=dict(color='white'),  # Ensure text is visible
        height=350 #height 200px 
    )
    return fig
    
@callback(
    Output('profit-with-slider', 'figure'),
    [Input('year-slider', 'value'),
     Input('region-dropdown', 'value')]
)
def update_figure_profit(selected_year,selected_region):
    filtered_df = df[(df['Order Year'] == selected_year) & (df['Region'] == selected_region)]
    profit_by_subcategory = filtered_df.groupby('Sub-Category')['Profit'].sum().reset_index()
    fig = px.bar(profit_by_subcategory, x='Sub-Category', 
             y='Profit')
    fig.update_layout(title_text='Profit Analysis by Sub-Category', title_x=0.5,title_font=dict(size=20))
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot area
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent outer area
        font=dict(color='white'),  # Ensure text is visible
        height=350 #height 200px 
    )
    return fig
    

@callback(
    Output('salse-with-slider', 'figure'),
    [Input('year-slider', 'value'),
     Input('region-dropdown', 'value')]
)
def update_figure_profit(selected_year,selected_region):
    filtered_df = df[(df['Order Year'] == selected_year) & (df['Region'] == selected_region)]
    sales_profit_by_segment = filtered_df.groupby('Segment').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()

    color_palette = colors.qualitative.Pastel

    fig = go.Figure()
    fig.add_trace(go.Bar(x=sales_profit_by_segment['Segment'], 
                        y=sales_profit_by_segment['Sales'], 
                        name='Sales',
                        marker_color=color_palette[0]))

    fig.add_trace(go.Bar(x=sales_profit_by_segment['Segment'], 
                        y=sales_profit_by_segment['Profit'], 
                        name='Profit',
                        marker_color=color_palette[1]))

    fig.update_layout(title_text='Sales and Profit Analysis by Customer Segment',
                    xaxis_title='Customer Segment',title_x=0.5, yaxis_title='Amount',title_font=dict(size=15))
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot area
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent outer area
        font=dict(color='white'),  # Ensure text is visible
        height=350 #height 200px 
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

    
    
