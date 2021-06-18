import pygame
import pygame.freetype
import sys
import win32api
import win32con
import win32gui
from button_functions import close_sidebar, toggle_wellness_sidebar, toggle_items_sidebar, toggle_activities_sidebar, toggle_options_sidebar

TRANSPARENT = (255, 0, 128)

def init():
	pygame.init()
	info = pygame.display.Info()
	width, height = info.current_w, info.current_h
	screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
	systemID = pygame.display.get_wm_info()["window"]
	win32gui.SetWindowLong(systemID, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(systemID, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
	win32gui.SetLayeredWindowAttributes(systemID, win32api.RGB(*TRANSPARENT), 0, win32con.LWA_COLORKEY)
	win32gui.SetWindowPos(systemID, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
	return screen

def update(screen, sans):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			end()
		elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			if sans.isClicked(event.pos):
				sans.draging = True
				sans.dragOffset = sans.rect.x - event.pos[0], sans.rect.y - event.pos[1]
			elif not sans.toolbar.isHidden():
				for button in sans.toolbar.buttons:
					button.setStatus(event.pos)
		elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
			sans.draging = False
	if sans.draging:
		mouseX, mouseY = win32api.GetCursorPos()
		sans.move(mouseX + sans.dragOffset[0], mouseY + sans.dragOffset[1])
	screen.fill(TRANSPARENT)
	sans.draw()
	pygame.display.update()

def end():
	pygame.quit()
	print("Program Closed.")
	sys.exit()

class Sans:
	def __init__(self, window: pygame.Surface, x: int, y: int, width: int, height: int):
		self.window = window
		self.rect = pygame.Rect(x, y, width, height)
		self.draging = False
		self.dragOffset = (0, 0)
		self.sidebar = self.Sidebar(window, x - 140, y - 80, 120, 180)
		self.toolbar = self.Toolbar(window, x - 40, y + 120, 180, 40, (0, 128, 128), self.sidebar)

	def move(self, x: int, y: int):
		self.rect.x, self.rect.y = x, y
		self.toolbar.move(x - 40, y + 120)
		self.sidebar.move(x - 140, y - 80)

	def draw(self):
		pygame.draw.rect(self.window, (0, 150, 255), self.rect)
		self.sidebar.draw() if not self.sidebar.isHidden() else None
		self.toolbar.draw() if not self.toolbar.isHidden() else None

	def isClicked(self, mousePos: tuple):
		return self.rect.collidepoint(mousePos)

	class Toolbar:
		def __init__(self, window: pygame.Surface, x: int, y: int, width: int, height: int, color: tuple, sidebar):
			self.window = window
			self.rect = pygame.Rect(x, y, width, height)
			self.color = color
			self.sidebar = sidebar
			button1 = Sans.Button(window, x + 5, y + 5, 30, 30, (95, 146, 40), lambda: toggle_wellness_sidebar(self.sidebar) if self.sidebar.status != 1 else close_sidebar(sidebar))
			button2 = Sans.Button(window, x + 40, y + 5, 30, 30, (95, 146, 40), lambda: toggle_items_sidebar(self.sidebar) if self.sidebar.status != 2 else close_sidebar(sidebar))
			button3 = Sans.Button(window, x + 75, y + 5, 30, 30, (95, 146, 40), lambda: toggle_activities_sidebar(self.sidebar) if self.sidebar.status != 3 else close_sidebar(sidebar))
			button4 = Sans.Button(window, x + 110, y + 5, 30, 30, (95, 146, 40), lambda: toggle_options_sidebar(self.sidebar) if self.sidebar.status != 4 else close_sidebar(sidebar))
			button5 = Sans.Button(window, x + 145, y + 5, 30, 30, (241, 60, 32), end)
			self.buttons = (button1, button2, button3, button4, button5)

		def move(self, x: int, y: int):
			for button in self.buttons:
				button.move(button.rect.x + x - self.rect.x, button.rect.y + y - self.rect.y)
			self.rect.x, self.rect.y = x, y

		def draw(self):
			pygame.draw.rect(self.window, self.color, self.rect)
			mousePos = pygame.mouse.get_pos()
			for button in self.buttons:
				button.setColor(mousePos)
				button.draw()

		def isHidden(self):
			return not pygame.key.get_focused()

	class Button:
		def __init__(self, window: pygame.Surface, x: int, y: int, width: int, height: int, color: tuple, function):
			self.window = window
			self.rect = pygame.Rect(x, y, width, height)
			self.originalColor = color
			self.highlightedColor = (min(color[0] + 50, 255), min(color[1] + 50, 255), min(color[2] + 50, 255))
			self.currentColor = color
			self.function = function

		def move(self, x: int, y: int):
			self.rect.x, self.rect.y = x, y

		def draw(self):
			pygame.draw.rect(self.window, self.color, self.rect)

		def setColor(self, mousePos: tuple):
			if self.rect.collidepoint(mousePos):
				self.color = self.highlightedColor
			else:
				self.color = self.originalColor

		def setStatus(self, mousePos: tuple):
			self.callFunction() if self.rect.collidepoint(mousePos) else None

		def callFunction(self):
			self.function()

	class Sidebar:
		def __init__(self, window: pygame.Surface, x: int, y: int, width: int, height: int):
			self.window = window
			self.border = pygame.Rect(x - 3, y - 3, width + 6, height + 6)
			self.rect = pygame.Rect(x, y, width, height)
			self.objects = []
			self.status = 0

		def add(self, object):
			self.objects.append(object)

		def clear(self):
			self.objects.clear()

		def move(self, x: int, y: int):
			for object in self.objects:
				object.move(object.rect.x + x - self.rect.x, object.rect.y + y - self.rect.y)
			self.border.x, self.border.y = x - 3, y - 3
			self.rect.x, self.rect.y = x, y

		def draw(self):
			pygame.draw.rect(self.window, (255, 255, 255), self.border)
			pygame.draw.rect(self.window, (0, 0, 0), self.rect)
			for object in self.objects:
				object.draw()

		def isHidden(self):
			return True if self.status == 0 else False

def main():
	screen = init()
	sans = Sans(screen, 250, 250, 100, 100)
	clock = pygame.time.Clock()
	while True:
		clock.tick(60)
		update(screen, sans)

if __name__ == "__main__":
	main()