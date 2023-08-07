{% if 'storage' in network %}
## Auto generated s3 buckets
  {% for key,value in network.storage.items() %}
resource "aws_s3_bucket" "{{ key }}" {
    bucket = "{{ key }}"
}

  {% if value.access_type and value.access_type == 'public' %}
resource "aws_s3_bucket_acl" "{{ key }}" {
  bucket = aws_s3_bucket.{{ key }}.id
  acl    = "public-read"
}
  {% endif %}

    {% if 'policies' in value %}
        {% for policy in value.policies %}
resource "aws_s3_bucket_policy" "{{ policy }}" {
  bucket = aws_s3_bucket.{{ key }}.id
  policy = aws_iam_policy.{{ policy }}.arn
}
        {% endfor %}
    {% endif %}

    {% if 'files' in value %}
        {% for file_key,file_value in value.files.items() %}
resource "aws_s3_object" "{{ file_key }}" {
  bucket = aws_s3_bucket.{{ key }}.id
  key    = "{{ file_value.path | default(file_key) }}"

  {% if 'source' in file_value %}
  source = "{{ file_value.source }}"
  {% endif %}

  {% if 'blob' in file_value %}
  content = "{{ file_value.blob }}"
  {% endif %}

  {% if 'blob_base64' in file_value %}
  content_base64 = "{{ file_value.blob_base64 }}"
  {% endif %}
}
        {% endfor %}
    {% endif %}

    {% if value.public %}
      resource "aws_s3_bucket_public_access_block" "{{ key }}" {
        bucket = aws_s3_bucket.{{ key }}.id

        block_public_acls       = false
        block_public_policy     = false
      }
    {% endif %}
  {% endfor %}
## Auto generation ended
{% endif %}