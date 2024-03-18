with open("test.txt", "r") as file:
    # Đọc nội dung của tệp
    content = file.read()


def extract_text_from_blocks(blocks):
    extracted_text = ""
    for block in blocks:
        lines = block.get("lines", [])
        for line in lines:
            spans = line.get("spans", [])
            for span in spans:
                text = span.get("text", "")
                extracted_text += text + " "
    return extracted_text


your_text = extract_text_from_blocks(content["blocks"])
print(your_text)
