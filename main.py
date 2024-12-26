import requests
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont



# Made by @.flod on Discord


def get_uuid(username):
    """Convert Minecraft username to UUID using Mojang API"""
    response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
    if response.status_code == 200:
        return response.json()['id']
    return None

def get_font_size_that_fits(draw, username, font_path, max_width, desired_size):
    """Calculate the largest font size that will fit within max_width"""
    font_size = desired_size
    
    while font_size > 8:  # Don't let font get smaller than 8pt
        try:
            font = ImageFont.truetype(font_path, font_size)
        except Exception:
            return ImageFont.load_default()
            
        text_bbox = draw.textbbox((0, 0), username, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        
        if text_width <= max_width:
            return font
            
        font_size -= 1
    
    return ImageFont.truetype(font_path, 8)

def create_avatar_with_name(avatar_bytes, username, font_path, desired_font_size=32):
    """Generates image with the avatar and username below it"""
    avatar = Image.open(BytesIO(avatar_bytes))
    
    padding = 10
    max_text_height = desired_font_size + 10
    new_width = avatar.width + padding * 2
    new_height = avatar.height + max_text_height + padding * 2
    
    final_image = Image.new('RGBA', (new_width, new_height), (255, 255, 255, 0))
    
    avatar_x = (new_width - avatar.width) // 2
    final_image.paste(avatar, (avatar_x, padding))
    
    draw = ImageDraw.Draw(final_image)
    
    font = get_font_size_that_fits(draw, username, font_path, avatar.width, desired_font_size)
    
    text_bbox = draw.textbbox((0, 0), username, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (new_width - text_width) // 2
    text_y = avatar.height + padding + 5
    
    draw.text((text_x + 1, text_y + 1), username, font=font, fill=(63, 63, 63))
    draw.text((text_x, text_y), username, font=font, fill=(255, 255, 255))
    
    return final_image

def download_avatar(uuid, username, folder, font_path, desired_font_size=32):
    """Download player head avatar from mc-heads.net and add username"""
    if uuid:
        avatar_url = f"https://mc-heads.net/avatar/{uuid}"
        response = requests.get(avatar_url)
        
        if response.status_code == 200:
            final_image = create_avatar_with_name(response.content, username, font_path, desired_font_size)
            
            file_path = folder / f"{username}.png"
            final_image.save(file_path, 'PNG')
            print(f"Successfully created avatar with name for {username}")
        else:
            print(f"Failed to download avatar for {username}")
    else:
        print(f"Could not find UUID for {username}")

def main():
    output_folder = Path("Minecraft-Players")
    output_folder.mkdir(exist_ok=True)
    
    # Path to Minecraft font
    # CHANGE IF YOU WANT TO USE A DIFFERENT FONT
    font_path = Path("Minecraft.ttf")
    if not font_path.exists():
        print("Warning: Minecraft.ttf not found in script directory!")
    
    # Set your desired font size here - DEFAULT: 32
    # (will be automatically reduced if text is too wide)
    DESIRED_FONT_SIZE = 32
    
    try:
        with open("players.txt", 'r') as f:
            usernames = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("Error: players.txt not found!")
        return
    
    print(f"Found {len(usernames)} players in file")
    
    for username in usernames:
        uuid = get_uuid(username)
        download_avatar(uuid, username, output_folder, font_path, DESIRED_FONT_SIZE)
        
    print("\nProcess completed!")

if __name__ == "__main__":
    from io import BytesIO
    main()