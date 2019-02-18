resource "aws_cloudwatch_event_rule" "runtask" {
    name        = "update_ssl_cert"
    description = "Update the SSL certificate."
    schedule_expression = "rate(2 days)"
}

resource "aws_cloudwatch_event_target" "runtask" {
    target_id = "update_ssl_certificate"
    arn       = "${aws_ecs_cluster.cluster.arn}"
    rule      = "${aws_cloudwatch_event_rule.runtask.name}"
    role_arn  = "arn:aws:iam::324139215624:role/ecsTaskExecutionRole"

    ecs_target = {
        launch_type         = "FARGATE"
        task_count          = 1
        task_definition_arn = "${aws_ecs_task_definition.service.arn}"
        network_configuration {
            subnets          = [
                "${data.aws_subnet.public_a.id}",
                "${data.aws_subnet.public_b.id}"
            ]
            security_groups  = ["${aws_security_group.allow_outbound.id}"]
            assign_public_ip = true
        }
        platform_version     = "LATEST"
    }
}

# vim:ts=4:sw=4:sts=4:expandtab:syntax=conf
