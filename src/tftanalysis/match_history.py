#!/usr/bin/env python
# coding: utf-8

# In[6]:


import requests
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict

# Function to retrieve the summoner's PUUID and TFT data
def fetch_summoner_data(api_key):
    """
    Fetches the PUUID of a summoner based on the summoner name.

    Parameters:
    api_key (str): The API key for Riot Games API.

    Returns:
    str: The PUUID of the summoner, or None if an error occurs.
    """
    # Function to get summoner ID and PUUID
    def get_summoner_details(summoner_name, api_key):
        """
        Fetches the summoner ID and PUUID from Riot Games API.

        Parameters:
        summoner_name (str): The name of the summoner.
        api_key (str): The API key for Riot Games API.

        Returns:
        tuple: A tuple containing the summoner ID and PUUID, or (None, None) if an error occurs.
        """
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
    Fetches the match history for a given PUUID.

    Parameters:
    puuid (str): The PUUID of the summoner.
    api_key (str): The API key for Riot Games API.

    Returns:
    list: A list of match IDs, or None if an error occurs.
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
    Fetches details of a specific match.

    Parameters:
    match_id (str): The ID of the match.
    api_key (str): The API key for Riot Games API.

    Returns:
    dict: A dictionary containing match details, or None if an error occurs.
    """
    url = f"https://americas.api.riotgames.com/tft/match/v1/matches/{match_id}"
    headers = {"X-Riot-Token": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve match details: {response.status_code}")
        return None

def get_api_key_from_user():
    """
    Prompts the user to enter their Riot API Key.

    Returns:
    str: The entered API Key.
    """
    api_key = input("Please enter your Riot API Key: ").strip()
    return api_key

def analyze_match(match_details):
    """
    Analyzes and displays various statistics from a TFT match.

    Parameters:
    match_details (dict): A dictionary containing details of the match.
    """
    # Participant Analysis
    participants_data = match_details['info']['participants']
    participants_df = pd.DataFrame(participants_data)
    summary_columns = ['placement', 'level', 'gold_left', 'players_eliminated', 'time_eliminated', 'total_damage_to_players']
    participants_summary_df = participants_df[summary_columns]
    print("\nParticipants Summary:")
    print(tabulate(participants_summary_df, headers='keys', tablefmt='psql', showindex=False))

    # Traits Analysis
    traits_analysis = defaultdict(lambda: {'count': 0, 'total_placement': 0, 'avg_placement': 0})
    for participant in participants_data:
        for trait in participant['traits']:
            trait_name = trait['name']
            traits_analysis[trait_name]['count'] += 1
            traits_analysis[trait_name]['total_placement'] += participant['placement']
    for trait, data in traits_analysis.items():
        data['avg_placement'] = data['total_placement'] / data['count']
    traits_df = pd.DataFrame(traits_analysis).T.reset_index()
    traits_df.rename(columns={'index': 'Trait', 'count': 'Usage Count', 'avg_placement': 'Average Placement'}, inplace=True)
    traits_df.sort_values(by=['Usage Count', 'Average Placement'], ascending=[False, True], inplace=True)
    print("\nTraits Analysis:")
    print(tabulate(traits_df, headers='keys', tablefmt='psql', showindex=False))

    # Items Analysis
    items_analysis = defaultdict(lambda: {'count': 0, 'total_placement': 0, 'avg_placement': 0})
    for participant in participants_data:
        for unit in participant['units']:
            for item in unit.get('itemNames', []):
                items_analysis[item]['count'] += 1
                items_analysis[item]['total_placement'] += participant['placement']
    for item, data in items_analysis.items():
        if data['count'] > 0:
            data['avg_placement'] = data['total_placement'] / data['count']
    items_df = pd.DataFrame(items_analysis).T.reset_index()
    items_df.rename(columns={'index': 'Item', 'count': 'Usage Count', 'avg_placement': 'Average Placement'}, inplace=True)
    items_df.sort_values(by=['Usage Count', 'Average Placement'], ascending=[False, True], inplace=True)
    print("\nItems Analysis:")
    print(tabulate(items_df, headers='keys', tablefmt='psql', showindex=False))

    # Visualizations
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Usage Count', y='Item', data=items_df, palette='viridis')
    plt.title('Item Usage Count in TFT Match')
    plt.xlabel('Usage Count')
    plt.ylabel('Item')
    plt.show()

    plt.figure(figsize=(12, 6))
    sns.barplot(x='Average Placement', y='Item', data=items_df, palette='magma')
    plt.title('Average Placement of Items in TFT Match')
    plt.xlabel('Average Placement')
    plt.ylabel('Item')
    plt.gca().invert_xaxis()
    plt.show()

def main():
    """
    Main function to run the program.
    """
    api_key = get_api_key_from_user()

    if api_key:
        puuid = fetch_summoner_data(api_key)
        if puuid:
            match_ids = fetch_match_history(puuid, api_key)
            if match_ids:
                print("\nFetched Match IDs:")
                for i, match_id in enumerate(match_ids, start=1):
                    print(f"{i}. {match_id}")

                # User selects which match to analyze
                selection = input("\nEnter the number of the match you want to analyze: ")
                try:
                    selected_index = int(selection) - 1
                    if 0 <= selected_index < len(match_ids):
                        selected_match_id = match_ids[selected_index]
                        match_details = fetch_match_details(selected_match_id, api_key)
                        if match_details:
                            analyze_match(match_details)
                    else:
                        print("Invalid selection. Please enter a number from the list.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
    else:
        print("API Key is required to proceed. Exiting the program.")

if __name__ == "__main__":
    main()


# In[ ]:




