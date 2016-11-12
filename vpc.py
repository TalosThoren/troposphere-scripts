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

# Imports from troposphere
from troposphere import Ref
from troposphere import Tags

# EC2 resource classes
from troposphere.ec2 import VPC
from troposphere.ec2 import Subnet
from troposphere.ec2 import RouteTable
from troposphere.ec2 import SubnetRouteTableAssociation

## Add resource functions to add resources to a template object ##
#

def add_vpc( template, key='VPC', name='', cidr_block='172.16.0.0/16' ):
    return template.add_resource(
            VPC(
                key,
                CidrBlock = cidr_block,
                Tags = Tags( Name=name )
                )
            )

def add_subnet( template, key, cidr_block, vpc, name='' ):
    return template.add_resource(
            Subnet(
                key,
                VpcId = Ref( vpc ),
                CidrBlock = cidr_block,
                Tags = Tags( Name=name )
                )
            )

def add_route_table( template, key, vpc, name='' ):
    return template.add_resource(
            RouteTable(
                key,
                VpcId = Ref( vpc ),
                Tags = Tags( Name=name )
                )
            )

def add_route_table_association( template, key, route_table, subnet ):
    return template.add_resource(
            SubnetRouteTableAssociation(
                key,
                RouteTableId = Ref( route_table ),
                SubnetId = Ref( subnet )
                )
            )

def add_eip( template, key ):
    return template.add_resource(
            )

def add_nat_gateway( template, key ):
    return template.add_resource(
            )
#
## End of add resource functions ##
