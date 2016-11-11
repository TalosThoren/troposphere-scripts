# Copyright (C) David Hayden 2016
# Description:  Proof of concept, High Availability base network template

# We're only going to be working with a few components
from troposphere import Ref, Template, Tags
from troposphere.ec2 import VPC, Subnet, RouteTable, SubnetRouteTableAssociation

# Instantiate a template and set the version
template = Template()
template.add_version('2010-09-09')

def add_vpc( key='VPC', name='', cidr_block='172.16.0.0/16' ):
    return template.add_resource(
            VPC(
                key,
                CidrBlock = cidr_block,
                Tags = Tags( Name=name )
                )
            )

def add_subnet( key, cidr_block, vpc, name='' ):
    return template.add_resource(
            Subnet(
                key,
                VpcId = Ref( vpc ),
                CidrBlock = cidr_block,
                Tags = Tags( Name=name )
                )
            )

def add_route_table( key, vpc, name='' ):
    return template.add_resource(
            RouteTable(
                key,
                VpcId = Ref( vpc ),
                Tags = Tags( Name=name )
                )
            )

BaseNetworkVPC = add_vpc( name='BaseNetworkVPC' )

# Create private subnet Route Table
PrivateSubnetRT = add_route_table(
        key = 'PrivateSubnetRT',
        name = 'PrivateSubnetRT',
        vpc = BaseNetworkVPC
        )

# Create private subnet
PrivateSubnet = add_subnet(
        key = 'PrivateSubnet',
        name = 'PrivateSubnet',
        cidr_block = '172.16.0.0/21',
        vpc = BaseNetworkVPC
        )

# Create public subnet Route Table
PublicSubnetRT = add_route_table(
        key = 'PublicSubnetRT',
        name = 'PublicSubnetRT',
        vpc = BaseNetworkVPC
        )

# Create public subnet
PublicSubnet = add_subnet(
        key = 'PulicSubnet',
        name = 'PublicSubnet',
        cidr_block = '172.16.32.0/22',
        vpc = BaseNetworkVPC
        )

# Output template
print(template.to_json())
