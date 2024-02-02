import requests
import json


class CelestialObjectCreator:
    def __init__(self, candidate_id) -> None:
        self.candidate_id = candidate_id

    def create_polyanet(self, positions) -> None:
        api_url = "https://challenge.crossmint.io/api/polyanets"
        polyanet_data = [{"row": row, "column": col, "candidateId": self.candidate_id} for row, col in positions]
        headers = {"Content-Type": "application/json"}
        requests.post(api_url, data=json.dumps(polyanet_data), headers=headers)


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
