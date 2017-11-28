import boto3
import zipfile
import StringIO
from botocore.client import Config
import mimetypes

def lambda_handler(event, context):

    sns = boto3.resource('sns')    
    topic = sns.Topic('arn:aws:sns:us-east-1:758566139275:PortfolioDeployed')
    
    location = {
        "bucketName": 'portfoliobuild.ambient.services',
        "objectKey": 'portfoliobuild.zip'
    }

    try:
        job = event.get("CodePipeline.job")
        if job:
            for artifact in job["data"]["inputArtifacts"]:
                if artifact["name"] == "MyAppBuild":
                    location = artifact["location"]["s3Location"]
        print "Building from " + str(location)
        
        s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))
        portfolio_bucket = s3.Bucket('portfolio.ambient.services')
        build_bucket = s3.Bucket(location["bucketName"])
    
        portfolio_zip = StringIO.StringIO()
        build_bucket.download_fileobj(location["objectKey"], portfolio_zip)
    
        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                portfolio_bucket.upload_fileobj(obj, nm, ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
                portfolio_bucket.Object(nm).Acl().put(ACL='public-read')
                
        print "Site Deployed"
        topic.publish(Subject='Portfolio Deployment', Message='Portfolio deployed successfully')
        if job:
            codepipeline = boto3.client("codepipeline")
            codepipeline.put_job_success_result(jobId=job["id"])
            
    except:
        print "Deployment Failed"
        topic.publish(Subject='Portfolio Deployment', Message='Portfolio deployment failed')
        raise
    
    return 'Site Deployed'
