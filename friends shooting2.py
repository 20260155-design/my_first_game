import pygame
import random
import sys
import math
import io
import base64

# --- 자산 파일 임포트 (상대 경로) ---
import assets
import assets2
import assets3

# --- 초기화 ---
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

# --- 창 설정 ---
is_fullscreen = False
WINDOW_SIZE = (WIDTH, HEIGHT)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Friends Shooting")
clock = pygame.time.Clock()

# --- 색상 정의 ---
WHITE, BLACK, GRAY = (255, 255, 255), (0, 0, 0), (20, 20, 40)
BLUE, RED, YELLOW, GREEN = (50, 150, 255), (220, 50, 50), (240, 220, 0), (50, 220, 80)
ORANGE, PURPLE = (240, 140, 0), (150, 50, 255)

# --- 이미지 및 사운드 리소스 로드 ---
# 1. 캐릭터 이미지 (assets.py)
PLAYER_IMG = pygame.transform.scale(assets.player_walk_frames[0], (40, 40))
E_RED_IMG = pygame.transform.scale(assets.red_enemy_walk_frames[0], (36, 36))
E_YEL_IMG = pygame.transform.scale(assets.yellow_enemy_walk_frames[0], (36, 36))
E_GRN_IMG = pygame.transform.scale(assets.green_enemy_walk_frames[0], (36, 36))
BOSS_IMGS = [
    pygame.transform.scale(assets.boss1_walk_frames[0], (100, 80)),
    pygame.transform.scale(assets.boss2_walk_frames[0], (100, 80)),
    pygame.transform.scale(assets.boss3_walk_frames[0], (100, 80)),
    pygame.transform.scale(assets.boss4_walk_frames[0], (100, 80)),
    pygame.transform.scale(assets.final_boss_walk_frames[0], (120, 100))
]

# 2. 탄환 이미지 (assets2.py)
bullet_data = assets2.load_bullets()
P_BULLET_IMG = pygame.transform.scale(bullet_data["player_bullet"]["walk"][0], (6, 14))
E_BULLET_IMG = pygame.transform.scale(bullet_data["enemy_bullet"]["walk"][0], (12, 12))

# 3. 아이템 이미지 (assets3.py)
item_anims = assets3.get_sprite_dict()
ITEM_IMGS = {
    'heart': pygame.transform.scale(item_anims['heart'][0], (25, 25)),
    'bomb': pygame.transform.scale(item_anims['boom'][0], (25, 25)),
    'shield': pygame.transform.scale(item_anims['shield'][0], (25, 25)),
    'special': pygame.transform.scale(item_anims['recovery'][0], (40, 40))
}

# 4. 효과음 (파일이 있을 경우에만 로드)
try:
    SND_SHOOT = pygame.mixer.Sound("shoot.wav")
    SND_EXPLODE = pygame.mixer.Sound("explosion.wav")
    SND_ITEM = pygame.mixer.Sound("item.wav")
except:
    SND_SHOOT = SND_EXPLODE = SND_ITEM = None

# --- 폰트 설정 ---
def get_korean_font(size):
    candidates = ["malgungothic", "nanumgothic", "notosanscjk", "arial"]
    for name in candidates:
        font = pygame.font.SysFont(name, size)
        if font.get_ascent() > 0: return font
    return pygame.font.SysFont(None, size)

font_small = get_korean_font(20)
font_mid = get_korean_font(36)
font_big = get_korean_font(72)

# --- 유틸리티 함수 ---
def get_safe_x(enemies, width, min_distance=60):
    max_tries = 10
    for _ in range(max_tries):
        x = random.randint(0, width - 40)
        safe = True
        for en in enemies:
            if en.rect.y < 100 and abs(en.rect.x - x) < min_distance:
                safe = False; break
        if safe: return x
    return random.randint(0, width - 40)

