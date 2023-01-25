from settings_constants import *


class Widget():
    total_widgets = 0
    preveous_y = 0
    widgets_list = []

    def __init__(self, *, pos_x, pos_y=0, width, text="", action=None):
        Widget.total_widgets += 1
        self.x = pos_x
        self.width = width
        self.height = 50
        # This made for "default" y position of widget
        if pos_y == 0:
            self.y = Widget.preveous_y + self.height + 25
        else:
            self.y = pos_y 
        self.text = text
        self.action = action
        self.button_rect = pygame.Rect((self.x, self.y), 
                                       (self.width, self.height))
        self.inner_border = pygame.Rect((self.x + BUTTON_BORDER_WIDTH, self.y + BUTTON_BORDER_WIDTH),
                                        (self.width - BUTTON_BORDER_WIDTH * 2, self.height - BUTTON_BORDER_WIDTH * 2))
        self.text_surf, self.text_rect = self.update_text(self.text)
        Widget.preveous_y = self.y
        Widget.widgets_list.append(self)
        


    def update_text(self, new_text):
        new_text = str(new_text)
        self.text_surf = font.render(new_text, True, COLOR_WHITE)
        self.text_rect = self.text_surf.get_rect(center=self.button_rect.center)
        self.text = new_text
        return self.text_surf, self.text_rect


    # Excecute function after button press
    def action_on_release(self, event):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONUP:
            if self.button_rect.collidepoint((mouse_x, mouse_y)):
                if self.action != None:
                    self.action()


    def draw_widget(self):
        ...


    def draw_all_widgets():
        for widget in Widget.widgets_list:
            widget.draw_widget()

    def action_all_widget(event):
        for widget in Widget.widgets_list:
            widget.action_on_release(event)


class Button(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pass

    def draw_widget(self):
        pygame.draw.rect(screen, COLOR_ACCENT_BLUE, self.button_rect, border_radius=15)
        pygame.draw.rect(screen, COLOR_BACKGROUND_BRIGHT, self.inner_border, border_radius=10)
        screen.blit(self.text_surf, self.text_rect)



class Slider(Widget):
    def __init__(self, max_value, min_value, **kwargs):
        super().__init__(**kwargs)

        self.slide = pygame.Rect((self.x, self.y), 
                                 (10, self.height))
        self.slider_drag = False
        self.max_value = max_value
        self.min_value = min_value
        self.value = ""
        

    def draw_widget(self):
        if self.slide.left < self.x + 15:
            self.slide.left = self.x + 15
        if self.slide.right > self.x + self.width - 15:
            self.slide.right = self.x + self.width - 15
        self.update_slider_value()
        pygame.draw.rect(screen, COLOR_ACCENT_BLUE, self.button_rect, border_radius=15)
        pygame.draw.rect(screen, COLOR_BACKGROUND_BRIGHT, self.inner_border, border_radius=10)
        pygame.draw.rect(screen, COLOR_ACCENT_BLUE, self.slide)
        screen.blit(self.text_surf, self.text_rect)


    def update_slider_value(self):
        self.value = str(int(self.min_value + (self.slide.x - self.x - 15) / 
                    (self.width - 40) * (self.max_value - self.min_value)))
        self.update_text(f"Sim speed: 1/{self.value}")


    def action_on_release(self, event):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint((mouse_x, mouse_y)):
                self.slide.centerx = mouse_x
                self.slider_drag = True

        elif event.type == pygame.MOUSEMOTION:
            if self.button_rect.collidepoint((mouse_x, mouse_y)) and self.slider_drag:
                self.slide.centerx = mouse_x

        elif event.type == pygame.MOUSEBUTTONUP:
            self.slider_drag = False
            if self.button_rect.collidepoint((mouse_x, mouse_y)) and self.action != None:
                self.action()
