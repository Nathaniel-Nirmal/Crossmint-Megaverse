import requests
import json
import time


class CelestialObjectCreator:
    def __init__(self, candidate_id) -> None:
        self.candidate_id = candidate_id

    def create_object(self, object_type, position, additional_data=None):
        api_url_base = "https://challenge.crossmint.io/api/"
        headers = {"Content-Type": "application/json"}
        data = {
            "candidateId": self.candidate_id,
            "row": position[0],
            "column": position[1],
        }

        if object_type == "polyanet":
            api_url = f"{api_url_base}polyanets"
        elif object_type == "soloon":
            api_url = f"{api_url_base}soloons"
            data.update(additional_data)  # Assuming color or other specifics are needed
        elif object_type == "cometh":
            api_url = f"{api_url_base}comeths"
            data.update(additional_data)  # Assuming direction is needed

        try:
            response = requests.post(api_url, data=json.dumps(data), headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to create {object_type} at {position}: {e}")

        time.sleep(2)  # Adjust based on API rate limits


class MapProcessor:
    def __init__(self, candidate_id) -> None:
        self.candidate_id = candidate_id

    def get_goal_map(self):
        api_map_url = f"https://challenge.crossmint.io/api/map/{self.candidate_id}/goal"
        response = requests.get(api_map_url)
        if response.status_code == 200:
            return response.json().get("goal")
        else:
            print("Failed to retrieve map data")
            return []

    def process_map(self):
        celestial_object_creator = CelestialObjectCreator(self.candidate_id)
        map_data = self.get_goal_map()

        for row_index, row in enumerate(map_data):
            for col_index, cell in enumerate(row):
                if cell != "SPACE":
                    if "POLYanet" in cell:
                        celestial_object_creator.create_object(
                            "polyanet", (row_index, col_index)
                        )
                    elif "SOLoon" in cell:
                        # Extract additional SOLoon data here
                        celestial_object_creator.create_object(
                            "soloon",
                            (row_index, col_index),
                            additional_data={"color": "example"},
                        )
                    elif "comETH" in cell:
                        # Extract comETH direction here
                        celestial_object_creator.create_object(
                            "cometh",
                            (row_index, col_index),
                            additional_data={"direction": "N"},
                        )


def main():
    candidate_id = "your-candidate-id"
    map_processor = MapProcessor(candidate_id)
    map_processor.process_map()
