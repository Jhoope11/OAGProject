# time_tracker.py
import csv
import time
import os
from datetime import datetime

def track_citation_metrics(citation_id, batch, query, log_file="citation_metrics.csv"):
    """
    Tracks and logs processing metrics for a citation.
    Returns a dictionary with timing markers that should be updated during processing.
    """
    metrics = {
        "CitationID": citation_id,
        "Batch": batch,
        "Date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "T1": {"Start": None, "End": None},  # DB open time
        "T2": {"Start": None, "End": None},  # Citation retrieval
        "T3": query,                         # Query text
        "T4": {"Start": None, "End": None},  # DeepSeek response time
        "T5": {"Start": time.time(), "End": None}  # Total time
    }
    
    # Create log file with headers if it doesn't exist
    if not os.path.exists(log_file):
        with open(log_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "CitationID", "Batch", "Date",
                "T1_Start", "T1_End", "T1_Duration",
                "T2_Start", "T2_End", "T2_Duration",
                "T3_Query",
                "T4_Start", "T4_End", "T4_Duration",
                "T5_Start", "T5_End", "T5_Duration"
            ])
    
    return metrics

def write_metrics_to_file(metrics, log_file="citation_metrics.csv"):
    """Writes the completed metrics to the log file"""
    # Calculate durations
    t1_duration = metrics["T1"]["End"] - metrics["T1"]["Start"] if metrics["T1"]["End"] else 0
    t2_duration = metrics["T2"]["End"] - metrics["T2"]["Start"] if metrics["T2"]["End"] else 0
    t4_duration = metrics["T4"]["End"] - metrics["T4"]["Start"] if metrics["T4"]["End"] else 0
    metrics["T5"]["End"] = time.time()
    t5_duration = metrics["T5"]["End"] - metrics["T5"]["Start"]

    with open(log_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            metrics["CitationID"],
            metrics["Batch"],
            metrics["Date"],
            metrics["T1"]["Start"],
            metrics["T1"]["End"],
            t1_duration,
            metrics["T2"]["Start"],
            metrics["T2"]["End"],
            t2_duration,
            metrics["T3"],
            metrics["T4"]["Start"],
            metrics["T4"]["End"],
            t4_duration,
            metrics["T5"]["Start"],
            metrics["T5"]["End"],
            t5_duration
        ])