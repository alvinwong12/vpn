resource "aws_instance" "vpn" {
  ami             = "ami-0915e09cc7ceee3ab"
  instance_type   = "t2.micro"
  key_name        = "${aws_key_pair.vpn.key_name}"
  security_groups = ["${aws_security_group.vpn.name}"]

  tags = {
    Name = "vpn-${var.country}"
  }

  connection {
    type        = "ssh"
    user        = "ec2-user"
    agent       = false
    private_key = file("~/.ssh/vpn.pem")
    host        = "${self.public_ip}"
  }

  provisioner "file" {
    content     = "${data.template_file.server_conf.rendered}"
    destination = "/tmp/server.conf"
  }

  provisioner "file" {
    source      = "${path.module}/scripts/server.sh"
    destination = "/tmp/server.sh"
  }

  provisioner "file" {
    source      = "${path.cwd}/vpn_config/pki.zip"
    destination = "/tmp/pki.zip"
  }

  provisioner "file" {
    source      = "${path.cwd}/vpn_config/pfs.key"
    destination = "/tmp/pfs.key"
  }

  provisioner "remote-exec" {
    scripts = [
      "${path.module}/scripts/install.sh",
      "${path.module}/scripts/ip_forward.sh",
      "${path.module}/scripts/start.sh"
    ]
  }

}

resource "aws_key_pair" "vpn" {
  key_name   = "vpn-${var.country}"
  public_key = file("~/.ssh/vpn.pub")
}

resource "aws_security_group" "vpn" {
  name        = "vpn-${var.country}"
  description = "Security group for VPN in ${var.country}"

  tags = {
    Name = "vpn-${var.country}"
  }

  ingress {
    description = "SSH to VPN - ${var.country} Server"
    protocol    = "tcp"
    from_port   = 22
    to_port     = 22
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "OpenVPN IPv4"
    protocol    = "udp"
    from_port   = 1194
    to_port     = 1194
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description      = "OpenVPN IPv6"
    protocol         = "udp"
    from_port        = 1194
    to_port          = 1194
    ipv6_cidr_blocks = ["::/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_eip" "vpn" {
  vpc      = true
  instance = "${aws_instance.vpn.id}"
  tags = {
    Name = "vpn-${var.country}"
  }
}
