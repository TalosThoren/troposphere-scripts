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
from troposphere import Template
import vpc

# Instantiate a template and set the version
template = Template()
template.add_version('2010-09-09')

# Create VPC
BaseNetworkVPC = vpc.add_vpc( 
        template,
        name='BaseNetworkVPC'
        )

# Create private subnet Route Table
PrivateSubnetRT = vpc.add_route_table(
        template = template,
        key = 'PrivateSubnetRT',
        name = 'PrivateSubnetRT',
        vpc = BaseNetworkVPC
        )

# Create private subnet
PrivateSubnet = vpc.add_subnet(
        template = template,
        key = 'PrivateSubnet',
        name = 'PrivateSubnet',
        cidr_block = '172.16.0.0/21',
        vpc = BaseNetworkVPC
        )

# Create private subnet route table association
PrivateSubnetRTAssociation = vpc.add_route_table_association(
        template = template,
        key = 'PrivateSubnetRouteTableAssociation',
        route_table = PrivateSubnetRT,
        subnet = PrivateSubnet 
        )

# Create public subnet Route Table
PublicSubnetRT = vpc.add_route_table(
        template = template,
        key = 'PublicSubnetRT',
        name = 'PublicSubnetRT',
        vpc = BaseNetworkVPC
        )

# Create public subnet
PublicSubnet = vpc.add_subnet(
        template = template,
        key = 'PulicSubnet',
        name = 'PublicSubnet',
        cidr_block = '172.16.32.0/22',
        vpc = BaseNetworkVPC
        )

# Create private subnet route table association
PublicSubnetRTAssociation = vpc.add_route_table_association(
        template = template,
        key = 'PublicSubnetRouteTableAssociation',
        route_table = PublicSubnetRT,
        subnet = PublicSubnet
        )

# Output template
print(template.to_json())
