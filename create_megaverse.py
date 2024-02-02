import requests
import json

class MapProcessor:
    def __init__(self, candidate_id) -> None:
        self.candidate_id = candidate_id

    def get_goal_map(self):
        api_map_url = f"https://challenge.crossmint.io/api/map/{self.candidate_id}/goal"
        response = requests.get(api_map_url)
        map_data = response.json()['goal']
        return map_data

def main():
    candidate_id = "3651da6b-463f-474f-bf58-2fb4edf94e5e"
    map_processor = MapProcessor(candidate_id)
    print(map_processor.get_goal_map())
    

if __name__ == "__main__":
    main()
