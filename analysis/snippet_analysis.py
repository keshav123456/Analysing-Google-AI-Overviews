# Snippet analysis is used to identify snippets that are not aligned with the title, or the main point of the article, is there selective picking of information?

import json
from openai import OpenAI
import requests
from bs4 import BeautifulSoup

def check_if_text_in_reference(text, references):
    for reference in references:
        if text.lower() in reference["text"].lower():
            if len(text) > 50:
                return (True, reference)
    return (False, {})

def write_to_file(text, reference):
    print(f"Text - {text} found in reference: {reference['source']}")
    result = {
        "text": text,
        "reference_source": reference["source"],
        "reference_link": reference["link"]
    }
    with open('analysed_data/snippet_references.json', 'a') as outfile:
        json.dump(result, outfile, indent=4)
        outfile.write("\n")


with open('dataset/data_with_ai_overview.json', 'r') as file:
    data_with_ai_overview = json.load(file)

    for i, overview in enumerate(data_with_ai_overview):
        print(f"Processing overview {i+1}")
        overview = overview[0]

        references = []
        for reference in overview["ai_overview"]["references"]:
            reference_dict = {}
            try:
                reference_dict["title"] = reference["title"]
                reference_dict["source"] = reference["source"]
                reference_dict["link"] = reference["link"]
                response = requests.get(reference["link"], timeout=1)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    text = soup.get_text()
                    reference_dict["text"] = text
                else:
                    reference_dict["text"] = "Failed to retrieve content"
            except Exception as e:
                reference_dict["text"] = f"Error occurred: {e}"

            references.append(reference_dict)
        
        for text_block in overview["ai_overview"]["text_blocks"]:
            try:
                if text_block["type"] == "paragraph":
                    text = text_block["snippet"]
                    found, reference = check_if_text_in_reference(text, references)
                    if found:
                        write_to_file(text, reference)
                if text_block["type"] == "list":
                    for item in text_block["list"]:
                        if "snippet" in item.keys():
                            text = item["snippet"]
                    found, reference = check_if_text_in_reference(text, references)
                    if found:
                        write_to_file(text, reference)
            except Exception as e:
                print(f"Error occurred: {e}")




        
