resource "aws_cloudwatch_metric_alarm" "vpn" {
  alarm_name          = "vpn-${var.country}-inactivity"
  comparison_operator = "LessThanOrEqualToThreshold"
  evaluation_periods  = 2
  metric_name         = "NetworkIn"
  namespace           = "AWS/EC2"
  period              = 900
  statistic           = "Average"
  threshold           = 100000
  alarm_description   = "Stop VPN Server upon inactivity"
  unit                = "Bytes"
  alarm_actions       = ["arn:aws:automate:${var.region}:ec2:stop"]
  ok_actions          = []
  dimensions = {
    InstanceId = "${aws_instance.vpn.id}"
  }
}
