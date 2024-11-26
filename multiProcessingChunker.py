import json
import os
from multiprocessing import Pool

# Specify the folders and file paths
papers_folder = 'F:/OAGProject/OAGFiles/OAGPublications/'
output_folder = 'F:/OAGProject/Output/'
references_folder = '/users/PGS0283/jhoope11/jack/Graphs/UpdatedFiles/'

def read_papers(file_path):
    print(f"Reading papers from file: {file_path}\n")
    papers = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            paper_data = json.loads(line.strip())  # Parse each line as JSON
            paper_id = paper_data.get("id")
            if not paper_id:
                continue  # Skip this line if id is missing
            title = paper_data.get("title", "")
            year = paper_data.get("year", "")
            venue_name = paper_data.get("venue", "")
            n_citation = paper_data.get("n_citation", "")
            authors = [{"Name": author.get("name", ""), "AuthorId": author.get("id", ""), "AuthorOrg": author.get("org", "")} for author in paper_data.get("authors", [])]
            num_authors = len(authors)
            keywords = paper_data.get("keywords", "")
            abstracts = paper_data.get("abstract", "")
            #fos = [field.get("name", "") for field in paper_data.get("fos", [])]
            papers[paper_id] = {
                "Title": title,
                "authors": authors,
                "Year": year,
                "Venue": venue_name,
                "NumCitations": n_citation,
                "NumAuthors": num_authors,
                "Authors": authors,
                "Keywords": keywords,
                "Abstracts": abstracts
            }
    print("Papers read.\n")
    return papers

def create_reference_file(output_folder, paper_id_mapping):
    reference_file_path = os.path.join(output_folder, "reference.json")
    with open(reference_file_path, 'w') as rf:
        json.dump(paper_id_mapping, rf, indent=4)
    print(f"Reference file created: {reference_file_path}\n")

def create_json_file(output_folder, papers, master_file_name):
    print(f"Creating JSON files in folder: {output_folder}\n")
    count = 0
    file_count = 0
    paper_id_mapping = {}

    if not os.path.exists(output_folder):
        os.makedirs(output_folder, exist_ok=True)
    
    output_file = os.path.join(output_folder, f"papers_chunk_{file_count}.json")
    with open(output_file, 'w') as f:
        f.write("[")
        for paper_id, paper_info in papers.items():
            if count == 2000:
                f.write("\n]")
                f.close()
                # Map the current chunk to its corresponding file
                paper_id_mapping.update({pid: f"papers_chunk_{file_count}.json" for pid in papers.keys()})
                
                # Start a new chunk
                count = 0
                file_count += 1
                output_file = os.path.join(output_folder, f"papers_chunk_{file_count}.json")
                f = open(output_file, 'w')
                f.write("[")
            if count != 0:
                f.write(",\n")
            f.write(json.dumps({
                'PaperId': paper_id,
                'PaperTitle': paper_info['Title'],
                'MasterFileName': master_file_name,
                'Journal': paper_info['Venue'],
                'Year': paper_info['Year'],
                'NumAuthors': paper_info['NumAuthors'],
                'Authors': paper_info['Authors']
            }))
            count += 1
        f.write("\n]")
    
    # Finalize mapping for the last chunk
    paper_id_mapping.update({pid: f"papers_chunk_{file_count}.json" for pid in papers.keys()})

    # Call function to create reference file
    create_reference_file(output_folder, paper_id_mapping)

    print(f"JSON files created in folder: {output_folder}\n")
def process_papers(i, papers_folder):
    print(f"Processing papers file {i}\n")
    papers_file = os.path.join(papers_folder, f"v3.1_oag_publication_{i}.json")
    papers = read_papers(papers_file)

    # for j in range(5):  # Assuming authors files are named mag_authors_0.txt to mag_authors_4.txt
    #     print(f"Processing authors file {j} for papers file {i}\n")
    #     #authors_file = os.path.join(authors_folder, f"mag_authors_{j}.txt")
    #     #read_authors(authors_file, affiliations, papers)

    output_file = os.path.join(output_folder, f"papers_chunk_{i}.json")
    create_json_file(output_file, papers, f"v3.1_oag_publication_{i}.json")
    print(f"Chunk {i} processing complete\n")
def process_files(papers_folder, output_folder):
    print("Processing files...\n")
    
    # with Pool(processes=28) as pool:
    #     pool.starmap(process_papers, [(i, papers_folder) for i in range(5)])
    # pool.close()
    # pool.join()
    process_papers(1, papers_folder)
    print("All files processed.")
# Process all files
process_files(papers_folder, output_folder)