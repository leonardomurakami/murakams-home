import json
from pathlib import Path
from typing import Dict, List

DATA_DIR = Path("static/data")
PROJECTS_FILE = DATA_DIR / "projects.json"
CONTACTS_FILE = DATA_DIR / "contacts.json"

def load_projects() -> List[Dict]:
    """Load local projects from JSON file."""
    if PROJECTS_FILE.exists():
        with PROJECTS_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_contact(name: str, email: str, message: str) -> None:
    """Persist contact form submissions to a JSON file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    contacts: List[Dict] = []
    if CONTACTS_FILE.exists():
        with CONTACTS_FILE.open("r", encoding="utf-8") as f:
            contacts = json.load(f)
    contacts.append({"name": name, "email": email, "message": message})
    with CONTACTS_FILE.open("w", encoding="utf-8") as f:
        json.dump(contacts, f, ensure_ascii=False, indent=2)
