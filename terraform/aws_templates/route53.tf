# Auto generated route53
{% if 'cloud' in network and 'aws' in network.cloud and 'route53' in network.cloud.aws %}
  {% for key, value in network.cloud.aws.route53.items() %}
resource "aws_route53_zone" "{{ key }}" {
  name = "{{ value.name }}"
}

    {% for record_key, record_value in value.records.items() %}
resource "aws_route53_record" "{{ record_key }}" {
  zone_id = aws_route53_zone.{{ key }}.zone_id
  name    = "{{ record_value.name }}"
  type    = "{{ record_value.type | default('A') }}"
  ttl     = {{ record_value.ttl | default(300) }}
  records = {{ record_value.records | tojson }}
}
    {% endfor %}
  {% endfor %}
{% endif %}
# End of auto generated route53