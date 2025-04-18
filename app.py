from flask import Flask, render_template, request
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import os
import csv
from collections import defaultdict

app = Flask(__name__)

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

def load_citations_data(csvFile):
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
        'YearsDistribution': defaultdict(int),
        'CollaborationCountries': defaultdict(int)
    }
    
    target_country = query_params.get('SelectedCountry', '')
    target_country_iso = COUNTRIES_ISO.get(target_country, '')
    
    for citation in filtered_data:
        # Count authors
        authors = citation.get('Authors', [])
        metrics['NumberOfAuthors'] += len(authors)
        
        # Count collaborations (authors from different countries)
        author_countries = set()
        for author in authors:
            if isinstance(author, dict) and author.get('AuthCountryISO'):
                country_iso = author.get('AuthCountryISO')
                country_name = next(
                    (name for name, iso in COUNTRIES_ISO.items() if iso == country_iso),
                    country_iso  # fallback to ISO if name not found
                )
                author_countries.add(country_name)
        
        if target_country in author_countries:
            collaborating_countries = author_countries - {target_country}
            metrics['NumOfCollaborations'] += len(collaborating_countries)
            metrics['ConnectedCountries'].update(collaborating_countries)
            
            for country in collaborating_countries:
                metrics['CollaborationCountries'][country] += 1
        
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
    fig = plt.figure(figsize=(16, 8))
    fig.suptitle(title, fontsize=16)
    
    # Main metrics bar chart
    ax1 = plt.subplot(121)  # 1 row, 2 columns, 1st subplot
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
    
    # Collaboration countries circular bar plot
    if metrics.get('CollaborationCountries'):
        countries = list(metrics['CollaborationCountries'].keys())
        counts = list(metrics['CollaborationCountries'].values())
        
        # Sort data by count (highest first)
        sorted_indices = np.argsort(counts)[::-1]
        countries = [countries[i] for i in sorted_indices]
        counts = [counts[i] for i in sorted_indices]
        
        # Initialize layout in polar coordinates
        ax2 = plt.subplot(122, polar=True)
        
        # Set number of bars and compute angles
        N = len(countries)
        theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
        width = 2 * np.pi / N
        
        # Set color gradient based on count
        colors = plt.cm.viridis(np.linspace(0.2, 0.8, N))
        
        # Plot bars
        bars = ax2.bar(
            theta, counts, 
            width=width-0.1,  # Slightly smaller width for gaps
            color=colors,
            alpha=0.8,
            linewidth=1,
            edgecolor="white"
        )
        
        # Set the label for each bar
        rotation = np.degrees(theta)
        for angle, label, count in zip(rotation, countries, counts):
            ax2.text(
                angle * np.pi / 180,  # Convert to radians
                max(counts) * 1.1,  # Position slightly above highest bar
                label,
                ha='center',
                va='center',
                rotation=angle if angle <=180 else angle-180,
                fontsize=9
            )
        
        # Set axis limits and remove unnecessary elements
        ax2.set_ylim(0, max(counts) * 1.3)
        ax2.set_xticks([])
        ax2.set_yticks([])
        ax2.spines['polar'].set_visible(False)
        
        # Add count labels inside bars
        for angle, count in zip(theta, counts):
            ax2.text(
                angle,
                count + max(counts) * 0.02,
                str(count),
                ha='center',
                va='center',
                fontsize=8
            )
        
        # Add title
        ax2.set_title('International Collaborations by Country', pad=20)
    
    plt.tight_layout()
    
    # Save the plot to a bytes buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
    buffer.seek(0)
    plt.close()
    
    # Convert to base64 for HTML embedding
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

def retrieveCountries():
    countries = set()
    citations_data = []
    startYear = 1999  # Adjust as needed
    endYear = 2013    # Adjust as needed
    
    while startYear <= endYear:
        citationPath = os.path.join('years', f"{str(startYear)}.csv")
        if os.path.exists(citationPath):
            citations_data.extend(load_citations_data(citationPath))
        startYear += 1
    
    for citation in citations_data:
        authors = citation.get('Authors', [])
        for author in authors:
            if isinstance(author, dict):
                country_iso = author.get('AuthCountryISO')
                if country_iso:
                    # Find country name from ISO code
                    country_name = next(
                        (name for name, iso in COUNTRIES_ISO.items() if iso == country_iso),
                        None
                    )
                    if country_name:
                        countries.add(country_name)
    
    return sorted(countries)

@app.route('/')
def base():
    return render_template('base.html')

@app.route('/collab-table-form')
def collab_table_form():
    countries_list = retrieveCountries()
    return render_template('collabTableForm.html', 
                         fields_of_study=FIELDS_OF_STUDY, 
                         countries=countries_list)

@app.route('/collab-with-selected-country')
def collab_with_selected_country():
    countries_list = retrieveCountries()
    return render_template('collabWithSelectedCountryForm.html', 
                         fields_of_study=FIELDS_OF_STUDY, 
                         countries=countries_list)
    
