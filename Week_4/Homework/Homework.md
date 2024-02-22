# Homework Week 4

## Analytics Engineering

### Q1. What happens when we execute dbt build --vars '{'is_test_run':'true'}'?

- It's the same as running dbt build
- It applies a limit 100 to all of our models
- It applies a limit 100 only to our staging models
- Nothing

**Solution: It applies a limit 100 to all of our models**

### Q2. What is the code that our CI job will run? Where is this code coming from?

- The code that has been merged into the main branch
- The code that is behind the creation object on the dbt_cloud_pr_ schema
- The code from any development branch that has been opened based on main
- The code from the development branch we are requesting to merge to main

**Solution: The code from the development branch we are requesting to merge to main**

### Q3. What is the count of records in the model fact_fhv_trips after running all dependencies with the test run variable disabled (:false)?

- 12998722
- 22998722
- 32998722
- 42998722

**Solution:**

### Q4. What is the service that had the most rides during the month of July 2019 month with the biggest amount of rides after building a tile for the fact_fhv_trips table?

- FHV
- Green
- Yellow
- FHV and Green

**Solution:**
