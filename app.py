"""
Task 3 & 4: Dash Application for Soul Foods Sales Visualization

This Dash application visualizes Pink Morsel sales data and allows users to:
- View sales trends over time as a line chart
- Filter by region using radio buttons
- See whether sales were higher before or after January 15th, 2021
"""

import dash
from dash import dcc, html, callback, Output, Input
import pandas as pd
import plotly.express as px

# Load the processed data
df = pd.read_csv('data/formatted_sales_data.csv')
df['Date'] = pd.to_datetime(df['Date'])

# Get unique regions for the radio buttons
regions = ['all'] + sorted(df['Region'].unique().tolist())

# Initialize the Dash app
app = dash.Dash(__name__)

# Custom CSS styles
app.layout = html.Div(
    style={
        'fontFamily': '"Segoe UI", Tahoma, Geneva, Verdana, sans-serif',
        'backgroundColor': '#1a1a2e',
        'minHeight': '100vh',
        'padding': '20px'
    },
    children=[
        # Header
        html.Div(
            style={
                'textAlign': 'center',
                'marginBottom': '30px',
                'padding': '20px',
                'backgroundColor': '#16213e',
                'borderRadius': '10px',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.3)'
            },
            children=[
                html.H1(
                    "Soul Foods - Pink Morsel Sales Dashboard",
                    style={
                        'color': '#e94560',
                        'marginBottom': '10px',
                        'fontSize': '2.5rem'
                    }
                ),
                html.P(
                    "Track the profitability of your top performing candy bar",
                    style={
                        'color': '#a0a0a0',
                        'fontSize': '1.1rem'
                    }
                )
            ]
        ),
        
        # Controls section
        html.Div(
            style={
                'backgroundColor': '#16213e',
                'padding': '20px',
                'borderRadius': '10px',
                'marginBottom': '20px',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.3)'
            },
            children=[
                html.Label(
                    "Select Region:",
                    style={
                        'color': '#e94560',
                        'fontSize': '1.2rem',
                        'fontWeight': 'bold',
                        'marginBottom': '10px',
                        'display': 'block'
                    }
                ),
                dcc.RadioItems(
                    id='region-radio',
                    options=[{'label': r.capitalize() if r != 'all' else 'All Regions', 'value': r} for r in regions],
                    value='all',
                    style={
                        'color': '#ffffff',
                        'display': 'flex',
                        'gap': '20px',
                        'flexWrap': 'wrap'
                    },
                    labelStyle={
                        'padding': '10px 20px',
                        'backgroundColor': '#0f3460',
                        'borderRadius': '5px',
                        'cursor': 'pointer',
                        'transition': 'all 0.3s ease'
                    },
                    inputStyle={
                        'marginRight': '8px'
                    }
                )
            ]
        ),
        
        # Chart section
        html.Div(
            style={
                'backgroundColor': '#16213e',
                'padding': '20px',
                'borderRadius': '10px',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.3)'
            },
            children=[
                dcc.Graph(
                    id='sales-chart',
                    config={'displayModeBar': True, 'scrollZoom': True}
                )
            ]
        ),
        
        # Summary stats section
        html.Div(
            id='summary-stats',
            style={
                'marginTop': '20px',
                'backgroundColor': '#16213e',
                'padding': '20px',
                'borderRadius': '10px',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.3)',
                'color': '#ffffff'
            }
        ),
        
        # Footer
        html.Div(
            style={
                'textAlign': 'center',
                'marginTop': '30px',
                'padding': '15px',
                'color': '#666'
            },
            children=[
                html.P("Quantium Software Engineering Virtual Experience | Built with Dash")
            ]
        )
    ]
)


