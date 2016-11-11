# Copyright (C) David Hayden 2016
# Description:  Proof of concept, High Availability base network template

# We're only going to be working with a few components
from troposphere import Ref, Template, Tags
from troposphere.ec2 import VPC, Subnet, RouteTable, SubnetRouteTableAssociation

# Instantiate a template and set the version
template = Template()
template.add_version('2010-09-09')

# Add VPC to template
BaseNetwork_VPC = template.add_resource(
        VPC(
            'VPC',
            CidrBlock = '172.16.0.0/16',
            Tags = Tags( Name='BaseNetwork' )
            )
        )

# Create private subnet Route Table
PrivateSubnetRT = template.add_resource(
        RouteTable(
            'PrivateRouteTable',
            VpcId = Ref( BaseNetwork_VPC ),
            Tags = Tags( Name='PrivateRT' )
            )
        )

# Create private subnet
PrivateSubnet = template.add_resource(
        Subnet(
            'PrivateSubnet',
            VpcId = Ref( BaseNetwork_VPC ),
            CidrBlock = '172.16.0.0/21',
            Tags = Tags( Name='PrivateSubnet' )
            )
        )

# Create public subnet Route Table
PublicSubnetRT = template.add_resource(
        RouteTable(
            'PublicRouteTable',
            VpcId = Ref( BaseNetwork_VPC ),
            Tags = Tags( Name='PublicRT' )
            )
        )

# Create public subnet
PublicSubnet = template.add_resource(
        Subnet(
            'PublicSubnet',
            VpcId = Ref( BaseNetwork_VPC ),
            CidrBlock = '172.16.32.0/22',
            Tags = Tags( Name='PublicSubnet' )
            )
        )

# Output template
print(template.to_json())
