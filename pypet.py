import pygame
import sys
import win32api
import win32con
import win32gui

class Program:
	def __init__(self):
		pygame.init()
		info = pygame.display.Info()
		self.width, self.height = info.current_w, info.current_h
		self.screen = pygame.display.set_mode((self.width, self.height), pygame.NOFRAME)
		self.transparentColor = (255, 0, 128)
		systemID = pygame.display.get_wm_info()["window"]
		win32gui.SetWindowLong(systemID, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(systemID, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
		win32gui.SetLayeredWindowAttributes(systemID, win32api.RGB(*self.transparentColor), 0, win32con.LWA_COLORKEY)
		win32gui.SetWindowPos(systemID, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
		self.clock = pygame.time.Clock()
		self.pet = self.Pet(self.screen, 250, 250, 80, 80)

	def run(self):
		while True:
			self.clock.tick(60)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.end()
				elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					if self.pet.isClicked(event.pos):
						self.pet.draging = True
						offsetX = self.pet.rect.x - event.pos[0]
						offsetY = self.pet.rect.y - event.pos[1]
					elif not self.pet.toolbar.isHidden():
						for button in self.pet.toolbar.buttons:
							button.setStatus(event.pos)
				elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
					self.pet.draging = False
			if self.pet.draging:
				mouseX, mouseY = win32api.GetCursorPos()
				self.pet.move(mouseX + offsetX, mouseY + offsetY)
			self.screen.fill(self.transparentColor)
			self.pet.draw()
			pygame.display.update()

	@staticmethod
	def end():
		pygame.quit()
		print("Program Closed.")
		sys.exit()

	class Pet:
		def __init__(self, window: pygame.Surface, x: int, y: int, width: int, height: int):
			self.window = window
			self.x, self.y = x, y
			self.rect = pygame.Rect(x, y, width, height)
			self.draging = False
			self.toolbar = self.Toolbar(window, x - 50, y + 100, 180, 40)

		def move(self, x: int, y: int):
			self.rect.x, self.rect.y = x, y
			self.toolbar.move(x - 50, y + 100)

		def draw(self):
			pygame.draw.rect(self.window, (0, 150, 255), self.rect)
			self.toolbar.draw() if not self.toolbar.isHidden() else None

		def isClicked(self, mousePos: tuple):
			return self.rect.collidepoint(mousePos)

		class Toolbar:
			def __init__(self, window: pygame.Surface, x: int, y: int, width: int, height: int):
				self.window = window
				self.x, self.y = x, y
				self.rect = pygame.Rect(x, y, width, height)
				button1 = self.Button(window, x + 5, y + 5, 30, 30, (95, 146, 40), lambda: print(1))
				button2 = self.Button(window, x + 40, y + 5, 30, 30, (95, 146, 40), lambda: print(2))
				button3 = self.Button(window, x + 75, y + 5, 30, 30, (95, 146, 40), lambda: print(3))
				button4 = self.Button(window, x + 110, y + 5, 30, 30, (95, 146, 40), lambda: print(4))
				button5 = self.Button(window, x + 145, y + 5, 30, 30, (241, 60, 32), Program.end)
				self.buttons = (button1, button2, button3, button4, button5)

			def move(self, x: int, y: int):
				for button in self.buttons:
					button.move(button.rect.x + x - self.rect.x, button.rect.y + y - self.rect.y)
				self.rect.x, self.rect.y = x, y

			def draw(self):
				pygame.draw.rect(self.window, (0, 128, 128), self.rect)
				mousePos = pygame.mouse.get_pos()
				for button in self.buttons:
					button.setColor(mousePos)
					button.draw()

			def isHidden(self):
				return not pygame.key.get_focused()

			class Button:
				def __init__(self, window: pygame.Surface, x: int, y: int, width: int, height: int, color: tuple, function):
					self.window = window
					self.x, self.y = x, y
					self.width, self.height = width, height
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

def main():
	program = Program()
	program.run()

main()
