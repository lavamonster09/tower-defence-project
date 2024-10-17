import pygame
import sys
import os 

from .level import Generator
from engine import *
from .screens import *
from .entities import *

screens = {
    "menu": Menu,
    "game_select": Game_select, 
    "settings": Settings,
    "heroes": Heroes,
    "upgrades": Upgrades
    }

class Game(Engine):
    def __init__(self):
        super().__init__(screens)
        # holds whether or not the game screen is open
        self.game_active = False

        # holds game state information
        self.paused = False
        self.hp = 1000
        self.game_speed = 1.0

        # the information needed for the current round 
        self.round_started = False
        self.enemy_types = {
            "standard": {
                "type": Standard,
                "chance": 100,
                "sprite": self.assets.get("enemy")
                },
            "fast": {
                "type": Fast,
                "chance": 50,
                "sprite": self.assets.get("enemy")
                }
            }
        self.current_round = Round(self, 0,self.enemy_types)

        # popups
        self.popups = {"upgrade_choice": UpgradeChoicePopup(self)}
        self.popups = {
            "upgrade_choice": UpgradeChoicePopup(self),
            "pause": Pause(self),
            "upgrade_decision": UpgradeDecision(self),
            "death": DeathPopup(self),
            "boss_warning": BossWarning(self)
        }

        # setup GUI
        self.gui.add_item("lbl_fps", Label(LABEL_DARK, rect = (98, 98, 125, 50), text = self.get_fps, font_size=20, positioning="relative"))
        self.gui.add_item("lbl_round", Label(LABEL_DARK, rect = (98, 2, 125, 50), text = self.get_round_number, font_size=30, positioning="relative"))
        self.gui.add_item("btn_roundstart", Button(BUTTON_DARK , rect = (95,90,100,100), text = get_icon_hex("play_arrow"), on_click= self.start_round, positioning="relative"))
        self.gui.add_item("btn_fastforward", Button(BUTTON_DARK , rect = (95,90,100,100), text = get_icon_hex("fast_forward"), on_click= self.fast_forward, positioning="relative"))
        lbl_hp = Label(LABEL_DARK, rect= (62,25, 125,50), text=self.get_hp, font_size=30, positioning="absolute")
        lbl_hp.fore_color = (255,50,50)
        self.gui.add_item("lbl_hp", lbl_hp)
        self.gui.items["btn_fastforward"].hidden = True

        self.screen_manager.add_screen("game", self.gui)
        
        # level data / generation
        self.level_data = {
            "no_turns": 6,
            "no_boxes": 6,
            "max_line_len": 1000
            }
        self.generator = Generator(self.screen.get_size())
        self.level = self.generator.generate_level(self.level_data)
        
        # setup draw and update queues
        self.draw_queue = []
        self.update_queue = []

        # add the level and entity manager to the draw queue
        self.draw_queue.append((1, self.level))
        self.draw_queue.append((2, self.entity_manager))
        self.draw_queue.append((6, self.screen_manager))
        self.update_queue.append(self.entity_manager)
        self.update_queue.append(self.screen_manager)
        self.update_queue.append(self.current_round)

        self.entity_manager.add_entity(Player(self,"player"),"player")

        self.console.add_command("upgrade", self.give_upgrade, [('speed', 'damage', 'range'), 'number'])
        self.console.add_command("fastforward", self.fast_forward, [])
        self.console.add_command("hp", self.set_hp, ["hp"])

        self.spawn_tower()


    def draw(self):
        if self.game_active:
            self.draw_queue.sort()
            for item in self.draw_queue:
                if self.paused and item[1] == self.screen_manager:
                    item[1].draw()
                    pygame.display.flip()
                    break
                item[1].draw()
            pygame.display.flip()
        else:
            super().draw()

    def update(self):
        self.game_active = self.screen_manager.current_screen == "game"
        if self.game_active:
            if pygame.key.get_just_pressed()[self.keybinds.get("pause", -1)]:
                self.toggle_popup(self.popups["pause"])
            if self.paused:
                for item in self.update_queue:
                    if item == self.screen_manager:
                        item.update()
                return
            for item in self.update_queue:
                item.update()
                if self.game_speed == 2.0:
                    item.update()
        else:
            super().update()

    def get_fps(self):
        return int(self.clock.get_fps())

    def get_round_number(self):
        return self.current_round.get_round_number()
    
    def get_hp(self):
        return self.hp / 10

    def set_hp(self, hp):
        self.hp = int(hp)
    
    def give_upgrade(self, upgrade_name: str, number: int):
        number = int(number)
        for _ in range(number):
            upgrade = Upgrade(self, pygame.Vector2(SCREEN_WIDTH / 2, 0), self.assets.get(f"{upgrade_name}_upgrade"), upgrade_name)
            upgrade.velocity = pygame.Vector2(0,random.randrange(8,15))
            upgrade.velocity.rotate_ip(random.randrange(-45,45))
            self.entity_manager.add_entity(upgrade, "upgrade")

    def start_round(self):
        self.gui.items["btn_roundstart"].hidden = True
        self.gui.items["btn_fastforward"].hidden = False
        self.update_queue.remove(self.current_round)
        self.current_round = Round(self, self.current_round.get_round_number()+1, self.enemy_types)
        self.update_queue.append(self.current_round)
        self.round_started = True
        self.fast_forward()
        self.entity_manager.entities["player"][0].input_lock = True
        if (self.current_round.round_number + 1)%10 == 0:
            self.toggle_popup(self.popups["boss_warning"])

    def fast_forward(self):
        btn = self.gui.items["btn_fastforward"]
        if self.game_speed == 2.0:
            self.game_speed = 1.0
            btn.border_color = DARK_ACCENT_COLOR
            btn.border_width = 2 
            btn.hover_color = btn.theme.get()["hover_color"]
            btn.fore_color = DARK_ACCENT_COLOR
        else:
            self.game_speed = 2.0
            btn.color = btn.theme.get()["color"]
            btn.border_color = btn.theme.get()["fore_color"]
            btn.border_width = 2 
            btn.hover_color = btn.theme.get()["hover_color"]
            btn.fore_color = btn.theme.get()["fore_color"]

    def spawn_upgrade(self, upgrade):
        upgrade = Upgrade(self, pygame.Vector2(SCREEN_WIDTH / 2, 0), self.assets.get(f"{upgrade}_upgrade"), upgrade)
        upgrade.velocity = pygame.Vector2(0,random.randrange(8,15))
        upgrade.velocity.rotate_ip(random.randrange(-45,45))
        self.entity_manager.add_entity(upgrade, "upgrade")
        self.toggle_popup(self.popups["upgrade_choice"])

    def spawn_tower(self):
        tower = Tower(self, pygame.Vector2(SCREEN_WIDTH / 2, 0))
        tower.velocity = pygame.Vector2(0,random.randrange(8,15))
        tower.velocity.rotate_ip(random.randrange(-45,45))
        self.entity_manager.add_entity(tower, "tower")

    def upgrade_tower(self, upgrade, tower):
        tower.upgrade(upgrade)
        self.toggle_popup(self.popups["upgrade_decision"])
        upgrade.alive = False

