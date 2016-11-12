# Troposphere Script Collection

## Description

This repository serves as a place to store and distribute scripts for building
out bits of infrastructure using troposphere. At present, this is just a small
proof of concept. I'm working now to create a modular VPC manufacturer. Of
course we're talking about generating CloudFormation (CFN) templates as our
output, but a goal is to automate the deployment of segments of infrastructure
without needing to store or think very much about generated templates.

## Progress

The current code has been tested on AWS. The current draft needs some
changes to be considered complete:

- A NAT Gateway and associated EIP should be created in the public subnet.
- An Internet gateway needs to be created and associated with the VPC
- Public route table needs an entry to allow communication through the
  internet gateway
- Private route table needs an entry to allow communication to the NAT
  gateways

