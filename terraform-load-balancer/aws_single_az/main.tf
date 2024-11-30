# main.tf
provider "aws" {
  region = "us-west-2"  # specify your desired region
}

resource "aws_instance" "server-A" {
  count = 4
  ami = "ami-0aa7af122f4c85ca1"
  instance_market_options {
    market_type = "spot"
    spot_options {
      max_price = 0.01
    }
  }
  instance_type = "t4g.micro"
  vpc_security_group_ids = ["sg-0fb3cf99924149dd3"]
  tags = {
    Name = "Server-A-${count.index}"
  }
  user_data = <<-EOF
    #!/bin/bash
    echo '172.31.1.1' | sudo tee /home/ec2-user/ip.info
    EOF
}

resource "aws_instance" "cluster-load-balancer-A" {
  ami = "ami-0a5c6629f3228fb08"
  instance_type = "t4g.nano"
  vpc_security_group_ids = ["sg-0e0077397807cf0fe"]
  subnet_id = "subnet-092c80b5b1b449e69"
  private_ip = "172.31.1.1"
  tags = {
    Name = "Load-Balancer-A"
  }
}

resource "aws_instance" "server-B" {
  count = 4
  ami = "ami-001b153068473d76c"
  instance_market_options {
    market_type = "spot"
    spot_options {
      max_price = 0.01
    }
  }
  instance_type = "t4g.micro"
  vpc_security_group_ids = ["sg-0fb3cf99924149dd3"]
  tags = {
    Name = "Server-B-${count.index}"
  }
  user_data = <<-EOF
    #!/bin/bash
    echo '172.31.2.1' | sudo tee /home/ec2-user/ip.info
    EOF
}

resource "aws_instance" "cluster-load-balancer-B" {
  ami = "ami-0a5c6629f3228fb08"
  instance_type = "t4g.nano"
  vpc_security_group_ids = ["sg-0e0077397807cf0fe"]
  subnet_id = "subnet-092c80b5b1b449e69"
  private_ip = "172.31.2.1"
  tags = {
    Name = "Load-Balancer-B"
  }
}


