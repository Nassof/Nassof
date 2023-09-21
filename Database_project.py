import pandas as pd
import numpy as np

df = pd.read_csv("bank_marketing.csv")

client = pd.DataFrame(df[["client_id","age", "job", "marital", "education", "credit_default", "housing", "loan"]])

campaign = pd.DataFrame(df[["client_id", "campaign", "month", "day", "duration", "pdays", "previous", "poutcome", "y"]])

economics = pd.DataFrame(df[["client_id", "emp_var_rate", "cons_price_idx", "euribor3m", "nr_employed"]])

client = client.rename(columns={"client_id": "id", "col2": "col_two"})

# renaming columns
client = client.rename(columns = {"client_id":"id"})
campaign = campaign.rename(columns= {"duration":"contact_duration", 
                                     "previous":"previous_campaign_contacts", 
                                     "y":"campaign_outcome", 
                                     "campaign":"number_contacts",
                                     "poutcome":"previous_outcome"})
economics = economics.rename(columns= {"euribor3m":"euribor_three_months",
                                       "nr_employed":"number_employed"})

# cleaning data
client['education'] = client['education'].str.replace('.','-').replace('unknown',np.NaN)
campaign['campaign_outcome'] = campaign['campaign_outcome'].replace('yes',1).replace('no',0)
campaign['previous_outcome'] = campaign['previous_outcome'].replace('nonexistent',np.NaN)

# creating new columns
campaign['month'] = campaign['month'].str.capitalize()
campaign['year'] = "2022"
campaign['day'] = campaign['day'].astype(str)
campaign['last_contact_date'] = campaign['year']+'-'+campaign['month']+'-'+ campaign['day']
campaign['last_contact_date'] = pd.to_datetime(campaign['last_contact_date'],format='%Y-%b-%d')
campaign['campaign_id'] = 1

# droping columns
campaign = campaign.drop(columns = ['month','day','year'])

# saving data
client.to_csv("client.csv", index=False)
campaign.to_csv("campaign.csv", index=False)
economics.to_csv("economics.csv", index=False)

### creating the tables ### 

# client table
client_table = """
CREATE TABLE client
(
   id SERIAL PRIMARY KEY,
 age INTEGER,
 job TEXT,
 marital TEXT,
 education TEXT,
 credit_default BOOLEAN,
 housing BOOLEAN,
 loan BOOLEAN
);
\copy client from 'client.csv' DELIMITER ',' CSV HEADER
"""

# campaign table

campaign_table = """
CREATE TABLE campaign
(
   campaign_id SERIAL PRIMARY KEY,
    client_id SERIAL references client (id),
    number_contacts INTEGER,
    contact_duration INTEGER, 
    pdays INTEGER, 
    previous_campaign_contacts INTEGER, 
    previous_outcome BOOLEAN, 
    campaign_outcome BOOLEAN, 
    last_contact_date DATE
);
\copy campaign from 'campaign.csv' DELIMITER ',' CSV HEADER
"""

# economics table 

economics_table = """
CREATE TABLE economics
(
   client_id SERIAL references client (id),
    emp_var_rate FLOAT,
    cons_price_idx FLOAT,
    euribor_three_months FLOAT,
    number_employed FLOAT
);
\copy economics from 'economics.csv' DELIMITER ',' CSV HEADER
"""