# --- 클래스 정의 ---
class Bullet:
    def __init__(self, x, y, dx=0, dy=-10, color=YELLOW, is_homing=False):
        self.rect = pygame.Rect(x, y, 6, 14)
        self.dx, self.dy = dx, dy
        self.color = color
        self.is_homing = is_homing

    def update(self, enemies, boss=None, player_rect=None):
        if self.is_homing:
            target = boss if boss else (player_rect if player_rect else (min(enemies, key=lambda e: math.hypot(e.rect.centerx - self.rect.centerx, e.rect.centery - self.rect.centery)) if enemies else None))
            if target:
                target_rect = target.rect if hasattr(target, 'rect') else target
                tx, ty = target_rect.center
                angle = math.atan2(ty - self.rect.centery, tx - self.rect.centerx)
                self.dx, self.dy = math.cos(angle) * 7, math.sin(angle) * 7
        self.rect.x += self.dx
        self.rect.y += self.dy

class Enemy:
    def __init__(self, type_name, stiffness, x=None): 
        self.type = type_name
        start_x = x if x is not None else random.randint(0, WIDTH-40)
        self.rect = pygame.Rect(start_x, -40, 36, 36)
        self.hp = stiffness
        self.speed = 3
        self.dir = 1
        self.shoot_timer = random.randint(0, 100)

    def update(self, e_bullets):
        if self.type == "red": self.rect.y += self.speed
        elif self.type == "yellow":
            self.rect.y += self.speed
            self.rect.x += self.dir * 3
            if self.rect.right >= WIDTH or self.rect.left <= 0: self.dir *= -1
        elif self.type == "green":
            self.rect.y += self.speed
            self.shoot_timer += 1
            if self.shoot_timer >= 100:
                for angle in [-0.5, 0, 0.5]:
                    e_bullets.append(Bullet(self.rect.centerx, self.rect.bottom, math.sin(angle)*5, math.cos(angle)*5, GREEN))
                self.shoot_timer = 0

