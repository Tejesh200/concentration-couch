#!/usr/bin/env python3
"""
Simple script to view database contents for Concentration Couch
"""
import sqlite3
import sys
from datetime import datetime

def view_logs_db():
    """View logs.db (used by backend/app/main.py)"""
    print("=" * 80)
    print("LOGS.DB - Website Visit Logs")
    print("=" * 80)
    
    try:
        conn = sqlite3.connect("logs.db")
        c = conn.cursor()
        
        # Get total count
        c.execute("SELECT COUNT(*) FROM logs")
        total = c.fetchone()[0]
        print(f"\nTotal records: {total}\n")
        
        if total > 0:
            # Get summary by label
            c.execute("SELECT label, COUNT(*) FROM logs GROUP BY label")
            print("Summary by classification:")
            for label, count in c.fetchall():
                print(f"  {label or 'NULL'}: {count}")
            
            # Get recent visits
            print("\nRecent visits (last 10):")
            c.execute("""
                SELECT url, label, score, created_at 
                FROM logs 
                ORDER BY created_at DESC 
                LIMIT 10
            """)
            
            print(f"\n{'URL':<50} {'Label':<15} {'Score':<8} {'Timestamp'}")
            print("-" * 100)
            for url, label, score, timestamp in c.fetchall():
                url_short = url[:47] + "..." if len(url) > 50 else url
                score_str = f"{score:.3f}" if score else "N/A"
                print(f"{url_short:<50} {label or 'NULL':<15} {score_str:<8} {timestamp or 'N/A'}")
        
        conn.close()
    except Exception as e:
        print(f"Error reading logs.db: {e}")

def view_stats_db():
    """View stats.db (used by app.py)"""
    print("\n" + "=" * 80)
    print("STATS.DB - Website Usage Statistics")
    print("=" * 80)
    
    try:
        conn = sqlite3.connect("stats.db")
        c = conn.cursor()
        
        # Get total count
        c.execute("SELECT COUNT(*) FROM usage")
        total = c.fetchone()[0]
        print(f"\nTotal records: {total}\n")
        
        if total > 0:
            # Get summary by classification
            c.execute("SELECT classification, COUNT(*) FROM usage GROUP BY classification")
            print("Summary by classification:")
            for classification, count in c.fetchall():
                print(f"  {classification or 'NULL'}: {count}")
            
            # Get recent visits
            print("\nRecent visits (last 10):")
            c.execute("""
                SELECT url, classification, timestamp 
                FROM usage 
                ORDER BY timestamp DESC 
                LIMIT 10
            """)
            
            print(f"\n{'URL':<50} {'Classification':<15} {'Timestamp'}")
            print("-" * 100)
            for url, classification, timestamp in c.fetchall():
                url_short = url[:47] + "..." if len(url) > 50 else url
                print(f"{url_short:<50} {classification or 'NULL':<15} {timestamp or 'N/A'}")
        
        conn.close()
    except Exception as e:
        print(f"Error reading stats.db: {e}")

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("CONCENTRATION COUCH - DATABASE VIEWER")
    print("=" * 80)
    
    # Check which database exists
    import os
    logs_exists = os.path.exists("logs.db")
    stats_exists = os.path.exists("stats.db")
    
    if not logs_exists and not stats_exists:
        print("\nNo database files found!")
        print("Databases will be created when the backend starts and receives requests.")
        sys.exit(0)
    
    if logs_exists:
        view_logs_db()
    else:
        print("\nlogs.db not found (used by backend/app/main.py)")
    
    if stats_exists:
        view_stats_db()
    else:
        print("\nstats.db not found (used by app.py)")
    
    print("\n" + "=" * 80)
    print("Tip: Run this script anytime to check your database contents!")
    print("=" * 80 + "\n")

