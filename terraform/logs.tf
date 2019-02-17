resource "aws_cloudwatch_log_group" "ssl" {
    name = "ssl-logs-${var.env}"

    tags {
        Name        = "ssl-logs-${var.env}"
        Creator     = "ssl"
        Environment = "${var.env}"
        Description = "Cloudwatch log group for ssl"
    }
}

# vim:ts=4:sw=4:sts=4:expandtab:syntax=conf
