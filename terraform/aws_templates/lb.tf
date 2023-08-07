# Auto generated alb
{% if 'load_balancers' in network %}
  {% for key, value in network.load_balancers.items() %}
# Generate the ALB
resource "aws_lb" "{{ key }}" {
  name               = "{{ key }}"
  internal           = {{ value.internal | default('false') }}
  load_balancer_type = "{{ value.load_balancer_type | default('application') }}"

  {% if value.subnets %}
  subnets            = [{% for subnet in value.subnets %}aws_subnet.{{ subnet }}.id,{% endfor %}]
  {% endif %}

  security_groups    = {{ value.security_groups | default(['allow_sincity']) | to_terraform_array('aws_security_group', 'id') }}

  enable_deletion_protection = {{ value.enable_deletion_protection | default('false') }}

  {% if value.access_logs %}
  access_logs {
    {{ value.access_logs | to_terraform_json(2, True) | safe }}
  }
  {% endif %}

  {% if value.tags %}
  tags = {
    {{ value.tags | to_terraform_json(2, True) | safe }}
  }
  {% endif %}
}


  {% if 'hosts' in value %}
# Generate the target group
resource "aws_lb_target_group" "{{ key }}" {
  name        = "{{ key }}"
  port        = {{ value.host_port | default(80) }}
  protocol    = "{{ value.host_protocol | default('HTTP') | upper }}"
  vpc_id      = aws_vpc.main_vpc.id
  target_type = "instance"
}

# Attach the target computers
  {% for hostname, value in network.hosts.items() %}
resource "aws_lb_target_group_attachment" "{{ key }}-{{ hostname }}" {
  target_group_arn = aws_lb_target_group.{{ key }}.arn
  target_id        = aws_instance.{{ hostname }}.id
}
  {% endfor %}

# Generate the listener
resource "aws_lb_listener" "{{ key }}" {
  load_balancer_arn = aws_lb.{{ key }}.arn
  port              = {{ value.forward_port | default(80) }}
  protocol          = "{{ value.protocol | default('HTTP') | upper }}"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.{{ key }}.arn
  }
}
  {% endif %}

  {% endfor %}
{% endif %}
# End of auto generated alb