#!/usr/bin/env python3

import boto3
import sys
import time

OPTIONS = ['list', 'start', 'stop']
REGIONS = ['us-east-1', 'us-east-2', 'us-west-1', 'us-west-2', 'af-south-1', 'ap-east-1', 'ap-south-1', 'ap-northeast-2', 'ap-southeast-1', 'ap-southeast-2', 'ap-northeast-1', 'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'eu-south-1', 'eu-west-3', 'eu-north-1', 'me-south-1', 'sa-east-1']

if len(sys.argv) < 3 or sys.argv[1].lower() not in REGIONS or sys.argv[2].lower() not in OPTIONS:
	sys.stderr.write('Options: <REGION> {0}\n'.format(','.join(OPTIONS)))
	sys.stderr.write('Regions: {0}\n'.format(','.join(REGIONS)))
	sys.exit(1)

region = sys.argv[1].lower()
option = sys.argv[2].lower()

if option == 'start' or option == 'stop':
	try:
		vpn_name = sys.argv[3]
	except:
		sys.stderr.write('Specify vpn name\n')
		sys.exit(1)


ec2 = boto3.client('ec2', region_name=region)

nextToken = ""
instances = {}

def getName(instance):
	tags = instance.get('Tags', [])
	for tag in tags:
		if tag['Key'] == 'Name': return tag['Value']
	return ""

def getId(instance):
	return instance.get("InstanceId", "")

def getState(instance):
	return instance.get('State', {}).get('Name', '')

def monitor(instance, desired_state, timeout=300):
	t = 0
	state = ""
	while t < timeout:
		res = ec2.describe_instances(InstanceIds=[instance])
		reservations = res.get('Reservations', [])
		for reservation in reservations:
			for i in reservation.get('Instances', []):
				state = getState(i)
				print("Instance state: {0}. time={1}s".format(state, t))
				if state == desired_state:
					print("Instance state reached desired state - {0}. Instance state: {1}".format(desired_state, state))
					return
		t += 5
		time.sleep(5)
	sys.stderr.write("Instance state failed to reach desired state - {0}. Instance state: {1}\n".format(desired_state, state))


while True:
	res = ec2.describe_instances(NextToken=nextToken)
	reservations = res.get('Reservations', [])
	for reservation in reservations:
		for instance in reservation.get('Instances', []):
			instances[getName(instance)] = { 'id': getId(instance), 'state': getState(instance)}

	if 'NextToken' not in res: break
	nextToken = res['NextToken']


if option == 'list':
	for k,v in instances.items():
		print("VPN Name: {0} -> ID: {1}, state: {2}".format(k,v['id'], v['state']))
elif option == 'start':
	ec2.start_instances(InstanceIds=[instances[vpn_name]['id']])
	monitor(instances[vpn_name]['id'], desired_state = "running")
else:
	ec2.stop_instances(InstanceIds=[instances[vpn_name]['id']])
	monitor(instances[vpn_name]['id'], desired_state = "stopped")
