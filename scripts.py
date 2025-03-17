import json 

def simplify_jsonl():
    # Read the original file
    simplified_data = []
    with open('dataset/dev.jsonl', 'r') as file:
        for line in file:
            data = json.loads(line)
            # Keep only question and source
            simplified_data.append({
                'question': data['question'],
                'source': data['source']
            })
    
    # Write the simplified data back
    with open('dataset/data.jsonl', 'w') as file:
        for item in simplified_data:
            json.dump(item, file)
            file.write('\n')

def generate_questions(topics):
    questions = []
    for topic in topics:
        questions.append({"question": f"What is {topic}?", "source": "Current Issues by UMichigan"})
        questions.append({"question": f"Is {topic} good for society?", "source": "Current Issues by UMichigan"})
        questions.append({"question": f"Is {topic} bad for society?", "source": "Current Issues by UMichigan"})
        questions.append({"question": f"What are the benefits of {topic}?", "source": "Current Issues by UMichigan"})
        questions.append({"question": f"What are the drawbacks of {topic}?", "source": "Current Issues by UMichigan"})
    
    with open('dataset/data.jsonl', 'a') as file:
        for question in questions:
            json.dump(question, file)
            file.write('\n')

def generate_leading_questions(topics):
    questions = []
    for topic in topics:
        questions.append({"question": f"Why is {topic} good for society?", "source": "Current Issues by UMichigan"})
        questions.append({"question": f"Why is {topic} bad for society?", "source": "Current Issues by UMichigan"})
    
    with open('dataset/data.jsonl', 'a') as file:
        for question in questions:
            json.dump(question, file)
            file.write('\n')

def modify_leading_questions():
    modified_data = []
    with open('dataset/data.jsonl', 'r') as file:
        for index, line in enumerate(file):
            data = json.loads(line)
            if index >= 3406:
                data['source'] = "Leading questions - Current Issues by UMichigan"
                data['index'] = index
            modified_data.append(data)
    
    with open('dataset/data.jsonl', 'w') as file:
        for item in modified_data:
            json.dump(item, file)
            file.write('\n')

topics = [
    "Affirmative Action",
    "Affordable Care Act",
    "Alternative medicine",
    "Alt-right",
    "America's global influence",
    "Antifa",
    "Artificial intelligence",
    "Assisted suicide",
    "Atheism",
    "Bilingual education",
    "Biofuels",
    "Black Lives Matter",
    "Border security",
    "Capital punishment",
    "Censorship",
    "Charter schools",
    "Childhood obesity",
    "Civil rights",
    "Climate change",
    "Concussions in football",
    "COVID restrictions",
    "Cryptocurrency",
    "Cyber bullying",
    "Cybersecurity",
    "DACA",
    "Drug legalization",
    "Early voting",
    "Eating disorders",
    "Equal Rights Amendment",
    "Executive order",
    "Extremism",
    "Factory farming",
    "Filibuster",
    "Foreign aid",
    "Fracking",
    "Freedom of speech",
    "General Data Protection Regulation",
    "Genetic engineering",
    "Gerrymandering",
    "Green New Deal",
    "Hacking",
    "Hate speech",
    "Health insurance",
    "Human trafficking",
    "Immigration",
    "Israel-Palestine relations",
    "Judicial activism",
    "Labor unions",
    "Land acknowledgments",
    "#MeToo movement",
    "Minimum wage",
    "Misinformation",
    "Net neutrality",
    "Nuclear energy",
    "Offshore drilling",
    "Online anonymity",
    "Organic food",
    "Outsourcing",
    "PFAs",
    "Police reform",
    "Political activism",
    "Prescription drug addiction",
    "QAnon",
    "Racial profiling",
    "Reparations",
    "Russian hacking",
    "Sanctuary city",
    "Screen addiction",
    "Self-driving cars",
    "Sex education",
    "Smart speakers",
    "Social Security reform",
    "Socialism",
    "Standardized testing",
    "Stem cells",
    "Stimulus packages",
    "Supreme Court confirmation",
    "Sweatshops",
    "Syrian civil war",
    "Title IX enforcement",
    "Trade tariffs",
    "Transgender rights",
    "Ukraine and Russia",
    "Urban agriculture",
    "Vaccination mandates",
    "Vaping",
    "Violence in the media",
    "Voter ID laws",
    "Voting fraud and security",
    "White nationalism",
    "Wildfires",
    "Women's rights",
    "Zero tolerance policies"
]


def add_index_to_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    indexed_data = []
    for index, line in enumerate(lines):
        data = json.loads(line)
        data['index'] = index
        indexed_data.append(data)

    with open(file_path, 'w') as file:
        for data in indexed_data:
            file.write(json.dumps(data) + '\n')

data_file_path = 'dataset/data.jsonl'


def read_misformatted_json(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        # Fix the misformatted JSON by adding a comma between the lists
        fixed_content = content.replace('][', '],[')
        return json.loads(fixed_content)

# raw_final_run_data = read_misformatted_json('dataset/raw_final_run.json')
# with_ai_overview = []
# without_ai_overview = []

# for item in raw_final_run_data:
#     if item[0]["ai_overview"] != "No AI overview found":
#         with_ai_overview.append(item)
#     else:
#         without_ai_overview.append(item)

# with open('dataset/data_with_ai_overview.json', 'w') as file:
#     json.dump(with_ai_overview, file, indent=4)

# with open('dataset/data_without_ai_overview.json', 'w') as file:
#     json.dump(without_ai_overview, file, indent=4)
