#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pytest
import requests_mock
from show_player_info import fetch_tft_data_to_dataframe  # Import the function to be tested

@pytest.fixture
def mock_api_responses():
    with requests_mock.Mocker() as mock:
        # Mock response for summoner details
        mock.get("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/test_summoner",
                 json={"id": "test_id", "puuid": "test_puuid"},
                 status_code=200)
        # Mock response for TFT league data
        mock.get("https://na1.api.riotgames.com/tft/league/v1/entries/by-summoner/test_id",
                 json=[{"leaguePoints": 100, "wins": 20}],
                 status_code=200)
        yield

def test_fetch_tft_data_to_dataframe(mock_api_responses):
    df = fetch_tft_data_to_dataframe("test_api_key")
    
    # Assertions to validate the output
    assert df is not None
    assert df['leaguePoints'][0] == 100
    assert df['wins'][0] == 20


# In[ ]:




