import pygame
from config import *

# Pygame init
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Calculator")

button_font = pygame.font.SysFont('Consolas', 42)

# Global variables
buttonList = []


class CalculatorButton:
	def __init__(self, text, value, x, y):
		self.text = text
		self.value = value
		self.x = x
		self.y = y

		self.rendered_text = button_font.render(self.text, True, BLACK)
		self.text_width, self.text_height = button_font.size(self.text)

		self.width = SCREEN_WIDTH / 4
		self.height = SCREEN_HEIGHT / 5
		self.center_x = self.x + self.width / 2
		self.center_y = self.y + self.height / 2
		self.padding = 1
		self.selected = False


	def check_if_clicked_on(self, mouse_x, mouse_y):
		max_distance_x = self.width / 2 - self.padding
		max_distance_y = self.height / 2 - self.padding

		is_within_x = -max_distance_x  < mouse_x - self.center_x < max_distance_x 
		is_within_y = -max_distance_y < mouse_y - self.center_y < max_distance_y

		if is_within_x and is_within_y:
			self.selected = True
		else:
			self.selected = False



	def blit_self(self):
		if self.selected:
			color = BUTTON_SELECTED_COLOR
		else:
			color = BUTTON_COLOR

		pygame.draw.rect(screen, color,
							(self.x + self.padding, self.y + self.padding,
							self.width - self.padding, 	self.height - self.padding))

		mid_x = self.center_x - self.text_width / 2
		mid_y = self.center_y - self.text_height / 2
		screen.blit(self.rendered_text, (mid_x, mid_y))


def sum(x, y):   return x + y


def subtract(x, y):   return x - y


def multiply(x, y):   return x * y


def divide(x, y):
	try:
		return x / y
	except ZeroDivisionError:
		return "error"


def buttons_init():
	buttons = [["7", "8", "9", "+"],
				["4", "5", "6", "-"],
				["1", "2", "3", "×"],
				["C", "0", "=", "÷"]]
	y = SCREEN_HEIGHT / 5

	for row in buttons:
		x = 0

		for i in row:
			buttonList.append(CalculatorButton(i, None, x, y))
			x += SCREEN_WIDTH / 4

		y += SCREEN_HEIGHT / 5


def update_screen():
	screen.fill(BLACK)
	for button in buttonList:
		button.blit_self()
	pygame.display.flip()


def keyboard_input():
	global quitApp
	if event.type == pygame.KEYDOWN:
		# Stops the app.
		if event.key == pygame.K_DELETE or event.key == pygame.K_ESCAPE:
			quitApp = True


def mouse_input():
	if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
		mouse_x, mouse_y = pygame.mouse.get_pos()
		for button in buttonList:
			button.check_if_clicked_on(mouse_x, mouse_y)

	if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
		for button in buttonList:
			button.selected = False


# App init
buttons_init()
update_screen()


quitApp = False
while not quitApp:
	for event in pygame.event.get():
		# Closes the app if clicked on exit.
		if event.type == pygame.QUIT:
			quitApp = True

		keyboard_input()
		mouse_input()


	update_screen()