class Pause(Popup):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.name = "pause"
        self.add_item(Rect(RECT_DARK, (50, 50, 500, 500), positioning="relative"))
        self.add_item(Label(LABEL_DARK, (50, 8, 1000, 100), text= "PAUSED", positioning="relative", font_size=80))
        self.add_item(Button(BUTTON_DARK, (50, 51, 400, 100), text="SETTINGS", on_click=self.game.screen_manager.change_screen, click_args=["settings", 1], positioning="relative"))
        self.add_item(Button(BUTTON_DARK, (50, 28, 400, 100), text="CONTINUE", on_click=self.game.toggle_popup, click_args=[self], positioning="relative"))
        self.add_item(Button(BUTTON_DARK, (50, 73, 400, 100), text="EXIT", on_click=self.game.screen_manager.change_screen, click_args=["game_select", 1], positioning="relative"))

    def on_close(self):
        self.game.paused = False

    def on_open(self):
        self.game.paused = True

class UpgradeChoicePopup(Popup):
    def __init__(self, game):
        super().__init__(game)
        self.name = "upgrade"
        btn_speed = Button(BUTTON_DARK, (20,65,310,200), "speed", positioning="relative", on_click=game.spawn_upgrade, click_args=["speed"])
        btn_speed.fore_color = (34,177,76)
        btn_damage = Button(BUTTON_DARK, (50,65,430,200), "damage", positioning="relative", on_click=game.spawn_upgrade, click_args=["damage"])
        btn_damage.fore_color = (235,51,36)
        btn_range = Button(BUTTON_DARK, (80,65,310,200), "range", positioning="relative", on_click=game.spawn_upgrade, click_args=["range"])
        btn_range.fore_color = (230,230,230)
        self.add_item(Label(LABEL_DARK_FILLED, (50,25,770,150), f"chose an upgrade", positioning="relative", font_size=80))
        self.add_item(btn_speed)
        self.add_item(btn_damage)
        self.add_item(btn_range)
    
    def on_close(self):
        self.game.paused = False

    def on_open(self):
        self.game.paused = True

