resource "aws_key_pair" "default" {
  key_name   = local.keypair.name
  public_key = local.keypair.public_key
}


resource "aws_security_group" "allow_sincity" {
  name        = "allow_sincity"
  description = "Allow SinCity lab traffic"
  vpc_id      = aws_vpc.main_vpc.id


  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow the entire subnet to talk on all traffic
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  #   ingress {
  #     description      = "TLS from VPC"
  #     from_port        = 443
  #     to_port          = 443
  #     protocol         = "tcp"
  #     cidr_blocks      = [aws_vpc.main.cidr_block]
  #     ipv6_cidr_blocks = [aws_vpc.main.ipv6_cidr_block]
  #   }

  #   egress {
  #     from_port        = 0
  #     to_port          = 0
  #     protocol         = "-1"
  #     cidr_blocks      = ["0.0.0.0/0"]
  #     ipv6_cidr_blocks = ["::/0"]
  #   }

  tags = merge(
    var.additional_tags,
    {
      Name = "allow_sincity"
  })
}


{% if 'security_groups' in network %}
# Auto generated security groups
  {% for key, value in network.security_groups.items() %}
resource "aws_security_group" "{{ key }}" {
  name        = "{{ key }}"
  description = "{{ value.description | default("") }}"
  vpc_id      = aws_vpc.main_vpc.id

  {% if 'inbound' in network.security_groups[key]  %}
    {% for key, value in network.security_groups[key].inbound.items() %}
  ingress {
    from_port   = {{ value.start_port }}
    to_port     = {{ value.end_port }}
    protocol    = "{{ value.protocol | default("-1") }}"
    cidr_blocks = {{ value.cidr_blocks | tojson }}
  }
    {% endfor %}
  {% endif %}

  {% if 'outbound' in network.security_groups[key]  %}
    {% for key, value in network.security_groups[key].outbound.items() %}
  egress {
    from_port   = {{ value.start_port }}
    to_port     = {{ value.end_port }}
    protocol    = "{{ value.protocol | default("-1") }}"
    cidr_blocks = {{ value.cidr_blocks | tojson }}
  }
    {% endfor %}
  {% endif %}
}
  {% endfor %}
# End auto generated security groups
{% endif %}