# Minecraft Tierlist Player Generator
Generate player head avatars with usernames using the Minecraft font for multiple players at once.

---



## Installation Instructions

### Windows

1. Install [Python](https://www.python.org/downloads/):

2. Install required libraries:
     ```
     pip install requests Pillow
     ```
3. Open Command Prompt and run `main.py`
     ```
     cd path\to\folder
     python main.py
     ```


### Mac

1. Install [Python](https://www.python.org/downloads/):

2. Install required libraries:
     ```
     pip3 install requests
     pip3 install Pillow
     ```
3. Open Terminal and run `main.py`
     ```
     cd path\to\folder
     python3 main.py
     ```

---


## Setting Up the Files

Create your `players.txt`:
   - Open a text editor
   - Add one Minecraft username per line
   - Save the file

---

## Running the Script

### Windows
1. Open Command Prompt
2. Navigate to your project folder:
   ```
   cd path\to\your\folder
   ```
3. Run the script:
   ```
   python main.py
   ```

### Mac
1. Open Terminal
2. Navigate to your project folder:
   ```
   cd path/to/your/folder
   ```
3. Run the script:
   ```
   python3 main.py
   ```
---


## Customization
1. You can adjust the default font size by changing `DESIRED_FONT_SIZE`:

   ```python
   DESIRED_FONT_SIZE = 32 
   ```

2. You can change the font by putting a new font inside the folder and changing:

   ```python
   font_path = Path("Minecraft.ttf")
   ```

---

## Notes
- The script requires an internet connection to fetch avatars
- Processing time depends on the number of players
- Invalid usernames will be skipped with a warning message
- The font will automatically scale down for long usernames
