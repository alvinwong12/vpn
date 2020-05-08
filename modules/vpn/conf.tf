data "template_file" "server_conf" {
  template = "${file("${path.module}/conf/server.conf")}"
  vars = {
    dns_option1 = "push \"dhcp-option DNS ${var.dns1}\"",
    dns_option2 = "${var.dns2 == "" ? "" : "push \"dhcp-option DNS ${var.dns2}\""}"
  }
}