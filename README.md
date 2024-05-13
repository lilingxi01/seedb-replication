# SeeDB Replication

## Database Setup

### 1. Create Database

Connect to your database through `psql` command-line tool or any other tool of your choice. Then, create a database named `census_income`: 

```sql
CREATE DATABASE census_income;
```

After creating the database, connect to it:

```sql
\c census_income
```

### 2. Create Tables

Copy and run the following commands to create the tables:

```sql
CREATE TABLE adult_data (
    age INT,
    workclass VARCHAR(255),
    fnlwgt INT,
    education VARCHAR(255),
    education_num INT,
    marital_status VARCHAR(255),
    occupation VARCHAR(255),
    relationship VARCHAR(255),
    race VARCHAR(255),
    sex VARCHAR(255),
    capital_gain INT,
    capital_loss INT,
    hours_per_week INT,
    native_country VARCHAR(255),
    income VARCHAR(255),
    partition_id INT
);
CREATE INDEX partition_id_index ON adult_data (partition_id);
```

### 3. Load Data

We have already prepared the data in CSV format. The data partitioning has already been done. You can load the data into the table using the following command in your `psql` session:

```sql
\copy adult_data FROM './DataProcess/par_adult_data.data' WITH (FORMAT csv);
```

Alternatively, if you are using a different tool, you can use the `COPY` command with an absolute path to the CSV file. You should ignore this if you are using `psql` command-line tool and can execute the above command. Remember to replace `/absolute/path/to/DataProcess/par_adult_data.data` with the actual path to the CSV file:

```sql
COPY adult_data FROM '/absolute/path/to/DataProcess/par_adult_data.data' WITH (FORMAT csv);
```

### 4. Table Separations

Run the following commands to create two tables, `married_data` and `unmarried_data`, by separating the data based on the `marital_status` column:

```sql
CREATE TABLE married_data AS 
SELECT age, workclass, fnlwgt, education, education_num, occupation, relationship, race, sex, capital_gain, capital_loss, hours_per_week, native_country, income, partition_id
FROM adult_data
WHERE marital_status = 'Married';

CREATE TABLE unmarried_data AS 
SELECT age, workclass, fnlwgt, education, education_num, occupation, relationship, race, sex, capital_gain, capital_loss, hours_per_week, native_country, income, partition_id
FROM adult_data
WHERE marital_status = 'Unmarried';
```

### 5. Setup Environment Variables

Create a `.env` file in the root directory of the project and add the following environment variables:

```env
DATABASE_URL=postgresql://postgres:1234@localhost:5432/census_income
```

If you are using a different database configuration, replace the `DATABASE_URL` value with your database URL (e.g. remote database, another port, etc.).
