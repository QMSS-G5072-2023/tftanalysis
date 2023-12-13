#!/usr/bin/env python
# coding: utf-8

# In[1]:


# pip install requests


# In[7]:


import requests
import pandas as pd
from tabulate import tabulate

# Function to retrieve and display the TFT data as a DataFrame
def fetch_tft_data_to_dataframe(api_key):
    """Fetches TFT data for a given summoner and displays it as a DataFrame.

    Args:
    - api_key (str): Riot API Key for authorization.

    Returns:
    - pd.DataFrame or None: DataFrame containing TFT data or None if no data found.
    """
    # Function to get summoner ID
    def get_summoner_id(summoner_name, api_key):
        url = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
        headers = {
            "X-Riot-Token": api_key
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get("id")
        else:
            print(f"Failed to retrieve summoner ID: {response.status_code}")
            return None

    # Function to get TFT league entries
    def get_tft_league_entries(summoner_id, api_key):
        url = f"https://na1.api.riotgames.com/tft/league/v1/entries/by-summoner/{summoner_id}"
        headers = {
            "X-Riot-Token": api_key
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to retrieve TFT league data: {response.status_code}")
            return None

    # Main process to fetch data
    while True:
        summoner_name = input("Please enter your summoner name: ")
        summoner_id = get_summoner_id(summoner_name, api_key)
        if summoner_id:
            tft_data = get_tft_league_entries(summoner_id, api_key)
            if tft_data:
                print("Data retrieved successfully.")
                df = pd.DataFrame(tft_data)
                return df
            else:
                print("No TFT data found for this summoner. Try again.")
        else:
            print("Summoner name not found or an error occurred. Try again.")
            
# Function to ask the user which specific data they want to check
def get_user_selected_data(df):
    """Allows the user to select specific TFT data to display from the DataFrame.

    Args:
    - df (pd.DataFrame): DataFrame containing TFT data.

    Returns:
    - None
    """
    columns = df.columns.tolist()
    columns.append('Stop')

    while True:  # Start of the loop
        print("\nWhich data would you like to check? Here are the available options:")
        for i, column in enumerate(columns, 1):
            print(f"{i}. {column}")

        selection = input("\nEnter the number of the option you want to check, or type 'Stop' to end: ")
        if selection.lower() == 'stop':
            print("Exiting the data check.")
            break  # Exit the loop

        try:
            selected_index = int(selection) - 1
            selected_column = columns[selected_index]
            print(f"\nHere is the data for {selected_column}:")
            print(tabulate(pd.DataFrame(df[selected_column]), headers=[selected_column], tablefmt='psql', showindex=False))

            # Ask if the user wants to continue
            continue_choice = input("\nDo you want to check more data? (yes/no): ")
            if continue_choice.lower() != 'yes':
                print("Exiting the data check.")
                break  # Exit the loop if the user does not want to continue

        except (ValueError, IndexError):
            print("Invalid selection. Please enter a valid number or type 'Stop' to end.")

def get_user_api_key():
    """Prompts the user to enter their Riot API Key.

    Returns:
    - str: User-entered Riot API Key.
    """
    # Prompt the user to enter their API key
    api_key = input("Please enter your Riot API Key: ").strip()
    return api_key

def main_menu():
    """Main function to execute the TFT Player Information System."""
    print("Welcome to the TFT Player Information System.")
    user_api_key = get_user_api_key()

    if not user_api_key:
        print("No API Key was entered. Exiting the program.")
        return

    df = fetch_tft_data_to_dataframe(user_api_key)
    if df is not None:
        print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
        get_user_selected_data(df)
    else:
        print("No data to display. Exiting the program.")

if __name__ == "__main__":
    main_menu()


# In[ ]:




