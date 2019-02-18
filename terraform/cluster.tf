resource "aws_ecs_cluster" "cluster" {
    name = "ssl"

    tags {
        Name        = "ssl-cluster"
        Creator     = "ssl"
        Description = "Cluster for the SSL"
    }
}

# vim:ts=4:sw=4:sts=4:expandtab:syntax=conf
