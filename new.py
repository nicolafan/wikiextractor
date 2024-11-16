import re


def extract_infobox(page_content):
    # Find the infobox section in the page content
    infobox_start = page_content.find("{{Infobox")
    if infobox_start == -1:
        return None

    # Extract the infobox by finding the matching closing braces
    braces_count = 2  # We start right after "{{"
    infobox_end = infobox_start + 2
    while braces_count > 0 and infobox_end < len(page_content):
        if page_content[infobox_end : infobox_end + 2] == "{{":
            braces_count += 2
            infobox_end += 2
        elif page_content[infobox_end : infobox_end + 2] == "}}":
            braces_count -= 2
            infobox_end += 2
        else:
            infobox_end += 1

    infobox = page_content[infobox_start:infobox_end]
    return infobox


def extract_image_and_caption(infobox):
    fields = [field.strip() for field in infobox.split("\n")]
    fields = [field[1:].strip() if (field and field[0] == "|") else "" for field in fields]
    image = None
    caption = None

    for field in fields:
        if field.startswith("image"):
            image = field.split("=", 1)[-1].strip()
        elif field.startswith("caption"):
            caption = field.split("=", 1)[-1].strip()

    if not image:
        return None, None
    return image, caption


def split_by_first_level_pipes(s):
    substrings = []
    stack = []
    last = ""
    skip_next = False
    for i in range(len(s)):
        if skip_next:
            skip_next = False
            continue
        if s[i] == "{" and len(s) > (i + 1) and s[i + 1] == "{":
            stack.append("{{")
            last += "{{"
            skip_next = True
        elif s[i] == "[" and len(s) > (i + 1) and s[i + 1] == "[":
            stack.append("[[")
            last += "[["
            skip_next = True
        elif s[i] == "[":
            stack.append("[")
            last += "["
        elif s[i] == "}" and len(s) > (i + 1) and s[i + 1] == "}" and stack and stack[-1] == "{{":
            stack.pop()
            last += "}}"
            skip_next = True
        elif s[i] == "]" and len(s) > (i + 1) and s[i + 1] == "]" and stack and stack[-1] == "[[":
            stack.pop()
            last += "]]"
            skip_next = True
        elif s[i] == "]" and stack and stack[-1] == "[":
            stack.pop()
            last += "]"
        elif s[i] == "|" and not stack:
            substrings.append(last)
            last = ""
        else:
            last += s[i]
    substrings.append(last)
    return substrings


s = "Ancient Greek polychromatic [[Ancient Greek vase painting|pottery painting]] (dating to {{circa|300}} BC) of Achilles during the Trojan War"
print(split_by_first_level_pipes(s))