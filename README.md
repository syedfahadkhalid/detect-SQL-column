# Onboarding Exapnsion Scripts

## Steps: 
1. Clone the latest branch of this repository and create a custom branch for your expansion script.
2. You should create a separate .sql file for the expansion script that needs to be run on schema.
3. Your expansion script .sql file needs to be started with the database end point (Route 53 is preferable) and schema name followed by your expansion script. For e.g.
```sql
#database = <Database End Point>
#schema = <Schema Name>

CREATE TABLE FOO (
    --COLUMN DEFINITION
);
```
4. Submit a pull request to the storage team for approval.
5. Merge the pull request once approved.

## MySQL Prerequisite for DDL scripts 

Following are some important amendments as a prerequisite for submitting PR on expansion script for MySQL instances.

1. For any DDL query a comment attribute must be there for every column that will be created, for e.g. 
```sql
CREATE TABLE FOO (
    `id` INT NOT NULL COMMENT '[NOT-PII]'
);
```
2. For every PII column a person must need to provide what PII column is it, followed by the tag ‘[PII]’, for eg. 
```sql
CREATE TABLE FOO (
    `ip_address` VARCHAR(250) NOT NULL COMMENT '[PII] Linkable PII'
);
```
3. For every non PII column you must add a tag '[NOT-PII]'
```sql
CREATE TABLE FOO (
    `id` INT NOT NULL COMMENT '[NOT-PII]',
    `firstname` VARCHAR(233) NOT NULL COMMENT '[NOT-PII]'
);
```

## Postgre Prerequisite for DDL scripts 

Following are some important amendments as a prerequisite for submitting PR on expansion script for Postgre instances. Comments in Postgre are treated differently. 
1. For any DDL query a comment attribute must be there for every column that will be created, for e.g. 
```sql
CREATE TABLE FOO (
    id INT NOT NULL
);
COMMENT ON COLUMN FOO.id is '[NOT-PII]';
```
2. For every PII column a person must need to provide what PII column is it, followed by the tag ‘[PII]’, for eg. 
```sql
CREATE TABLE FOO (
    ip_address VARCHAR(250) NOT NULL 
);
COMMENT ON COLUMN FOO.ip_address is '[PII] Linkable PII';
```
3. For every non PII column you must add a tag '[NOT-PII]'
```sql
CREATE TABLE FOO (
    id INT NOT NULL,
    firstname VARCHAR(233) NOT NULL
);
COMMENT ON COLUMN FOO.id is '[NOT-PII]';
COMMENT ON COLUMN FOO.firstname is '[NOT-PII]';
```

You can find the details about the data protection program & PII column description over here.
- <a href="#">Data Protection Program</a>
- <a href="#">PII classification</a>

