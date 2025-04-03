import json
import os
import requests
import time
from collections import defaultdict
from fuzzywuzzy import process
from TimeTracker import track_citation_metrics, write_metrics_to_file

country_to_iso = {
    "Andorra": "AD",
    "United Arab Emirates": "AE",
    "Afghanistan": "AF",
    "Antigua and Barbuda": "AG",
    "Anguilla": "AI",
    "Albania": "AL",
    "Armenia": "AM",
    "Angola": "AO",
    "Antarctica": "AQ",
    "Argentina": "AR",
    "American Samoa": "AS",
    "Austria": "AT",
    "Australia": "AU",
    "Aruba": "AW",
    "Åland Islands": "AX",
    "Azerbaijan": "AZ",
    "Bosnia and Herzegovina": "BA",
    "Barbados": "BB",
    "Bangladesh": "BD",
    "Belgium": "BE",
    "Burkina Faso": "BF",
    "Bulgaria": "BG",
    "Bahrain": "BH",
    "Burundi": "BI",
    "Benin": "BJ",
    "Saint Barthélemy": "BL",
    "Bermuda": "BM",
    "Brunei Darussalam": "BN",
    "Bolivia, Plurinational State of": "BO",
    "Bonaire, Sint Eustatius and Saba": "BQ",
    "Brazil": "BR",
    "Bahamas": "BS",
    "Bhutan": "BT",
    "Bouvet Island": "BV",
    "Botswana": "BW",
    "Belarus": "BY",
    "Belize": "BZ",
    "Canada": "CA",
    "Cocos (Keeling) Islands": "CC",
    "Congo, Democratic Republic of the": "CD",
    "Central African Republic": "CF",
    "Congo": "CG",
    "Switzerland": "CH",
    "Côte d'Ivoire": "CI",
    "Cook Islands": "CK",
    "Chile": "CL",
    "Cameroon": "CM",
    "China": "CN",
    "Colombia": "CO",
    "Costa Rica": "CR",
    "Cuba": "CU",
    "Cabo Verde": "CV",
    "Curaçao": "CW",
    "Christmas Island": "CX",
    "Cyprus": "CY",
    "Czechia": "CZ",
    "Germany": "DE",
    "Djibouti": "DJ",
    "Denmark": "DK",
    "Dominica": "DM",
    "Dominican Republic": "DO",
    "Algeria": "DZ",
    "Ecuador": "EC",
    "Estonia": "EE",
    "Egypt": "EG",
    "Western Sahara": "EH",
    "Eritrea": "ER",
    "Spain": "ES",
    "Ethiopia": "ET",
    "Finland": "FI",
    "Fiji": "FJ",
    "Falkland Islands (Malvinas)": "FK",
    "Micronesia, Federated States of": "FM",
    "Faroe Islands": "FO",
    "France": "FR",
    "Gabon": "GA",
    "United Kingdom of Great Britain and Northern Ireland": "GB",
    "Grenada": "GD",
    "Georgia": "GE",
    "French Guiana": "GF",
    "Guernsey": "GG",
    "Ghana": "GH",
    "Gibraltar": "GI",
    "Greenland": "GL",
    "Gambia": "GM",
    "Guinea": "GN",
    "Guadeloupe": "GP",
    "Equatorial Guinea": "GQ",
    "Greece": "GR",
    "South Georgia and the South Sandwich Islands": "GS",
    "Guatemala": "GT",
    "Guam": "GU",
    "Guinea-Bissau": "GW",
    "Guyana": "GY",
    "Hong Kong": "HK",
    "Heard Island and McDonald Islands": "HM",
    "Honduras": "HN",
    "Croatia": "HR",
    "Haiti": "HT",
    "Hungary": "HU",
    "Indonesia": "ID",
    "Ireland": "IE",
    "Israel": "IL",
    "Isle of Man": "IM",
    "India": "IN",
    "British Indian Ocean Territory": "IO",
    "Iraq": "IQ",
    "Iran, Islamic Republic of": "IR",
    "Iceland": "IS",
    "Italy": "IT",
    "Jersey": "JE",
    "Jamaica": "JM",
    "Jordan": "JO",
    "Japan": "JP",
    "Kenya": "KE",
    "Kyrgyzstan": "KG",
    "Cambodia": "KH",
    "Kiribati": "KI",
    "Comoros": "KM",
    "Saint Kitts and Nevis": "KN",
    "Korea, Democratic People's Republic of": "KP",
    "Korea, Republic of": "KR",
    "Kuwait": "KW",
    "Cayman Islands": "KY",
    "Kazakhstan": "KZ",
    "Lao People's Democratic Republic": "LA",
    "Lebanon": "LB",
    "Saint Lucia": "LC",
    "Liechtenstein": "LI",
    "Sri Lanka": "LK",
    "Liberia": "LR",
    "Lesotho": "LS",
    "Lithuania": "LT",
    "Luxembourg": "LU",
    "Latvia": "LV",
    "Libya": "LY",
    "Morocco": "MA",
    "Monaco": "MC",
    "Moldova, Republic of": "MD",
    "Montenegro": "ME",
    "Saint Martin (French part)": "MF",
    "Madagascar": "MG",
    "Marshall Islands": "MH",
    "North Macedonia": "MK",
    "Mali": "ML",
    "Myanmar": "MM",
    "Mongolia": "MN",
    "Macao": "MO",
    "Northern Mariana Islands": "MP",
    "Martinique": "MQ",
    "Mauritania": "MR",
    "Montserrat": "MS",
    "Malta": "MT",
    "Mauritius": "MU",
    "Maldives": "MV",
    "Malawi": "MW",
    "Mexico": "MX",
    "Malaysia": "MY",
    "Mozambique": "MZ",
    "Namibia": "NA",
    "New Caledonia": "NC",
    "Niger": "NE",
    "Norfolk Island": "NF",
    "Nigeria": "NG",
    "Nicaragua": "NI",
    "Netherlands, Kingdom of the": "NL",
    "Norway": "NO",
    "Nepal": "NP",
    "Nauru": "NR",
    "Niue": "NU",
    "New Zealand": "NZ",
    "Oman": "OM",
    "Panama": "PA",
    "Peru": "PE",
    "French Polynesia": "PF",
    "Papua New Guinea": "PG",
    "Philippines": "PH",
    "Pakistan": "PK",
    "Poland": "PL",
    "Saint Pierre and Miquelon": "PM",
    "Pitcairn": "PN",
    "Puerto Rico": "PR",
    "Palestine, State of": "PS",
    "Portugal": "PT",
    "Palau": "PW",
    "Paraguay": "PY",
    "Qatar": "QA",
    "Réunion": "RE",
    "Romania": "RO",
    "Serbia": "RS",
    "Russian Federation": "RU",
    "Rwanda": "RW",
    "Saudi Arabia": "SA",
    "Solomon Islands": "SB",
    "Seychelles": "SC",
    "Sudan": "SD",
    "Sweden": "SE",
    "Singapore": "SG",
    "Saint Helena, Ascension and Tristan da Cunha": "SH",
    "Slovenia": "SI",
    "Svalbard and Jan Mayen": "SJ",
    "Slovakia": "SK",
    "Sierra Leone": "SL",
    "San Marino": "SM",
    "Senegal": "SN",
    "Somalia": "SO",
    "Suriname": "SR",
    "South Sudan": "SS",
    "Sao Tome and Principe": "ST",
    "El Salvador": "SV",
    "Sint Maarten (Dutch part)": "SX",
    "Syrian Arab Republic": "SY",
    "Eswatini": "SZ",
    "Turks and Caicos Islands": "TC",
    "Chad": "TD",
    "French Southern Territories": "TF",
    "Togo": "TG",
    "Thailand": "TH",
    "Tajikistan": "TJ",
    "Tokelau": "TK",
    "Timor-Leste": "TL",
    "Turkmenistan": "TM",
    "Tunisia": "TN",
    "Tonga": "TO",
    "Türkiye": "TR",
    "Trinidad and Tobago": "TT",
    "Tuvalu": "TV",
    "Taiwan, Province of China": "TW",
    "Tanzania, United Republic of": "TZ",
    "Ukraine": "UA",
    "Uganda": "UG",
    "United States Minor Outlying Islands": "UM",
    "United States of America": "US",
    "Uruguay": "UY",
    "Uzbekistan": "UZ",
    "Holy See": "VA",
    "Saint Vincent and the Grenadines": "VC",
    "Venezuela, Bolivarian Republic of": "VE",
    "Virgin Islands (British)": "VG",
    "Virgin Islands (U.S.)": "VI",
    "Viet Nam": "VN",
    "Vanuatu": "VU",
    "Wallis and Futuna": "WF",
    "Samoa": "WS",
    "Yemen": "YE",
    "Mayotte": "YT",
    "South Africa": "ZA",
    "Zambia": "ZM",
    "Zimbabwe": "ZW"
}

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

