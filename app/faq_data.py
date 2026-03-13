from __future__ import annotations

import json
from pathlib import Path


FAQ_PATH = Path(__file__).resolve().parent.parent / "data" / "faq.json"


def load_faq_items() -> list[dict[str, str]]:
    with FAQ_PATH.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError("FAQ data must be a list of objects.")

    items: list[dict[str, str]] = []
    for item in data:
        if not isinstance(item, dict):
            raise ValueError("Each FAQ item must be an object.")

        faq_id = str(item.get("id", "")).strip()
        question = str(item.get("question", "")).strip()
        answer = str(item.get("answer", "")).strip()

        if not faq_id or not question or not answer:
            raise ValueError("Each FAQ item must contain non-empty id, question, and answer.")

        items.append({"id": faq_id, "question": question, "answer": answer})

    return items


def get_faq_item(faq_id: str) -> dict[str, str] | None:
    for item in load_faq_items():
        if item["id"] == faq_id:
            return item
    return None
