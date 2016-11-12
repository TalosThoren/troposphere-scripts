#   Copyright 2016 David Hayden
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

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

def add_route_table_association( key, route_table, subnet ):
    return template.add_resource(
            SubnetRouteTableAssociation(
                key,
                RouteTableId = Ref( route_table ),
                SubnetId = Ref( subnet )
                )
            )

# Create VPC
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

# Create private subnet route table association
PrivateSubnetRTAssociation = add_route_table_association(
        key = 'PrivateSubnetRouteTableAssociation',
        route_table = PrivateSubnetRT,
        subnet = PrivateSubnet 
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

# Create private subnet route table association
PublicSubnetRTAssociation = add_route_table_association(
        key = 'PublicSubnetRouteTableAssociation',
        route_table = PublicSubnetRT,
        subnet = PublicSubnet
        )

# Output template
print(template.to_json())
