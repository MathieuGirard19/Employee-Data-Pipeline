from faker import Faker
import random
import string
import csv
import pandas as pd
from google.cloud import storage

num_employees = 100
fake = Faker()
employee_data = []
password_characters = string.ascii_letters + string.digits + 'm'

with open('employee_data.csv', mode='w', newline='') as file:
    fieldnames = ['first_name', 'last_name', 'job_title', 'department', 'email', 
        'address', 'phone_number', 'salary', 'password']

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    for _ in range(num_employees):
        writer.writerow({
            "first_name": fake.first_name().replace(',', '').replace('\n', ' '),
            "last_name": fake.last_name().replace(',', '').replace('\n', ' '),
            "job_title": fake.job().replace(',', '').replace('\n', ' '),
            "department": fake.job().replace(',', '').replace('\n', ' '),
            "email": fake.email().replace(',', '').replace('\n', ' '),
            "address": fake.address().replace(',', '').replace('\n', ' '),
            "phone_number": fake.phone_number().replace(',', '').replace('\n', ' '),
            "salary": str(fake.random_number(digits=5)),
            "password": ''.join(random.choice(password_characters) for _ in range(8)).replace(',', '').replace('\n', ' ')
        })

def upload_to_gcs(project, bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client(project)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(f'File {source_file_name} uploaded to {destination_blob_name} in {bucket_name}.')

project='etl-project-464719'
bucket_name = 'etl-project-bkt-employee-data'
source_file_name = 'employee_data.csv'
destination_blob_name = 'employee_data.csv'

upload_to_gcs(project, bucket_name, source_file_name, destination_blob_name)