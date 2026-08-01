terraform {
  required_version = ">= 1.6.0"
  required_providers { aws = { source = "hashicorp/aws", version = "~> 5.0" } }
}
provider "aws" { region = var.aws_region }

data "aws_availability_zones" "available" { state = "available" }
resource "aws_vpc" "main" { cidr_block = var.vpc_cidr; enable_dns_hostnames = true; tags = {Name = "student-api-vpc"} }
resource "aws_subnet" "public" { vpc_id = aws_vpc.main.id; cidr_block = var.public_subnet_cidr; availability_zone = data.aws_availability_zones.available.names[0]; map_public_ip_on_launch = true; tags = {Name = "student-api-public"} }
resource "aws_internet_gateway" "main" { vpc_id = aws_vpc.main.id }
resource "aws_route_table" "public" { vpc_id = aws_vpc.main.id; route {cidr_block = "0.0.0.0/0"; gateway_id = aws_internet_gateway.main.id} }
resource "aws_route_table_association" "public" { subnet_id = aws_subnet.public.id; route_table_id = aws_route_table.public.id }
resource "aws_security_group" "app" { name = "student-api-sg"; vpc_id = aws_vpc.main.id; ingress {from_port=22; to_port=22; protocol="tcp"; cidr_blocks=var.admin_cidr_blocks}; ingress {from_port=80; to_port=80; protocol="tcp"; cidr_blocks=["0.0.0.0/0"]}; egress {from_port=0; to_port=0; protocol="-1"; cidr_blocks=["0.0.0.0/0"]} }
resource "aws_iam_role" "ec2" { name = "student-api-ec2-role"; assume_role_policy = jsonencode({Version="2012-10-17", Statement=[{Effect="Allow", Principal={Service="ec2.amazonaws.com"}, Action="sts:AssumeRole"}]}) }
resource "aws_iam_instance_profile" "ec2" { name = "student-api-ec2-profile"; role = aws_iam_role.ec2.name }
resource "aws_instance" "app" { ami=var.ami_id; instance_type=var.instance_type; subnet_id=aws_subnet.public.id; vpc_security_group_ids=[aws_security_group.app.id]; iam_instance_profile=aws_iam_instance_profile.ec2.name; tags={Name="student-api-host"} }
