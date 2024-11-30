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

# Create a public subnet for frontend
public_subnet1 = aws.ec2.Subnet("todo-app-public-frontend-subnet-1",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    map_public_ip_on_launch=True,
    availability_zone="ap-southeast-1a",
    tags={
        "Name": "todo-app-public-frontend-subnet-1",
    }
)

# Create the second public subnet for backend instance one
public_subnet2 = aws.ec2.Subnet("todo-app-public-backend-subnet-1",
    vpc_id=vpc.id,
    cidr_block="10.0.2.0/24",
    map_public_ip_on_launch=True,
    availability_zone="ap-southeast-1b",
    tags={
        "Name": "todo-app-public-backend-subnet-1",
    }
)

# Create the third public subnet for backend instance two
public_subnet3 = aws.ec2.Subnet("todo-app-public-backend-subnet-2",
    vpc_id=vpc.id,
    cidr_block="10.0.3.0/24",
    map_public_ip_on_launch=True,
    availability_zone="ap-southeast-1c",
    tags={
        "Name": "todo-app-public-backend-subnet-2",
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

# Associate route table with the public subnets
aws.ec2.RouteTableAssociation("todo-app-rt-association-frontend-1",
    subnet_id=public_subnet1.id,
    route_table_id=route_table.id
)

aws.ec2.RouteTableAssociation("todo-app-rt-association-backend-1",
    subnet_id=public_subnet2.id,
    route_table_id=route_table.id
)

aws.ec2.RouteTableAssociation("todo-app-rt-association-backend-2",
    subnet_id=public_subnet3.id,
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

ami_id = "ami-060e277c0d4cce553"

frontend_instance = aws.ec2.Instance("todo-app-frontend-instance-1",
    instance_type="t2.micro",
    ami=ami_id,
    subnet_id=public_subnet1.id,
    vpc_security_group_ids=[security_group.id],
    key_name="MyKeyPair",
    associate_public_ip_address=True,
    tags={"Name": "todo-app-frontend-instance-1"},
)

backend_instance1 = aws.ec2.Instance("todo-app-backend-instance-1",
    instance_type="t2.micro",
    ami=ami_id,
    subnet_id=public_subnet2.id,
    vpc_security_group_ids=[security_group.id],
    key_name="MyKeyPair",
    associate_public_ip_address=True,
    tags={"Name": "todo-app-backend-instance-1"},
)

backend_instance2 = aws.ec2.Instance("todo-app-backend-instance-2",
    instance_type="t2.micro",
    ami=ami_id,
    subnet_id=public_subnet2.id,
    vpc_security_group_ids=[security_group.id],
    key_name="MyKeyPair",
    associate_public_ip_address=True,
    tags={"Name": "todo-app-backend-instance-2"},
)

























