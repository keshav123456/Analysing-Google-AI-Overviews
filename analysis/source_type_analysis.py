# Source analysis
import json

with open('dataset/data_with_ai_overview.json', 'r') as file:
    data_with_ai_overview = json.load(file)

with open('dataset/data_without_ai_overview.json', 'r') as file:
    data_without_ai_overview = json.load(file)

total_count_with = len(data_with_ai_overview)
total_count_without = len(data_without_ai_overview)
total_count = total_count_with + total_count_without

print(f"Total count with AI overview: {total_count_with}")
print(f"Total count without AI overview: {total_count_without}")
print(f"Total count: {total_count}")
print(f"Percentage of AI overview: {total_count_with / total_count * 100}%")

def analyze_sources(data, domain, domain2="zzzzzzzzzzz"):
    with open(data, 'r') as file:
        data = json.load(file)
    total_ai_sources = 0
    domain_ai_sources = 0
    total_sources = 0
    domain_sources = 0
    domain_ai_index = 0
    domain_index = 0
    ai_overview_count = 0
    common_sources = 0

    for item in data:
        if item[0]["ai_overview"] != "No AI overview found":
            ai_overview = item[0]["ai_overview"]
            organic_links = [result["link"] for result in item[0]["organic_results"]]
            ai_overview_count += 1
            try:
                for source in ai_overview["references"]:
                    if domain in source["link"] or domain2 in source["link"]:
                        domain_ai_sources += 1
                        domain_ai_index += source['index']
                    total_ai_sources += 1
                    if source["link"] in organic_links:
                        common_sources += 1
            except:
                pass
            organic_results = item[0]["organic_results"]
            try:
                for result in organic_results:
                    if domain in result["link"] or domain2 in result["link"]:
                        domain_sources += 1
                        domain_index += result['position']
                    total_sources += 1
            except:
                pass

    avg_domain_position = domain_index / domain_sources
    avg_domain_ai_position = domain_ai_index / domain_ai_sources
    avg_ai_sources_per_overview = total_ai_sources / ai_overview_count if ai_overview_count > 0 else 0
    percent_common_sources = common_sources / total_ai_sources * 100
    
    print(f"Average number of AI sources per overview: {avg_ai_sources_per_overview:.2f}")
    print(f"Percentage of common sources: {percent_common_sources:.2f}%")
    
    from prettytable import PrettyTable

    table = PrettyTable()
    table.field_names = ["Metric", "Value"]
    table.add_row([f"% of {domain} sources:", f"{domain_sources/total_sources*100:.2f}%"])
    table.add_row([f"% of {domain} AI sources:", f"{domain_ai_sources/total_ai_sources*100:.2f}%"])
    table.add_row([f"Average position of {domain} sources:", f"{avg_domain_position:.2f}"])
    table.add_row([f"Average position of {domain} AI sources:", f"{avg_domain_ai_position:.2f}"])

    print(table)


# Run the analysis for different domains
analyze_sources("dataset/data_with_ai_overview.json", ".gov")
print(f"{'-'*60}")
analyze_sources("dataset/data_with_ai_overview.json", ".org")
print(f"{'-'*60}")
analyze_sources("dataset/data_with_ai_overview.json", ".edu", ".ac.uk")
print(f"{'-'*60}")
analyze_sources("dataset/data_with_ai_overview.json", "wikipedia")