from color_manager import ColorManager

# Example usage
colors_file_path = 'colors.json'
color_manager = ColorManager(colors_file_path)

# Accessing a color object using a friendly name
blue_gray = color_manager.get_color('#7393b3')
print(blue_gray.darken[0])  # This will print the first darkened color

# Accessing a color object using a hex code
hex_color = color_manager.get_color('#7eb373')
print(hex_color.brighten[0])  # This will print the first brightened color

# Accessing a color object using a hex code
hex_color = color_manager.get_color('#b373a8')
print(hex_color.brighten[0])  # This will print the first brightened color

# Getting the list of all accessible colors
color_palette = color_manager.get_color_palette()
print(color_palette)
