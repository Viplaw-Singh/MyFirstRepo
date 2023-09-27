import boto3
import os
import time

# Initialize the S3 client
s3 = boto3.client('s3')

# Set the S3 bucket name
bucket_name = 'demo-sftp-test-1'

# Set the object key (object name) to just the file name
object_key = 'data100.csv'

# Get the absolute path to the file
file_path = os.path.abspath('data100.csv')

# Record the start time
start_time = time.time()

# Calculate the number of parts you want (e.g., 20 parts)
num_parts = 20

# Get the file size in bytes
file_size = os.path.getsize(file_path)

# Calculate the chunk size based on the number of parts
chunk_size = file_size // num_parts

# Create a new multipart upload
response = s3.create_multipart_upload(Bucket=bucket_name, Key=object_key)
upload_id = response['UploadId']
print(f'Multipart upload initiated with UploadId: {upload_id}')

# Initialize the part number and parts list
part_number = 1
parts = []

# Open and upload chunks of the file
with open(file_path, 'rb') as file:
    while True:
        chunk = file.read(chunk_size)
        if not chunk:
            break

        # Create a temporary chunk file
        temp_chunk_file = f'temp_chunk_{part_number}.csv'
        with open(temp_chunk_file, 'wb') as temp_file:
            temp_file.write(chunk)

        # Upload the chunk as a part
        response = s3.upload_part(
            Bucket=bucket_name,
            Key=object_key,
            PartNumber=part_number,
            UploadId=upload_id,
            Body=chunk
        )

        # Append the part number and ETag to the parts list
        parts.append({'PartNumber': part_number, 'ETag': response['ETag']})
        print(f'Uploaded part {part_number} with ETag: {response["ETag"]}')

        part_number += 1

# Clean up temporary chunk files
for part_number in range(1, part_number):
    temp_chunk_file = f'temp_chunk_{part_number}.csv'
    os.remove(temp_chunk_file)

print('All parts uploaded.')

# Complete the multipart upload
s3.complete_multipart_upload(
    Bucket=bucket_name,
    Key=object_key,
    UploadId=upload_id,
    MultipartUpload={'Parts': parts}
)

# Calculate and display the total time spent
end_time = time.time()
elapsed_time = end_time - start_time
print(f'File uploaded successfully to {bucket_name}/{object_key}')
print(f'Total time spent: {elapsed_time:.2f} seconds')
