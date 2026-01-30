"""Capitalize first English letter in JSON mappings.

Updates:
- data/en2mm.json: capitalize first letter of each key if it's A-Z/a-z
- data/mm2en.json: capitalize first letter of each value if it's A-Z/a-z
"""

from __future__ import annotations

import json
import string
from pathlib import Path


ASCII_LETTERS = set(string.ascii_letters)


def _capitalize_first_english(text: str) -> str:
	if not text:
		return text
	first = text[0]
	if first in ASCII_LETTERS:
		return first.upper() + text[1:]
	return text


def _load_json(path: Path) -> dict:
	with path.open("r", encoding="utf-8") as file:
		return json.load(file)


def _save_json(path: Path, data: dict) -> None:
	with path.open("w", encoding="utf-8") as file:
		json.dump(data, file, ensure_ascii=False, indent=4)
		file.write("\n")


def _update_en2mm(path: Path) -> None:
	data = _load_json(path)
	updated: dict[str, str] = {}
	conflicts: list[str] = []
	for key, value in data.items():
		new_key = _capitalize_first_english(str(key))
		if new_key in updated and updated[new_key] != value:
			conflicts.append(new_key)
			continue
		updated[new_key] = value

	_save_json(path, updated)

	if conflicts:
		conflict_list = ", ".join(sorted(set(conflicts)))
		print(f"[en2mm] Conflicting keys skipped: {conflict_list}")


def _update_mm2en(path: Path) -> None:
	data = _load_json(path)
	updated: dict[str, str] = {}
	for key, value in data.items():
		new_value = _capitalize_first_english(str(value))
		updated[key] = new_value

	_save_json(path, updated)


def main() -> None:
	base_dir = Path(__file__).resolve().parent
	data_dir = base_dir / "data"
	en2mm_path = data_dir / "en2mm.json"
	mm2en_path = data_dir / "mm2en.json"

	if not en2mm_path.exists():
		raise FileNotFoundError(f"Missing file: {en2mm_path}")
	if not mm2en_path.exists():
		raise FileNotFoundError(f"Missing file: {mm2en_path}")

	_update_en2mm(en2mm_path)
	_update_mm2en(mm2en_path)


if __name__ == "__main__":
	main()
