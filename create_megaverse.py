import requests
import json
import time


class CelestialObjectCreator:
    def __init__(self, candidate_id) -> None:
        self.candidate_id = candidate_id

    def create_polyanet(self, positions) -> None:
        api_url = "https://challenge.crossmint.io/api/polyanets"
        headers = {"Content-Type": "application/json"}

        # Bulk update was not supported by this api, so proceeding with individual update
        for row, col in positions:
            data = {"row": row, "column": col, "candidateId": self.candidate_id}
            try:
                response = requests.post(
                    api_url, data=json.dumps(data), headers=headers
                )
                response.raise_for_status()  # Raise an exception if the request fails
            except requests.exceptions.RequestException as e:
                print(f"Failed to create polyanet at ({row}, {col}): {e}")

            time.sleep(2)  # Add a delay of 3 seconds between requests


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
        # For bulk polyanets position update
        polyanet_positions = []
        for row_index in range(len(map_data)):
            for col_index in range(len(map_data[0])):
                if map_data[row_index][col_index] != "SPACE":
                    string = map_data[row_index][col_index].lower()
                    if string == "polyanet":
                        polyanet_positions.append((row_index, col_index))

        celestial_object.create_polyanet(polyanet_positions)


def main():
    candidate_id = "3651da6b-463f-474f-bf58-2fb4edf94e5e"
    map_processor = MapProcessor(candidate_id)
    map_processor.process_map()


if __name__ == "__main__":
    main()
