#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pytest
import requests_mock
from match_history import fetch_summoner_data, fetch_match_history  # Import other functions as needed

@pytest.fixture
def mock_api():
    with requests_mock.Mocker() as m:
        # Mock response for summoner details
        m.get("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/test_summoner",
              json={"id": "test_id", "puuid": "test_puuid"},
              status_code=200)
        # Mock response for match history
        m.get("https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/test_puuid/ids",
              json=["match1", "match2", "match3"],
              status_code=200)
        yield m

def test_fetch_summoner_data(mock_api):
    puuid = fetch_summoner_data("test_api_key")
    assert puuid == "test_puuid"

def test_fetch_match_history(mock_api):
    match_ids = fetch_match_history("test_puuid", "test_api_key")
    assert match_ids == ["match1", "match2", "match3"]

