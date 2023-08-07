
{% if 'cloud' in network and 'aws' in network.cloud and 'launch_configurations' in network.cloud.aws %}
## Auto generated launch configurations
    {% for key,value in network.cloud.aws.launch_configurations.items() %}
resource "aws_launch_configuration" "{{ key }}" {
  name          = "{{ key }}"
  image_id      = "{{ value.image_id }}"
  instance_type = "{{ value.instance_type }}"
  user_data_base64 = "{{ value.user_data_base64 }}"
}
    {% endfor %}
## Auto generated launch configurations end
{% endif %}