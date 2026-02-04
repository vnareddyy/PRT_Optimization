"""
PRT Survey Data Analysis - Main Pipeline
"""
import pandas as pd
import re
from collections import Counter, defaultdict
import os
import json

def is_valid_route(route):
    route = str(route).strip().upper()
    patterns = [r'^[1-9]\d[A-Z]?$', r'^[OPXY][1-9]\d?$', r'^[DN][1-9]\d{0,2}$', r'^[G][1-9]\d?$', r'^[Y][1-9]\d$']
    return any(re.match(p, route) for p in patterns)

def extract_routes(df):
    all_routes = []
    
    # Route columns only (columns 3, 4, 5)
    route_cols = [
        'What is the bus route you take most often?',
        'What is the bus route you take second most often?',
        'What is the bus route you take third most often?'
    ]
    
    for col in route_cols:
        if col in df.columns:
            for value in df[col].dropna():
                value = str(value).strip()
                if is_valid_route(value):
                    all_routes.append(value.upper())
    
    # Text response columns (columns 9-12) - free text responses
    text_cols = [
        'If you answered significant positive impact (1) or positive impact (2) in any of the above questions, please tell us why.',
        'If you answered significant negative impact (5) and/or negative impact (4) in any of the above questions, please tell us why..',
        'Is there a route change that you are most excited to see implemented? Why?',
        'Do you have any additional ideas or comments about the proposed network to the project team?'
    ]
    
    for col in text_cols:
        if col in df.columns:
            for value in df[col].dropna():
                text = str(value)
                # Match route patterns in text
                patterns = [r'\b([1-9]\d[A-Z]?)\b', r'\b([OPXY][1-9]\d?)\b', r'\b([DN][1-9]\d{0,2})\b', r'\b([G][1-9]\d?)\b', r'\b([Y][1-9]\d)\b']
                for pattern in patterns:
                    for match in re.findall(pattern, text, re.IGNORECASE):
                        if is_valid_route(match):
                            all_routes.append(match.upper())
    
    return Counter(all_routes)

def classify_action_types(df):
    action_patterns = {
        'INCREASE_FREQUENCY': [r'more frequent', r'frequent service', r'increase.*frequency', r'15 minute', r'more buses', r'more often', r'shorter.*wait', r'better frequency'],
        'IMPROVE_COVERAGE': [r'coverage', r'access', r'walk.*distance', r'near.*stop', r'closer.*stop', r'walk.*far', r'too far'],
        'ADD_SERVICE': [r'\badd\b', r'\bnew\b.*\broute', r'extension', r'extend.*route', r'need.*route', r'would like'],
        'DIRECT_CONNECTION': [r'direct.*route', r'one bus', r'no transfer', r'without transfer', r'skip.*transfer', r'direct.*service'],
        'PREVENT_ELIMINATION': [r"don't.*(cut|eliminate|remove)", r'keep.*route', r'preserve', r'do not.*cut', r'don\'t.*get rid'],
        'IMPROVE_RELIABILITY': [r'reliable', r'on time', r'consistent', r'bus bunching', r'missed.*bus', r'no show'],
        'RESTORE_SERVICE': [r'bring back', r'restore', r'used to have', r'past.*service'],
    }
    
    action_counts = defaultdict(int)
    
    # Only text response columns
    text_cols = [
        'If you answered significant positive impact (1) or positive impact (2) in any of the above questions, please tell us why.',
        'If you answered significant negative impact (5) and/or negative impact (4) in any of the above questions, please tell us why..',
        'Is there a route change that you are most excited to see implemented? Why?',
        'Do you have any additional ideas or comments about the proposed network to the project team?'
    ]
    
    for col in text_cols:
        if col in df.columns:
            for value in df[col].dropna():
                text = str(value).lower()
                for action, patterns in action_patterns.items():
                    for pattern in patterns:
                        matches = len(re.findall(pattern, text))
                        action_counts[action] += matches
    
    return dict(action_counts)

