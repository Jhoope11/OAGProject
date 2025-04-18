import json
import requests
import os
import csv
from collections import defaultdict
from fuzzywuzzy import process


# Define the path to the single JSON file
single_json_file = "Output/papers_chunk_14/papers_chunk_156.json"  # Replace with the actual path to your JSON file

# Define the output directory for results
output_dir = "results"
os.makedirs(output_dir, exist_ok=True)  # Create the output directory if it doesn't exist

# Define the FieldsOfStudy variable
FieldsOfStudy = [
    "materials science",
    "medicine",
    "chemistry",
    "computer science",
    "biology",
    "mathematics",
    "engineering",
    "physics",
    "environmental science",
    "geology",
    "psychology",
    "business",
    "geography",
    "economics",
    "sociology",
    "political science",
    "history",
    "art",
    "philosophy"
]

# Define the ListOfCountries variable
ListOfCountries = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", 
    "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", 
    "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", 
    "Burkina Faso", "Burundi", "Côte d'Ivoire", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", 
    "Chad", "Chile", "China", "Colombia", "Comoros", "Congo (Congo-Brazzaville)", "Costa Rica", "Croatia", "Cuba", 
    "Cyprus", "Czechia (Czech Republic)", "Democratic Republic of the Congo", "Denmark", "Djibouti", "Dominica", 
    "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", 
    "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", 
    "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", 
    "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", 
    "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", 
    "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", 
    "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", 
    "Myanmar (Burma)", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", 
    "North Korea", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Palestine State", "Panama", "Papua New Guinea", 
    "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", 
    "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", 
    "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", 
    "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", 
    "Syria", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", 
    "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States of America", 
    "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
]

# Convert FieldsOfStudy and ListOfCountries to formatted strings for the prompt
fields_str = ", ".join(FieldsOfStudy)
countries_str = ", ".join(ListOfCountries)

# Initialize data structures for aggregation
field_stats = defaultdict(lambda: {
    "country_counts": defaultdict(int),
    "total_publications": 0,
    "single_authored": 0,
    "domestic_collaborations": 0,
    "international_collaborations": 0
})

# Read the single JSON file
try:
    with open(single_json_file, "r") as file:
        papers_data = json.load(file)
except FileNotFoundError:
    print(f"File not found: {single_json_file}")
    exit()
except json.JSONDecodeError:
    print(f"Invalid JSON format in file: {single_json_file}")
    exit()

# Process each row in the file
for index, journal_data in enumerate(papers_data):
    # Check if required fields are present
    if not all(key in journal_data for key in ["PaperTitle", "Journal", "Year", "Authors", "Keywords"]):
        print(f"Skipping row {index + 1}: Missing required fields.")
        continue

    # Define the Ollama API endpoint
    url = "http://localhost:11434/api/generate"

    # Engineer the prompt
    prompt = f"""
    Based on the following journal information, determine which country should be credited for this publication.
    The field of study must be one of the following: {fields_str}.
    The country must be one of the following: {countries_str}.

    Journal Information:
    - Title: {journal_data.get("PaperTitle", "N/A")}
    - Journal: {journal_data.get("Journal", "N/A")}
    - Year: {journal_data.get("Year", "N/A")}
    - Authors: {', '.join([author.get("Name", "N/A") for author in journal_data.get("Authors", [])])}
    - Keywords: {', '.join(journal_data.get("Keywords", []))}

    Provide **only the country name** as the output. Do not include any explanations or additional text.
    """

    # Prepare the payload
    payload = {
        "model": "deepseek-r1",  # Replace with the correct model name
        "prompt": prompt,
        "stream": False
    }

    # Set the headers
    headers = {
        "Content-Type": "application/json"
    }

    # Send the POST request
    response = requests.post(url, headers=headers, json=payload)

    # Process the response
    if response.status_code == 200:
        result = response.json()
        response_text = result.get("response", "").strip()

        # Extract the country name from the response
        country = None
        for country_name in ListOfCountries:
            if country_name.lower() in response_text.lower():
                country = country_name
                break

        # If no country is found, default to "Unknown"
        if not country:
            print(f"Could not determine country from response: {response_text}. Defaulting to 'Unknown'.")
            country = "Unknown"

        print(f"Row {index + 1}: Country to be credited: {country}")

        # Determine the field of study using fuzzy matching
        keywords = journal_data.get("Keywords", [])
        field_of_study = "Unknown"
        for keyword in keywords:
            match, score = process.extractOne(keyword.lower(), [f.lower() for f in FieldsOfStudy])
            if score >= 80:  # Adjust the threshold as needed
                field_of_study = FieldsOfStudy[[f.lower() for f in FieldsOfStudy].index(match)]
                break

        # Update field statistics
        field_stats[field_of_study]["country_counts"][country] += 1
        field_stats[field_of_study]["total_publications"] += 1

        # Check if the publication is single-authored or collaborative
        num_authors = journal_data.get("NumAuthors", 0)
        if num_authors == 1:
            field_stats[field_of_study]["single_authored"] += 1
        else:
            # Check if the collaboration is domestic or international
            author_countries = set()
            for author in journal_data.get("Authors", []):
                org = author.get("AuthorOrg", "")
                if org:
                    # Extract the country from the organization (assume it's the last part)
                    country_from_org = org.split(",")[-1].strip()
                    if country_from_org in ListOfCountries:
                        author_countries.add(country_from_org)
                else:
                    print(f"Skipping author {author.get('Name', 'N/A')}: Missing 'AuthorOrg'.")
            
            if len(author_countries) == 1:
                field_stats[field_of_study]["domestic_collaborations"] += 1
            elif len(author_countries) > 1:
                field_stats[field_of_study]["international_collaborations"] += 1
            else:
                print(f"Skipping collaboration type determination: No valid countries found in 'AuthorOrg'.")
    else:
        print(f"Row {index + 1}: Failed to get a response:", response.status_code, response.text)

