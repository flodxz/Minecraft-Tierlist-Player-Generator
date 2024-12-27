import requests
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO



# Made by @.flod on Discord
# Shoot a message if you need any help

# ----------------------------------------------- #

def bold(to_bold: str) -> str:
    return '\033[1m' + to_bold + '\033[0m'

def green(to_green: str) -> str:
    return '\033[92m' + to_green + '\033[0m'

def red(to_red: str) -> str:
    return '\033[91m' + to_red + '\033[0m'

# ----------------------------------------------- #

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


def create_head_avatar(avatar_bytes, username, font_path, desired_font_size=32):
    """Generate head + name"""

    avatar = Image.open(BytesIO(avatar_bytes))
    
    padding = 10
    max_text_height = desired_font_size + 10
    new_width = avatar.width + padding * 2
    new_height = avatar.height + max_text_height + padding * 2
    
    final_image = Image.new('RGBA', (new_width, new_height), (0, 0, 0, 0))
    
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


def create_body_avatar(avatar_bytes, username, font_path, desired_font_size=64):
    """Generate body + nametag"""

    avatar = Image.open(BytesIO(avatar_bytes))
    
    padding = 10
    max_text_height = desired_font_size + 10
    new_width = max(avatar.width + padding * 2, 200)
    new_height = avatar.height + max_text_height + padding * 2
    
    final_image = Image.new('RGBA', (new_width, new_height), (0, 0, 0, 0))
    
    avatar_x = (new_width - avatar.width) // 2
    avatar_y = max_text_height + padding
    
    final_image.paste(avatar, (avatar_x, avatar_y))
    
    draw = ImageDraw.Draw(final_image)
    
    font = get_font_size_that_fits(draw, username, font_path, new_width - padding * 4, desired_font_size)
    text_bbox = draw.textbbox((0, 0), username, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    text_x = (new_width - text_width) // 2
    text_y = padding
    padding_x = 8
    padding_y = 4
    
    draw.rectangle(
        (text_x - padding_x, text_y - padding_y,
         text_x + text_width + padding_x, text_y + text_height + padding_y),
        fill=(0, 0, 0, 180)
    )
    
    draw.text((text_x + 1, text_y + 1), username, font=font, fill=(63, 63, 63))
    draw.text((text_x, text_y), username, font=font, fill=(255, 255, 255))
    
    return final_image


def get_generation_type():
    """User input"""

    while True:
        print("\n")
        print(bold("What would you like to generate?"))
        print("1. Both head and body avatars")
        print("2. Body avatars only")
        print("3. Head avatars only")
        print("\n")
        choice = input(bold("Enter your choice (1-3): ")).strip()
        
        if choice in ['1', '2', '3']:
            return choice
        print("Invalid choice. Please enter 1, 2, or 3.")


def download_and_save_avatar(uuid, username, head_folder, body_folder, font_path, generation_type, font_size_head=32, font_size_body=64):
    """Download and create final images based on user's choice"""
    if not uuid:
        print(f"Could not find UUID for {username}")
        return
    
    # Generate head avatar
    if generation_type in ['1', '3']:
        head_url = f"https://mc-heads.net/avatar/{uuid}"
        head_response = requests.get(head_url)
        
        if head_response.status_code == 200:
            head_image = create_head_avatar(head_response.content, username, font_path, font_size_head)
            head_path = head_folder / f"{username}.png"
            head_image.save(head_path, 'PNG')
            print(f"Successfully created head avatar for {username}")
        else:
            print(red(f"Failed to download head avatar for {username}"))
    
    # Generate body avatar
    if generation_type in ['1', '2']:
        body_url = f"https://nmsr.nickac.dev/fullbody/{uuid}"
        body_response = requests.get(body_url)
        
        if body_response.status_code == 200:
            body_image = create_body_avatar(body_response.content, username, font_path, font_size_body)
            body_path = body_folder / f"{username}.png"
            body_image.save(body_path, 'PNG')
            print(f"Successfully created body avatar for {username}")
        else:
            print(red(f"Failed to download body avatar for {username}"))
    

def main():
    head_folder = Path("Minecraft-Players-Head")
    body_folder = Path("Minecraft-Players-Body")

    generation_type = get_generation_type()
    
    head_folder.mkdir(exist_ok=True)
    body_folder.mkdir(exist_ok=True)
    

    # Path to Minecraft font
    # CHANGE IF YOU WANT TO USE A DIFFERENT FONT
    font_path = Path("Minecraft.ttf")
    
    if not font_path.exists():
        print(red("Warning: Minecraft.ttf not found in script directory!"))
    

    # Set your desired font size here 
    #       DEFAULT HEAD: 32
    #       DEFAULT BODY: 64
    # (will be automatically reduced if text is too wide)
    FONT_SIZE_HEAD = 32
    FONT_SIZE_BODY = 64
    
    try:
        with open("players.txt", 'r') as f:
            usernames = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(red("Error: players.txt not found!"))
        return
    
    print("\n")
    print(f"Found {len(usernames)} players in file")
    
    for username in usernames:
        uuid = get_uuid(username)
        if uuid:
            download_and_save_avatar(
                uuid,
                username,
                head_folder,
                body_folder,
                font_path,
                generation_type,
                font_size_head=FONT_SIZE_HEAD,
                font_size_body=FONT_SIZE_BODY
            )
    
    print("\n")
    print(green("Process completed!"))

if __name__ == "__main__":
    main()