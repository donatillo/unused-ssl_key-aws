resource "aws_ecr_repository" "repository" {
    name = "ssl-${var.env}"

    tags {
        Name        = "ssl-repository"
        Creator     = "ssl"
        Environment = "${var.env}"
        Description = "Repository containing docker images for the ssl service."
    }
}

# vim:ts=4:sw=4:sts=4:expandtab:syntax=conf
