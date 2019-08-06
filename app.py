import re
import json
import boto3

#boto3 library to intreact with AWS services
codecommit = boto3.client('codecommit')
sns = boto3.client('sns')

def lambda_handler(event, context):
     
    #Get the repository details and commit ID
	
    repository = event['Records'][0]['eventSourceARN'].split(':')[5]
    commitId = event['Records'][0]['codecommit']['references'][0]['commit']
	
    try:
        response = codecommit.get_repository(repositoryName=repository)
                
        commitMessage = codecommit.get_commit(
                repositoryName=repository,
                commitId=commitId
                )
                
        commitMsg = commitMessage['commit']['message']
		
		# Regex pattern to find the Jira issue number
		## Have given the below sample where jira issue number might be JIRA-1101
		### Replace the pattern which is relevant to your regex pattern
		
        result = re.search(r"JIRA-\d\d\d\d", commitMsg)
        
		# Replace the topic ARN with the one you had created
		# find the topic ARN by going to SNS -> Topics -> click on the topic which was created for this example
		# find the ARN under the Details tab
		# it will begin with arn:aws:sns:
		# copy and replace that in the below sections instead of REPLACE_WITH_SNS_TOPIC_ARN
		
        if result:
            response = sns.publish(
                TopicArn='REPLACE_WITH_SNS_TOPIC_ARN',
                Message= commitMsg,
                Subject='Code Commit Message Validation Passed',
                MessageStructure='string'
                )
        else:
            response = sns.publish(
                TopicArn='REPLACE_WITH_SNS_TOPIC_ARN',
                Message= commitMsg,
                Subject='Code Commit Message Validation Failed',
                MessageStructure='string'
                )
                
    except Exception as e:
        return('Error')
        raise e