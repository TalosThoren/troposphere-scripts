#   Copyright 2016 David Hayden
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use self file except in compliance with the License.
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
from troposphere import Template

# Imports from local source
import vpc

# Description: Very rough version of a BaseNetwork generator. At present things
# are hardcoded just to get stuff working. Long term goals for generator type
# classes include:
#
# - Parse configuration input from standard config files (standardized on a
# language like yml or hcl)
#
# - Minimize configuration options on generated template files. Prefer files
# that are as static a possible, allowing only required parameters, configurable
# in finished templates. Prefer to set all configuration data as input to the
# generator object.
#
# - Build infrastructure layers conforming to best practices from modular
# resource components. Generator objects should rely on genericized code for
# adding resources, but should enforce standards that work well in AWS.

class BaseNetwork:

    # We'll want these to be accessible throughout
    _vpc_template = Template()
    _BaseNetworkVPC = None

    # Take a template as input and begin configuring it
    def __init__( self, name='BaseNetworkVPC', version='2010-09-09' ):
        # Begin initializing a template
        self._vpc_template.add_version( version )
        # Create VPC
        self._BaseNetworkVPC = vpc.add_vpc( 
                self._vpc_template,
                cidr_block = '172.16.0.0/16',
                name = name
                )
        self.__generate_az_network(
                priv_cidr_block = '172.16.0.0/21',
                pub_cidr_block = '172.16.32.0/22',
                suffix='AZ1'
                )
        self.__generate_az_network(
                priv_cidr_block='172.16.4.0/21',
                pub_cidr_block = '172.16.40.0/22',
                suffix='AZ2'
                )


    # Add an entire set of components for a single AZ to vpc template
    def __generate_az_network( self, priv_cidr_block, pub_cidr_block, suffix ):
        # We could probably build these strings elsewhere
        priv_subnet_name = 'PrivateSubnet' + suffix
        priv_subnet_route_table_name = 'PrivateSubnetRouteTable' + suffix
        priv_subnet_route_table_association_name = 'PrivateRouteTableAssociation' + suffix

        pub_subnet_name = 'PublicSubnet' + suffix
        pub_subnet_route_table_name = 'PublicSubnetRouteTable' + suffix
        pub_subnet_route_table_association_name = 'PublicRouteTableAssociation' + suffix

        # Create private subnet
        PrivateSubnet = vpc.add_subnet(
                template = self._vpc_template,
                key = priv_subnet_name,
                name =  priv_subnet_name,
                cidr_block = priv_cidr_block,
                vpc = self._BaseNetworkVPC
                )

        # Create private subnet Route Table
        PrivateSubnetRouteTable = vpc.add_route_table(
                template = self._vpc_template,
                key = priv_subnet_route_table_name,
                name = priv_subnet_route_table_name, 
                vpc = self._BaseNetworkVPC
                )

        # Create private subnet route table association
        PrivateSubnetRouteTableAssociation = vpc.add_route_table_association(
                template = self._vpc_template,
                key = priv_subnet_route_table_association_name,
                route_table = PrivateSubnetRouteTable,
                subnet = PrivateSubnet 
                )

        # Create public subnet
        PublicSubnet = vpc.add_subnet(
                template = self._vpc_template,
                key = pub_subnet_name,
                name = pub_subnet_name,
                cidr_block = pub_cidr_block,
                vpc = self._BaseNetworkVPC
                )

        # Create public subnet Route Table
        PublicSubnetRouteTable = vpc.add_route_table(
                template = self._vpc_template,
                key = pub_subnet_route_table_name,
                name = pub_subnet_route_table_name,
                vpc = self._BaseNetworkVPC
                )

        # Create private subnet route table association
        PublicSubnetRouteTableAssociation = vpc.add_route_table_association(
                template = self._vpc_template,
                key = pub_subnet_route_table_association_name,
                route_table = PublicSubnetRouteTable,
                subnet = PublicSubnet
                )

    # Let's output the template in json format
    def print_template( self ):
        print( self._vpc_template.to_json() )
