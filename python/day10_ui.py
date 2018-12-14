import pygame


class Day10UIHelper(object):
    def __init__(self, fontcolor, fontsize, padding, width, height):
        pygame.init()
        pygame.font.init()

        pygame.display.set_caption('Advent of Code 2018 - Day 10')

        self.screen = pygame.display.set_mode((width, height))
        self.font = pygame.font.SysFont('Arial', fontsize)
        self.fontcolor = fontcolor
        self.padding = padding
        self.width = width
        self.height = height
        self.clock = pygame.time.Clock()
        self.done = False
        self.keys = {
            pygame.K_DOWN: False,
            pygame.K_UP: False,
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False
        }

    def draw_coordinate(self, coordinate, color):
        pygame.draw.rect(self.screen,
                         color,
                         (coordinate.x, coordinate.y, 5, 5))

    def draw(self):
        pygame.display.flip()
        self.clock.tick(60)

    def onloop(self, background_color, current_step, steps):
        self.screen.fill(background_color)
        self.__render_hud(current_step, steps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.keys[pygame.K_UP] = True
                elif event.key == pygame.K_DOWN:
                    self.keys[pygame.K_DOWN] = True
                elif event.key == pygame.K_RIGHT:
                    self.keys[pygame.K_RIGHT] = True
                elif event.key == pygame.K_LEFT:
                    self.keys[pygame.K_LEFT] = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.keys[pygame.K_UP] = False
                elif event.key == pygame.K_DOWN:
                    self.keys[pygame.K_DOWN] = False
                elif event.key == pygame.K_RIGHT:
                    self.keys[pygame.K_RIGHT] = False
                elif event.key == pygame.K_LEFT:
                    self.keys[pygame.K_LEFT] = False

    def is_down_pressed(self):
        return self.keys[pygame.K_DOWN]

    def is_up_pressed(self):
        return self.keys[pygame.K_UP]

    def is_left_pressed(self):
        return self.keys[pygame.K_LEFT]

    def is_right_pressed(self):
        return self.keys[pygame.K_RIGHT]

    def __render_hud(self, current_step, steps):
        text = self.font.render(
            'Right arrow: next step', False, self.fontcolor)
        rightarrow_rect = text.get_rect()
        rightarrow_rect.left = self.padding
        rightarrow_rect.top = self.height - rightarrow_rect.height - self.padding
        self.screen.blit(text, rightarrow_rect)

        text = self.font.render(
            'Left arrow: previous step', False, self.fontcolor)
        leftarrow_rect = text.get_rect()
        leftarrow_rect.left = rightarrow_rect.left
        leftarrow_rect.top = rightarrow_rect.top - leftarrow_rect.height
        self.screen.blit(text, leftarrow_rect)

        text = self.font.render(
            'Up arrow: increase step', False, self.fontcolor)
        uparrow_rect = text.get_rect()
        uparrow_rect.left = self.width - uparrow_rect.width - self.padding
        uparrow_rect.top = self.height - rightarrow_rect.height - self.padding
        self.screen.blit(text, uparrow_rect)

        text = self.font.render(
            'Down arrow: decrease step', False, self.fontcolor)
        downarrow_rect = text.get_rect()
        downarrow_rect.left = self.width - downarrow_rect.width - self.padding
        downarrow_rect.top = uparrow_rect.top - downarrow_rect.height
        self.screen.blit(text, downarrow_rect)

        text = self.font.render(
            f'Current step: {current_step}', False, self.fontcolor)
        self.screen.blit(text, (self.padding, 0))

        text = self.font.render(f'Steps: {steps}', False, self.fontcolor)
        step_rect = text.get_rect()
        step_rect.left = self.width - step_rect.width - self.padding
        step_rect.top = self.padding
        self.screen.blit(text, step_rect)
