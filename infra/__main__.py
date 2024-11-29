"""A Python Pulumi program"""
import pulumi
import pulumi_aws as aws


# Configurations
config = pulumi.Config()
region = aws.config.region

# Create a VPC
vpc = aws.ec2.Vpc("my-vpc",
    cidr_block="10.0.0.0/16",
    enable_dns_support=True,
    enable_dns_hostnames=True,
    tags={
        "Name": "todo-app-vpc",
    }
)

# Create a public subnet
public_subnet = aws.ec2.Subnet("todo-app-public-subnet",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    map_public_ip_on_launch=True,
    tags={
        "Name": "todo-app-public-subnet",
    }
)

# Create an Internet Gateway
internet_gateway = aws.ec2.InternetGateway("todo-app-igw",
    vpc_id=vpc.id,
    tags={
        "Name": "todo-app-igw",
    }
)

# Create a routing table
route_table = aws.ec2.RouteTable("todo-app-route-table",
    vpc_id=vpc.id,
    routes=[
        {
            "cidr_block": "0.0.0.0/0", # Default route to the internet
            "gateway_id": internet_gateway.id,
        }
    ],
    tags={
        "Name": "todo-app-route-table",
    }
)

# Associate route table with the public subnet
route_table_association = aws.ec2.RouteTableAssociation("todo-app-rt-association",
    subnet_id=public_subnet.id,
    route_table_id=route_table.id
)

# Security Group
security_group = aws.ec2.SecurityGroup("todo-app-sg",
    vpc_id=vpc.id,
    description="Allow HTTP and SSH",
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=80,
            to_port=80,
            cidr_blocks=["0.0.0.0/0"],  # Allow HTTP from anywhere
        ),
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=22,
            to_port=22,
            cidr_blocks=["0.0.0.0/0"],  # Allow SSH from anywhere
        ),
    ],
    egress=[
        aws.ec2.SecurityGroupEgressArgs(
            protocol="-1",
            from_port=0,
            to_port=0,
            cidr_blocks=["0.0.0.0/0"],  # Allow all outbound traffic
        ),
    ],
    tags={
        "Name": "todo-app-sg",
    }
)

# Creating the ec2 instances
instances = []
number_of_instances = 2
ami_id = "ami-060e277c0d4cce553"

for i in range(number_of_instances):
    instance = aws.ec2.Instance(f"todo-app-instance-{i}",
        instance_type="t2.micro",
        ami=ami_id,
        subnet_id=public_subnet.id,
        vpc_security_group_ids=[security_group.id],
        key_name="MyKeyPair",
        associate_public_ip_address=True,
        tags={"Name": f"todo-app-instance-{i}"},
    )

    instances.append(instance)


























