from openai import OpenAI 
import os
import base64
import json

# Path to your JPEG image
image_path = "1.png"

# Open the image in binary mode
with open(image_path, "rb") as image_file:
    # Read the image file and encode it as Base64
    base64_image = base64.b64encode(image_file.read()).decode("utf-8")


instruction = "You are a helpful assistant that Extract all text from the image without missing anything."
prompt = """
#Advance Information 
The input image is part of a customs document.
This includes customer name, order number, product code, unit price, weight, date, etc.

# instructions
Extract all text from the image without missing anything.

# Constraints
However, please be sure to observe the following two points.
- Extract all words and expressions even if they are duplicated in the image.
- Extract in the order they are in the image."""

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("ENDPOINT"),
)

response = client.chat.completions.create(
    model="openai.gpt-4o",
    messages=[
            {"role": "system", "content": instruction},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}",
                            "detail": "auto"
                        },
                    },
                ],
            },
        ],
    )

# Extract the message content (text) from the response
generated_text = response.choices[0].message.content #not using response.choices[0].message['content'] because we cannot use dictionary-style indexing

# Replace "\n" with an actual newline
formatted_content = generated_text.replace("\\n", "\n")

#message_string = json.dumps(formatted_content)  # Convert to JSON string

# Write the generated text to a .txt file
with open("output.txt", "w") as txt_file:
    txt_file.write(formatted_content)

print("Output saved to output.txt")
