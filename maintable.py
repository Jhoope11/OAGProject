import json
import os
from collections import defaultdict

# Predefined country to ISO code mappings (replace with your complete list)
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

def get_iso_code(country_name):
    """Helper function to get ISO code with some basic cleaning"""
    if not country_name:
        return ""
    
    # Basic cleaning of country names
    country_name = country_name.strip()
    if country_name.endswith("."):
        country_name = country_name[:-1]
    
    # Lookup in our mapping (with case insensitivity)
    for country, iso in country_to_iso.items():
        if country.lower() == country_name.lower():
            return iso
    
    # Return empty string if not found
    return ""

def transform_chunked_files(input_base_dir, output_base_dir):
    """
    Transforms chunked JSON files to match the new format with ISO codes.
    
    Args:
        input_base_dir (str): Base directory containing the chunked JSON files
        output_base_dir (str): Base directory where transformed files will be saved
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
                with open(input_path, 'r') as f:
                    try:
                        papers_data = json.load(f)
                    except json.JSONDecodeError:
                        print(f"Error reading {input_path} - invalid JSON")
                        continue
                
                transformed_data = []
                
                for paper in papers_data:
                    # Transform each paper to the new format
                    transformed = {
                        "CitationID": paper.get("PaperId", ""),
                        "YearOfPub": paper.get("Year", ""),
                        "CategoryOfPub": "",  # Will need to be filled based on your data
                        "ListOfFieldsOfStudy": paper.get("Keywords", []),
                        "CountOfAuthors": len(paper.get("Authors", [])),
                        "CountOfCountrys": 0,  # Will be calculated below
                        "ListOfAuthors": [author.get("Name", "") for author in paper.get("Authors", [])],
                        "Subfields": [],  # Will need to be filled based on your data
                        "AuthorID": [author.get("AuthorId", "") for author in paper.get("Authors", [])],
                        "AuthCountryID": [],  # Will be filled below
                        "ISOCode": []  # Will be filled from our mapping
                    }
                    
                    # Process countries and ISO codes
                    countries = set()
                    for author in paper.get("Authors", []):
                        # Extract country from AuthorOrg (assuming it's the last part after comma)
                        org = author.get("AuthorOrg", "")
                        country = ""
                        if org:
                            country = org.split(",")[-1].strip()
                        
                        if country:
                            transformed["AuthCountryID"].append(country)
                            iso_code = get_iso_code(country)
                            transformed["ISOCode"].append(iso_code)
                            countries.add(country)
                    
                    transformed["CountOfCountrys"] = len(countries)
                    
                    transformed_data.append(transformed)
                
                # Save transformed data
                with open(output_path, 'w') as f:
                    json.dump(transformed_data, f, indent=4)
                
                print(f"Processed {input_path} -> {output_path}")

# Example usage
if __name__ == "__main__":
    transform_chunked_files(
        input_base_dir="output",  # Your original chunked files directory
        output_base_dir="transformed_output"  # Where to save transformed files
    )