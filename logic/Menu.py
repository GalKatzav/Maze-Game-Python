import pygame
from interfaces.IMenu import IMenu

class Menu(IMenu):
    def __init__(self):
        self.difficulties = ['easy', 'medium', 'hard']
        self.selected_difficulty = 0

        # Load GIF frames
        self.gif_frames = []
        frame_count = 5  # Number of frames in the GIF
        for i in range(frame_count):
            frame_path = f'Pic/frame_{i}.png'
            frame = pygame.image.load(frame_path)
            frame = pygame.transform.scale(frame, (800, 300))
            self.gif_frames.append(frame)

        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 300  # Time between frames in milliseconds

        # Load menu move sound
        self.move_sound_path = 'sounds/menu_move.wav'
        self.move_sound = pygame.mixer.Sound(self.move_sound_path)

    def draw(self, screen):
        screen.fill((0, 0, 0))

        # Display GIF frames at the top of the page
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.gif_frames)

        gif_image = self.gif_frames[self.current_frame]
        screen.blit(gif_image, (0, 0))

        font = pygame.font.Font(None, 36)
        for i, difficulty in enumerate(self.difficulties):
            color = (255, 255, 255) if i == self.selected_difficulty else (100, 100, 100)
            text = font.render(difficulty, True, color)
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 320 + i * 40))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_difficulty = (self.selected_difficulty - 1) % len(self.difficulties)
                self.move_sound.play()
            elif event.key == pygame.K_DOWN:
                self.selected_difficulty = (self.selected_difficulty + 1) % len(self.difficulties)
                self.move_sound.play()
            elif event.key == pygame.K_RETURN:
                return self.difficulties[self.selected_difficulty]
        return None

    def get_selected_difficulty(self):
        return self.difficulties[self.selected_difficulty]
