resource "aws_resourcegroups_group" "resg-ssl" {
    name = "ssl-${var.env}"
    description = "Resources built for the ssl - ${var.env}."
    
    resource_query {
    query = <<JSON
{
  "ResourceTypeFilters": ["AWS::AllSupported"],
  "TagFilters": [
    {
      "Key": "Creator",
      "Values": ["ssl"]
    },
    {
      "Key": "Environment",
      "Values": ["${var.env}"]
    }
  ]
}
JSON
  }
}

# vim:ts=4:sw=4:sts=4:expandtab:syntax=conf
