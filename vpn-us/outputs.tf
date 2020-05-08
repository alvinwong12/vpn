output "vpn" {
  value = "${module.vpn.vpn_server}"
}

output "vpn_ip" {
  value = "${module.vpn.vpn_ip}"
}

output "vpn_dns" {
  value = "${module.vpn.vpn_dns}"
}

output "country" {
  value = "${module.vpn.vpn_country}"
}
