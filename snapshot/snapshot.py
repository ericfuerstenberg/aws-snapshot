import boto3
import botocore
import click

session = boto3.Session(profile_name='aws-snapshot')
ec2 = session.resource('ec2')

# Creating a function to filter our instances before executing any individual command
def filter_instances(project):
	instances = []

	if project:
		filters = [{'Name': 'tag:project', 'Values':[project]}]
		instances = ec2.instances.filter(Filters=filters)
	else:
		instances = ec2.instances.all()	
	
	return instances


@click.group()
def cli():
	"""aws-snapshot manages snapshots"""

@cli.group('snapshots')
def snapshots():
	"""Commands for snapshots"""

@snapshots.command('list')
@click.option('--project', default=None,
	help="Only snapshots for project")
def list_snapshots(project):
	"List EC2 snapshots"

	instances = filter_instances(project)

	for i in instances:
		for v in i.volumes.all():
			for s in v.snapshots.all():
				print(", ".join((
					s.id,
					v.id,
					i.id,
					s.start_time.strftime("%c"),
					s.progress,
					s.state
				)))
	return

@cli.group('volumes')
def volumes():
	"""Commands for volumes"""

@volumes.command('list')
@click.option('--project', default=None,
	help="Only volumes for project")
def list_volumes(project):
	"List EC2 volumes"

	instances = filter_instances(project)

	for i in instances:
		for v in i.volumes.all():
			print(", ".join((
				v.id,
				i.id,
				v.state,
				str(v.size) + "GiB",
				v.encrypted and "Encrypted" or "Not Encrypted"
			)))
	return

@cli.group('instances')
def instances():
	"""Commands for instances"""

@instances.command('snapshot',
	help="Create snapshots of all volumes")
@click.option('--project', default=None,
	help="Only instances for project (tag project:<name>)")
def create_snapshots(project):
	"Create snapshots for EC2 instances"

	instances = filter_instances(project)

	for i in instances: 
		print("Stopping {0}... ".format(i.id))
		
		i.stop()
		i.wait_until_stopped()
		
		for v in i.volumes.all():
			print("Creating snapshot of volume {0} ".format(v.id))
			v.create_snapshot(Description="Created by aws-snapshot automation")
		
		print("Starting {0}... ".format(i.id))
		
		i.start()
		i.wait_until_running()
	
	print("Snapshots completed!")

	return

# Defines our CLI commands - "list"
@instances.command('list')
@click.option('--project', default=None,
	help="Only instances for project (tag project:<name>)")
def list_instances(project):
	"List EC2 instances"
	
	instances = filter_instances(project)

	for i in instances:
		tags = { t['Key']: t['Value'] for t in i.tags or [] }
		print(', '.join((
			i.id,
			i.instance_type,
			i.placement['AvailabilityZone'],
			i.state['Name'],
			i.public_dns_name,
			tags.get('project', '<no project>')
			)))
	return

# Defines our CLI commands - "stop"
@instances.command('stop')
@click.option('--project', default=None,
	help="Only instances for project")
def stop_instances(project):
	"Stop EC2 instances"

	instances = filter_instances(project)

	for i in instances:
		print("Stopping {0}... ".format(i.id))
		try:
			i.stop()
		except botocore.exceptions.ClientError as e:
			print("ERROR: Could not stop {0}. ".format(i.id) + str(e))
			continue
	
	return

# Defines our CLI commands - "start"
@instances.command('start')
@click.option('--project', default=None,
	help="Only instances for project")
def start_instances(project):
	"Start EC2 instances"

	instances = filter_instances(project)

	for i in instances:
		print("Starting {0}... ".format(i.id))
		try:
			i.start()
		except botocore.exceptions.ClientError as e:
			print("ERROR: Could not start {0}. ".format(i.id) + str(e))
			continue
	
	return



if __name__ == '__main__':
	cli()


# What features do we want?
# What are the nouns and verbs our scripts will handle? 
# Nouns: instances, volumes, snapshots
# Verbs: take snapshot of instance, list instances, start and stop instances, add tags

# snapshot list instances
# snapshot instances list

#snapshot snapshot instances
#snapshot instances snapshot
#snapshot instances create-snapshots
#snapshot volumes list
#snapshot instances stop tag=Project:project_tag
#snapshot start instances --project=project_tag
#snapshot instances stop

