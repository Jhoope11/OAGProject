# main_program.py
import json
import os
import csv
import time
import requests
from tenacity import retry, stop_after_attempt, wait_exponential
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Optional
from TimeTracker import track_citation_metrics, write_metrics_to_file

# Configuration

INPUT_DIR = "output"
OUTPUT_FILE = "formatted_citations.csv"
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
DEEPSEEK_URL = "http://localhost:11434/api/generate"
FIELDS_STR = "|".join(FIELDS_OF_STUDY)
COUNTRIES_STR = ",".join(COUNTRIES_ISO.keys())


# Add this helper function
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def query_deepseek(prompt: str) -> str:
    """Query local DeepSeek R1 instance with retry logic"""
    try:
        response = requests.post(
            DEEPSEEK_URL,
            json={
                "model": "deepseek-r1",
                "prompt": prompt,
                "stream": False
            },
            timeout=1000
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except Exception as e:
        print(f"DeepSeek query failed: {str(e)}")
        raise

def extract_country_from_org(org: str) -> Optional[str]:
    """Enhanced country extraction with DeepSeek fallback"""
    # First try simple parsing
    org_parts = [part.strip() for part in org.split(",")]
    for part in reversed(org_parts):
        if part in COUNTRIES_ISO:
            return part
    
    # If simple parsing fails, use DeepSeek

    prompt = f"""
    Determine which country this research organization belongs to: {org}
    The country must be one of these exact names: {COUNTRIES_STR}
    Return ONLY the country name, nothing else.
    """
        
    try:
        print(f"\n[DEBUG] Sending to DeepSeek:\n{prompt}")  # Log input
        result = query_deepseek(prompt)
        print(f"[DEBUG] Raw DeepSeek response: {repr(result)}")  # Log raw output
        
        if result and result in COUNTRIES_ISO:
            print(f"[SUCCESS] DeepSeek identified country: {result}")
            return result
        elif result:
            print(f"[WARNING] DeepSeek returned non-matching country: {result}")
        
    except Exception as e:
        print(f"[ERROR] DeepSeek query failed: {str(e)}")
    
    return None


def extract_author_info(authors: List[Dict]) -> List[Dict]:
    """Updated version with DeepSeek integration"""
    author_info = []
    for author in authors:
        metrics = track_citation_metrics(
            citation_id=author.get("AuthorId", "unknown_author"),
            batch="author_processing",
            query=f"Extract country for author {author.get('Name', '')}"
        )
        
        try:
            metrics["T1"]["Start"] = time.time()
            author_id = author.get("AuthorId", "")
            country = None
            
            if "AuthorOrg" in author:
                metrics["T2"]["Start"] = time.time()
                country = extract_country_from_org(author["AuthorOrg"])
                metrics["T2"]["End"] = time.time()
                
                if country:
                    author_info.append({
                        "AuthorID": author_id,
                        "AuthCountryISO": COUNTRIES_ISO[country],
                        "OriginalOrg": author["AuthorOrg"]  # Keep original for verification
                    })
                    
        except Exception as e:
            print(f"Error processing author: {str(e)}")
        finally:
            metrics["T1"]["End"] = time.time()
            write_metrics_to_file(metrics)
    
    return author_info


def process_citation(citation: Dict, batch_name: str, chunk_file: str) -> Optional[Dict]:
    citation_id = citation.get("PaperId", "unknown")
    metrics = track_citation_metrics(
        citation_id=citation_id,
        batch=batch_name,
        query=f"Processing {citation_id} from {chunk_file}"
    )
    
    try:
        metrics["T1"]["Start"] = time.time()
        if not all(key in citation for key in ["PaperId", "Year", "Keywords", "Authors"]):
            return None
            
        year = citation["Year"]
        keywords = citation.get("Keywords", [])
        authors = citation.get("Authors", [])
        metrics["T1"]["End"] = time.time()
        
        metrics["T2"]["Start"] = time.time()
        fields_of_study = []
        for keyword in keywords:
            keyword_lower = keyword.lower()
            for field in FIELDS_OF_STUDY:
                if keyword_lower == field.lower():
                    fields_of_study.append(field)
                    break
        
        # Use DeepSeek for field determination if needed
        if not fields_of_study:
            prompt = f"""
            Classify this paper's field based on keywords: {', '.join(keywords)}
            Choose ONLY from: {FIELDS_STR}
            Return ONLY the field name.
            """
            try:
                field = query_deepseek(prompt)
                if field in FIELDS_OF_STUDY:
                    fields_of_study.append(field)
            except Exception as e:
                print(f"Field classification failed for {citation_id}: {str(e)}")
            fields_of_study = fields_of_study or ["Unknown"]
        
        metrics["T2"]["End"] = time.time()
        
        metrics["T4"]["Start"] = time.time()
        author_info = extract_author_info(authors)
        metrics["T4"]["End"] = time.time()
        
        if not author_info:
            return None
            
        unique_countries = set(auth["AuthCountryISO"] for auth in author_info)
        
        return {
            "CitationID": citation_id,
            "YearOfPub": year,
            "CategoryOfPub": "Research Article",
            "ListOfFieldsOfStudy": "|".join(fields_of_study),
            "CountOfAuthors": len(authors),
            "CountOfCountries": len(unique_countries),
            "ListOfAuthors": json.dumps(author_info, ensure_ascii=False),
            "ProcessingMethod": "DeepSeek-R1"  # Track which processing was used
        }
        
    except Exception as e:
        print(f"Error processing citation {citation_id}: {str(e)}")
        return None
    finally:
        write_metrics_to_file(metrics)

def process_all_files():
    processed_data = []
    chunk_timings = []
    
    for chunk_dir in os.listdir(INPUT_DIR):
        chunk_path = os.path.join(INPUT_DIR, chunk_dir)
        if not os.path.isdir(chunk_path):
            continue
        
        chunk_start = time.time()
        chunk_files_processed = 0
        chunk_citations_processed = 0
        
        for file in os.listdir(chunk_path):
            if not file.endswith('.json'):
                continue
            
            file_path = os.path.join(chunk_path, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    citations = json.load(f)
                
                for citation in citations:
                    # Process each citation with chunk context
                    result = process_citation(
                        citation=citation,
                        batch_name=f"chunk_{chunk_dir}",
                        chunk_file=file  # Pass the chunk filename
                    )
                    
                    if result:
                        processed_data.append(result)
                        chunk_citations_processed += 1
                
                chunk_files_processed += 1
            
            except Exception as e:
                print(f"Error in {file_path}: {str(e)}")
        
        # Record chunk performance
        chunk_timings.append({
            "chunk": chunk_dir,
            "files": chunk_files_processed,
            "citations": chunk_citations_processed,
            "time_sec": time.time() - chunk_start
        })
    
    # Save outputs
    save_outputs(processed_data, chunk_timings)

def save_outputs(processed_data, chunk_timings):
    """Save results and metrics"""
    # Save formatted citations
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "citation_id", "year", "fields", 
            "author_count", "country_count", 
            "authors_json", "source_chunk"  # New field
        ])
        writer.writeheader()
        for row in processed_data:
            writer.writerow({
                "citation_id": row["citation_id"],
                "year": row["year"],
                "fields": "|".join(row["fields_of_study"]),
                "author_count": len(row["authors"]),
                "country_count": len({a["country"] for a in row["authors"]}),
                "authors_json": json.dumps(row["authors"], ensure_ascii=False),
                "source_chunk": row["source"]  # Preserve chunk origin
            })
    
    # Save chunk timings
    with open('chunk_metrics.csv', 'w', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "chunk", "files", "citations", "time_sec"
        ])
        writer.writeheader()
        writer.writerows(chunk_timings)

if __name__ == "__main__":
    process_all_files()