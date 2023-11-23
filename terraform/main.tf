
terraform {
  required_providers {
    aws = {
        source = "hashicorp/aws"
        version = "> 5.0"
    }
  }
  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "ap-northeast-1"
}

### IaCを体験してみよう(S3バケットの作成)
resource "aws_s3_bucket" "terraform" {
  bucket = "terraform-study-meeting" # 任意のバケット名
}

### IaCを体験してみよう(S3バケットライフサイクルポリシーの作成)
resource "aws_s3_bucket_lifecycle_configuration" "terraform" {
  bucket = aws_s3_bucket.terraform.bucket

  rule {
    id     = "delete a_week"
    status = "Enabled"

    expiration {
      days                         = 7
      expired_object_delete_marker = false
    }

    noncurrent_version_expiration {
      noncurrent_days = 1
    }
  }
}

### lambda関数を作成しよう
resource "aws_lambda_function" "lambda_function" {
  filename      = "${path.module}/source/lambda_function.zip"
  function_name = "notify_aws_cost"  # 任意の関数名に
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.10"
  source_code_hash = filebase64sha256("${path.module}/source/lambda_function.zip")

  environment {
    variables = {
      REGION_NAME = "ap-northeast-1"
      SET_ADDRESS = "hirohero876@gmail.com"
    }
  }
}

### 問題②lambdaの実行ロールを作成しよう
resource "aws_iam_role" "lambda_exec_role" {
  name = "lambda_exec_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

### put
resource "aws_s3_object" "lambda_function_zip" {
  bucket = aws_s3_bucket.terraform.bucket
  key    = "lambda/lambda_function.zip"
  source = "${path.module}/source/lambda_function.zip" 
}

### ses
resource "aws_iam_policy" "ses_policy" {
  name        = "ses_policy"
  description = "SES Policy for Lambda"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ses:SendEmail",
        "ses:SendRawEmail"
      ],
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_ses_policy_attachment" {
  policy_arn = aws_iam_policy.ses_policy.arn
  role       = aws_iam_role.lambda_exec_role.name
}

### cost
resource "aws_iam_policy" "ce_policy" {
  name        = "ce_policy"
  description = "Cost Explorer Policy for Lambda"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ce:GetCostAndUsage"
      ],
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_ce_policy_attachment" {
  policy_arn = aws_iam_policy.ce_policy.arn
  role       = aws_iam_role.lambda_exec_role.name
}