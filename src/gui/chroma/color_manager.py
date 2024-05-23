import json
import os
import re
from typing import List, Dict
from color import Color

class ColorManager:
    def __init__(self, json_file_path: str):
        self.json_file_path = json_file_path
        self.colors_data = self.load_colors()
        self.colors_cache = {}

    def load_colors(self) -> Dict[str, Dict]:
        if os.path.exists(self.json_file_path):
            with open(self.json_file_path, 'r') as file:
                return json.load(file)
        return {}

    def save_colors(self):
        with open(self.json_file_path, 'w') as file:
            json.dump(self.colors_data, file, indent=4)

    def add_color_if_not_exists(self, color_name_snake: str, new_color_data: dict):
        self.colors_data[color_name_snake] = new_color_data
        self.save_colors()
        print(f"Added new color: {color_name_snake} - {new_color_data['code']}")

    def get_color(self, color_identifier: str) -> Color:
        formatted_color_identifier = color_identifier.lstrip('#').lower()

        for name, color_info in self.colors_data.items():
            if color_info["code"].lstrip('#').lower() == formatted_color_identifier or name == formatted_color_identifier:
                if name in self.colors_cache:
                    return self.colors_cache[name]

                color = Color(
                    name=color_info['name'],
                    code=color_info['code'],
                    brighten=color_info.get('Brighten', {}).get('colors', []),
                    darken=color_info.get('Darken', {}).get('colors', []),
                    desaturate=color_info.get('Desaturate', {}).get('colors', []),
                    hue=color_info.get('Hue', {}).get('colors', []),
                    analogous=color_info.get('Analogous', {}).get('colors', []),
                    monochromatic=color_info.get('Monochromatic', {}).get('colors', []),
                    complementary=color_info.get('Complementary', {}).get('colors', []),
                    split_complement=color_info.get('Split Complement', {}).get('colors', []),
                    triad=color_info.get('Triad', {}).get('colors', []),
                    tetrad=color_info.get('Tetrad', {}).get('colors', [])
                )
                self.colors_cache[name] = color
                return color

        if re.match(r'^[0-9a-f]{6}$', formatted_color_identifier):
            from selenium_fetcher import SeleniumFetcher
            fetcher = SeleniumFetcher()
            color_name_snake, new_color_data = fetcher.fetch_color_data(formatted_color_identifier)
            self.add_color_if_not_exists(color_name_snake, new_color_data)
            return self.get_color(formatted_color_identifier)
        else:
            raise ValueError(f"Color '{color_identifier}' not found in data and is not a valid hex code.")

    def get_color_palette(self) -> List[str]:
        return list(self.colors_data.keys())
