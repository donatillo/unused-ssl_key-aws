terraform {
    backend "s3" {
        region = "us-east-1"
        key = "ssl.state"
    }
}

# vim:ts=4:sw=4:sts=4:expandtab:syntax=conf