def extract_geographic_entities(df):
    areas = ['oakland', 'downtown', 'squirrel hill', 'greenfield', 'millvale', 'airport', 
             'south hills', 'south side', 'bloomfield', 'east liberty', 'lawrenceville', 
             'friendship', 'shadyside', 'east end', 'strip district', 'highland park', 
             'brookline', 'dormont', 'mt lebanon', 'uptown', 'pitt', 'cmu', 'carrick', 
             'allentown', 'troy hill', 'homestead', 'verona', 'monroeville', 'forest hills', 
             'swissvale', 'edgewood', 'whitehall', 'brentwood', 'bellefonte', 'point breeze', 
             'regent square', 'polish hill', 'morningside', 'stanton heights', 'garfield',
             'north side', 'sharpsburg', 'natrona', 'harwick', 'harmar']
    
    area_counts = Counter()
    
    text_cols = [
        'If you answered significant positive impact (1) or positive impact (2) in any of the above questions, please tell us why.',
        'If you answered significant negative impact (5) and/or negative impact (4) in any of the above questions, please tell us why..',
        'Is there a route change that you are most excited to see implemented? Why?',
        'Do you have any additional ideas or comments about the proposed network to the project team?'
    ]
    
    for col in text_cols:
        if col in df.columns:
            for value in df[col].dropna():
                text = str(value).lower()
                for area in areas:
                    if re.search(r'\b' + re.escape(area) + r'\b', text):
                        area_counts[area] += 1
    
    return area_counts

def main():
    print("="*70)
    print("PRT SURVEY DATA ANALYSIS")
    print("="*70)
    
    df = pd.read_csv('/Users/vinaynareddy/Downloads/PRT_SurveyData_.csv')
    print(f"\nLoaded {len(df)} responses with {len(df.columns)} columns")
    
    # Clean
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].fillna('').astype(str).str.strip()
    
    print("\n" + "="*70)
    print("[1] ROUTE EXTRACTION")
    print("="*70)
    route_counts = extract_routes(df)
    print(f"Found {len(route_counts)} unique routes")
    print("\nTop 20 Most Mentioned Routes:")
    for route, count in route_counts.most_common(20):
        print(f"  Route {route}: {count}")
    
    print("\n" + "="*70)
    print("[2] ACTION TYPE CLASSIFICATION")
    print("="*70)
    action_counts = classify_action_types(df)
    print("Action Type Distribution:")
    for action, count in sorted(action_counts.items(), key=lambda x: -x[1]):
        if count > 0:
            print(f"  {action}: {count}")
    
    print("\n" + "="*70)
    print("[3] GEOGRAPHIC ENTITIES")
    print("="*70)
    area_counts = extract_geographic_entities(df)
    print("Top 15 Geographic Areas:")
    for area, count in area_counts.most_common(15):
        if count > 0:
            print(f"  {area.title()}: {count}")
    
    # Save
    os.makedirs('/Users/vinaynareddy/Documents/ds_practicum/data/processed', exist_ok=True)
    os.makedirs('/Users/vinaynareddy/Documents/ds_practicum/reports', exist_ok=True)
    
    pd.DataFrame(route_counts.most_common(), columns=['Route', 'Count']).to_csv('/Users/vinaynareddy/Documents/ds_practicum/data/processed/routes_mentioned.csv', index=False)
    pd.DataFrame([{'Action_Type': k, 'Count': v} for k, v in action_counts.items()]).to_csv('/Users/vinaynareddy/Documents/ds_practicum/data/processed/action_types.csv', index=False)
    pd.DataFrame(area_counts.most_common(), columns=['Area', 'Count']).to_csv('/Users/vinaynareddy/Documents/ds_practicum/data/processed/geographic_areas.csv', index=False)
    
    insights = {
        'total_responses': len(df),
        'unique_routes': len(route_counts),
        'top_routes': route_counts.most_common(15),
        'action_types': action_counts,
        'top_areas': area_counts.most_common(15)
    }
    with open('/Users/vinaynareddy/Documents/ds_practicum/reports/insights.json', 'w') as f:
        json.dump(insights, f, indent=2)
    
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)
    print("\nFiles saved:")
    print("  - data/processed/routes_mentioned.csv")
    print("  - data/processed/action_types.csv")
    print("  - data/processed/geographic_areas.csv")
    print("  - reports/insights.json")

if __name__ == "__main__":
    main()

