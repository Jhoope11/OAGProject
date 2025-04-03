import csv
import time
import os
from datetime import datetime

def track_citation_metrics(citation_id, batch, query):
    """Initialize metrics tracking with chunk awareness"""
    return {
        "CitationID": citation_id,
        "Batch": batch,
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Query": query,
        "T1": {"Start": None, "End": None},  # Total processing
        "T2": {"Start": None, "End": None},  # Author processing
        "T3": {"Start": None, "End": None},  # DeepSeek queries
        "T4": {"Start": None, "End": None}   # File I/O
    }

def write_metrics_to_file(metrics, log_file="citation_metrics.csv"):
    """Write metrics with additional context"""
    # Calculate durations
    durations = {
        k: (v["End"] - v["Start"]) if v["End"] else 0 
        for k, v in metrics.items() 
        if isinstance(v, dict)
    }

    # Prepare row
    row = {
        **{k: v for k, v in metrics.items() if not isinstance(v, dict)},
        **{f"{k}_Duration": v for k, v in durations.items()}
    }

    # Write to file
    file_exists = os.path.exists(log_file)
    with open(log_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)