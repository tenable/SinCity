resource "aws_vpc" "main_vpc" {
  cidr_block           = local.cloud.aws.vpc_cidr_block
  instance_tenancy     = "default"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = merge(
    var.additional_tags,
    {
      Name = "sincity_vpc"
  })
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main_vpc.id

  tags = merge(
    var.additional_tags,
    {
      Name = "sincity_ig"
  })
}

# Grant the VPC internet access on its main route table
resource "aws_route" "internet_access" {
  route_table_id         = aws_vpc.main_vpc.main_route_table_id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.gw.id
}

resource "aws_route_table" "aws_internet_route_table" {
  vpc_id = aws_vpc.main_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }

  # route {
  #   ipv6_cidr_block        = "::/0"
  #   egress_only_gateway_id = aws_egress_only_internet_gateway.gw.id
  # }

  tags = merge(
    var.additional_tags,
    {
      Name = "sincity_route"
  })
}

{% if 'subnets' in network %}
# Auto generated subnets start
    {% for key, value in network.subnets.items() %}
resource "aws_subnet" "{{ key }}" {
  vpc_id                  = aws_vpc.main_vpc.id
  cidr_block              = "{{ value.address }}"
  map_public_ip_on_launch = true
  {% if 'availability_zone' in value %}availability_zone = "{{ value.availability_zone }}"{% endif %}

  tags = merge(
    var.additional_tags,
    {
      Name = "{{ key }}"
  })
}

resource "aws_route_table_association" "{{ key }}_table_association" {
  subnet_id      = aws_subnet.{{ key }}.id
  route_table_id = aws_route_table.aws_internet_route_table.id
}
    {% endfor %}
# Auto generated subnets end
{% endif %}

# resource "aws_network_interface" "network_interfaces" {
#   count       = length(local.servers)
#   subnet_id   = aws_subnet.subnets[local.servers[count.index].subnet_index].id
#   private_ips = [local.servers[count.index].ip]
#   security_groups = ["allow_sincity"]

#   tags = {
#     Name = "primary_network_interface"
#   }
# }