
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

resource "aws_s3_bucket" "terraform" {
  bucket = "terraform-study-meeting" # 任意のバケット名
}

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

resource "aws_lambda_function" "lambda_function" {
  filename      = "${path.module}/source/lambda_function.zip"
  function_name = "notify_aws_cost"  # 任意の関数名に
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.10"
  source_code_hash = filebase64sha256("${path.module}/source/lambda_function.zip")

  environment {
    variables = {
      SNS_TOPIC_ARN = aws_sns_topic.lambda_sns_topic.arn
    }
  }
}

# resource "aws_iam_role" "lambda_exec_role" {
#   name = "lambda_exec_role"

#   assume_role_policy = <<EOF
# {
#   "Version": "2012-10-17",
#   "Statement": [
#     {
#       "Effect": "Allow",
#       "Principal": {
#         "Service": "lambda.amazonaws.com"
#       },
#       "Action": "sts:AssumeRole"
#     }
#   ]
# }
# EOF
# }

# resource "aws_s3_object" "lambda_function_zip" {
#   bucket = aws_s3_bucket.terraform.bucket
#   key    = "lambda/notify_aws_cost.zip"
#   source = "${path.module}/lambda/notify_aws_cost.zip" 
# }

# resource "aws_lambda_permission" "allow_sns" {
#   statement_id  = "AllowExecutionFromSNS"
#   action        = "lambda:InvokeFunction"
#   function_name = aws_lambda_function.lambda_function.function_name
#   principal     = "sns.amazonaws.com"
#   source_arn    = aws_sns_topic.lambda_sns_topic.arn
# }

