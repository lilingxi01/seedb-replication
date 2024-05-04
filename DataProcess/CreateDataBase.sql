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
    income VARCHAR(255)
);

//Change the local location of your data file.   eg: 'D:\course\645\project\pro_adult_data.data'
COPY adult_data FROM '*/pro_adult_data.data' WITH (FORMAT csv);

select * from adult_data limit 10

CREATE TABLE married_data AS 
SELECT age, workclass, fnlwgt, education, education_num, occupation, relationship, race, sex, capital_gain, capital_loss, hours_per_week, native_country, income
FROM adult_data
WHERE marital_status = 'Married';

select * from married_data limit 10

CREATE TABLE unmarried_data AS 
SELECT age, workclass, fnlwgt, education, education_num, occupation, relationship, race, sex, capital_gain, capital_loss, hours_per_week, native_country, income
FROM adult_data
WHERE marital_status = 'Unmarried';

select * from unmarried_data limit 10
