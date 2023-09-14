import boto3


def lambda_handler(event, context):
    source_bucket = 'demo-training-csw'  # Replace with your source S3 bucket name
    source_key = 'my_encrypted.txt'  # Replace with the path of your input text file in the bucket

    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=source_bucket, Key=source_key)    

    var_input = event["p_even_odd"]

    if var_input == "odd":
    
        lines = response['Body'].read().decode('utf-8').split('\n')
        odd_lines = [line for i, line in enumerate(lines) if i % 2 == 0]
        

        return {
            'statusCode': 200,
            'texto_lineas': odd_lines,
            'type_lines': var_input
        }
    
    if var_input == "even":

        lines = response['Body'].read().decode('utf-8').split('\n')
        even_lines = [line for i, line in enumerate(lines) if i % 2 != 0]
        

        return {
            'statusCode': 200,
            'texto_lineas': even_lines,
            'type_lines': var_input
        }