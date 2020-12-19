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
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import re
import plotly.express as px


# Read in our RACA raw data files and append them to the initial df dataframe
df = pd.read_excel('clensed.xlsx')

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
# create our function to work through df['risk_id'] and just extract
# the alpha prefix from the risk_id. E.g 'GMBH-P01-R01' becomes 'GMBH'
# 'GMBH' is then appended to the list prefix[]

prefix = []
def business_unit():
    prefix_search=re.compile(r'^[a-zA-Z]+')

    for value in raca_df['risk_id']:
        zz = prefix_search.findall(str(value))
        prefix.append(zz)
    return prefix

business_unit()

# This takes our list of lists, 'prefix', from the function above and pulls out all its members into one list 'extract'
extract = [item[0] for item in prefix]

# Insert a new column to hold our business unit and populate it with Business Unit Names
# We get the byusiness unit names from the 'extract[]' list in the step above
result = []
for value in extract:
    print(value)
    if value == 'DP':
        result.append('Data Privacy')
    elif value == 'AP':
        result.append('Accounts Payable')
    elif value == 'BP':
        result.append('British Petroleum')
    elif value == 'CP':
        result.append('Client Profile')
    else:
        print(f"Business Unit {value} has not been added to the function yet")
    #print(f'DEBUG1: Results just in {result}')

print(f"DEBUG-99: Results list:  {result}")

# Apply reuslts to 'business_unit' to create the column in the dataframe
raca_df['business_unit'] = result

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
# print('Data loaded successfully')
# print(raca_df.head())
# print(raca_df['risk_types'].unique())
# print(raca_df['risk'].unique())
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
            html.H3("Risk Type",className='text-center text-primary')
        ], width=3),
        dbc.Col([
            html.H3("Risk", className='text-center text-primary')
        ], width=3),
        dbc.Col([
            html.H3("Level 3", className='text-center text-primary')
        ], width=3),
    ], align='center'),
    html.Br(),
    dbc.Row([
        dbc.Col([
            # Taxonomy Level 1 Dropdown List box. # '+[{'label': 'All', 'value': 'All'}] adds alkl option
            dcc.Dropdown(id='risk_types', multi=False, value = 'Financial Risk', clearable=False,
                         options=[{'label': k, 'value': k} for k in sorted(raca_df['risk_types'].astype(str).unique())]
                                 + [{'label': 'All', 'value': 'All'}],
                         placeholder='Select...'),
        ], width=3),

        dbc.Col([
            dcc.Dropdown(id='risk', multi=False,
                         options=[{'label': k, 'value': k} for k in sorted(raca_df['risk'].astype(str).unique())]
                                 + [{'label': 'All', 'value': 'All'}],
                         placeholder='Select...'),
        ], width=3),

        dbc.Col([
            dcc.Dropdown(id='level3', multi=False,
                         options=[],
                         placeholder='Select...'),
        ], width=3),
    ], align='top'),
])

@app.callback(
    Output('risk', 'options'),
    Input('risk_types', 'value'))
def set_tl2_options(tl1_options):
    if tl1_options != 'All':
        raca_options = raca_df[raca_df['risk_types'] == tl1_options]
    else:
        raca_options = raca_df
    return [{'label': i, 'value': i} for i in sorted(raca_options['risk'].astype(str).unique())]

@app.callback(
    Output('level3', 'options'),
    Input('risk', 'value'))
def set_tl3_options(tl2_options):
    if tl2_options != 'All':
        raca_options = raca_df[raca_df['risk'] == tl2_options]
    else:
        raca_options = raca_df
    return [{'label': i, 'value': i} for i in sorted(raca_options['level3'].astype(str).unique())]

# # Get all the inputs and output them to a sentence
# # This proves we can get values from the dropdowns
# # so we should now be able to pull values to sort
# # dataframes
#
#
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

z = 'HELLO MAGGOTS!!!!'

@app.callback(
    Output('maggot', 'children'),
    Input('z', 'value'),
    )

def return_dropdown_selections(risk_types, risk, level3):
    return 'Taxonomy Level 1 is {}, Taxonomy Level 2 is {} and level 3 is {}'.format(
        risk_types, risk,  level3,
    )

if __name__ == '__main__':
    app.run_server(debug=True)
