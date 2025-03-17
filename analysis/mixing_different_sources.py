# This identifies sources with very different information integrity - for e.g it uses the NYPost articles alongside government sources

import json
from call_openai import call_openai

with open('analysed_data/mixing_different_sources.json', 'r') as file:
    data = json.load(file)

    print(len(data))
        

# with open('dataset/data_with_ai_overview.json', 'r') as file:
#     data_with_ai_overview = json.load(file)

#     for i, overview in enumerate(data_with_ai_overview):
#         print(f"Processing overview {i}")
#         overview = overview[0]
#         try:
#             all_sources = []
#             for reference in overview["ai_overview"]["references"]:
#                 if "wikipedia" not in reference["source"].lower():
#                     title = reference["title"]
#                     source = reference["source"]
#                     link = reference["link"]
#                     all_sources.append({"source": source, "title": title, "link": link})


#             prompt = f"Are there 2 or more sources in {all_sources} that differ GREATLY in their trustworthiness?"
#             prompt += f"the criteria must be exacting, for example, mainstream news organisations, academic organisations, government sources are NOT VERY DIFFERENT in terms of trustworthiness, you should respond with 'no' if you see NYTimes and an academic institution as sources."
#             prompt += f"For example, respond yes if you have a government source alongside a tabloid such as the NYPost, or a social media post you should respond with 'yes'."
#             prompt += f"If they do, return 'yes', else return 'no', followed mandatorily by a short description of which sources differ, max 30 words."

#             answer = call_openai(prompt)    
#             if "yes" in answer[0:10].lower():
#                 differing_sources_entry = {
#                     "question_number": i,
#                     "answer": answer,
#                     "question": overview["search_parameters"]["q"],
#                 }

#                 with open('analysed_data/mixing_different_sources.json', 'a') as outfile:
#                     json.dump(differing_sources_entry, outfile, indent=4)
#                     outfile.write("\n")
#         except KeyError:
#             continue
