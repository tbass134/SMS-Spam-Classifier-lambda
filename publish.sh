ZIP_NAME=$1
S3_BUCKET=$2
FUNCTION_NAME=$3

rm $ZIP_NAME
cd lambda
rm *.zip
zip -r $ZIP_NAME *
aws s3 cp $ZIP_NAME s3://$S3_BUCKET/$ZIP_NAME
aws lambda update-function-code --function-name $FUNCTION_NAME --s3-bucket $S3_BUCKET --s3-key $ZIP_NAME --region us-east-1
