#!/bin/bash

sudo yum install -y unzip
sudo yum install -y openvpn

sudo mkdir /etc/openvpn/easy-rsa

sudo mv /tmp/server.sh /etc/openvpn/server.sh
sudo mv /tmp/server.conf /etc/openvpn/server.conf

cd /tmp
sudo unzip /tmp/pki.zip
sudo mv /tmp/pki /etc/openvpn/easy-rsa
sudo mv /tmp/pfs.key /etc/openvpn

sudo rm /etc/openvpn/easy-rsa/pki/private/ca.key
