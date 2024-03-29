import requests
import json
import time


class CelestialObjectCreator:
    def __init__(self, candidate_id) -> None:
        self.candidate_id = candidate_id

    def create_object(self, object_type, positions, additional_data=None) -> None:
        api_url_base = "https://challenge.crossmint.io/api/"
        headers = {"Content-Type": "application/json"}
        data = {
            "candidateId": self.candidate_id,
            "row": positions[0],
            "column": positions[1],
        }
        if object_type == "polyanet":
            api_url = f"{api_url_base}polyanets"
        elif object_type == "soloon":
            api_url = f"{api_url_base}soloons"
            data.update(additional_data)  # To add color
        elif object_type == "cometh":
            api_url = f"{api_url_base}comeths"
            data.update(additional_data)  # To add direction

        try:
            response = requests.post(api_url, data=json.dumps(data), headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to create {object_type} at {positions}: {e}")

        time.sleep(2)  # Adjust based on API rate limits


class MapProcessor:
    def __init__(self, candidate_id) -> None:
        self.candidate_id = candidate_id

    def get_goal_map(self):
        api_map_url = f"https://challenge.crossmint.io/api/map/{self.candidate_id}/goal"
        response = requests.get(api_map_url)
        map_data = response.json()["goal"]
        return map_data

    def process_map(self):
        celestial_object = CelestialObjectCreator(self.candidate_id)
        map_data = self.get_goal_map()

        for row_index, row in enumerate(map_data):
            for col_index, cell in enumerate(row):
                if cell != "SPACE":
                    item = cell.lower()
                    if "polyanet" in item:
                        celestial_object.create_object(
                            "polyanet", (row_index, col_index)
                        )
                    elif "soloon" in item:
                        # Extract color data here
                        celestial_object.create_object(
                            "soloon",
                            (row_index, col_index),
                            additional_data={"color": item.split("_")[0]},
                        )
                    elif "cometh" in item:
                        # Extract direction direction here
                        celestial_object.create_object(
                            "cometh",
                            (row_index, col_index),
                            additional_data={"direction": item.split("_")[0]},
                        )


def main():
    candidate_id = "3651da6b-463f-474f-bf58-2fb4edf94e5e"
    map_processor = MapProcessor(candidate_id)
    map_processor.process_map()


if __name__ == "__main__":
    main()
