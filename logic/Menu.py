import pygame
from interfaces.IMenu import IMenu

class Menu(IMenu):
    def __init__(self):
        self.options = ['blue', 'red', 'yellow', 'green']
        self.difficulties = ['easy', 'medium', 'hard']
        self.colors = {
            'blue': (0, 0, 255),
            'red': (255, 0, 0),
            'yellow': (255, 255, 0),
            'green': (0, 255, 0)
        }
        self.selected_color = 0
        self.selected_difficulty = 0
        self.in_color_selection = True

        # טען את פריימי ה-GIF
        self.gif_frames = []
        frame_count = 5  # מספר הפריימים בגיף
        for i in range(frame_count):
            frame_path = f'Pic/frame_{i}.png'
            frame = pygame.image.load(frame_path)
            # שינוי גודל הפריימים כך שיכסו את החלק העליון של המסך
            frame = pygame.transform.scale(frame, (800, 300))
            self.gif_frames.append(frame)

        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 300  # זמן בין פריימים במילישניות (האטה)

        # טען סאונד לתנועה בתפריט
        self.move_sound_path = 'sounds/menu_move.wav'
        self.move_sound = pygame.mixer.Sound(self.move_sound_path)

    def draw(self, screen):
        screen.fill((0, 0, 0))

        # הצג את פריימי ה-GIF בראשית העמוד
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.gif_frames)

        gif_image = self.gif_frames[self.current_frame]
        screen.blit(gif_image, (0, 0))  # הצגת התמונה מהחלק העליון של המסך

        font = pygame.font.Font(None, 36)
        if self.in_color_selection:
            for i, option in enumerate(self.options):
                color = (255, 255, 255) if i == self.selected_color else (100, 100, 100)
                text = font.render(option, True, color)
                screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 320 + i * 40))  # מיקום הטקסט מתחת לתמונה
        else:
            for i, difficulty in enumerate(self.difficulties):
                color = (255, 255, 255) if i == self.selected_difficulty else (100, 100, 100)
                text = font.render(difficulty, True, color)
                screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 320 + i * 40))  # מיקום הטקסט מתחת לתמונה

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.in_color_selection:
                if event.key == pygame.K_UP:
                    self.selected_color = (self.selected_color - 1) % len(self.options)
                    self.move_sound.play()
                elif event.key == pygame.K_DOWN:
                    self.selected_color = (self.selected_color + 1) % len(self.options)
                    self.move_sound.play()
                elif event.key == pygame.K_RETURN:
                    self.in_color_selection = False  # מעבר לבחירת רמת קושי
                    self.move_sound.play()
            else:
                if event.key == pygame.K_UP:
                    self.selected_difficulty = (self.selected_difficulty - 1) % len(self.difficulties)
                    self.move_sound.play()
                elif event.key == pygame.K_DOWN:
                    self.selected_difficulty = (self.selected_difficulty + 1) % len(self.difficulties)
                    self.move_sound.play()
                elif event.key == pygame.K_RETURN:
                    return self.options[self.selected_color], self.difficulties[self.selected_difficulty]
        return None

    def get_selected_color(self):
        return self.colors[self.options[self.selected_color]]

    def get_selected_difficulty(self):
        return self.difficulties[self.selected_difficulty]
