# parse task file
data "template_file" "task" {
    template    = "${file("task.json")}"
    vars {
        access_id  = "${var.dynamo_access_id}"
        secret_key = "${var.dynamo_secret_key}"
        domain     = "${var.domain}"
        mail       = "${var.mail}"
        basename   = "${var.basename}"
    }
}

# create task definition
resource "aws_ecs_task_definition" "service" {
    family          = "ssl-app"
    network_mode    = "awsvpc"
    requires_compatibilities = ["FARGATE"]
	cpu             = 256 
	memory          = 512
    execution_role_arn = "arn:aws:iam::324139215624:role/ecsTaskExecutionRole"
    container_definitions = "${data.template_file.task.rendered}"

    tags {
        Name        = "ssl-taskdefs"
        Creator     = "ssl"
        Description = "Task definition for ssl app."
    }
}

# vim:ts=4:sw=4:sts=4:expandtab:syntax=conf
