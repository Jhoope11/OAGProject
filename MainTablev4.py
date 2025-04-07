import json
import os
import csv
import time
import requests
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Optional
from TimeTracker import track_citation_metrics, write_metrics_to_file

# Configuration
INPUT_DIR = "output"
OUTPUT_FILE = "formatted_citations.csv"
DEEPSEEK_URL = "http://localhost:11434/api/generate"
REQUEST_TIMEOUT = 1000

COUNTRIES_ISO = {
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
FIELDS_OF_STUDY = [
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

def init_output_file():
    headers = [
        "CitationID", "Year", "Title", "Fields",
        "Authors", "SourceChunk", "ProcessingTime"
    ]
    if not os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()

def query_deepseek(prompt: str, citation_id: str, max_retries=3) -> Optional[str]:
    """Query DeepSeek with retry logic and enhanced error handling"""
    for attempt in range(max_retries):
        try:
            response = requests.post(
                DEEPSEEK_URL,
                json={
                    "model": "deepseek-r1",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            result = response.json().get("response", "").strip()
            
            # Log the interaction
            with open("deepseek_queries.log", "a", encoding='utf-8') as log_file:
                log_file.write(f"\n{'='*40}\nCitation: {citation_id}\nPrompt:\n{prompt}\nResponse:\n{result}\n")
                
            return result
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for {citation_id}: {str(e)}")
            time.sleep(2 ** attempt)  # Exponential backoff
    return None

def build_country_prompt(org: str, citation_context: Dict) -> str:
    """Generate a fast prompt with full citation context"""
    return f"""
    Determine the research institution's country with this context:
    
    INSTITUTION: "{org}"
    
    AUTHOR COLLABORATORS:
    {', '.join([auth.get('Name', '') for auth in citation_context.get('Authors', [])])}
    
    REQUIREMENTS:
    1. Select from these exact country names: {', '.join(COUNTRIES_ISO.keys())}
    2. Return ONLY the country name
    3. If unclear, respond with "Unknown"
    """

def extract_author_info(authors: List[Dict], citation_context: Dict) -> List[Dict]:
    """Process authors with full citation context"""
    author_info = []
    for author in authors:
        metrics = track_citation_metrics(
            citation_id=citation_context["PaperId"],
            batch="author_processing",
            query=f"Processing author from {citation_context['SourceFile']}"
        )
        
        try:
            metrics["T1"]["Start"] = time.time()
            author_id = author.get("AuthorId", "")
            org = author.get("AuthorOrg", "")
            detection_method = "Parser"  # Default method
            
            if not org:
                continue

            # Try simple parsing first
            country = None
            org_parts = [p.strip() for p in org.split(",")]
            for part in reversed(org_parts):
                if part in COUNTRIES_ISO:
                    country = part
                    break

            # Fallback to DeepSeek if simple parsing fails
            if not country:
                prompt = build_country_prompt(org, citation_context)
                deepseek_response = query_deepseek(prompt, citation_context["PaperId"])
                if deepseek_response and deepseek_response in COUNTRIES_ISO:
                    country = deepseek_response
                    detection_method = "DeepSeek"

            if country:
                author_info.append({
                    "AuthorID": author_id,
                    "AuthCountryISO": COUNTRIES_ISO[country],
                    "OriginalOrg": org,
                    "SourceFile": citation_context["SourceFile"],
                    "Method": detection_method
                })

        except Exception as e:
            print(f"Error processing author: {str(e)}")
        finally:
            metrics["T1"]["End"] = time.time()
            write_metrics_to_file(metrics)
    
    return author_info

def process_citation(citation: Dict, chunk_file: str) -> Optional[Dict]:
    """Process citation with chunk file context"""
    citation_id = citation.get("PaperId", "unknown")
    metrics = track_citation_metrics(
        citation_id=citation_id,
        batch=os.path.basename(chunk_file),
        query=f"Processing from {chunk_file}"
    )

    try:
        # Build complete context
        citation_context = {
            **citation,
            "SourceFile": chunk_file
        }

        # Process authors with context
        author_info = extract_author_info(citation.get("Authors", []), citation_context)
        if not author_info:
            return None

        # Process fields of study
        fields = []
        for keyword in citation.get("Keywords", []):
            kw_lower = keyword.lower()
            if any(f.lower() == kw_lower for f in FIELDS_OF_STUDY):
                fields.append(next(f for f in FIELDS_OF_STUDY if f.lower() == kw_lower))

        if not fields:
            fields = ["Unknown"]

        return {
            "CitationID": citation_id,
            "Year": citation.get("Year", ""),
            "Title": citation.get("PaperTitle", ""),
            "Fields": "|".join(fields),
            "Authors": json.dumps(author_info, ensure_ascii=False),
            "SourceChunk": chunk_file,
            "ProcessingTime": datetime.now().isoformat()
        }

    except Exception as e:
        print(f"Error processing {citation_id}: {str(e)}")
        return None
    finally:
        write_metrics_to_file(metrics)

def process_all_files():
    """Process all chunked files with real-time CSV updates"""
    # Initialize output file
    output_headers = [
        "CitationID", "Year", "Title", "Fields",
        "Authors", "SourceChunk", "ProcessingTime"
    ]
    if not os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
            csv.DictWriter(f, fieldnames=output_headers).writeheader()

    # Setup progress tracking
    processed_count = 0
    failed_files = []
    start_time = time.time()
    skip_first_rows = 1017
    first_file_processed = False

    # Process each chunk
    for chunk_dir in sorted(os.listdir(INPUT_DIR)):
        chunk_path = os.path.join(INPUT_DIR, chunk_dir)
        if not os.path.isdir(chunk_path):
            continue

        # Open CSV in append mode for real-time writing
        with open(OUTPUT_FILE, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=output_headers)
            
            # Process each file in chunk
            for file in sorted(os.listdir(chunk_path)):
                if not file.endswith('.json'):
                    continue

                file_path = os.path.join(chunk_path, file)
                try:
                    # Load citations
                    with open(file_path, 'r', encoding='utf-8') as f:
                        citations = json.load(f)

                     # Skip rows in first file
                    if not first_file_processed:
                        citations = citations[skip_first_rows:]
                        first_file_processed = True

                    # Process each citation
                    for citation in citations:
                        result = process_citation(citation, file_path)
                        if result:
                            writer.writerow(result)
                            processed_count += 1
                            
                            # Flush periodically
                            if processed_count % 100 == 0:
                                csvfile.flush()
                                print(
                                    f"Processed {processed_count} citations "
                                    f"({processed_count/(time.time()-start_time):.1f}/sec) "
                                    f"| Current file: {file_path}"
                                )

                except Exception as e:
                    print(f"Failed to process {file_path}: {str(e)}")
                    failed_files.append(file_path)
                    # Log failed file for retry
                    with open('failed_files.log', 'a', encoding='utf-8') as err_log:
                        err_log.write(f"{file_path}\t{str(e)}\n")

        # Chunk completion report
        print(
            f"Completed {chunk_dir} "
            f"({processed_count} total citations in {time.time()-start_time:.1f}s)"
        )

    # Final report
    print("\n" + "="*50)
    print(f"Total citations processed: {processed_count}")
    print(f"Failed files: {len(failed_files)} (see failed_files.log)")
    print(f"Processing rate: {processed_count/(time.time()-start_time):.1f} citations/sec")
    
    if failed_files:
        print("\nFailed files to reprocess:")
        for f in failed_files[:5]:  # Show first 5 as samples
            print(f" - {f}")

if __name__ == "__main__":
    process_all_files()