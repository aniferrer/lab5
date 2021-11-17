#!/usr/bin/env python3
import boto3

def create_table(
        ddb_table_name,
        partition_key,
        sort_key,
        status,
        date
        ):

    dynamodb = boto3.resource('dynamodb')

    # The variables below transform the arguments into the parameters expected by dynamodb.create_table.

    table_name = ddb_table_name
    
    attribute_definitions = [
        {'AttributeName': partition_key, 'AttributeType': 'S'},
        {'AttributeName': sort_key, 'AttributeType': 'S'},
        {'AttributeName': status, 'AttributeType': 'S'},
        {'AttributeName': date, 'AttributeType': 'S'}
        ]
    
    key_schema = [{'AttributeName': partition_key, 'KeyType': 'HASH'}, 
                  {'AttributeName': sort_key, 'KeyType': 'RANGE'}]
                  
    provisioned_throughput = {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 10}
    
    global_secondary_indexes = [{
            'IndexName': 'inverted-index',
            'KeySchema': [
                {'AttributeName': sort_key, 'KeyType': 'HASH'},
                {'AttributeName': partition_key, 'KeyType': 'RANGE'}],
            'Projection': {'ProjectionType': 'ALL'},
            'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 10}
    }, {
            'IndexName': 'pending-index',
            'KeySchema': [
                {'AttributeName': status, 'KeyType': 'HASH'},
                {'AttributeName': partition_key, 'KeyType': 'RANGE'}],
            'Projection': {'ProjectionType': 'ALL'},
            'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 10}
    }]
    
    local_secondary_indexes = [{
            'IndexName': 'status-index',
            'KeySchema': [
                {'AttributeName': partition_key, 'KeyType': 'HASH'},
                {'AttributeName': status, 'KeyType': 'RANGE'}],
            'Projection': {'ProjectionType': 'ALL'}
    }, {
            'IndexName': 'date-index',
            'KeySchema': [
                {'AttributeName': partition_key, 'KeyType': 'HASH'},
                {'AttributeName': date, 'KeyType': 'RANGE'}],
            'Projection': {'ProjectionType': 'ALL'}
    }]
    
    try:
        # Create a DynamoDB table with the parameters provided
        table = dynamodb.create_table(TableName=table_name,
                                      KeySchema=key_schema,
                                      AttributeDefinitions=attribute_definitions,
                                      ProvisionedThroughput=provisioned_throughput,
                                      GlobalSecondaryIndexes=global_secondary_indexes,
                                      LocalSecondaryIndexes=local_secondary_indexes
                                      )
        return table
    except Exception as err:
        print("{0} Table could not be created".format(table_name))
        print("Error message {0}".format(err))

if __name__ == '__main__':
    table = create_table("users-orders-items", "pk", "sk", "status", "date")