@app.route('/researchCollabAnalyzerForm', methods=['GET', 'POST'])
def researchCollabAnalyzerForm():
    citations_data = []
    
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
        #Load data based on the specified year count
        startYear = int(request.form.get('YearOfStart', ''))
        endYear = int(request.form.get('YearOfEnd', ''))
        while startYear != endYear+1:
            citationPath = os.path.join('years', f"{str(startYear)}.csv")
            citations_data.extend(load_citations_data(citationPath))
            startYear += 1
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
        # Generates graphs
        graph = create_graph(metrics, form_data['TitleOfChart'])
        
        return render_template('collabWithSelectedCountryResults.html', 
                            graph=graph,
                            form_data=form_data,
                            metrics=metrics)
    else:
        # For GET request, show form with default values
        return render_template('collabWithSelectedCountryForm.html', 
                            countries=sorted(COUNTRIES_ISO.keys()),
                            fields_of_study=FIELDS_OF_STUDY)

def analyze_country_collaborations(data, selected_country, field_of_study, year_start, year_end):
    """Analyze collaborations between selected country and others across time periods"""
    # Define time periods
    time_periods = [
        (1999, 2001),
        (2004, 2007),
        (2010, 2013)
    ]    
    # Filter data for selected country and field
    filtered_data = []
    for citation in data:
        # Check if citation is valid
        if not isinstance(citation, dict):
            continue
            
        # Check year
        try:
            year = int(citation.get('Year', 0))
            if not (year_start <= year <= year_end):
                continue
        except (ValueError, TypeError):
            continue
        # Check field of study if specified
        if field_of_study and field_of_study.lower() != 'all':
            fields = citation.get('Fields', '').split('|')
            if field_of_study.lower() not in [f.lower() for f in fields]:
                continue
        # Check if selected country is in authors
        authors = citation.get('Authors', [])
        has_selected_country = any(
            isinstance(author, dict) and 
            author.get('AuthCountryISO') == COUNTRIES_ISO.get(selected_country, '')
            for author in authors
        )
        if has_selected_country:
            filtered_data.append(citation)
    
    # Count collaborations by country and time period
    results = defaultdict(lambda: defaultdict(int))
    total_collaborations = 0
    for citation in filtered_data:
        try:
            year = int(citation.get('Year', 0))
            authors = citation.get('Authors', []) 
            # Get all collaborating countries (excluding selected country)
            collaborating_countries = set()
            for author in authors:
                if isinstance(author, dict):
                    country_iso = author.get('AuthCountryISO')
                    if country_iso and country_iso != COUNTRIES_ISO.get(selected_country, ''):
                        # Find country name from ISO code
                        country_name = next(
                            (name for name, iso in COUNTRIES_ISO.items() if iso == country_iso),
                            country_iso  # fallback to ISO code if name not found
                        )
                        collaborating_countries.add(country_name)
            # Assign to time period
            period = None
            for i, (start, end) in enumerate(time_periods):
                if start <= year <= end:
                    period = i
                    break
            if period is not None:
                for country in collaborating_countries:
                    results[country][period] += 1
                    results[country]['total'] += 1
                    total_collaborations += 1
        except (ValueError, TypeError):
            continue
    # Converts to sorted list of dictionaries for the table
    sorted_countries = sorted(results.items(), key=lambda x: x[1]['total'], reverse=True)
    table_data = []
    for country, counts in sorted_countries:
        row = {'Country': country}
        for i in range(len(time_periods)):
            row[f'{time_periods[i][0]}-{time_periods[i][1]}'] = counts.get(i, 0)
        row['Total'] = counts.get('total', 0)
        row['Percent'] = (counts.get('total', 0) / total_collaborations * 100) if total_collaborations > 0 else 0
        table_data.append(row)
    return table_data


@app.route('/collabTableResults', methods=['GET', 'POST'])
def collaboration_table():
    if request.method == 'POST':
        # Gets form data
        form_data = {
            'Title': request.form.get('Title', 'Collaboration With Selected Country'),
            'SelectedCountry': request.form.get('SelectedCountry', ''),
            'FieldOfStudy': request.form.get('FieldOfStudy', 'all'),
            'YearOfStart': int(request.form.get('YearOfStart', 1999)),
            'YearOfEnd': int(request.form.get('YearOfEnd', 2013))
        }
        # Loads data
        citations_data = []
        start_year = form_data['YearOfStart']
        end_year = form_data['YearOfEnd']
        current_year = start_year
        while current_year <= end_year:
            citation_path = os.path.join('years', f"{current_year}.csv")
            if os.path.exists(citation_path):
                citations_data.extend(load_citations_data(citation_path))
            current_year += 1
        # Analyzes data
        table_data = analyze_country_collaborations(
            citations_data,
            form_data['SelectedCountry'],
            form_data['FieldOfStudy'],
            form_data['YearOfStart'],
            form_data['YearOfEnd']
        )
        # Gets time period labels
        time_periods = [
            f"{form_data['YearOfStart']}-{form_data['YearOfStart']+2}",
            f"{form_data['YearOfStart']+5}-{form_data['YearOfStart']+8}",
            f"{form_data['YearOfStart']+11}-{form_data['YearOfEnd']}"
        ]
        return render_template('collabTableResults.html',
                            form_data=form_data,
                            table_data=table_data,
                            time_periods=time_periods)
    else:
        return render_template('collabTableForm.html',
                            countries=sorted(COUNTRIES_ISO.keys()),
                            fields_of_study=['all'] + FIELDS_OF_STUDY)
        
        
if __name__ == '__main__':
    app.run(debug=True)