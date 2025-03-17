from serpapi import GoogleSearch
import json
from datetime import datetime


def extract_AI_overviews(query, index):
    print("Running query: ", index)
    params = {
        "q": query,
        "engine": "google",
        "api_key": "b96afc5a44fe2980d2b2e9fc2499eed8a30047daa277cf163a90555f932de179",
        "hl": "en",
        "gl": "us"
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    try: 
        ai_overview = results["ai_overview"]

        if "page_token" in ai_overview:
            
            params = {
                "engine": "google_ai_overview",
                "page_token": ai_overview["page_token"],
                "api_key": "b96afc5a44fe2980d2b2e9fc2499eed8a30047daa277cf163a90555f932de179"
            }
            search = GoogleSearch(params)
            new_results = search.get_dict()
            ai_overview = new_results["ai_overview"]
            results["ai_overview"] = ai_overview
        
        if "error" in ai_overview:
            results["ai_overview"] = "No AI overview found"
        else:
            print("AI overview found")

    except KeyError:
        print("No AI overview found")
        results["ai_overview"] = "No AI overview found"

    results["index"] = index
    return results

def run_on_data():

    data_file_path = 'dataset/questions.jsonl'
    today_date = datetime.today().strftime('%Y-%m-%d')
    file_path = f'dataset/raw_results_{today_date}.json'

    with open(data_file_path, 'r') as file, open(file_path, 'w') as output_file:
        results = []
        for line in file.readlines()[0:]:
            data = json.loads(line)
            question = data["question"]
            index = data["index"]

            result = extract_AI_overviews(question, index)
            results.append(result)
            json.dump(results, output_file, indent=4)
            results = []


run_on_data()