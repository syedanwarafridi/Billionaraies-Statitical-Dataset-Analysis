from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

df = pd.read_csv('Billionaires_Statistics_Dataset.csv')
mode_value = df['residenceStateRegion'].mode().values[0]
df['residenceStateRegion'] = df['residenceStateRegion'].fillna(mode_value)
selfmade_counts = df['selfMade'].value_counts()
industry_counts = df['industries'].value_counts()



external_stylesheets = [dbc.themes.CERULEAN]

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = dbc.Container([
    dbc.Row([
        html.H1('Billionaires Statistical Analysis', className="text-primary text-center fs-3",
                style={'textAlign': 'center', 'font-weight': 'bold', 'color': 'white'}),
    ], style={'backgroundColor': 'black'}),
    
    dbc.Row([
        
        dbc.Col([dash_table.DataTable(
            data=df.to_dict('records'),
            page_size=12,
            style_table={'overflowX': 'auto'},
            style_cell={'backgroundColor': 'black', 'color': 'white'},
            )
            ], width=6),
        
        dbc.Col([
            dbc.RadioItems(
            options=[{'label': x, 'value': x} for x in ['cpi_country', 'population_country', 'life_expectancy_country']],
            value='cpi_country',
            inline=True,
            id='radio-button-gender',
            style={'color': 'white', 'font-size': '20px', 'display': 'flex', 'flex-direction': 'row', 'align-items': 'center'}),
            
            dcc.Graph(figure={}, id='graph-gender')
        ], width=6)
        
    ]),
    
    dbc.Row([
        
        dbc.Col([
            dcc.Graph(figure=px.pie(
                values=selfmade_counts,
                names=selfmade_counts.index,
                title="Self-Made Status of Billionaires",
                hole=0.5
                ).update_layout(
                plot_bgcolor='black',
                paper_bgcolor='black',
                title=dict(text='Self-Made Status of Billionaires', font=dict(color='white')),
                legend=dict(title=dict(font=dict(color='white')),font=dict(color='white'),),
                ))
            ]),
        
        dbc.Col([
            dcc.Graph(figure=px.pie(
                values=industry_counts,
                names=industry_counts.index,
                title="Distribution of Billionaires by Industry",
                hole=0.5
            ).update_layout(
                plot_bgcolor='black',
                paper_bgcolor='black',
                title=dict(text='Count of Billionaires in Each Industry', font=dict(color='white')),
                legend=dict(title=dict(font=dict(color='white')),font=dict(color='white'),),
            ))
            ]),
        
        dbc.Col([
            dcc.Graph(figure=px.pie(
                values=df['finalWorth'],
                names=df['gender'],
                title="Wealth Distribution by Gender",
                hole=0.5
                ).update_layout(
                plot_bgcolor='black',
                paper_bgcolor='black',
                title=dict(text='Wealth Distribution by Gender', font=dict(color='white')),
                legend=dict(title=dict(font=dict(color='white')),font=dict(color='white'),),
                ))
            
            ]),
        ])
       
], fluid=True, style={'backgroundColor': 'black'})

""" Callbacks """

## Scatter Plot
@callback(
    Output(component_id='graph-gender', component_property='figure'),
    Input(component_id='radio-button-gender', component_property='value')
)
def update_scatter_plot(col_chosen):

    fig = px.scatter(df, x=col_chosen, y="total_tax_rate_country", size="finalWorth",
                     color="residenceStateRegion", hover_name="personName", hover_data=["country"],
                     log_x=True, size_max=40)
    
    
    fig.update_xaxes(tickfont=dict(color='white'))
    fig.update_yaxes(tickfont=dict(color='white'))
    
    fig.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    title=dict(text='Scatter Plot Multivariate Analysis', font=dict(color='white'), x=0.5),
    xaxis_title=dict(text=col_chosen, font=dict(color='white')),
    yaxis_title=dict(text="total_tax_rate_country", font=dict(color='white')),
    xaxis=dict(showline=True, linewidth=2, linecolor='white', mirror=True),
    yaxis=dict(showline=True, linewidth=2, linecolor='white', mirror=True),
    )
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
