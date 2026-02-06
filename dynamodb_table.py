import boto3
from botocore.exceptions import ClientError

AWS_REGION = "us-east-1"   # SAME as Flask app

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)

# CREATE USERS TABLE

def create_users_table():
    try:
        table = dynamodb.create_table(
            TableName="cinemy_users",

            KeySchema=[
                {
                    "AttributeName": "email",
                    "KeyType": "HASH"
                }
            ],

            AttributeDefinitions=[
                {
                    "AttributeName": "email",
                    "AttributeType": "S"
                }
            ],

            BillingMode="PAY_PER_REQUEST"   # On-Demand (Best for production)
        )

        table.wait_until_exists()
        print("✅ cinemy_users table created")

    except ClientError as e:
        print("Users Table Error:", e.response["Error"]["Message"])

# CREATE ADMINS TABLE

def create_admins_table():
    try:
        table = dynamodb.create_table(
            TableName="cinemy_admins",

            KeySchema=[
                {
                    "AttributeName": "username",
                    "KeyType": "HASH"
                }
            ],

            AttributeDefinitions=[
                {
                    "AttributeName": "username",
                    "AttributeType": "S"
                }
            ],

            BillingMode="PAY_PER_REQUEST"
        )

        table.wait_until_exists()
        print("✅ cinemy_admins table created")

    except ClientError as e:
        print("Admins Table Error:", e.response["Error"]["Message"])

# CREATE MOVIES TABLE

def create_movies_table():
    try:
        table = dynamodb.create_table(
            TableName="movies",

            KeySchema=[
                {
                    "AttributeName": "name",
                    "KeyType": "HASH"
                }
            ],

            AttributeDefinitions=[
                {
                    "AttributeName": "name",
                    "AttributeType": "S"
                }
            ],

            BillingMode="PAY_PER_REQUEST"
        )

        table.wait_until_exists()
        print("✅ movies table created")

    except ClientError as e:
        print("Movies Table Error:", e.response["Error"]["Message"])

# RUN ALL

if __name__ == "__main__":

    print("🚀 Creating DynamoDB Tables...\n")

    create_users_table()
    create_admins_table()
    create_movies_table()

    print("\n🎯 All Tables Ready For Production")
