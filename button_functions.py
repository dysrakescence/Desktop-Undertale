import pygame
from pygame.freetype import Font, init
from json import load

init()
comic_sans_font = Font("fonts/comic_sans.ttf", 15)
papyrus_font = Font("fonts/papyrus.ttf", 15)
dialogue_font = Font("fonts/determination_mono.otf", 40/3)
menu_font = Font("fonts/determination_sans.otf", 40/3)
file = open("stats.json")
stats = load(file)
file.close()
wellness = stats["wellness"]
record = stats["record"]
equipments = stats["equipments"]
items = stats["items"]

def close_sidebar(sidebar):
	sidebar.status = 0

def toggle_stats_sidebar(sidebar):
	sidebar.status = 1
	sidebar.clear()
	sidebar.add(MenuText(sidebar.window, sidebar.rect.x + 10, sidebar.rect.y + 10, f'"{record["Name"]}"'))
	sidebar.add(MenuText(sidebar.window, sidebar.rect.x + 10, sidebar.rect.y + 35, "LV"))
	sidebar.add(MenuText(sidebar.window, sidebar.rect.x + 30, sidebar.rect.y + 35, record["Level of Violence"]))
	sidebar.add(MenuText(sidebar.window, sidebar.rect.x + 10, sidebar.rect.y + 50, "HP"))
	sidebar.add(MenuText(sidebar.window, sidebar.rect.x + 30, sidebar.rect.y + 50, f"{record['Hit Points']['current']} / {record['Hit Points']['max']}"))
	sidebar.add(MenuText(sidebar.window, sidebar.rect.x + 10, sidebar.rect.y + 75, "AT"))
	sidebar.add(MenuText(sidebar.window, sidebar.rect.x + 30, sidebar.rect.y + 75, record["Attack"]))
	sidebar.add(MenuText(sidebar.window, sidebar.rect.x + 10, sidebar.rect.y + 90, "DF"))
	sidebar.add(MenuText(sidebar.window, sidebar.rect.x + 30, sidebar.rect.y + 90, record["Defense"]))
	sidebar.add(MenuText(sidebar.window, sidebar.rect.x + 60, sidebar.rect.y + 75, "EXP:"))
	sidebar.add(MenuText(sidebar.window, sidebar.rect.x + 95, sidebar.rect.y + 75, record["Execution Points"]))
	sidebar.add(MenuText(sidebar.window, sidebar.rect.x + 60, sidebar.rect.y + 90, "NEXT:"))
	sidebar.add(MenuText(sidebar.window, sidebar.rect.x + 95, sidebar.rect.y + 90, 10))
	sidebar.add(MenuText(sidebar.window, sidebar.rect.x + 10, sidebar.rect.y + 115, "WEAPON:"))
	sidebar.add(MenuText(sidebar.window, sidebar.rect.x + 60, sidebar.rect.y + 115, equipments["weapon"]))
	sidebar.add(MenuText(sidebar.window, sidebar.rect.x + 10, sidebar.rect.y + 130, "ARMOR:"))
	sidebar.add(MenuText(sidebar.window, sidebar.rect.x + 60, sidebar.rect.y + 130, equipments["armor"]))
	sidebar.add(MenuText(sidebar.window, sidebar.rect.x + 10, sidebar.rect.y + 155, f"GOLD: {record['Gold']}"))

def toggle_items_sidebar(sidebar):
	sidebar.status = 2
	sidebar.clear()
	for i, item in enumerate(items):
		sidebar.add(MenuText(sidebar.window, sidebar.rect.x + 5, sidebar.rect.y + 10 + (i * 20), f"* {item}"))

def toggle_wellness_sidebar(sidebar):
	sidebar.status = 3
	sidebar.clear()
	for i, attribute in enumerate(wellness.keys()):
		sidebar.add(MenuText(sidebar.window, sidebar.rect.x + 5, sidebar.rect.y + 5 + (i * 35), f"{attribute}:"))
		sidebar.add(MenuText(sidebar.window, sidebar.rect.x + 5, sidebar.rect.y + 23 + (i * 35), str(wellness[attribute])))
		sidebar.add(ProgressBar(sidebar.window, sidebar.rect.x + 30, sidebar.rect.y + 22 + (i * 35), 80, 12, (0, 100, 255)))

def toggle_options_sidebar(sidebar):
	sidebar.status = 4
	sidebar.clear()
	sidebar.add(MenuText(sidebar.window, sidebar.rect.x + 10, sidebar.rect.y + 10, "Settings"))

class MenuText:
	def __init__(self, window: pygame.Surface, x: int, y: int, text):
		self.window = window
		self.rect = pygame.Rect(x, y, 0, 0)
		self.font = menu_font
		self.color = (255, 255, 255)
		self.background = (0, 0, 0)
		self.text = self.font.render(str(text), self.color, self.background)[0]

	def move(self, x: int, y: int):
		self.rect.x, self.rect.y = x, y

	def draw(self):
		self.window.blit(self.text, (self.rect.x, self.rect.y))

	def edit(self, text: str):
		self.text = self.font.render(text, self.color, self.background)[0]

class ProgressBar:
	def __init__(self, window: pygame.Surface, x: int, y: int, width: int, height: int, color: tuple):
		self.window = window
		self.border = pygame.Rect(x - 1, y - 1, width + 2, height + 2)
		self.rect = pygame.Rect(x, y, width, height)
		self.color = color

	def move(self, x: int, y: int):
		self.border.x, self.border.y = x - 1, y - 1
		self.rect.x, self.rect.y = x, y

	def draw(self):
		pygame.draw.rect(self.window, (255, 255, 255), self.border)
		pygame.draw.rect(self.window, self.color, self.rect)