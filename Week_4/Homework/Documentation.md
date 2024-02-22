# Documentation for DBT Analytics

## 1: Sign in to DBT and create project

This step is fairly straight forward. Follow the steps on screen and configure your backend database.
If you are using BigQuery, remember to specify the correct location where your dataset resides. eg 'US' or 'EU' or 'us-central1'.
For this, check the location in BigQuery schema/table details, and mention the same location under credentials in dbt profile settings.

## 2: Create Development Branch

As dbt doesn't enable users to work in the main/master branch in dbt, we need to create a new branch. Do this by clicking on the dropdown on left hand side.

## 3: Initialize dbt

Click on intialize dbt, so that dbt will build you a fresh boiler plate template to work on.