@callback(
    [Output('sales-chart', 'figure'),
     Output('summary-stats', 'children')],
    [Input('region-radio', 'value')]
)
def update_chart(selected_region):
    """Update the chart and summary stats based on selected region."""
    
    # Filter data based on selected region
    if selected_region == 'all':
        filtered_df = df.copy()
        title = "Pink Morsel Sales Over Time - All Regions"
    else:
        filtered_df = df[df['Region'] == selected_region]
        title = f"Pink Morsel Sales Over Time - {selected_region.capitalize()} Region"
    
    # Aggregate sales by date
    daily_sales = filtered_df.groupby('Date')['Sales'].sum().reset_index()
    
    # Create the line chart
    fig = px.line(
        daily_sales,
        x='Date',
        y='Sales',
        title=title,
        template='plotly_dark'
    )
    
    # Add a vertical line at January 15, 2021
    jan_15_2021 = pd.to_datetime('2021-01-15')
    fig.add_vline(
        x=jan_15_2021,
        line_dash="dash",
        line_color="#e94560",
        annotation_text="Jan 15, 2021",
        annotation_position="top"
    )
    
    # Customize the chart appearance
    fig.update_traces(
        line=dict(color='#00d4ff', width=2),
        mode='lines'
    )
    
    fig.update_layout(
        paper_bgcolor='#16213e',
        plot_bgcolor='#0f3460',
        font=dict(color='#ffffff'),
        title=dict(
            font=dict(size=18, color='#e94560'),
            x=0.5
        ),
        xaxis=dict(
            title='Date',
            gridcolor='#1a1a2e',
            showgrid=True
        ),
        yaxis=dict(
            title='Sales ($)',
            gridcolor='#1a1a2e',
            showgrid=True,
            tickformat='$,.0f'
        ),
        hovermode='x unified'
    )
    
    # Calculate summary statistics
    # Split data before and after Jan 15, 2021
    before_jan15 = daily_sales[daily_sales['Date'] < jan_15_2021]['Sales'].sum()
    after_jan15 = daily_sales[daily_sales['Date'] >= jan_15_2021]['Sales'].sum()
    
    # Determine which period had higher sales
    if before_jan15 > after_jan15:
        comparison = "Sales were HIGHER before January 15th, 2021"
        comparison_color = "#4caf50"
    else:
        comparison = "Sales were HIGHER after January 15th, 2021"
        comparison_color = "#ff9800"
    
    total_sales = daily_sales['Sales'].sum()
    avg_daily_sales = daily_sales['Sales'].mean()
    
    # Create summary stats display
    summary = html.Div([
        html.H3("Sales Summary", style={'color': '#e94560', 'marginBottom': '15px'}),
        html.Div(
            style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(200px, 1fr))', 'gap': '20px'},
            children=[
                html.Div([
                    html.P("Total Sales", style={'color': '#a0a0a0', 'marginBottom': '5px'}),
                    html.P(f"${total_sales:,.2f}", style={'fontSize': '1.5rem', 'fontWeight': 'bold', 'color': '#00d4ff'})
                ]),
                html.Div([
                    html.P("Avg Daily Sales", style={'color': '#a0a0a0', 'marginBottom': '5px'}),
                    html.P(f"${avg_daily_sales:,.2f}", style={'fontSize': '1.5rem', 'fontWeight': 'bold', 'color': '#00d4ff'})
                ]),
                html.Div([
                    html.P("Before Jan 15, 2021", style={'color': '#a0a0a0', 'marginBottom': '5px'}),
                    html.P(f"${before_jan15:,.2f}", style={'fontSize': '1.5rem', 'fontWeight': 'bold', 'color': '#4caf50'})
                ]),
                html.Div([
                    html.P("After Jan 15, 2021", style={'color': '#a0a0a0', 'marginBottom': '5px'}),
                    html.P(f"${after_jan15:,.2f}", style={'fontSize': '1.5rem', 'fontWeight': 'bold', 'color': '#ff9800'})
                ])
            ]
        ),
        html.Div(
            style={
                'marginTop': '20px',
                'padding': '15px',
                'backgroundColor': '#0f3460',
                'borderRadius': '8px',
                'textAlign': 'center'
            },
            children=[
                html.P(
                    comparison,
                    style={
                        'fontSize': '1.3rem',
                        'fontWeight': 'bold',
                        'color': comparison_color,
                        'margin': '0'
                    }
                )
            ]
        )
    ])
    
    return fig, summary


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
