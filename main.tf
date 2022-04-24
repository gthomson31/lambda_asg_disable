data "archive_file" "lambda_asg_rescale" {
  type = "zip"

  source_dir  = "${path.module}/lambda_code"
  output_path = "${path.module}/lambda_asg_rescale.zip"
}

resource "aws_s3_object" "lambda_asg_rescale" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "lambda_asg_rescale.zip"
  source = data.archive_file.lambda_asg_rescale.output_path

  etag = filemd5(data.archive_file.lambda_asg_rescale.output_path)
}
