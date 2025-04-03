import json
import csv
from collections import Counter

def validate_output():
    """Validate the processed output"""
    with open('formatted_citations.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = list(reader)

    print(f"\nValidation Report ({len(data)} citations)")
    
    # 1. Check source chunk tracking
    chunk_dist = Counter(item['SourceChunk'] for item in data)
    print("\nTop 5 Source Files:")
    for file, count in chunk_dist.most_common(5):
        print(f"{file}: {count} citations")

    # 2. Check DeepSeek usage
    deepseek_calls = 0
    for item in data:
        authors = json.loads(item['Authors'])
        for auth in authors:
            if auth.get('Method') == 'DeepSeek':
                deepseek_calls += 1
    print(f"\nDeepSeek queries: {deepseek_calls} ({deepseek_calls/len(data)*100:.1f}%)")

    # 3. Check country resolution
    countries = Counter()
    for item in data:
        authors = json.loads(item['Authors'])
        for auth in authors:
            countries[auth['AuthCountryISO']] += 1
    print("\nTop 5 Countries:")
    for country, count in countries.most_common(5):
        print(f"{country}: {count} authors")

if __name__ == "__main__":
    validate_output()