# Generate the additional table file
table_file_path = os.path.join(output_dir, "field_of_study_stats.csv")
with open(table_file_path, "w", newline="") as table_file:
    writer = csv.writer(table_file)
    # Write the header row
    writer.writerow([
        "FieldOfStudy",
        "Country with the most credits",
        "Number of Publications",
        "Single Authored Publications (%)",
        "Domestic Collaborations (%)",
        "International Collaborations (%)"
    ])

    # Initialize totals
    total_stats = {
        "total_publications": 0,
        "single_authored": 0,
        "domestic_collaborations": 0,
        "international_collaborations": 0
    }

    # Write data for each field of study
    for field in FieldsOfStudy:
        stats = field_stats.get(field, {
            "country_counts": defaultdict(int),
            "total_publications": 0,
            "single_authored": 0,
            "domestic_collaborations": 0,
            "international_collaborations": 0
        })

        total_publications = stats["total_publications"]
        single_authored = stats["single_authored"]
        domestic_collaborations = stats["domestic_collaborations"]
        international_collaborations = stats["international_collaborations"]

        # Calculate percentages
        single_authored_pct = (single_authored / total_publications) * 100 if total_publications > 0 else 0
        domestic_collaborations_pct = (domestic_collaborations / total_publications) * 100 if total_publications > 0 else 0
        international_collaborations_pct = (international_collaborations / total_publications) * 100 if total_publications > 0 else 0

        # Find the country with the most credits
        most_credited_country = max(stats["country_counts"], key=stats["country_counts"].get, default="N/A")

        # Write the row
        writer.writerow([
            field,
            most_credited_country,
            total_publications,
            f"{single_authored_pct:.2f}%" if total_publications > 0 else "0.00%",
            f"{domestic_collaborations_pct:.2f}%" if total_publications > 0 else "0.00%",
            f"{international_collaborations_pct:.2f}%" if total_publications > 0 else "0.00%"
        ])

        # Update totals
        total_stats["total_publications"] += total_publications
        total_stats["single_authored"] += single_authored
        total_stats["domestic_collaborations"] += domestic_collaborations
        total_stats["international_collaborations"] += international_collaborations

    # Write the final row with totals
    total_single_authored_pct = (total_stats["single_authored"] / total_stats["total_publications"]) * 100 if total_stats["total_publications"] > 0 else 0
    total_domestic_collaborations_pct = (total_stats["domestic_collaborations"] / total_stats["total_publications"]) * 100 if total_stats["total_publications"] > 0 else 0
    total_international_collaborations_pct = (total_stats["international_collaborations"] / total_stats["total_publications"]) * 100 if total_stats["total_publications"] > 0 else 0

    writer.writerow([
        "All Fields",
        "N/A",
        total_stats["total_publications"],
        f"{total_single_authored_pct:.2f}%",
        f"{total_domestic_collaborations_pct:.2f}%",
        f"{total_international_collaborations_pct:.2f}%"
    ])

print(f"Field of study statistics written to {table_file_path}")