class Boss:
    def __init__(self, hp, level, is_final=False):
        self.rect = pygame.Rect(WIDTH//2 - 50, -100, 100, 80)
        self.hp = hp
        self.max_hp = hp
        self.level = min(level, 5)
        self.is_final = is_final
        self.timer = 0
        self.pattern = [1, 2, 3, 4] if is_final else random.sample([1, 2, 3, 4], 2)
        self.current_p_idx = 0
        self.image = BOSS_IMGS[4] if is_final else BOSS_IMGS[self.level-1]

    def update(self, e_bullets, enemies, player_rect):
        if self.rect.y < 120: self.rect.y += 2; return
        self.rect.x = (WIDTH//2 - 50) + math.sin(self.timer * 0.03) * (250 if self.is_final else 150)
        self.timer += 1
        if self.timer % 300 == 0: self.current_p_idx = (self.current_p_idx + 1) % len(self.pattern)
        p = self.pattern[self.current_p_idx]
        if p == 1 and self.timer % 40 == 0:
            for i in range(-2, 3): e_bullets.append(Bullet(self.rect.centerx, self.rect.bottom, i*2, 5, RED))
        elif p == 2 and self.timer % 50 == 0:
            for i in range(8):
                ang = i * (math.pi/4)
                e_bullets.append(Bullet(self.rect.centerx, self.rect.centery, math.cos(ang)*4, math.sin(ang)*4, PURPLE))
        elif p == 3 and self.timer % 15 == 0:
            angle = math.atan2(player_rect.centery - self.rect.centery, player_rect.centerx - self.rect.centerx)
            e_bullets.append(Bullet(self.rect.centerx, self.rect.centery, math.cos(angle)*8, math.sin(angle)*8, ORANGE))
        elif p == 4 and self.timer % 100 == 0:
            enemies.append(Enemy(random.choice(["red", "yellow", "green"]), (self.level + 1) // 2))

class Companion:
    def __init__(self, level):
        self.level = level
        self.angle = 0
        self.shoot_delay = 7000 - (self.level - 1) * 2000
        self.last_shoot = pygame.time.get_ticks()

    def update(self, px, py, enemies, boss, bullets, companions):
        count = len(companions)
        idx = companions.index(self)
        target_angle = (2 * math.pi / count) * idx + (pygame.time.get_ticks() / 1000)
        self.angle += (target_angle - self.angle) * 0.1
        now = pygame.time.get_ticks()
        if now - self.last_shoot > self.shoot_delay:
            if enemies or boss:
                cx, cy = px + math.cos(self.angle) * 60, py + math.sin(self.angle) * 60
                bullets.append(Bullet(cx, cy, 0, -10, color=ORANGE, is_homing=True))
                self.last_shoot = now

class Item:
    def __init__(self, x, y, itype):
        self.rect = pygame.Rect(x, y, 25, 25)
        self.type = itype

# --- 메인 게임 루프 ---
def main():
    player_rect = pygame.Rect(WIDTH // 2 - 20, HEIGHT - 70, 40, 40)
    bullets, e_bullets, enemies, companions, items = [], [], [], [], []
    score = 0; level = 1; lives = 3.0; max_lives = 3.0; invincible = 0; shield_timer = 0
    boss = None; is_final = False; start_time = pygame.time.get_ticks()
    stat_items = stat_enemies = stat_special = stat_lives_lost = stat_lives_recovered = 0
    last_shot_time = 0

    running = True
    while running:
        clock.tick(FPS)
        now = pygame.time.get_ticks()
        screen.fill(GRAY)

        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()

        # 입력 처리
        keys = pygame.key.get_pressed()
        speed = 6
        if keys[pygame.K_LEFT] and player_rect.left > 0: player_rect.x -= speed
        if keys[pygame.K_RIGHT] and player_rect.right < WIDTH: player_rect.x += speed
        if keys[pygame.K_UP] and player_rect.top > 0: player_rect.y -= speed
        if keys[pygame.K_DOWN] and player_rect.bottom < HEIGHT: player_rect.y += speed

        # 발사 및 효과음
        if keys[pygame.K_SPACE] and now - last_shot_time > 150:
            bullets.append(Bullet(player_rect.centerx - 3, player_rect.top))
            if SND_SHOOT: SND_SHOOT.play()
            last_shot_time = now

        # 적 스폰 및 보스 등장
        if score >= level * 500 and boss is None and not is_final:
            if level < 5: boss = Boss(100 + (level-1)*200, level)
            else: boss = Boss(1000, level, is_final=True); is_final = True

        if boss is None and random.random() < 0.025:
            enemies.append(Enemy(random.choice(["red", "yellow", "green"]), (level + 1) // 2, get_safe_x(enemies, WIDTH)))

        # 업데이트 로직
        if boss: boss.update(e_bullets, enemies, player_rect)
        for en in enemies[:]:
            en.update(e_bullets)
            if en.rect.top > HEIGHT: enemies.remove(en)
        
        for c in companions: c.update(player_rect.centerx, player_rect.centery, enemies, boss, bullets, companions)
        
        # 충돌 처리 (플레이어 탄환)
        for b in bullets[:]:
            b.update(enemies, boss)
            if b.rect.bottom < 0: bullets.remove(b); continue
            if boss and b.rect.colliderect(boss.rect):
                boss.hp -= 1; bullets.remove(b)
                if boss.hp <= 0:
                    if SND_EXPLODE: SND_EXPLODE.play()
                    items.append(Item(boss.rect.centerx, boss.rect.centery, 'special'))
                    boss = None; level += 1; stat_special += 1
                    if is_final: running = False
                continue
            for en in enemies[:]:
                if b.rect.colliderect(en.rect):
                    en.hp -= 1; bullets.remove(b)
                    if en.hp <= 0:
                        enemies.remove(en); score += 10; stat_enemies += 1
                        if random.random() < 0.15 and len(companions) < 10: companions.append(Companion(1))
                        elif random.random() < 0.1: items.append(Item(en.rect.centerx, en.rect.centery, random.choice(['shield', 'bomb', 'heart'])))
                    break

        # 충돌 처리 (적 탄환 및 몸체)
        for eb in e_bullets[:]:
            eb.update([], None, player_rect)
            if eb.rect.colliderect(player_rect) and invincible <= 0:
                e_bullets.remove(eb)
                if shield_timer > 0: shield_timer = 0
                else: 
                    lives -= 1; stat_lives_lost += 1; invincible = 60
                    if lives <= 0: running = False

        for it in items[:]:
            it.rect.y += 2
            if it.rect.colliderect(player_rect):
                if SND_ITEM: SND_ITEM.play()
                if it.type == 'shield': shield_timer = 600
                elif it.type == 'heart': lives = min(max_lives, lives + 0.5); stat_lives_recovered += 0.5
                elif it.type == 'special': max_lives += 1; lives = max_lives
                elif it.type == 'bomb': 
                    enemies.clear(); score += len(enemies)*10
                items.remove(it)

        if invincible > 0: invincible -= 1
        if shield_timer > 0: shield_timer -= 1

        # --- 그리기 섹션 (이미지 적용) ---
        # 1. 배경 및 UI
        screen.blit(font_mid.render(f"Score: {score} Lv: {level}", True, WHITE), (10, 10))
        h_str = "♥" * int(lives) + ("½" if lives % 1 != 0 else "")
        screen.blit(font_mid.render(f"HP: {h_str}", True, RED), (WIDTH - 250, 10))

        # 2. 보스 체력바
        if boss:
            pygame.draw.rect(screen, RED, (WIDTH//2-100, 50, 200, 10))
            pygame.draw.rect(screen, GREEN, (WIDTH//2-100, 50, 200 * (boss.hp/boss.max_hp), 10))
            screen.blit(boss.image, boss.rect)

        # 3. 플레이어 및 방패
        if invincible % 10 < 5:
            screen.blit(PLAYER_IMG, player_rect)
            if shield_timer > 0: pygame.draw.circle(screen, BLUE, player_rect.center, 35, 2)

        # 4. 동료 (Companion)
        for c in companions:
            cx, cy = player_rect.centerx + math.cos(c.angle) * 60, player_rect.centery + math.sin(c.angle) * 60
            img = assets.boss1_walk_frames[0] if c.level == 1 else assets.boss3_walk_frames[0]
            screen.blit(pygame.transform.scale(img, (20, 20)), (int(cx)-10, int(cy)-10))

        # 5. 탄환
        for b in bullets: screen.blit(P_BULLET_IMG, b.rect)
        for eb in e_bullets: screen.blit(E_BULLET_IMG, eb.rect)

        # 6. 적
        for en in enemies:
            img = E_RED_IMG if en.type == "red" else E_YEL_IMG if en.type == "yellow" else E_GRN_IMG
            screen.blit(img, en.rect)

        # 7. 아이템
        for it in items:
            img = ITEM_IMGS.get(it.type, ITEM_IMGS['heart'])
            screen.blit(img, it.rect)

        pygame.display.flip()

    # 게임 오버 통계 화면 (기존 코드 유지)
    show_game_over(score, stat_items, stat_enemies, stat_special, stat_lives_lost, stat_lives_recovered, (now - start_time)//1000)

def show_game_over(score, items, enemies, special, lost, recov, time):
    while True:
        screen.fill((10, 10, 30))
        screen.blit(font_big.render("GAME OVER", True, YELLOW), (WIDTH//2-180, 100))
        stats = [f"Score: {score}", f"Enemies: {enemies}", f"Items: {items}", f"Time: {time}s"]
        for i, s in enumerate(stats):
            txt = font_mid.render(s, True, WHITE)
            screen.blit(txt, (WIDTH//2-100, 250 + i*40))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN: main()

if __name__ == "__main__":
    main()


