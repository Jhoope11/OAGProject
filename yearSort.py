import csv
import os
import io
outputFolder = 'years/'
def init_output_file(OUTPUT_FILE):
    headers = [
        "CitationID", "Year", "Title", "Fields",
        "Authors", "SourceChunk", "ProcessingTime"
    ]
    if not os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()

def yearSort():
    headers = [
        "CitationID", "Year", "Title", "Fields",
        "Authors", "SourceChunk", "ProcessingTime"
    ]
    with open('formatted_citations2.csv', 'r') as csvFile:
        reader = csv.DictReader(csvFile)
        if not os.path.exists(outputFolder):
            os.makedirs(outputFolder, exist_ok=True)
        for row in reader:
            print(row['Year'])
            checkYearExists = os.path.join(outputFolder, f"{row['Year']}.csv")
            if not os.path.exists(checkYearExists):
                init_output_file(checkYearExists)
            with open(checkYearExists, 'a', newline='', encoding='utf-8') as f:
                print(row)
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writerow(row)
            
            
def testMain():
    init_output_file('formatted_citations2.csv')


if __name__ == "__main__":
    yearSort()