DEEPSEEK_CONFIG = {
    "base_url": "http://localhost:11434/api/generate",
    "max_retries": 3,
    "initial_timeout": 30,
    "backoff_factor": 2,
    "model_name": "deepseek-r1"
}

def get_iso_code(country_name):
    """Helper function to get ISO code with improved cleaning"""
    if not country_name:
        return ""
    
    # Enhanced cleaning of country names
    country_name = country_name.strip().replace(".", "")
    
    # Remove any content in parentheses from country names
    if "(" in country_name:
        country_name = country_name.split("(")[0].strip()
    
    # Lookup in our mapping (with case insensitivity)
    for country, iso in country_to_iso.items():
        if country.lower() == country_name.lower():
            return iso
    
    # Try common alternative names
    alternative_names = {
        "USA": "US",
        "United States": "US",
        "UK": "GB",
        "England": "GB",
        "Scotland": "GB",
        "Wales": "GB",
        "Northern Ireland": "GB",
        "Republic of Korea": "KR",
        "South Korea": "KR",
        "North Korea": "KP",
        "Russia": "RU",
        "Vietnam": "VN"
    }
    
    if country_name in alternative_names:
        return alternative_names[country_name]
    
    # Return empty string if not found
    return ""

def determine_field_of_study(keywords):
    """Determine the most likely field of study from keywords"""
    if not keywords:
        return None
    
    # Try to find the best matching field of study
    best_match = None
    highest_score = 0
    
    for keyword in keywords:
        # Find the best match in FieldsOfStudy for this keyword
        match, score = process.extractOne(keyword.lower(), [f.lower() for f in FieldsOfStudy])
        if score > highest_score and score >= 75:  # Minimum confidence threshold
            highest_score = score
            best_match = FieldsOfStudy[[f.lower() for f in FieldsOfStudy].index(match)]
    
    return best_match

