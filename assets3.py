import base64
import io
import pygame

# ── 1. 모든 애니메이션 통합 Base64 데이터 ──
# (모든 프레임이 포함된 시트 하나만 있으면 됩니다)
SHEET_B64 = "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"

# ── 2. 초기화 함수 ──
def get_sprite_dict():
    """게임에서 사용할 모든 애니메이션 딕셔너리를 생성하여 반환합니다."""
    sheet_bytes = base64.b64decode(SHEET_B64)
    sheet = pygame.image.load(io.BytesIO(sheet_bytes)).convert_alpha()
    
    FRAME_W, FRAME_H = 8, 8
    COLS = 13
    
    # 전체 프레임 미리 추출
    all_frames = []
    for i in range(104):
        row, col = divmod(i, COLS)
        rect = pygame.Rect(col * FRAME_W, row * FRAME_H, FRAME_W, FRAME_H)
        all_frames.append(sheet.subsurface(rect))
        
    # 딕셔너리 구성 (요청하신 모든 모션 합체)
    animations = {
        "heart": [all_frames[2]], # 하트 (2)
        "boom": [all_frames[i] for i in [90, 89, 88]], # 폭탄 (90, 89, 88)
        "recovery": [all_frames[52]], # 회복 (52)
        "shield": [all_frames[39]], # 보호막 (39)
        "explosion": [all_frames[16]] # 폭발 (16)
    }
    return animations

# ── 3. 실제 게임 실행 루프 (테스트용) ──
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((400, 400))
    clock = pygame.time.Clock()
    
    # 애니메이션 데이터 불러오기
    anims = get_sprite_dict()
    
    # 설정 변수
    states = list(anims.keys())
    current_idx = 0
    frame_idx = 0
    
    print(f"현재 로드된 상태: {states}")
    print("스페이스바를 눌러 상태를 변경하세요!")

    running = True
    while running:
        screen.fill((30, 30, 30))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    current_idx = (current_idx + 1) % len(states)
                    frame_idx = 0

        # 현재 상태의 프레임 가져오기
        state = states[current_idx]
        frames = anims[state]
        
        # 애니메이션 업데이트
        frame_idx = (frame_idx + 0.1) % len(frames)
        img = frames[int(frame_idx)]
        
        # 10배 확대 출력
        scaled = pygame.transform.scale(img, (80, 80))
        screen.blit(scaled, (160, 160))
        
        # 화면에 상태 텍스트 표시 (참고용)
        # 폰트 설정이 필요할 수 있으나 생략
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
