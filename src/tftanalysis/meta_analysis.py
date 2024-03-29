#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
from tabulate import tabulate
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns

# Function to retrieve the summoner's PUUID and TFT data
def fetch_summoner_data(api_key):
    """
    Fetches the PUUID of a summoner based on their summoner name.
    
    Parameters:
    api_key (str): The API key for accessing Riot Games API.
    
    Returns:
    str: The PUUID of the summoner if found, otherwise None.
    
    Example:
    puuid = fetch_summoner_data('YOUR_RIOT_API_KEY')
    """
    # Function to get summoner ID and PUUID
    def get_summoner_details(summoner_name, api_key):
        url = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
        headers = {"X-Riot-Token": api_key}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get("id"), data.get("puuid")
        else:
            print(f"Failed to retrieve summoner details: {response.status_code}")
            return None, None

    summoner_name = input("Please enter your summoner name: ")
    summoner_id, puuid = get_summoner_details(summoner_name, api_key)
    if summoner_id and puuid:
        print("Summoner details retrieved successfully.")
        return puuid
    else:
        print("Summoner name not found or an error occurred.")
        return None

# Function to fetch match history
def fetch_match_history(puuid, api_key):
    """
    Fetches the recent match history of a summoner using their PUUID.
    
    Parameters:
    puuid (str): The PUUID of the summoner.
    api_key (str): The API key for accessing Riot Games API.
    
    Returns:
    list: A list of match IDs if successful, otherwise None.
    
    Example:
    match_history = fetch_match_history('SUMMONER_PUUID', 'YOUR_RIOT_API_KEY')
    """
    url = f"https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?start=0&count=20"
    headers = {"X-Riot-Token": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve match history: {response.status_code}")
        return None

# Function to fetch details of a specific match
def fetch_match_details(match_id, api_key):
    """
    Fetches details for a specific TFT match using the match ID.
    
    Parameters:
    match_id (str): The ID of the match to fetch details for.
    api_key (str): The API key for accessing Riot Games API.
    
    Returns:
    dict: A dictionary containing match details if successful, otherwise None.
    
    Example:
    match_details = fetch_match_details('MATCH_ID', 'YOUR_RIOT_API_KEY')
    """
    url = f"https://americas.api.riotgames.com/tft/match/v1/matches/{match_id}"
    headers = {"X-Riot-Token": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve match details: {response.status_code}")
        return None
    
def frequency_analysis(matches):
    """
    Performs a frequency analysis on the provided matches, counting the occurrences of champions, traits, and items.
    
    Parameters:
    matches (list): A list of match details.
    
    Returns:
    tuple: Three Counters for champions, traits, and items, respectively.
    
    Example:
    champion_count, trait_count, item_count = frequency_analysis(match_data)
    """

    champion_count = Counter()
    trait_count = Counter()
    item_count = Counter()

    for match in matches:
        for participant in match['info']['participants']:
            for unit in participant['units']:
                champion_count[unit['character_id']] += 1
                for item in unit.get('itemNames', []):
                    item_count[item] += 1
            for trait in participant['traits']:
                if trait['tier_current'] > 0:  # Only count active traits
                    trait_count[trait['name']] += 1

    return champion_count, trait_count, item_count

def correlation_analysis(matches):
    """
    Analyzes the correlation of champion usage in top placements in matches.
    
    Parameters:
    matches (list): A list of match details.
    
    Returns:
    Counter: A Counter representing common patterns in top placements.
    
    Example:
    top_placement_patterns = correlation_analysis(match_data)
    """
    # This can get complex and might require statistical models to identify correlations
    # For simplicity, this example will just identify common patterns in top placements

    top_placement_patterns = Counter()
    for match in matches:
        for participant in match['info']['participants']:
            if participant['placement'] <= 4:  # Assuming top 4 as high placement
                pattern = frozenset(unit['character_id'] for unit in participant['units'])
                top_placement_patterns[pattern] += 1
    return top_placement_patterns

def trend_analysis(matches):
    # Trend analysis over time. This requires match data to be sorted by date.
    # Implementing a full trend analysis is complex and would need more space than allowed here.
    # This function is a placeholder for where that analysis would go.
    pass

def plot_top_usage(counter, title, ylabel, num_top=10):
    """
    Plots the top usage statistics for champions, traits, or items.
    
    Parameters:
    counter (Counter): A Counter object with the items to plot.
    title (str): The title for the plot.
    ylabel (str): The label for the Y-axis.
    num_top (int, optional): The number of top items to plot. Defaults to 10.
    
    Example:
    plot_top_usage(champion_count, 'Top Champions', 'Champion')
    """
    top_items = counter.most_common(num_top)
    labels, values = zip(*top_items)

    plt.figure(figsize=(10, 6))
    sns.barplot(list(values), list(labels), palette='viridis')
    plt.title(title)
    plt.xlabel('Count')
    plt.ylabel(ylabel)
    plt.show()

def visualize_data(champion_count, trait_count, item_count):
    """
    Visualizes the data of top champions, traits, and items using bar plots.

    Parameters:
    champion_count (Counter): Counter of champions.
    trait_count (Counter): Counter of traits.
    item_count (Counter): Counter of items.

    No return value.
    """
    plot_top_usage(champion_count, 'Top Champions', 'Champion')
    plot_top_usage(trait_count, 'Top Traits', 'Trait')
    plot_top_usage(item_count, 'Top Items', 'Item')

def generate_report(champion_count, trait_count, item_count, top_placement_patterns, total_matches):
    """
    Generates a textual report from the analysis results.

    Parameters:
    champion_count (Counter): Counter of champions.
    trait_count (Counter): Counter of traits.
    item_count (Counter): Counter of items.
    top_placement_patterns (Counter): Counter of top placement patterns.
    total_matches (int): Total number of matches analyzed.

    Returns:
    str: A formatted string representing the analysis report.
    """
    def format_counter(counter):
        total = sum(counter.values())
        return {k: f"{v} ({v / total:.2%})" for k, v in counter.most_common(10)}

    report = "TFT Meta Analysis Report\n"
    report += "-----------------------\n\n"
    
    report += "Top Champions (Usage %):\n"
    for champ, count in format_counter(champion_count).items():
        report += f"- {champ}: {count}\n"
    report += "\n"

    report += "Top Traits (Usage %):\n"
    for trait, count in format_counter(trait_count).items():
        report += f"- {trait}: {count}\n"
    report += "\n"

    report += "Top Items (Usage %):\n"
    for item, count in format_counter(item_count).items():
        report += f"- {item}: {count}\n"
    report += "\n"

    report += "Common Patterns in Top Placements (Count in Top 4):\n"
    for pattern, count in top_placement_patterns.most_common(5):
        report += f"- {', '.join(pattern)}: {count} times\n"
    report += "\n"

    report += "Summary:\n"
    report += "The above data represents the most commonly used champions, traits, and items among the top players in the analyzed matches. "
    report += "Frequent patterns in top placements suggest successful combinations for competitive play.\n"

    return report

def get_api_key_from_user():
    """
    Prompts the user to enter their Riot API Key and returns it.
    """
    api_key = input("Please enter your Riot API Key: ").strip()
    return api_key

def main_menu_meta():
    api_key = get_api_key_from_user()
    if not api_key:
        print("API Key is required to proceed. Exiting the program.")
        return

    puuid = fetch_summoner_data(api_key)
    if not puuid:
        return

    match_ids = fetch_match_history(puuid, api_key)
    if not match_ids:
        return

    matches = [fetch_match_details(match_id, api_key) for match_id in match_ids]

    # Perform analyses
    champion_count, trait_count, item_count = frequency_analysis(matches)
    top_placement_patterns = correlation_analysis(matches)

    # Generate and print the report
    total_matches = len(matches)
    report = generate_report(champion_count, trait_count, item_count, top_placement_patterns, total_matches)
    print(report)
    
    # Visualize the data
    visualize_data(champion_count, trait_count, item_count)

if __name__ == "__main__":
    main_menu_meta()


# In[ ]:




