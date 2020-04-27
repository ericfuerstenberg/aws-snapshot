# aws-snapshot

Tool to manage AWS EC2 instances, volumes, and snapshots

## About

This tool uses Python and boto3 to manage AWS EC2 instances, volumes, and snaphsots.

## Configuring

aws-snapshot uses the configuration file created by the AWS cli. e.g.,

`aws configure --profile aws-snapshot`

## Running

`pipenv run python snapshot/snapshot.py <command> <subcommand> <--project=PROJECT>"`

*command* is instances, volume, or snapshots

*subcommand* depends on command

*project* is optional
