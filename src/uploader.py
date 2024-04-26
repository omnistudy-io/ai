# Ignore for now
# This will be used for uploading to mysql so users can quickly upload pdfs and the 
# long process of embedding can happen even after they close the site

# For now User -> Pinecone
# Later User -> SQL -> Pinecone




from google.cloud import storage
import os
import tempfile
import shutil
import mysql.connector

def upload_document_to_database(file_path):
    # Connect to MySQL database
    connection = mysql.connector.connect(
        host="your_mysql_host",
        user="your_mysql_username",
        password="your_mysql_password",
        database="your_database_name"
    )
    
    cursor = connection.cursor()
    
    try:
        # Open the document file
        with open(file_path, 'rb') as file:
            document_data = file.read()
        
        # Upload the document data to MySQL
        cursor.execute("INSERT INTO documents (document_data) VALUES (%s)", (document_data,))
        connection.commit()
        print("Document uploaded successfully!")
    except Exception as e:
        print("Error uploading document:", e)
    finally:
        cursor.close()
        connection.close()

def download_and_upload_document_from_gcs(bucket_name, blob_name):
    # Create a temporary directory to store the downloaded file
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Download the document from GCS
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        file_path = os.path.join(temp_dir, 'temp_document.txt')
        blob.download_to_filename(file_path)
        
        # Upload the document to the database
        upload_document_to_database(file_path)
    except Exception as e:
        print("Error:", e)
    finally:
        # Clean up: delete the temporary directory and its contents
        shutil.rmtree(temp_dir)

# Example usage:
if __name__ == "__main__":
    bucket_name = "your_gcs_bucket_name"
    blob_name = "path/to/your/document.txt"
    download_and_upload_document_from_gcs(bucket_name, blob_name)