def query_deepseek_for_country(paper_data, country_to_iso, log_file="citation_metrics.csv"):
    """
    Query DeepSeek API to determine country for a paper with:
    - Automatic retries with exponential backoff
    - Comprehensive time tracking
    - Robust error handling
    
    Args:
        paper_data (dict): Paper metadata including title, authors, etc.
        country_to_iso (dict): Mapping of country names to ISO codes
        log_file (str): Path to save time tracking metrics
    
    Returns:
        str: Detected country name or None if failed
    """
    # Initialize time tracking
    metrics = track_citation_metrics(
        citation_id=paper_data.get("PaperId", "unknown"),
        batch=os.path.basename(os.path.dirname(paper_data.get("MasterFileName", ""))) or "unknown",
        query=f"Country detection for: {paper_data.get('PaperTitle', '')[:50]}...",
        log_file=log_file
    )
    
    # Prepare the prompt
    countries_str = ", ".join(country_to_iso.keys())
    prompt = f"""Based on this journal information, determine which country should be credited:
    Title: {paper_data.get("PaperTitle", "N/A")}
    Journal: {paper_data.get("Journal", "N/A")}
    Authors: {', '.join([author.get("Name", "N/A") for author in paper_data.get("Authors", [])])}
    
    Provide ONLY the country name from this list: {countries_str}
    Do NOT include any explanations or additional text."""
    
    # Try with exponential backoff
    for attempt in range(DEEPSEEK_CONFIG["max_retries"]):
        current_timeout = DEEPSEEK_CONFIG["initial_timeout"] * (attempt + 1)
        try:
            metrics["T4"]["Start"] = time.time()
            
            response = requests.post(
                DEEPSEEK_CONFIG["base_url"],
                headers={"Content-Type": "application/json"},
                json={
                    "model": DEEPSEEK_CONFIG["model_name"],
                    "prompt": prompt,
                    "stream": False,
                    "options": {"timeout": current_timeout * 1000}
                },
                timeout=current_timeout
            )
            
            metrics["T4"]["End"] = time.time()
            
            if response.status_code == 200:
                response_text = response.json().get("response", "").strip()
                
                # Validate the response contains a known country
                for country in country_to_iso:
                    if country.lower() in response_text.lower():
                        write_metrics_to_file(metrics, log_file)
                        return country
                
                print(f"Invalid country in response: {response_text}")
            
            else:
                print(f"Attempt {attempt+1}: API returned {response.status_code}")
                
        except requests.exceptions.Timeout:
            print(f"Attempt {attempt+1}: Timeout after {current_timeout}s")
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt+1}: Request failed - {str(e)}")
        except Exception as e:
            print(f"Attempt {attempt+1}: Unexpected error - {str(e)}")
        
        # Exponential backoff before retry
        if attempt < DEEPSEEK_CONFIG["max_retries"] - 1:
            backoff = DEEPSEEK_CONFIG["backoff_factor"] ** attempt
            time.sleep(backoff)
    
    # If all retries failed
    metrics["T4"]["End"] = time.time()
    write_metrics_to_file(metrics, log_file)
    return None


