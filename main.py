import pygame

# Consts (kinda)
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SECTION_WIDTH = SCREEN_WIDTH / 4
SECTION_HEIGHT = SCREEN_HEIGHT / 5

BLACK = 0, 0, 0
BUTTON_COLOR = 200, 245, 20
BUTTON_SELECTED_COLOR = 160, 195, 10

# Pygame init
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Calculator")

button_font = pygame.font.SysFont('Consolas', 42)
calc_font = pygame.font.SysFont('Consolas', 64)	

# Global variables
buttonList = []
calcDisplayText = ""

x = 5
y = 2

class CalculatorButton:
	def __init__(self, text, value, x, y):
		self.text = text
		self.value = value
		self.x = x
		self.y = y

		self.rendered_text = button_font.render(self.text, True, BLACK)
		self.text_width, self.text_height = button_font.size(self.text)

		self.width = SECTION_WIDTH
		self.height = SECTION_HEIGHT
		self.center_x = self.x + self.width / 2
		self.center_y = self.y + self.height / 2
		self.padding = 1
		self.selected = False


	def check_if_clicked_on(self, mouse_x, mouse_y):
		global calcDisplayText

		max_distance_x = self.width / 2 - self.padding
		max_distance_y = self.height / 2 - self.padding

		is_mouse_within_x = -max_distance_x  < mouse_x - self.center_x < max_distance_x 
		is_mouse_within_y = -max_distance_y < mouse_y - self.center_y < max_distance_y

		if is_mouse_within_x and is_mouse_within_y:
			self.selected = True
			#if self.value:
			#	print("z")
			calcDisplayText = self.text

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
		return "error: division by 0"


def clear():
	pass


def calculate():
	global fDict
	calcInstructions = ["7", "sum", "1", "2"]
	index = 0
	
	# Make all str numbers to ints and put them together if neccesary
	for item in calcInstructions:
		if item.isdigit():
		
			toInt = int(item)
			calcInstructions.pop(index)
			calcInstructions.insert(index, toInt)

			print(calcInstructions)
			if index != 0:
				if type(calcInstructions[index-1]) == int:
					newItem = str(calcInstructions[index-1]) + str(calcInstructions[index])
					newItem = int(newItem)
					calcInstructions.pop(index-1)
					calcInstructions.pop(index-1)
					calcInstructions.insert(index, newItem)

		index += 1
	
	# Do all calculations
	index = 0
	for item in calcInstructions:
		if type(item) == str:
			operation = fDict[item]
			x = calcInstructions[index - 1]
			y = calcInstructions[index + 1]

			doneOperation = operation(x, y)

			print(calcInstructions)
			calcInstructions[index] = doneOperation
			calcInstructions.pop(index + 1)
			calcInstructions.pop(index - 1)

		index += 1

	print(calcInstructions)


fDict = {
	"sum" 		: sum,
	"subtract" 	: subtract,
	"multiply" 	: multiply,
	"divide" 	: divide,
	"clear" 	: clear,
	"calculate" : calculate
}


calculate()


def buttons_init():
	global x, y
	buttons = [[["7", 7], ["8", 8], ["9", 9], ["+", "sum"]],
			   [["4", 4], ["5", 5], ["6", 6], ["-", "subtract"]],
			   [["1", 1], ["2", 2], ["3", 3], ["×", "multiply"]],
			   [["C", "clear"], ["0", 0 ], ["=", "calculate"], ["÷", "divide"]]]

	y = SECTION_HEIGHT

	for row in buttons:
		x = 0

		for i in row:
			buttonList.append(CalculatorButton(i[0], None, x, y))
			x += SECTION_WIDTH

		y += SECTION_HEIGHT


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


def update_calc_display():
	padding = 30
	calc_text_width, calc_text_height = calc_font.size(calcDisplayText)
	x = SCREEN_WIDTH - padding - calc_text_width
	y = SECTION_HEIGHT / 2 - calc_text_height / 2
	calc_rendered_text = calc_font.render(calcDisplayText, True, BUTTON_COLOR)
	screen.blit(calc_rendered_text, (x, y))


def update_screen():
	screen.fill(BLACK)
	update_calc_display()

	for button in buttonList:
		button.blit_self()
	
	pygame.display.flip()


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
