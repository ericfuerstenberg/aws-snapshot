import boto3
import click

session = boto3.Session(profile_name='aws-snapshot')
ec2 = session.resource('ec2')

@click.command()
def list_instances():
	"List EC2 instances"
	for i in ec2.instances.all():
		print(', '.join((
			i.id,
			i.instance_type,
			i.placement['AvailabilityZone'],
			i.state['Name'],
			i.public_dns_name)))
	return


if __name__ == '__main__':
	list_instances()




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

