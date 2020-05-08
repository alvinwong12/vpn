module "vpn" {
  source = "../modules/vpn"

  country = "${var.country}"

  dns1 = "${var.dns1}"
  dns2 = "${var.dns2}"
}

