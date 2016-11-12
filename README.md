# Troposphere Script Collection

## Usage

For now you can only really do one thing:

```
python ./test.py
```

This will output a CloudFormation (CFN) template which you can redirect into a
.template file. 

```
python ./test.py > BaseNetwork.template
```

Caveat: This proof of concept is more about learning to generate templates using
troposphere and is very immature. Changes are needed to make the generated
template more useful. Continue reading for detail.

## Description

This repository serves as a place to store and distribute scripts for building
out bits of infrastructure using troposphere. At present, this is just a small
proof of concept. I'm working now to create a modular VPC manufacturer. Of
course we're talking about generating CloudFormation (CFN) templates as our
output, but a goal is to automate the deployment of segments of infrastructure
without needing to store or think very much about generated templates.

## Progress and Status of BaseNetwork

The current code has been tested on AWS. The current draft needs some
changes to be considered complete:

- A NAT Gateway and associated EIP should be created in the public subnet.
- An Internet gateway needs to be created and associated with the VPC
- Public route table needs an entry to allow communication through the
  internet gateway
- Private route table needs an entry to allow communication to the NAT
  gateways

## Next Steps

Proof of concept phase is considered complete at this point. No more code
changes will occur without design steps. Among the questions to answer before
making further changes are:

- What are the exact configuration settings required to set up a correctly
  implemented HA VPC?
- How do we implement configurable input for the minimum required (and optional)
  configuration settings that we identify?
- Can we implement template generators that inherit from the template class and
  are there facilities in place for easing the input of configuring settings?

The BaseNetwork class as it is written is very much non-modular, and it is still
missing the pieces described above (NAT Gateways, EIPs, Route Table entries, and
associations.)

We also need to ensure that each set of public/private subnet pairs are built in
their own availablility zone. That is to say PrivateSubnetAZ1/PublicSubnetAZ1
are in the same AZ and PrivateSubnetAZ2/PublicSubnetAZ2 are in a separate AZ (or
else HA fails when one AZ goes down.) This probably should be handled by a
helper function.
