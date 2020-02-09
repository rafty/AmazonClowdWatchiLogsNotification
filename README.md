# AmazonClowdWatchiLogsNotification

Email the content of AWS CloudWatch Logs event messages.

1. Set variables (terminal)

```bash
$ PROJECTNAME=opstools
$ ROLENAME=logsAlarm
$ LAMBDAUPLOADBUCKETNAME=xxxxxxxxxxxx
$ MAILADDRESS=xxxxx@xxx.xxx
```


2. Upload local artifacts(Lambda)
```bash
$ aws cloudformation package \
    --template-file template.yml \
    --s3-bucket $LAMBDAUPLOADBUCKETNAME \
    --output-template-file packaged.yml
```

3. Deploys the specified AWS CloudFormation template
```bash
$ aws cloudformation deploy \
    --stack-name $PROJECTNAME-$ROLENAME \
    --region ap-northeast-1 \
    --template-file packaged.yml \
    --capabilities CAPABILITY_NAMED_IAM \
    --output text \
    --parameter-overrides \
        NortificationMail=$MAILADDRESS
```