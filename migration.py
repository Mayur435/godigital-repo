import boto3
import csv
import pymysql
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def read_from_s3(bucket_name, file_key):
    s3 = boto3.client('s3')
    try:
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        data = response['Body'].read().decode('utf-8').splitlines()
        reader = csv.DictReader(data)
        return list(reader)
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f"Credentials error: {e}")
        return None
    except Exception as e:
        print(f"Failed to read from S3: {e}")
        return None

def push_to_rds(data, rds_config):
    try:
        connection = pymysql.connect(
            host=rds_config['host'],
            user=rds_config['user'],
            password=rds_config['password'],
            db=rds_config['database']
        )
        with connection.cursor() as cursor:
            sql = "INSERT INTO employee (empid, empname, empaddress) VALUES (%s, %s, %s)"
            for record in data:
                cursor.execute(sql, (record['empid'], record['empname'], record['empaddress']))
        connection.commit()
        connection.close()
        return True
    except Exception as e:
        print(f"Failed to push to RDS: {e}")
        return False

def main():
    # Example configuration
    bucket_name = 'app1-project1'
    file_key = 'employee.csv'
    rds_config = {
        'host': 'demo-rds-database.czmwwqkugo8a.us-east-1.rds.amazonaws.com',
        'user': 'root',
        'password': 'root123456',
        'database': 'employeedb'
    }

    data = read_from_s3(bucket_name, file_key)
    glue_config": {
            'database': 'employeedbe',
            'table': 'employee',
            'location': 'lambdaMigrationFunction'

    data = read_from_s3(bucket_name, file_key)
    if data:
        if not push_to_rds(data, rds_config):
            push_to_glue(data, glue_config)

if __name__ == "__main__":
    main()