def validate_country_response(response_text, country_to_iso):
    """Helper to validate the API response contains a known country"""
    response_text = response_text.strip().lower()
    for country in country_to_iso:
        if country.lower() in response_text:
            return country
    return None

def transform_chunked_files(input_base_dir, output_base_dir, country_to_iso):
    """
    Transforms chunked JSON files with DeepSeek integration for country detection
    and automatic field of study classification.
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_base_dir, exist_ok=True)
    
    # Walk through the input directory structure
    for root, dirs, files in os.walk(input_base_dir):
        for file in files:
            if file.endswith('.json'):
                input_path = os.path.join(root, file)
                
                # Determine output path (maintaining same directory structure)
                rel_path = os.path.relpath(root, input_base_dir)
                output_dir = os.path.join(output_base_dir, rel_path)
                os.makedirs(output_dir, exist_ok=True)
                output_path = os.path.join(output_dir, file)
                
                # Process each file
                with open(input_path, 'r', encoding='utf-8') as f:
                    try:
                        papers_data = json.load(f)
                    except json.JSONDecodeError:
                        print(f"Error reading {input_path} - invalid JSON")
                        continue
                
                transformed_data = []
                skipped_count = 0
                
                for paper in papers_data:
                    # Skip if missing required fields
                    if not all(key in paper for key in ["PaperTitle", "Journal", "Year", "Authors", "Keywords"]):
                        skipped_count += 1
                        continue
                    
                    # Determine field of study from keywords
                    field_of_study = determine_field_of_study(paper.get("Keywords", []))
                    if not field_of_study:
                        skipped_count += 1
                        continue
                    
                    authors = paper.get("Authors", [])
                    countries = set()
                    list_of_authors = []
                    
                    # First pass: Try to get countries from AuthorOrg
                    for author in authors:
                        org = author.get("AuthorOrg", "")
                        country = ""
                        if org:
                            country = org.split(",")[-1].strip()
                            country = ''.join([c for c in country if c.isalpha() or c.isspace()]).strip()
                        
                        iso_code = get_iso_code(country) if country else ""
                        
                        if iso_code:
                            countries.add(iso_code)
                            list_of_authors.append({
                                "AuthorID": author.get("AuthorId", ""),
                                "AuthCountryISO": iso_code
                            })
                    
                    # If no countries found in AuthorOrg, try DeepSeek
                    if not countries:
                        deepseek_country = query_deepseek_for_country(paper)
                        if deepseek_country:
                            iso_code = get_iso_code(deepseek_country)
                            if iso_code:
                                countries.add(iso_code)
                                # Apply this country to all authors
                                for author in authors:
                                    list_of_authors.append({
                                        "AuthorID": author.get("AuthorId", ""),
                                        "AuthCountryISO": iso_code
                                    })
                    
                    # Skip this paper if no countries could be identified
                    if not countries:
                        skipped_count += 1
                        continue
                    
                    # Create transformed record
                    transformed = {
                        "CitationID": paper.get("PaperId", ""),
                        "YearOfPub": paper.get("Year", ""),
                        "CategoryOfPub": field_of_study,
                        "ListOfFieldsOfStudy": paper.get("Keywords", []),
                        "CountOfAuthors": len(authors),
                        "CountOfCountrys": len(countries),
                        "ListOfAuthors": list_of_authors
                    }
                    
                    transformed_data.append(transformed)
                
                # Only save if we have valid records
                if transformed_data:
                    with open(output_path, 'w', encoding='utf-8') as f:
                        json.dump(transformed_data, f, indent=4, ensure_ascii=False)
                    print(f"Processed {input_path} -> {output_path} (skipped {skipped_count} records)")
                else:
                    print(f"Skipped {input_path} - no valid records after processing")

# Example usage
if __name__ == "__main__":
    transform_chunked_files(
        input_base_dir="output",  
        output_base_dir="Output2"
    )
