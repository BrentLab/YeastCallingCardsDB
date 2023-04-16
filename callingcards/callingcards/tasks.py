
import csv
import io
from django.utils.module_loading import import_string
from django.contrib.auth import get_user_model
from celery import shared_task
from django.db import connection, DatabaseError
from psycopg2 import errors
from django.utils.timezone import now

from ..celery import app

@app.task
def process_upload(data, many_flag, kwargs):
    """
    Function to upload records using a serializer with a request.user
    to determine the uploader field value.
    """
    serializer_class_path = kwargs.pop("serializer_class_path")
    serializer_class = import_string(serializer_class_path)

    user_pk = kwargs.pop("uploader")
    User = get_user_model()
    user = User.objects.get(pk=user_pk)
    kwargs["uploader"] = user

    if many_flag:
        serializer = serializer_class(data=data, many=True)
    else:
        serializer = serializer_class(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save(**kwargs)
    return serializer.data


@shared_task
def upload_csv_postgres_task(file_data, 
                             user_uuid, 
                             table_name, 
                             foreign_key_fields):
    # Read the input CSV file and add the user_uuid to each row
    input_data = io.StringIO(file_data)

    # Create a new StringIO object to store the modified data
    data_file = io.StringIO()
    reader = csv.reader(input_data)
    writer = csv.writer(data_file)

    # Process the header row and add the additional columns
    header = next(reader)

    # Check for foreign key fields and add "_id" to them
    header = [field + '_id' if field in foreign_key_fields
              else field for field in header]

    # append the django managed fields
    header.append('uploader_id')
    header.append('uploadDate')
    header.append('modified')
    writer.writerow(header)

    # Process the remaining rows and add the additional columns to each row
    for row in reader:
        row.append(user_uuid) 
        # Add the current date for uploadDate
        row.append(now().date())
        # Add the current datetime for modified
        row.append(now())
        writer.writerow(row)

    # Reset the data_file cursor to the beginning
    data_file.seek(0)

    # Connect to the database using Django's connection
    conn = connection
    conn.ensure_connection()

    with conn.connection as db_conn:
        try:
            # Load the data using the COPY command
            cursor = db_conn.cursor()

            # Read the header line to get the column names
            header_line = data_file.readline().strip()
            columns = [f'"{col}"' for col in csv.reader([header_line]).__next__()]  # noqa

            copy_command = f"COPY {table_name} ({', '.join(columns)}) FROM STDIN WITH CSV HEADER"  # noqa
            cursor.copy_expert(copy_command, data_file)

            db_conn.commit()

        except (errors.UniqueViolation, errors.ForeignKeyViolation) as err:
            db_conn.rollback()
            error_message = f"Error during CSV upload: {err}"
            if hasattr(err, 'lineno'):
                error_message += f" at line {err.lineno}"
            raise Exception(error_message)

        except DatabaseError as err:
            db_conn.rollback()
            raise Exception(f"Error during CSV upload: {err}")
