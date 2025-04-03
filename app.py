from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import io
import base64
import tkinter as tk 
import os
import csv
from collections import defaultdict

app = Flask(__name__)
csvFile = "formatted_citations.csv"
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

def load_citations_data():
    """Load and index the citations data from CSV"""
    data = []
    if os.path.exists(csvFile):
        with open(csvFile, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Parse the authors JSON string
                try:
                    row['Authors'] = eval(row['Authors'])  # Using eval for simplicity (be cautious with untrusted data)
                except:
                    row['Authors'] = []
                data.append(row)
    return data

def filter_citations(data, query_params):
    """Filters citations based on user query parameters"""
    filtered = []
    for citation in data:
        # Checks year range
        if 'YearOfStart' in query_params and 'YearOfEnd' in query_params:
            try:
                year = int(citation['Year'])
                if not (int(query_params['YearOfStart']) <= year <= int(query_params['YearOfEnd'])):
                    continue
            except ValueError:
                continue
        # Checks country
        if 'SelectedCountry' in query_params and query_params['SelectedCountry']:
            target_country = query_params['SelectedCountry']
            authors = citation.get('Authors', [])
            country_match = any(author.get('AuthCountryISO') == COUNTRIES_ISO.get(target_country, '') 
                              for author in authors)
            if not country_match:
                continue
        # Checks field of study
        if 'FieldOfStudy' in query_params and query_params['FieldOfStudy']:
            fields = citation.get('Fields', '').split('|')
            if query_params['FieldOfStudy'].lower() not in [f.lower() for f in fields]:
                continue
        filtered.append(citation)
    return filtered

def analyze_collaborations(filtered_data, query_params):
    """Analyze collaboration metrics for the filtered data"""
    metrics = {
        'NumOfPapers': len(filtered_data),
        'NumOfCollaborations': 0,
        'NumberOfAuthors': 0,
        'ConnectedCountries': set(),
        'FieldsDistribution': defaultdict(int),
        'YearsDistribution': defaultdict(int)
    }
    
    target_country_iso = COUNTRIES_ISO.get(query_params.get('SelectedCountry', ''), '')
    
    for citation in filtered_data:
        # Count authors
        authors = citation.get('Authors', [])
        metrics['NumberOfAuthors'] += len(authors)
        
        # Count collaborations (authors from different countries)
        author_countries = {author.get('AuthCountryISO') for author in authors if author.get('AuthCountryISO')}
        if target_country_iso in author_countries:
            metrics['NumOfCollaborations'] += len(author_countries - {target_country_iso})
            metrics['ConnectedCountries'].update(author_countries - {target_country_iso})
        
        # Count fields
        fields = citation.get('Fields', '').split('|')
        for field in fields:
            metrics['FieldsDistribution'][field] += 1
        
        # Count years
        year = citation.get('Year', '')
        if year:
            metrics['YearsDistribution'][year] += 1
    
    metrics['ListOfConnectedCountries'] = ', '.join(metrics['ConnectedCountries'])
    return metrics

def create_graph(metrics, title):
    """Create visualization of the metrics"""
    # Prepare data for the main bar chart
    labels = ['Collaborations', 'Authors', 'Papers']
    values = [
        metrics['NumOfCollaborations'],
        metrics['NumberOfAuthors'],
        metrics['NumOfPapers']
    ]
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle(title, fontsize=16)
    
    # Main metrics bar chart
    bars = ax1.bar(labels, values, color=['blue', 'green', 'red'])
    ax1.set_xlabel('Metrics')
    ax1.set_ylabel('Count')
    ax1.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom')
    
    # Fields distribution pie chart
    if metrics['FieldsDistribution']:
        fields = list(metrics['FieldsDistribution'].keys())
        counts = list(metrics['FieldsDistribution'].values())
        ax2.pie(counts, labels=fields, autopct='%1.1f%%', startangle=90)
        ax2.axis('equal')  # Equal aspect ratio ensures pie is drawn as a circle
        ax2.set_title('Fields of Study Distribution')
    
    # Save the plot to a bytes buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    plt.close()
    
    # Convert to base64 for HTML embedding
    return base64.b64encode(buffer.getvalue()).decode('utf-8')


@app.route('/', methods=['GET', 'POST'])
def index():
    citations_data = load_citations_data()
    
    if request.method == 'POST':
        form_data = {
            'TitleOfChart': request.form.get('TitleOfChart', 'Research Collaboration Metrics'),
            'YearOfStart': request.form.get('YearOfStart', ''),
            'YearOfEnd': request.form.get('YearOfEnd', ''),
            'SelectedCountry': request.form.get('SelectedCountry', ''),
            'FieldOfStudy': request.form.get('FieldOfStudy', ''),
            'ListOfConnectedCountries': '',
            'NumOfCollaborations': 0,
            'NumberOfAuthors': 0,
            'NumOfPapers': 0
        }
        
        # Filter data based on query
        filtered_data = filter_citations(citations_data, form_data)
        
        # Analyze metrics
        metrics = analyze_collaborations(filtered_data, form_data)
        
        # Update form data with metrics
        form_data.update({
            'NumOfCollaborations': metrics['NumOfCollaborations'],
            'NumberOfAuthors': metrics['NumberOfAuthors'],
            'NumOfPapers': metrics['NumOfPapers'],
            'ListOfConnectedCountries': metrics['ListOfConnectedCountries']
        })
        
        # Generate visualization
        graph = create_graph(metrics, form_data['TitleOfChart'])
        
        return render_template('result.html', 
                            graph=graph,
                            form_data=form_data,
                            metrics=metrics)
    else:
        # For GET request, show form with default values
        return render_template('index.html', 
                            countries=sorted(COUNTRIES_ISO.keys()),
                            fields_of_study=FIELDS_OF_STUDY)

if __name__ == '__main__':
    app.run(debug=True)