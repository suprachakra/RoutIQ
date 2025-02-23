# main.tf
# IaC for cloud provisioning of networking, compute, and storage resources.
# This example is configured for AWS.

provider "aws" {
  region = var.aws_region
}

# Create a VPC for the application.
resource "aws_vpc" "fleet_vpc" {
  cidr_block = var.vpc_cidr
  enable_dns_support = true
  enable_dns_hostnames = true
  tags = {
    Name = "fleet-optimization-vpc"
  }
}

# Create public subnets.
resource "aws_subnet" "public_subnet" {
  count             = length(var.public_subnet_cidrs)
  vpc_id            = aws_vpc.fleet_vpc.id
  cidr_block        = var.public_subnet_cidrs[count.index]
  availability_zone = var.availability_zones[count.index]
  map_public_ip_on_launch = true
  tags = {
    Name = "public-subnet-${count.index + 1}"
  }
}

# Create an Internet Gateway.
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.fleet_vpc.id
  tags = {
    Name = "fleet-igw"
  }
}

# Create a Route Table for the public subnets.
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.fleet_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
  tags = {
    Name = "public-rt"
  }
}

# Associate the route table with the public subnets.
resource "aws_route_table_association" "public_rt_assoc" {
  count          = length(var.public_subnet_cidrs)
  subnet_id      = aws_subnet.public_subnet[count.index].id
  route_table_id = aws_route_table.public_rt.id
}

# Provision an EC2 instance as an example application server.
resource "aws_instance" "app_server" {
  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = aws_subnet.public_subnet[0].id
  key_name      = var.key_pair
  tags = {
    Name = "fleet-app-server"
  }
}

output "vpc_id" {
  value = aws_vpc.fleet_vpc.id
}
