import json
import uuid
import datetime
from pathlib import Path

class JsonlLogger:
    """
    Simple append-only JSONL logger to track conversations. Each line is a JSON object:
    { id, timestamp, question, answer, confidence, metadata }
    """
    def __init__(self, path="conversations.jsonl"):
        self.path = Path(path)
        # Ensure parent directory exists if user stores this in a subdirectory
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, question, answer, confidence=None, metadata=None):
        record = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "question": question,
            "answer": str(answer),
            "confidence": float(confidence) if confidence is not None else None,
            "metadata": metadata or {}
        }
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        return record