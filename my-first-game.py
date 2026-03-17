import pygame
import random
import math

pygame.init()

# 화면 설정
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sunset Firework Sparkler")

clock = pygame.time.Clock()
particles = []

class Particle:
    def __init__(self, x, y, is_firework=False):
        self.x = x
        self.y = y
        
        # 일반 마우스 스파클러와 불꽃놀이 폭발 효과 구분
        angle = random.uniform(0, math.pi * 2)
        if is_firework:
            speed = random.uniform(4, 12) # 폭발은 더 빠르게
        else:
            speed = random.uniform(1, 5)

        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

        self.max_life = random.randint(40, 80)
        self.life = self.max_life
        self.initial_size = random.randint(3, 7)
        
        # 불꽃 컬러 (빨강, 주황, 금색 위주)
        colors = [
            (255, 50, 0),   # 진한 빨강
            (255, 100, 0),  # 주황
            (255, 200, 50), # 금색/노랑
            (200, 20, 0)    # 핏빛 빨강
        ]
        self.color = random.choice(colors)

    def update(self):
        # 공기 저항 및 중력
        self.vx *= 0.96
        self.vy *= 0.96
        self.vy += 0.15 # 중력 적용
        
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self, surf):
        if self.life > 0:
            size = (self.life / self.max_life) * self.initial_size
            alpha = int((self.life / self.max_life) * 255)
            
            # 발광 효과를 위한 서피스
            s = pygame.Surface((size * 6, size * 6), pygame.SRCALPHA)
            # 바깥쪽 은은한 붉은 광원
            pygame.draw.circle(s, (*self.color, alpha // 3), (size * 3, size * 3), size * 2.5)
            # 중심부 밝은 빛
            pygame.draw.circle(s, (255, 255, 200, alpha), (size * 3, size * 3), size * 0.8)
            
            surf.blit(s, (int(self.x - size * 3), int(self.y - size * 3)))

    def alive(self):
        return self.life > 0

def draw_sunset_background(surface):
    # 위에서 아래로 흐르는 노을 그라데이션
    for y in range(HEIGHT):
        # 상단(진한 주황/빨강) -> 하단(어두운 보라/검정)
        r = max(0, min(255, 70 - y // 10)) 
        g = max(0, min(255, 30 - y // 20))
        b = max(0, min(255, 20 + y // 30))
        
        # 실제 노을 느낌의 색 배합
        r = int(120 - (y / HEIGHT) * 100)
        g = int(40 - (y / HEIGHT) * 40)
        b = int(60 - (y / HEIGHT) * 30)
        pygame.draw.line(surface, (max(r, 20), max(g, 5), max(b, 10)), (0, y), (WIDTH, y))

running = True

# 초기 배경 그리기
draw_sunset_background(screen)

while running:
    # 1. 잔상 효과를 위해 매 프레임 약간 투명한 배경 덮기
    # (완전히 새로 그리지 않고 덧칠하여 궤적을 만듭니다)
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(40) # 이 수치가 낮을수록 잔상이 길게 남습니다
    draw_sunset_background(overlay)
    screen.blit(overlay, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # 마우스 클릭 시 불꽃놀이 펑!
        if event.type == pygame.MOUSEBUTTONDOWN:
            for _ in range(100): # 한 번에 많은 입자 생성
                particles.append(Particle(event.pos[0], event.pos[1], True))

    # 마우스 누르고 있을 때 지속적인 불꽃 가루
    mouse = pygame.mouse.get_pos()
    buttons = pygame.mouse.get_pressed()
    if buttons[0]:
        for _ in range(3):
            particles.append(Particle(mouse[0], mouse[1]))

    # 업데이트 및 그리기
    for p in particles:
        p.update()
        p.draw(screen)

    particles = [p for p in particles if p.alive()]

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
