output "vpn_server" {
  value = "${aws_instance.vpn}"
}

output "vpn_country" {
  value = "${var.country}"
}

output "vpn_ip" {
  value = "${aws_eip.vpn.public_ip}"
}

output "vpn_dns" {
  value = "${aws_eip.vpn.public_dns}"
}
