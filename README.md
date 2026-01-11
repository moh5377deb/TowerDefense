# 🏰 TowerDefense — Python & Pygame

TowerDefense is a Tower Defense game developed in Python using the Pygame library.
The player must defend a base against successive waves of enemies by placing towers along a predefined path.
The game was created as a Terminale NSI project, focusing on object-oriented programming, data structures, and graphical interaction.

An instruction screen explains the controls before the game starts, and clear win/lose screens appear at the end of the game.

────────────────────────────────────────────────────────

📸 PREVIEW

(images/instructions.png)
(images/gameplay.png)
(images/victory.png)
(images/defeat.png)

────────────────────────────────────────────────────────

🧠 FEATURES

🎮 Interactive Tower Defense gameplay  
🧱 Grid-based map with predefined enemy paths  
🗼 Tower placement with limited capacity  
👾 Progressive enemy waves with increasing difficulty  
⚔️ Automatic tower attacks based on range and cadence  
❤️ Base health system with win/lose conditions  
📋 Instruction screen before the game starts  
🏁 Victory and defeat screens with confirmation button  
🎵 Integrated jukebox with multiple background musics  
⌨️ Keyboard and mouse controls  
🧰 Clean and structured object-oriented code  

────────────────────────────────────────────────────────

🧭 REQUIREMENTS

Software:
- Python 3.x
- Pygame library

Installation:
pip install pygame

────────────────────────────────────────────────────────

🚀 HOW TO RUN

1. Clone the repository:
git clone https://github.com/your-username/TowerDefense.git

2. Go into the folder:
cd TowerDefense

3. Run the game:
python TowerDefense.py

────────────────────────────────────────────────────────

🎮 CONTROLS

Mouse Left Click : Place a tower  
Button "Lancer la vague" : Start a wave  
SPACE : Change background music  
ESC : Quit the game  

────────────────────────────────────────────────────────

🧠 CODE STRUCTURE

- Ennemi class  
  Handles enemy movement, health, speed, damage, and path following.

- Tour class  
  Manages tower placement, range detection, damage, and attack cadence.

- Base class  
  Represents the base to defend and manages remaining lives.

- Jukebox class  
  Handles background music playback and switching.

- Main game loop  
  Manages events, updates, enemy spawning, attacks, rendering, and game states.

────────────────────────────────────────────────────────

📚 DATA STRUCTURES USED

deque:
The deque structure from the collections module is used to manage tower placement.
When the maximum number of towers is reached, the oldest tower is automatically removed.
This structure is efficient for adding and removing elements at both ends and fits well with this gameplay mechanic.

List copy [:]:
The [:] operator is used to create a copy of the music list:
self.file_musiques = musiques[:]
This prevents modifying the original list and avoids unwanted side effects.

────────────────────────────────────────────────────────

🛠️ POSSIBLE IMPROVEMENTS

- Add different tower types  
- Add enemy variety and bosses  
- Implement a score or currency system  
- Improve visuals and animations  

────────────────────────────────────────────────────────

📄 LICENSE

This project is for educational purposes (Terminale NSI).
