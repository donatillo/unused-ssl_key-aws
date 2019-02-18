resource "aws_cloudwatch_log_group" "ssl" {
    name = "ssl-logs"

    tags {
        Name        = "ssl-logs"
        Creator     = "ssl"
        Description = "Cloudwatch log group for ssl"
    }
}

# vim:ts=4:sw=4:sts=4:expandtab:syntax=conf
