import json
import requests
import os
import csv
from collections import defaultdict
from fuzzywuzzy import process
import TimeTracker
import maintable
import ColabCalc
# Define the base directory
base_dir = "output"

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

# Loop through all chunk folders and files
for chunk_x in os.listdir(base_dir):
    chunk_dir = os.path.join(base_dir, chunk_x)
    if os.path.isdir(chunk_dir):  # Ensure it's a directory
        # Process each JSON file in the chunk folder
        for chunk_y_file in os.listdir(chunk_dir):
            if chunk_y_file.endswith(".json"):  # Process only JSON files
                file_path = os.path.join(chunk_dir, chunk_y_file)

                # Read the JSON file
                try:
                    with open(file_path, "r") as file:
                        papers_data = json.load(file)
                except FileNotFoundError:
                    print(f"File not found: {file_path}")
                    continue
                except json.JSONDecodeError:
                    print(f"Invalid JSON format in file: {file_path}")
                    continue

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
                    Based on the following journal information, determine which country or countries should be credited for this publication. 
                    Every author should have a country credited for them at the end of the program.
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

                        print(f"File: {file_path}, Row {index + 1}: Country to be credited: {country}")

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
                        print(f"File: {file_path}, Row {index + 1}: Failed to get a response:", response.status_code, response.text)

