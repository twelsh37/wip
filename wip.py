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

# -------------------- Data Import and Cleansing---------------------------------#
# Read in our RACA raw data files and append them to the initial df dataframe
df = pd.read_excel('c:/Users/twelsh/data/racas/master/master1.xlsx')

# Rename all column headings to human readable and remove spaces, brackets in description names
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
                             'Completion Date': 'completion_date',
                             'Action ID': 'action_id'
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
    elif value == 'COSECG':
        result.append('Company Secretariat - London')
    elif value == 'BI':
        result.append('Business Inteligence')
    elif value == 'ITDEV':
        result.append('IT Development')
    elif value == 'GMBH':
        result.append('GmbH Subsiduary')
    elif value == 'SEC':
        result.append('Information Security')
    elif value == 'FR':
        result.append('Financial Risk')
    elif value == 'CASS':
        result.append('Client Money')
    elif value == 'PROD':
        result.append('Market Data')
    elif value == 'CSA':
        result.append('Client Services APAC')
    elif value == 'SDBO':
        result.append('Stockbroking Dealing & Business Operations')
    elif value == 'SBDC':
        result.append('Stockbroking Business Change')
    elif value == 'SBBC':
        result.append('Stockbroking Operations')
    elif value == 'SCM':
        result.append('Stockbroking Client Money')
    elif value == 'SOS':
        result.append('Stockbroking Operations - APAC')
    elif value == 'COSECA':
        result.append('Company Secretariat - Aus')
    elif value == 'SP':
        result.append('Stockbroking Partners - APAC')
    elif value == 'WD':
        result.append('Stockbroking Web Development')
    elif value == 'HR':
        result.append('Human Resources')
    elif value == 'BCG':
        result.append('Business Continuity')
    elif value == 'ISP':
        result.append('Institutional Sales & Partners')
    elif value == 'CSG':
        result.append('Client Services - London')
    elif value == 'ST':
        result.append('Sales Trading - London')
    elif value == 'TAX':
        result.append('Tax')
    elif value == 'FIN':
        result.append('Finance')
    elif value == 'FACL':
        result.append('Facilities')
    elif value == 'ITPROD':
        result.append('IT Production')
    else:
        print(f"Business Unit {value} has not been added to the function yet")
    #print(f'DEBUG1: Results just in {result}')

# Apply reuslts to 'business_unit' to create the column in the dataframe
raca_df['business_unit'] = result

# Create a new dataframe to hold our risk id's risk owners, action id, action owners and action due date.
action_df = raca_df[['action_id',
                     'risk_id',
                     'risk_title',
                     'risk_owner',
                     'business_unit',
                     'action_owner',
                     'action_due_date']]

# Setup some display options if we want to look at our Actions output
# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)

# Drop all rows in the action_df dataframe who do not have data in all 7 fields
# Write thgis back out to actiuon_id so we have a dataframe soley for tracking actions
action_df = action_df.dropna(thresh=7)

# calculate our gross and net risk scores
# it does this by multiplying the impact and likelihood columns
# the results are appended to teh df dataframe under columns
# gross_risk and net_risk respectivly
raca_df['gross_risk'] = raca_df['gross_impact'] * raca_df['gross_likelihood']

raca_df['net_risk'] = raca_df['net_impact'] * raca_df['net_likelihood']

# Reset our index colum so it is contiguous
raca_df.reset_index(drop=True,
                    inplace=True,
                    col_level=0)

# Start the row index at 1 just to make it easier for mortals
raca_df.index = raca_df.index + 1

# -------------------- Data Import and Cleansing Completed -------------------------#

# -----------------------------------------------------#

# Global variable to hold our data frame olutput from teh dropdown listboxes
output_dataframe = None

# DEBUGGING ##
# -----------------------------------------------------#
# Inform user that data loaded sucsessfully
#print('Data loaded successfully')
#print(raca_df.head())
#print(raca_df['risk_types'].unique())
# def which_operations():
#     if raca_df['risk'] == 'Operations':
#         print(raca_df['risk_id'].bool())
#
# which_operations()

# -----------------------------------------------------#

# ----------------Dash Page Layout---------------------#
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'OpRiskRACA '
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
            html.H3("Risk Type", className='text-center text-primary')
        ], width=2),
        dbc.Col([
            html.H3("Risk", className='text-center text-primary')
        ], width=2),
        dbc.Col([
            html.H3("Level 3", className='text-center text-primary')
        ], width=2),
    ], align='center'),
    html.Br(),
    dbc.Row([
        dbc.Col([
            # Taxonomy Level 1 Dropdown List box. # '+[{'label': 'All', 'value': 'All'}] adds alkl option
            dcc.Dropdown(id='risk_types', multi=False, value = 'All', clearable=False,
                         options=[{'label': k, 'value': k} for k in sorted(raca_df['risk_types'].astype(str).unique())]
                                 + [{'label': 'All', 'value': 'All'}],
                         placeholder='Select...'),
        ], width=2),

        dbc.Col([
            dcc.Dropdown(id='risk', multi=False,
                         options=[{'label': k, 'value': k} for k in sorted(raca_df['risk'].astype(str).unique())]
                                 + [{'label': 'All', 'value': 'All'}],
                         placeholder='Select...'),
        ], width=2),

        dbc.Col([
            dcc.Dropdown(id='level3', multi=False,
                         options=[],
                         placeholder='Select...'),
        ], width=2),
    ], align='top'),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.Div(id='answer', className='text-center text-primary')
        ], width=6),
    ], align='start'),
    # html.Br(),
    # dbc.Row([
    #     dbc.Col([
    #         html.Div(id='answer1', className='text-center text-primary')
    #     ], width=6),
    # ], align='center'),
# This styles the container
],style = {'padding': '50px',
           'backgroundColor': '#EBEFF0',
           'textPrimary': '#071633'},
fluid=True)

# ----------------Dash Page Layout Complete---------------------#

# ----------------Dash Page Callbacks---------------------#
@app.callback(
    Output('risk', 'options'),
    Input('risk_types', 'value'))
def set_tl2_options(tl1_options):
    if tl1_options != 'All':
        raca_options = raca_df[raca_df['risk_types'] == tl1_options]
        print(f'DEBUG1: TL 1 Not equal to all: {raca_options}')
    else:
        raca_options = raca_df
        print(f'DEBUG2: TL1 equal to all: {raca_options}')

    return [{'label': i, 'value': i} for i in sorted(raca_options['risk'].astype(str).unique())]

@app.callback(
    Output('level3', 'options'),
    Input('risk', 'value'))
def set_tl3_options(tl2_options):
    if tl2_options != 'All':
        raca_options = raca_df[raca_df['risk'] == tl2_options]
        print(f'DEBUG3: TL2 Not equal to all: {raca_options}')
    else:
        raca_options = raca_df
        print(f'DEBUG4: TL2 equal to all: {raca_options}')
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

# @app.callback(
#     Output('answer1', 'children'),
#     )
# def return_dropdown_selections(answer1):
#     return 'bitches be like weeeee!!!!'

# # Total Number of Risks in whole raca
# @app.callback(
#    Output('tnro', 'value'),
#    Input('tnro','value'))
# def tnro():
#     tnro = raca_df['risk_id'].nunique()
#     print('DEBUG: total number of Risks in Raca {}'.format(tnro,))
#     return 'Total Number of Risks is {}'.format(
#         tnro,
#     )

# ----------------Dash Page Callbacks Completed---------------------#

if __name__ == '__main__':
    app.run_server(debug=True)
