import boto3
import json

sender_email = "hh@gmail.com"
smtp_username = "xxx"
smtp_password = "xxx"
s3 = boto3.client('s3', aws_access_key_id=smtp_username, aws_secret_access_key=smtp_password)

recipients_list = [    
                       'abc@gmail.com',
                       'cc@gmail.com', 
                       'sks@gmail.com', 
                       'dd.com',
                       'sj@yahoo.com', 
                       'kki@gmail.com']

def lambda_handler(event, context):
  
    
   
    

    # Replace this with logic to fetch recipients
   

    #7

   
    current_person= receive_previous()
     # Get the current day in the EST timezone
    
    position = recipients_list.index(current_person)
    if(position>=0 and position < len(recipients_list)): #<7
        latest_receipient= position+1
        if(latest_receipient==len(recipients_list)):
            put_person(recipients_list[0])
            send_email(sender_email, recipients_list[0], smtp_username, smtp_password)
        else:
            put_person(recipients_list[latest_receipient])
            send_email(sender_email, recipients_list[latest_receipient] , smtp_username, smtp_password)
        
           
def receive_previous():
    object_key = 'state.json'
    response = s3.get_object(Bucket='riyaz-cross-buck', Key=object_key)
    json_data = json.loads(response['Body'].read().decode('utf-8'))
    value = json_data.get('key')
    print(value)
    return value          

def put_person(recepient):
    json_data = {'key': recepient}  # Replace this with your JSON data
    object_key = 'state.json'

    # Create an S3 client
   

    # Convert JSON to string
    json_string = json.dumps(json_data, indent=2)

    # Upload the JSON string to S3
    s3.put_object(Body=json_string, Bucket='riyaz-cross-buck', Key=object_key)

def send_email(sender, recipient, smtp_username, smtp_password):
    ses = boto3.client('ses', region_name='ca-central-1', aws_access_key_id=smtp_username, aws_secret_access_key=smtp_password)
    subject = "1110 Warden - Your Cleaning Day"
    body = "Assalamualaikum, Please Clean TOMORROW." + recipient
    # Send the email
    response = ses.send_email(
        Source=sender,
        Destination={
            'ToAddresses': [recipient],
             'CcAddresses': [recipients_list], 
        },
        Message={
            'Subject': {
                'Data': subject,
            },
            'Body': {
                'Text': {
                    'Data': body,
                },
            },
        },
    )
    print(f"Email sent to {recipient}. Message ID: {response['MessageId']}")
