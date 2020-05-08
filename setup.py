#!/usr/bin/env python3

import os
import subprocess
import sys

# This script is used to generate server or client certificates
OPTIONS = ['init', 'client', 'server', 'ovpn']
if len(sys.argv) == 1 or sys.argv[1].lower() not in OPTIONS:
	sys.stderr.write('Options: {0}\n'.format(','.join(OPTIONS)))
	sys.exit(1)

option = sys.argv[1].lower()
client_name , vpn_ip = '', ''

if option == 'client' or option == 'ovpn':
	try:
		client_name = sys.argv[2]
	except:
		sys.stderr.write('Specify client name\n')
		sys.exit(1)

folder = os.path.join(os.getcwd(), "vpn_config")

# Check if initialized
if not os.path.isdir(os.path.join(folder, 'pki')) and option != 'init':
	sys.stderr.write("Missing 'pki' folder. Run 'init' to initialize\n")
	sys.exit(1)

if (not os.path.isfile(os.path.join(folder, '{0}.key'.format(client_name))) or not os.path.isfile(os.path.join(folder, '{0}.crt'.format(client_name)))) and option == 'ovpn':
	sys.stderr.write("Missing '{0}.key' or '{0}.crt'\n".format(client_name))
	sys.exit(1)

if option == 'ovpn':
	try:
		p = subprocess.Popen(('terraform', 'output'), stdout=subprocess.PIPE)
		o = subprocess.check_output(('grep', 'vpn_ip'), stdin=p.stdout).decode('utf-8')
		vpn_ip = o.split('=')[1].strip()
	except:
		sys.stderr.write("VPN Server has not been provisioned yet. Please run 'terraform apply' to provision the VPN server\n".format(client_name))
		sys.exit(1)

SETUP_INIT_STEPS = [
	"sudo easyrsa init-pki",
	"sudo easyrsa build-ca",
	"sudo easyrsa gen-dh",
	"openvpn --genkey --secret pfs.key"
]

SETUP_SERVER_STEPS = [
	"sudo easyrsa gen-req server nopass",
	"sudo easyrsa sign-req server server",
]

SETUP_CLIENT_STEPS = [
	"sudo easyrsa gen-req {0} nopass".format(client_name),
	"sudo easyrsa sign-req client {0}".format(client_name)
]

SETUP_OVPN_STEPS = [
	"cp {0} {1}".format(os.path.join(os.getcwd(), '../modules/vpn/ovpn/vpn.ovpn'), os.path.join(os.getcwd(), "../modules/vpn/ovpn/{0}.ovpn".format(client_name))),
	"sed -i {2} s/<VPN_IP>/{0}/ {1}".format(vpn_ip, os.path.join(os.getcwd(), '../modules/vpn/ovpn/{0}.ovpn'.format(client_name)), ''),
	"sed -i {2} s/<CLIENT_NAME>/{0}/ {1}".format(client_name, os.path.join(os.getcwd(), "../modules/vpn/ovpn/{0}.ovpn".format(client_name)), ''),
	"mv {0} {1}".format(os.path.join(os.getcwd(), '../modules/vpn/ovpn/{0}.ovpn'.format(client_name)), folder),
	"sudo chmod -R +r {0}".format(folder),
	"sudo zip -v {0}.zip {0}.crt {0}.key ca.crt {0}.ovpn pfs.key".format(client_name),
	"rm -f {0}".format(os.path.join(os.getcwd(), "../modules/vpn/ovpn/{0}.ovpn".format(client_name)))
]

if option== 'client':
	steps = SETUP_CLIENT_STEPS
elif option == 'server':
	steps = SETUP_SERVER_STEPS
elif option == 'ovpn':
	steps = SETUP_OVPN_STEPS
else:
	steps = SETUP_INIT_STEPS

try:
	os.mkdir(folder)
except:
	pass

os.chdir(folder)

for step in steps:
	print("Executing '{0}'".format(step))
	subprocess.run(step.split(' '))

# Move necessary files out of pki folder for packaging .ovpn in the future
if option == 'server':
	try:
		subprocess.run(['zip', '-vr', 'pki.zip', './pki'])
		subprocess.run(['sudo', 'cp' , "{0}".format(os.path.join(folder, 'pki', 'ca.crt')), "{0}".format(os.path.join(folder, 'ca.crt'))])
	except Exception as e:
		sys.stderr.write(str(e)+'\n')
		sys.exit(1)
elif option == 'client':
	try:
		os.replace(os.path.join(folder, 'pki', 'private', '{0}.key'.format(client_name)), os.path.join(folder, "{0}.key".format(client_name)))
		os.replace(os.path.join(folder, 'pki', 'issued', '{0}.crt'.format(client_name)), os.path.join(folder, "{0}.crt".format(client_name)))
	except Exception as e:
		sys.stderr.write(str(e) + '\n')
		sys.exit(1)
elif option == 'ovpn':
	sys.stdout.write("'{0}.ovpn' has been generated under '{1}'\n".format(client_name, folder))
else:
	sys.stdout.write("Initialize completed. Please do not remove 'pki' folder\n")
