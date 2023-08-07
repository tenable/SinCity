import re


def remove_extra_spaces(text: str) -> str:
    # Remove multiple lines
    cleaned_text = re.sub(r'\n{2,}(\n)?', '\n\n', text)

    # Remove lines with spaces
    cleaned_text = re.sub(r'\n +\n', '\n\n', cleaned_text)

    # Remove empty spaces
    # cleaned_text = re.sub(r'\n +\n', '', text)
    return cleaned_text.strip()
