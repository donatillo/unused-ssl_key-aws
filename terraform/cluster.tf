resource "aws_ecs_cluster" "cluster" {
    name = "ssl-${var.env}"

    tags {
        Name        = "ssl-cluster"
        Creator     = "ssl"
        Environment = "${var.env}"
        Description = "Cluster for the SSL"
    }
}

# vim:ts=4:sw=4:sts=4:expandtab:syntax=conf
