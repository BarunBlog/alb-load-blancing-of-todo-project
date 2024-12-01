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


# Create a private subnet for backend instance 1
private_subnet1 = aws.ec2.Subnet("todo-app-private-backend-subnet-1",
    vpc_id=vpc.id,
    cidr_block="10.0.2.0/24",
    map_public_ip_on_launch=True,
    availability_zone="ap-southeast-1b",
    tags={
        "Name": "todo-app-private-backend-subnet-1",
    }
)


# Create the private subnet for backend instance 2
private_subnet2 = aws.ec2.Subnet("todo-app-private-backend-subnet-2",
    vpc_id=vpc.id,
    cidr_block="10.0.3.0/24",
    map_public_ip_on_launch=True,
    availability_zone="ap-southeast-1c",
    tags={
        "Name": "todo-app-private-backend-subnet-2",
    }
)

# Create an Elastic IP for the NAT Gateway
eip = aws.ec2.Eip("todo-app-nat-eip",
    domain="vpc",
)

# Create the NAT Gateway
nat_gateway = aws.ec2.NatGateway("todo-app-nat-gateway",
    allocation_id=eip.id,
    subnet_id=public_subnet1.id,  # NAT Gateway goes in a public subnet
    tags={
        "Name": "todo-app-nat-gateway",
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

# Route table for private subnets
private_route_table = aws.ec2.RouteTable("todo-app-private-route-table",
    vpc_id=vpc.id,
    routes=[
        {
            "cidr_block": "0.0.0.0/0",
            "nat_gateway_id": nat_gateway.id,
        }
    ],
    tags={
        "Name": "todo-app-private-route-table",
    }
)

# Associate route table with the public subnets
aws.ec2.RouteTableAssociation("todo-app-rt-association-frontend-1",
    subnet_id=public_subnet1.id,
    route_table_id=route_table.id
)

# Associate route tables with private subnets
aws.ec2.RouteTableAssociation("todo-app-rt-association-private-1",
    subnet_id=private_subnet1.id,
    route_table_id=private_route_table.id
)

aws.ec2.RouteTableAssociation("todo-app-rt-association-private-2",
    subnet_id=private_subnet2.id,
    route_table_id=private_route_table.id
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
            from_port=8000,
            to_port=8000,
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

# Security group for load balancer
alb_security_group = aws.ec2.SecurityGroup("todo-app-alb-sg",
    vpc_id=vpc.id,
    description="Allow HTTP",
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=80,
            to_port=80,
            cidr_blocks=["10.0.1.0/24"],  # Allow HTTP from frontend public subnet
        )
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
        "Name": "todo-app-alb-sg",
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
    subnet_id=private_subnet1.id,
    vpc_security_group_ids=[security_group.id],
    key_name="MyKeyPair",
    associate_public_ip_address=False,
    tags={"Name": "todo-app-backend-instance-1"},
)

backend_instance2 = aws.ec2.Instance("todo-app-backend-instance-2",
    instance_type="t2.micro",
    ami=ami_id,
    subnet_id=private_subnet2.id,
    vpc_security_group_ids=[security_group.id],
    key_name="MyKeyPair",
    associate_public_ip_address=False,
    tags={"Name": "todo-app-backend-instance-2"},
)

# Creating Application load balancer
alb = aws.lb.LoadBalancer("todo-app-alb",
    internal=True,
    security_groups=[alb_security_group.id],
    subnets=[private_subnet1.id, private_subnet2.id],
    enable_deletion_protection=False,
    tags={"Name": "todo-app-alb"},
)

# ALB Target Group
target_group = aws.lb.TargetGroup("todo-app-backend-tg",
    port=8000, # port of the backend instance
    protocol="HTTP",
    vpc_id=vpc.id,
    health_check=aws.lb.TargetGroupHealthCheckArgs(
        path="/todo/health/",
        interval=30,
        timeout=10,
        healthy_threshold=3,
        unhealthy_threshold=3,
    ),
    tags={"Name": "todo-app-backend-tg"},
)

# ALB Listener
listener = aws.lb.Listener("todo-app-alb-listener",
    load_balancer_arn=alb.arn,
    port=80,
    protocol="HTTP",
    default_actions=[aws.lb.ListenerDefaultActionArgs(
        type="forward",
        target_group_arn=target_group.arn,
    )],
)

# Register backend instances with the ALB Target Group
backend_attachment1 = aws.lb.TargetGroupAttachment("backend-attachment-1",
    target_group_arn=target_group.arn,
    target_id=backend_instance1.id,
    port=8000,
)

backend_attachment2 = aws.lb.TargetGroupAttachment("backend-attachment-2",
    target_group_arn=target_group.arn,
    target_id=backend_instance2.id,
    port=8000,
)