class UpgradeDecision(Popup):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.name = "upgrade_decision"
        self.target = None
        self.currently_upgrading = None
        self.btn_upgrade = Button(BUTTON_DARK, (75,65,450,200), "UPGRADE", positioning="relative", on_click=game.upgrade_tower, click_args=[])
        self.label = Label(LABEL_DARK_FILLED, (50,25,770,150), f"upgrade,", positioning="relative", font_size=80)
        self.add_item(self.btn_upgrade)
        self.add_item(self.label)
        

    def on_close(self):
        self.game.paused = False

    def set_tower(self, tower):
        self.target = tower

    def on_open(self):
        self.add_item(Button(BUTTON_DARK, (25,65,450,200), "CANCEL", positioning="relative", on_click=self.game.toggle_popup, click_args=[self]))
        self.currently_upgrading = None
        for upgrade in self.game.entity_manager.entities.get("upgrade", []):
            if upgrade.can_upgrade:
                self.currently_upgrading = upgrade
        self.btn_upgrade.click_args = [self.currently_upgrading, self.target]
        self.label.text = f"upgrade {self.currently_upgrading.type}?"
        self.game.paused = True

class DeathPopup(Popup):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.name = "death_popup"
        self.btn_replay = Button(BUTTON_DARK, (50,30,450,200), text="RETRY", positioning="relative", on_click=self.retry)
        self.btn_exit = Button(BUTTON_DARK, (50,70,450,200), text="EXIT", positioning="relative", on_click=self.exit)
        self.add_item(self.btn_exit)
        self.add_item(self.btn_replay)

    def retry(self):
        for enemy in self.game.entity_manager.entities["enemy"]:
            enemy.alive = False
        self.game.draw_queue.remove((1, self.game.level))
        self.game.level = self.game.generator.generate_level(self.game.level_data)
        self.game.draw_queue.append((1,self.game.level))
        self.game.current_round.round_number = 0
        self.game.round_started = False
        self.game.toggle_popup(self)

    def exit(self):
        for enemy in self.game.entity_manager.entities["enemy"]:
            enemy.alive = False
        self.game.draw_queue.remove((1, self.game.level))
        self.game.level = self.game.generator.generate_level(self.game.level_data)
        self.game.draw_queue.append((1,self.game.level))
        self.game.current_round.round_number = 0
        self.game.round_started = False
        self.game.screen_manager.change_screen("game_select", 10)
        self.game.toggle_popup(self)

    def on_open(self):
        self.game.paused = True
        self.game.round_started = False
        self.game.gui.items["btn_roundstart"].hidden = False
        self.game.gui.items["btn_fastforward"].hidden = True
        
    def on_close(self):
        self.game.paused = False
        self.game.game_speed = 1.0
        self.game.hp = 1000
        self.game.entity_manager.entities["player"][0].input_lock = False

class BossWarning(Popup):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.name = "boss_warning"
        self.add_item(Image(self.game.assets.get("warning"), (50,50,200,200), positioning = "relative"))
        self.add_item(Label(LABEL_DARK_FILLED, (50,70,400,50), f"boss coming up", positioning="relative", font_size=30))
        self.counter = 0

    def on_close(self):
        pass

    def update(self):
        super().update()
        self.counter += 1
        if self.counter // 60 % 2 == 0:
            self.hidden = False
        else:
            self.hidden = True
        if self.counter > 180:
            self.game.toggle_popup(self)

    def on_open(self):
        pass

class Round:
    def __init__(self, game, round_number, enemy_types):
        self.game = game
        self.round_number = round_number
        self.number_enemies = int(round_number ** 1.2)
        self.enemies = []
        self.enemy_delay = 60
        self.counter = 1000 
        for i in range(self.number_enemies):
            for enemy_type in enemy_types:
                for _ in range(self.number_enemies * enemy_types[enemy_type]["chance"] // 100):
                    self.enemies.append(enemy_types[enemy_type]["type"](game, sprite = enemy_types[enemy_type]["sprite"]))

    def get_round_number(self):
        return self.round_number

    def update(self):
        self.counter += 1 
        if self.game.round_started:
            if len(self.enemies) > 0 and self.counter >= self.enemy_delay:
                self.counter = 0
                enemy = random.choice(self.enemies)
                self.game.entity_manager.add_entity(enemy, "enemy")
                self.enemies.remove(enemy)
            if len(self.game.entity_manager.entities.get("enemy", [])) == 0 and len(self.enemies) == 0 and self.game.hp > 0:
                self.game.round_started = False
                self.game.gui.items["btn_roundstart"].hidden = False
                self.game.gui.items["btn_fastforward"].hidden = True
                self.game.game_speed = 1.0
                self.game.toggle_popup(self.game.popups["upgrade_choice"])
                self.game.entity_manager.entities["player"][0].input_lock = False
