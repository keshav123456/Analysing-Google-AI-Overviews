# Leading questions looks at whether the tilt of the question is leading to a different answer for the AI overview VS traditional search

import json
from call_openai import call_openai

def construct_text_block(data):
    full_Text = ""
    for text_block in data:
        if text_block["type"] == "paragraph":
            full_Text += text_block["snippet"]
            full_Text += "\n"
        if text_block["type"] == "list":
            for item in text_block["list"]:
                if "title" in item.keys():
                    full_Text += item["title"]
                    full_Text += "\n"  
                if "snippet" in item.keys():
                    full_Text += item["snippet"]
                    full_Text += "\n"
    return full_Text


def compare_traditional_sources(q1, q2):
    similar_sources = 0
    q2_links = [reference["link"] for reference in q2]
    for reference in q1:
        if reference["link"] in q2_links:
            similar_sources += 1
    return similar_sources

with open('dataset/data_with_ai_overview.json', 'r') as file:
    data_with_ai_overview = json.load(file)

    questions = {}
    for i, overview in enumerate(data_with_ai_overview):
        question = overview[0]["search_parameters"]["q"]
        questions[question.lower()] = i
    
    leading_questions = []
    for question in questions.keys():
        if "why " + question in questions.keys():
            leading_questions.append([questions[question], questions["why " + question]])
    
    print(len(leading_questions))
    for i, pair_of_questions in enumerate(leading_questions):
        text_block1 = construct_text_block(data_with_ai_overview[pair_of_questions[0]][0]["ai_overview"]["text_blocks"])
        text_block2 = construct_text_block(data_with_ai_overview[pair_of_questions[1]][0]["ai_overview"]["text_blocks"])
        
        similar_sources = compare_traditional_sources(data_with_ai_overview[pair_of_questions[0]][0]["organic_results"], data_with_ai_overview[pair_of_questions[1]][0]["organic_results"])
        answer = call_openai(f"Does the text block '{text_block1}' significantly differ to the text block '{text_block2}'? If it does, return yes, else return no.")
        print("processing question: ", i)
        if "yes" in answer.lower():

            leading_question_difference = {
                "question_1": data_with_ai_overview[pair_of_questions[0]][0]['search_parameters']['q'],
                "text_block_1": text_block1,
                "question_2": data_with_ai_overview[pair_of_questions[1]][0]['search_parameters']['q'],
                "text_block_2": text_block2,
                "difference": answer,
                "similar_sources": similar_sources
            }
            
            with open('analysed_data/leading_questions_and_differences.json', 'a') as outfile:
                json.dump(leading_question_difference, outfile, indent=4)
                outfile.write("\n")

with open('analysed_data/leading_questions_and_differences.json', 'r') as file:
    data = json.load(file)
    print(len(data))

    no_difference_count = 0
    for item in data:
        if "no" in item["difference"].lower():
            no_difference_count += 1
    print(no_difference_count)
