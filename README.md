# Risk and Controls Assesment Dashboard
### Author - Tom Welsh twelsh37@gmail.com

## Description
This program is used to read in a standard set of Risk and Control assesment forms and display various metrics that can
be gleaned from the data.

The program can also be used as a tool to help cleanse/sanataise your data. Those annoying humans that substitute '&'
for 'and' or as a spurious 's's at the end of some standard term from our lexicon

## Deconstruction
There are several key parts to the Application.
1. Which libraries we are going to use
2. Importing our data into a pandas data frame
3. Using Dash layout our page
4. Utilise dropdown list boxes to filter our data
5. Display the results of our filtered data in a collection of plotly graphs

The Risk Identification level lays out what should be attributed to each drop downlist box on initial filtering.
<ul>Risk Types (L1) equates to Risk Type</ul>
<ul>Risk (L2) Risk/ul>
<ul>Level 3 equated to Level 3</ul>

## Risk Identification Table
<table class="ri-table">
    <thead>
        <tr class="ri-firstrow">
            <th>Risk Types</th>
            <th>Risk</th>
            <th>Level 3</th>
        </tr>
    </thead>
        <tbody>
             <tr><td rowspan="41">Operational Risks</td><td rowspan="1">Business Change</td><td rowspan="1">Business Process Change</td></tr>
             <tr><td rowspan="2">Business Continuity & Disaster Recovery</td><td>Disaster & Other Events </td></tr>
             <tr><td>Business Continuity </td></tr>
             <tr><td rowspan="6">Financial Crime Risk</td><td>Unauthorised Activity by Internal Staff</td></tr>
             <tr><td>Internal Theft & Fraud</td></tr>
             <tr><td>External Fraud</td></tr>
             <tr><td>Anti-Money Laundering</td></tr>
             <tr><td>Sanctions</td></tr>
             <tr><td>Anti-Bribery & Corruption</td></tr>
             <tr><td rowspan="2">Information & Data Security</td><td>Information Security</td></tr>
             <tr><td>Data Protection</td></tr>
             <tr><td rowspan="8">Legal (Commercial/Litigation)</td><td>Confidentiality Agreements</td></tr>
             <tr><td>Legal Advice</td></tr>
             <tr><td>Changes in Legislative and Policy Interpretation</td></tr>
             <tr><td>Litigation</td></tr>
             <tr><td>Contracts and standard Documentation</td></tr>
             <tr><td>Intellectual Property</td></tr>
             <tr><td>Dawn Raids</td></tr>
             <tr><td>Competition</td></tr>
             <tr><td rowspan="2">Procurement Risk and Outsourcing Risk</td><td>Dealing with External Suppliers</td></tr>
             <tr><td>Procurement</td></tr>
             <tr><td rowspan="7">People</td><td>Rewarding and Developing Employees</td></tr>
             <tr><td>Supervision Failure</td></tr>
             <tr><td>Managing People Responsibly and Fairly</td></tr>
             <tr><td>Health, Safety and Environment</td></tr>
             <tr><td>Skills/Knowledge Gaps</td></tr>
             <tr><td>Capacity (Inadequate Resources)</td></tr>
             <tr><td>Training & Competence</td></tr>
             <tr><td rowspan="2">Information Technology & Infrastructure</td><td>Information Technology Management</td></tr>
             <tr><td>Technology Change</td></tr>
             <tr><td rowspan="7">Operations (Processing)</td><td>Transaction Operations</td></tr>
             <tr><td>Payment Processing</td></tr>
             <tr><td>Records Management</td></tr>
             <tr><td>Process Failure (circumvention of protocol)</td></tr>
             <tr><td>Lack of Escalation</td></tr>
             <tr><td>Human Error</td></tr>
             <tr><td>Process Change</td></tr>
             <tr><td rowspan="2">Regulatory & Compliance Risk</td><td>Compliance</td></tr>
             <tr><td>Regulatory Risk</td></tr>
             <tr><td>Conduct Risk</td><td>Conduct Risk</td></tr>
             <tr><td>Client Money Segregation</td><td>Client Money Segregation</td></tr>
             <tr><td rowspan="7">Financial Risk</td><td rowspan="2">Credit & Counterparty Risk</td><td rowspan="1">Credit Risk</td></tr>
             <tr><td>Trade Counterparty</td></tr>
             <tr><td>Insurance Risk</td><td>Insurance</td></tr>
             <tr><td rowspan="2">Tax & Financial Reporting</td><td>Financial Mis-reporting</td></tr>
             <tr><td>VAT & Corporation Tax</td></tr>
             <tr><td>Liquidity Risk</td><td>Liquidity Risk</td></tr>
             <tr><td>Market Risk</td><td>Market Risk</td></tr>
             <tr><td rowspan="4">Business & Strategic Risk</td><td>Acquisitions & Disposals</td><td>Acquisitions & Disposals</td></tr>
             <tr><td>Strategic/Business Model</td><td>Business Model</td></tr>
             <tr><td>Preparedness for Regulatory Change</td><td>Regulatory Change</td></tr>
             <tr><td>Reputational</td><td>Reputational Risk</td></tr>
        </tbody>
</table>
