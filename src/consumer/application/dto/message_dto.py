from dataclasses import dataclass

@dataclass
class MessageDto:
    sender: str
    message: str

    @classmethod
    def from_json(cls, json_data):
        return cls(**json_data)