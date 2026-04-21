import base64, io
import pygame

# ── 1. 캐릭터 리소스 데이터 (Base64 인코딩) ──
ASSETS_B64 = {
    # 16x16 픽셀 캐릭터 (플레이어 및 보스 유닛)
    "player_walk": "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAALGPC/xhBQAAADhlWElmTU0AKgAAAAgAAYdpAAQAAAABAAAAGgAAAAAAAqACAAQAAAABAAAAEKADAAQAAAABAAAAEAAAAAA0v8mUAAAAZ0lEQVQ4y2NgGAWjYBSMAt6A8df+f6B8v6H8PwN5+v8pU//v/08B8v6D8f8z8Of/r0G+/n8N/On/10C8f39O/j8N8f79Ofn/NMj79+fk/9Mgf76D7Wf4Px0o/x8oD7Z/FIyCUYAdAADuY6S99F59LwAAAABJRU5ErkJggg==",
    "boss1_walk": "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAALGPC/xhBQAAAD1JREFUKFNjYKA7YITid9mG/5kgHP7/DPjPBOEw/P9m6P9/CvD/X7S///+rYPyfCfr/P4PxfzrS/G8Ghv8A36gl7XpZ8T0AAAAASUVORK5CYII=",
    "boss2_walk": "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAALGPC/xhBQAAADtJREFUKFNjYKA7YITid9mG/5kgHP7/DPjPBOEw/P9m6P9/CvD/X7S///+rYPyfCfr/P4PxfzrS/G8Ghv8A39Ym7XpZ8X0AAAAASUVORK5CYII=",
    "boss3_walk": "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAALGPC/xhBQAAADtJREFUKFNjYKA7YITid9mG/5kgHP7/DPjPBOEw/P9m6P9/CvD/X7S///+rYPyfCfr/P4PxfzrS/G8Ghv8A3+Um7XpZ8X0AAAAASUVORK5CYII=",
    "boss4_walk": "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAALGPC/xhBQAAADtJREFUKFNjYKA7YITid9mG/5kgHP7/DPjPBOEw/P9m6P9/CvD/X7S///+rYPyfCfr/P4PxfzrS/G8Ghv8A3+cm7XpZ8X0AAAAASUVORK5CYII=",
    "final_boss_walk": "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAALGPC/xhBQAAADtJREFUKFNjYKA7YITid9mG/5kgHP7/DPjPBOEw/P9m6P9/CvD/X7S///+rYPyfCfr/P4PxfzrS/G8Ghv8A3+bm7XpZ8X0AAAAASUVORK5CYII=",

    # 8x8 픽셀 캐릭터 (일반 적 유닛)
    "red_enemy_walk": "iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAYAAADED76LAAAABGdBTUEAALGPC/xhBQAAAD5JREFUKFNjYMADGCHYmIGB4T8D7vB/0tj//58B0vj/p0z9v/8/Bcj7D8b/z8Cf/78G+fr/NfCn/18D8f79Ofn/NAAAtHskCis3B3QAAAAASUVORK5CYII=",
    "yellow_enemy_walk": "iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAYAAADED76LAAAABGdBTUEAALGPC/xhBQAAADtJREFUKFNjYMAA7pCH/5kgHIn/L5f/M0E4v0H8nx6Y8R/M+A/m/Acz/v8ZMP7/P8P//0f4/z8E8/9/ALZpIsW8R30HAAAAAElFTkSuQmCC",
    "green_enemy_walk": "iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAYAAADED76LAAAABGdBTUEAALGPC/xhBQAAADtJREFUKFNjYMACzpCH/5kgHIn/L5f/M0E4v0H8nx6Y8R/M+A/m/Acz/v8ZMP7/P8P//0f4/z8E8/9/ALaEIsVE9L9lAAAAAElFTkSuQmCC"
}

# ── 2. 엔진 초기화 및 데이터 변환 함수 ──
pygame.init()

def get_surface(b64_str):
    """Base64 문자열을 Pygame Surface 객체로 변환"""
    image_data = base64.b64decode(b64_str)
    return pygame.image.load(io.BytesIO(image_data)).convert_alpha()

# ── 3. 캐릭터별 애니메이션 프레임 리스트 생성 ──

# 16x16 유닛 그룹
player_walk_frames = [get_surface(ASSETS_B64["player_walk"])]
boss1_walk_frames = [get_surface(ASSETS_B64["boss1_walk"])]
boss2_walk_frames = [get_surface(ASSETS_B64["boss2_walk"])]
boss3_walk_frames = [get_surface(ASSETS_B64["boss3_walk"])]
boss4_walk_frames = [get_surface(ASSETS_B64["boss4_walk"])]
final_boss_walk_frames = [get_surface(ASSETS_B64["final_boss_walk"])]

# 8x8 유닛 그룹
red_enemy_walk_frames = [get_surface(ASSETS_B64["red_enemy_walk"])]
yellow_enemy_walk_frames = [get_surface(ASSETS_B64["yellow_enemy_walk"])]
green_enemy_walk_frames = [get_surface(ASSETS_B64["green_enemy_walk"])]

# ── 4. 런타임 적용 변수 설정 ──
# 현재 적용할 애니메이션 프레임셋을 할당합니다.
walk_frames = final_boss_walk_frames
