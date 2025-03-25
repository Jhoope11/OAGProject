import os
import csv
from collections import defaultdict

def collabCalc(output_dir, FieldsOfStudy, field_stats):
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

