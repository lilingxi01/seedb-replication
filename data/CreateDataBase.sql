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

-- Change the local location of your pro_adult_data.data file.   eg: 'D:\course\645\project\pro_adult_data.data'
COPY adult_data FROM '/absolute/path/to/data/par_adult_data.data' WITH (FORMAT csv);

CREATE TABLE married_data AS 
SELECT age, workclass, fnlwgt, education, education_num, occupation, relationship, race, sex, capital_gain, capital_loss, hours_per_week, native_country, income, partition_id
FROM adult_data
WHERE marital_status = 'Married';

CREATE TABLE unmarried_data AS 
SELECT age, workclass, fnlwgt, education, education_num, occupation, relationship, race, sex, capital_gain, capital_loss, hours_per_week, native_country, income, partition_id
FROM adult_data
WHERE marital_status = 'Unmarried';
