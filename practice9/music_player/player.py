import pygame

def runp():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((600, 200))
    pygame.display.set_caption("Music Player")
    font = pygame.font.SysFont(None, 40)

    playlist = [
        "music/t1.mp3",
        "music/t2.mp3",
        "music/t3.mp3",
        "music/t4.mp3"
    ]

    now = 0
    playing = False

    pygame.mixer.music.load(playlist[now])

    running = True
    while running:
        screen.fill((0, 0, 0))

        text = font.render(f"Track: [{playlist[now]}]", True, (255, 255, 255))
        screen.blit(text, (20, 20))

        state = "stop" if playing else "play"
        s = font.render(state, True, (255, 255, 255))
        screen.blit(s, (20, 60))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pygame.mixer.music.play()
                    playing = True

                elif event.key == pygame.K_s:
                    pygame.mixer.music.stop()
                    playing = False

                elif event.key == pygame.K_n:
                    now = (now + 1) % len(playlist)
                    pygame.mixer.music.load(playlist[now])
                    if playing:
                        pygame.mixer.music.play()

                elif event.key == pygame.K_b:
                    now = (now - 1) % len(playlist)
                    pygame.mixer.music.load(playlist[now])
                    if playing:
                        pygame.mixer.music.play()

                elif event.key == pygame.K_q:
                    running = False

        pygame.display.update()

    pygame.quit()