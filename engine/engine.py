import pygame
import sys
import os
import typing

from game.level import Generator
from .sound import SoundManager
from .entity import EntityManager
from .screen_manager import *
from .screen import Screen
from .ui import *

class Assets: 
    def __init__(self) -> None:
        self.assets = {}
        self.load()  # Load assets upon initialization
    
    def load(self):
        # Load all images from the assets/images directory
        dir = os.walk("assets/images")
        for d in dir:
            for file in d[2]:
                if file.split(".")[-1] == "png":
                    if file.startswith("sheet"):
                        sheet = pygame.image.load(d[0] + "/" + file)
                        sheet.set_colorkey((0,0,0))
                        for i in range(sheet.get_width()//32):
                            self.assets[f"{file.split('_')[1].split('.')[0]}_{i}"] = pygame.Surface((32,32), pygame.SRCALPHA)
                            self.assets[f"{file.split('_')[1].split('.')[0]}_{i}"].blit(sheet, (0,0), (i*32,0,32,32))
                    self.assets[file.split(".")[0]] = pygame.image.load(d[0] + "/" + file)
                    self.assets[file.split(".")[0]].set_colorkey((0,0,0))
       

    def get(self, key):
        # Retrieve an asset by key, return "null" asset if key is not found
        return self.assets.get(key, self.assets["null"])
    
    def get_frame(self, key, frame):
        # Retrieve a specific frame of an asset by key and frame number
        return self.assets.get(f"{key}_{frame}", self.assets["null"])

class Engine:
    def __init__(self, screens):
        self.assets = Assets()  # Initialize the Assets class
        self.config, self.keybinds = self.load_config()  
        self.running = True  
        
        # Setup the display
        self.screen = pygame.display.set_mode((int(self.config.get("SCREEN_WIDTH")), int(self.config.get("SCREEN_HEIGHT"))))
        
        # Initialize managers
        self.sound_manager = SoundManager(self)
        self.entity_manager = EntityManager()
        self.screen_manager = ScreenManager(self, "menu", screens)
        
        self.clock = pygame.time.Clock()  # Initialize the game clock
        self.gui = Screen(self.screen_manager)  # Initialize the GUI
        self.console = Console(self)  # Initialize the Console

    def run(self):
        while self.running:  # Main game loop
            self.check_events()  
            self.draw() 
            self.update() 
            self.clock.tick(60)  # Control the frame rate

    def check_events(self):
        for event in pygame.event.get():  # Process events
            if event.type == pygame.QUIT:  
                sys.exit()  
                pygame.quit() 
                self.running = False  # Set running flag to false
            if event.type == pygame.KEYDOWN: 
                if event.key == self.keybinds.get("console", -1):  # Check if the key is bound to the console
                    self.toggle_popup(self.console)  # Toggle the console popup
            
    def update(self):
        self.screen_manager.update()  

    def draw(self):
        self.screen.fill((0,0,0))  
        self.screen_manager.draw()  
        pygame.display.flip()  # Update the display
        
    def load_config(self):
        config = {}  # Initialize an empty config dictionary
        keybinds = {}  # Initialize an empty keybinds dictionary
        # Read the config file
        with open("config.cfg") as fconfig:
            for line in fconfig.readlines():
                split = line.split(" ")
                if line[0] != "#" and len(split) > 1:  # Ignore comments and invalid lines
                    if split[0].upper() == "BIND":
                        keybinds[split[2].strip("\n")] = pygame.key.key_code(split[1])  # Bind keys to commands
                        continue
                    config[split[0]] = split[1].strip("\n")  # Add config entries to the config dictionary
        return config, keybinds  # Return the config and keybinds

    def toggle_popup(self, popup):
        if popup.name in self.gui.items:  # If the popup is already in the GUI
            popup.on_close()  
            self.gui.remove_item(popup.name) 
        else:
            self.gui.add_item(popup.name, popup)  
            popup.on_open() 

class Console(Popup):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.name = "console"  # Set the name of the console
        self.commands = {}  # Initialize the commands dictionary
        # Add UI elements to the console
        self.add_item(Rect(RECT_DARK, pygame.Rect(700//2 + 10,200 + 10,700,400), positioning="absolute"))
        self.textbox = Textbox(TEXTBOX_DARK, pygame.Rect(700//2 + 10,400,700,50), positioning="absolute", on_submit=self.on_submit)
        self.console_output = Label(LABEL_DARK, rect = (700//2 + 10, 200 + 10, 700, 400), text = "WELCOME", positioning="absolute", font_size=20)
        self.console_output.centered = False
        self.add_item(self.console_output)
        self.add_item(self.textbox)
        # Add default commands
        self.add_command("help", self.help, [])
        self.add_command("bind", self.bind, ["key", "command"])
        self.add_command("getbinds", self.get_keybinds, [])

    def on_submit(self, text):
        # Handle command submission
        if text.split(" ")[0] in self.commands:
            command = self.commands[text.split(" ")[0]]
            if len(text.split(" ")[1:]) != len(command[1]):
                self.console_output.text += f"\nnot enough/ too many arguments"
            else:
                output = command[0](*text.split(" ")[1:])
                if output != None:
                    self.console_output.text += f"\n {output}"
        else:
            self.console_output.text += (f"\nCommand {text.split(' ')[0]} not found")
        self.textbox.text = ""
    
    def add_command(self, command_name, function, params):
        self.commands[command_name] = (function, params)  # Add a new command to the console

    def add_commands(self, commands):
        for command in commands:
            self.add_command(*command)  # Add multiple commands to the console

    def help(self, *args):
        # Display help information
        return "\n".join([f"{command} : {str(self.commands[command][1])[1:-1]}" for command in self.commands])
    
    def bind(self, key, command):
        # Bind a key to a command
        self.game.keybinds[command] = pygame.key.key_code(key)
        return f"bound key: {key} to command: {command}"

    def get_keybinds(self):
        # Get all key bindings
        return "\n".join([f"command: {bind} is bound to key: {self.game.keybinds[bind]}" for bind in self.game.keybinds])

    def on_open(self):
        pass

    def on_close(self):
        pass