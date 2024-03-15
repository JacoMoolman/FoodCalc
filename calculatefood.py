import base64
import requests
import os
import csv


api_key = 'sk-IINrMcHbh9sddsdfsdssDSFDSTGSDVFDFSDFDFenfhgFN91'

directory = 'e:/Projects/slips/photos'  

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

for filename in os.listdir(directory):
    if filename.lower().endswith(('.jpg', '.jpeg')) and '_done' not in filename.lower():
        image_path = os.path.join(directory, filename)
        base64_image = encode_image(image_path)

        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
              {
                "role": "user",
                "content": [
                  {
                    "type": "text",
                    "text": "Exact the food items from this list and give me a CSV formatted list back with the item and the cost. Just give the list no other text!"
                  },
                  {
                    "type": "image_url",
                    "image_url": {
                      "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                  }
                ]
              }
            ],
            "max_tokens": 300
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        print(f"Raw response for {filename}:")
        print(response.json())
        print()

        try:
            content = response.json()['choices'][0]['message']['content']
            csv_filename = os.path.splitext(filename)[0] + '.csv'
            csv_path = os.path.join(directory, csv_filename)
            with open(csv_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for line in content.split('\n'):
                    if ',' in line:
                        item, cost = line.split(',', 1)
                        item = item.strip().strip('"""')
                        cost = cost.strip()
                        writer.writerow([item, cost])
                    else:
                        print(f"Skipping line: {line}")

            print(f"CSV file created: {csv_filename}")
        except KeyError:
            print(f"Error: 'choices' key not found in the response for {filename}")

        new_image_filename = os.path.splitext(filename)[0] + '_done' + os.path.splitext(filename)[1]
        new_image_path = os.path.join(directory, new_image_filename)
        os.rename(image_path, new_image_path)
        print(f"Image file renamed: {new_image_filename}")

        print()