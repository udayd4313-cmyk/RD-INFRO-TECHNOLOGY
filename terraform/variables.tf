variable "aws_region" { default = "us-east-1" }
variable "ami_id" { description = "Ubuntu AMI for the selected region"; type = string }
variable "instance_type" { default = "t3.small" }
variable "vpc_cidr" { default = "10.0.0.0/16" }
variable "public_subnet_cidr" { default = "10.0.1.0/24" }
variable "admin_cidr_blocks" { type = list(string); description = "Restrict SSH to trusted IPs" }
