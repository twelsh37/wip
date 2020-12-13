"""Risk and Controls Assesment Dashboard
### Author - Tom Welsh twelsh37@gmail.com

## Description
This program is used to read ina  standard set of Risk and Control assesment forms and display various metrics that can
be gleaned from the data.

The program can also be used as a tool to help clense/sanataise your data. Those annoying humands that substitute '&'
for 'and' or as a spurious 's's at the end of some standard term from our lexicon

## Deconstruction

"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd


# Read in our RACA raw data files and append them to the initial df dataframe
df = pd.read_excel('c:/Users/twelsh/data/racas/master/master1.xlsx')

# Rename all column headings to human readable and remove spaces, brackets in description names
# Take our imported data in df and reassign it with new headers to raca_df.
# We will use raca_df and the new column headings from here forward.
raca_df = df.rename(columns={'Process (Title)': 'process_title',
                             'Process description': 'process_description',
                             'Risk ID': 'risk_id',
                             'Risk Owner': 'risk_owner',
                             'Risk(Title)': 'risk_title',
                             'Risk Description': 'risk_description',
                             'Risk Category 1': 'risk_types',
                             'Risk Category 2': 'risk',
                             'Risk Category 3': 'level3',
                             'Associated KRIs': 'associated_kris',
                             'I': 'gross_impact',
                             'L': 'gross_likelihood',
                             'Control ID': 'control_id',
                             'Control Owner': 'control_owner',
                             'Control (Title)': 'control_title',
                             'Control Description': 'control_description',
                             'Control Activity': 'control_activity',
                             'Control Type': 'control_type',
                             'Control Frequency': 'control_frequency',
                             'DE & OE?': 'de_oe',
                             'Commentary on DE & OE assessment': 'de_oe_commentary',
                             'I.1': 'net_impact',
                             'L.1': 'net_likelihood',
                             'Commentary on Net Risk Assessment': 'net_risk_assesment_commentary',
                             'Risk Decision': 'risk_decision',
                             'Issue Description (if applicable)': 'issue_description',
                             'Action Description': 'action_description',
                             'Action Owner': 'action_owner',
                             'Action Due Date': 'action_due_date',
                             'Completion Date': 'completion_date'
                             }
                    )

# Reset our index colum so it is contiguous
raca_df.reset_index(drop=True,
                    inplace=True,
                    col_level=0)

# Start the row index at 1 just to make it easier for mortals
raca_df.index = raca_df.index + 1
# -----------------------------------------------------#

# Global variable to hold our data frame olutput from teh dropdown listboxes
output_dataframe = None

# DEBUGGING ##
# -----------------------------------------------------#
# Inform user that data loaded sucsessfully
print('Data loaded successfully')
print(raca_df.head())
print(raca_df['risk_types'].unique())
# -----------------------------------------------------#

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP]),\
#       meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}]


# Dash layout - max 12 columns per page.
# 3 columns on Row 1 and two of width 4.
# 2 columns on row 3 with width 9 and 3.

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Risk and Controls Assessment Dashboard", className='text-center text-primary mb-4'),
        ], width=12),
    ], align='center'),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.H3("Taxonomy Level 1", className='text-center text-primary')
        ], width=4),
        dbc.Col([
            html.H3("Taxonomy Level 2", className='text-center text-primary')
        ], width=4),
        dbc.Col([
            html.H3("Level 3", className='text-center text-primary')
        ], width=4),
    ], align='center'),
    html.Br(),
    dbc.Row([
        dbc.Col([
            # Taxonomy Level 1 Dropdown List box
            dcc.Dropdown(id='risk_types', multi=True,
                         options=[{'label': k, 'value': k} for k in sorted(raca_df['risk_types'].astype(str).unique())],
                         placeholder='Select...'),
        ], width=4),

        dbc.Col([
            dcc.Dropdown(id='risk', multi=True,
                         placeholder='Select...'),
        ], width=4),

        dbc.Col([
            dcc.Dropdown(id='level3', multi=True,
                         placeholder='Select...'),
        ], width=4),
    ], align='top'),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.Div(id='answer', className='text-center text-primary')
        ], width=12),
    ], align='center'),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.Div(id='answer1', className='text-center text-primary')
        ], width=12),
    ], align='center'),
# This styles the container
],style = {'padding': '50px',
           'backgroundColor': '#EBEFF0',
           'textPrimary': '#071633'},
fluid=True)



@app.callback(
    Output('risk', 'options'),
    Input('risk_types', 'value'))
def set_tl2_options(tl1_options):
    return [{'label': i, 'value': i} for i in sorted(raca_df['risk'].astype(str).unique())]


@app.callback(
    Output('risk', 'value'),
    Input('risk', 'options'))
def set_tl2_value(tl2_options):
    return tl2_options[0]['value']


@app.callback(
    Output('level3', 'options'),
    Input('risk', 'value'))
def set_level3_options(tl3_options):
    return [{'label': i, 'value': i} for i in sorted(raca_df['level3'].astype(str).unique())]


@app.callback(
    Output('level3', 'value'),
    Input('level3', 'options'))
def set_level3_values(l3_options):
    return l3_options[0]['value']

# Get all the inputs and output them to a sentence
# This proves we can get values from the dropdowns
# so we should now be able to pull values to sort
# dataframes


@app.callback(
    Output('answer', 'children'),
    Input('risk_types', 'value'),
    Input('risk', 'value'),
    Input('level3', 'value')
)
def return_dropdown_selections(risk_types, risk, level3):
    return 'Taxonomy Level 1 is {}, Taxonomy Level 2 is {} and level 3 is {}'.format(
        risk_types, risk,  level3,
    )

# Total Number of Risks in whole raca
#@app.callback(
#    Output('tnro', 'value'),
#    Input('tnro','value'))
def tnro():
    tnro = raca_df['risk_id'].nunique()
    print('DEBUG: total number of Risks in Raca {}'.format(tnro,))
    return 'Total Number of Risks is {}'.format(
        tnro,
    )

if __name__ == '__main__':
    app.run_server(debug=True)
