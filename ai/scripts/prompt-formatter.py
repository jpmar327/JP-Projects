import re, glob

def load_framework(path):
    text = open(path, encoding="utf-8").read()
    # split off the YAML frontmatter between the --- markers
    _, frontmatter, body = text.split("---", 2)
    return body.strip()  # this is the ready-to-use system prompt

role_prompt = load_framework("prompt-engineering-framework-claude.md")
# then pass role_prompt as the system prompt to your Claude API call