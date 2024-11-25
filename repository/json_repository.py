import json
from repository.abstract_repository import AbstractRepository

class JSONRepository(AbstractRepository):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = self._load_data()

    def _load_data(self):
        try:
            with open(self.file_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _save_data(self):
        with open(self.file_path, "w") as f:
            json.dump(self.data, f, indent=4)

    def add(self, entity):
        entity_id = len(self.data.get("entities", [])) + 1
        entity["id"] = entity_id
        self.data.setdefault("entities", []).append(entity)
        self._save_data()

    def get_by_id(self, entity_id):
        return next((e for e in self.data.get("entities", []) if e["id"] == entity_id), None)

    def get_all(self):
        return self.data.get("entities", [])

    def delete(self, entity_id):
        entities = self.data.get("entities", [])
        self.data["entities"] = [e for e in entities if e["id"] != entity_id]
        self._save_data()

    def update(self, entity):
        entities = self.data.get("entities", [])
        for i, e in enumerate(entities):
            if e["id"] == entity["id"]:
                entities[i] = entity
                break
        self.data["entities"] = entities
        self._save_data()
