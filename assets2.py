import base64, io
import pygame

# ── Base64 Sprite Sheet Data (Shared) ──
# 하나의 이미지 시트 데이터를 공유하여 메모리를 절약합니다.
SHEET_B64 = "iVBORw0KGgoAAAANSUhEUgAAADAAAABQCAYAAABf9vbdAAAAAXNSR0IArs4c6QAAB2RJREFUaIHtWz1oHEcU/jaoSOHAFVZ3AQVikMCBU2GwwM02gissuHQqcrCNQYUCp0KwLlxcYYEKBdaFIY1gXAhcWLApDFdExQVUXCGBAgqcwQenbl0IJoW7l2L19ub25s39yrJjfSDuNG81+72fmXnzZgTc4hafD6ityClvNYhaDeczzZhEeXRGFJ3JcgCAIi0+oKjlJjhMgbBEFJbk/mspOf40Eahem/l9LJTVhpugglPerYC6Ffczt/hqQTqi5GyBkrMFIh1dS5i0dJ1aut7X9zfmL20/cL7498Qev8nZQtZ+d2FroI3hR03yo6b4DmokRI3EKm/pOp18fIaTj89gKpEp0PYD+nGhIipRUaDlb+uo5AYq6YjuLmzhQ2cvJX9nM/tuesKPmrTgL2TfbeRxcAwcHCOvBBvuyTy8J/PwzLYMcaFEFMQUF+RpLu8+ILU06Yj6YIQTE/ajJinSpEhTcNbt8wQ1EqIg7v0exJknWrpOeaOxQVu6TpkH1i5PvXedQ6xdnnqSAicfn1nbP3T2gH9f9BrubGahxGDrA0DnqNMne7ezDW9/LXuvt7/mvdvZzuSHVQxwsrXBZX0AA+EDpCHEFjetz+38HHshb/2ZYhIFACOMDPKTDOIbxaeYRv//aNbcecqwZG4WUCWZQ7cCysv7FrJHy46Or8hPqoS5vrgWzEI9Fvs4CWKcl8O+tkwBUiCsKGdGeXJx7CTJc7xNdu9o3+P5/d7RvnWqjuN0LQjDcGQjZQp4VXg4rqafDvIuJY7+voR/vyC/bX0FOHAbYW1tTVyHhsI1BmrdiMpqg2rdyWaYUUNIAnsHGM9DGXgzM2xTc4uvFm0/IApikuKTY9CMRRuG7YutfV+lMGEYEse3La2xrQPZiDeJ2WaCJElofn7e408reR2R992vHimQNJtJCMOQlpaWAADn5+fY2dkZ+PtuBXT0HqieCn0niX03lBEkdzmDcyBbIgcApcrgfoLJK6VIldKqhVKK8jNNHMcUxzGZXgJyK/G0+NDZA4CBvQCT33pTE5UAAP8H4Oi9XWZGhc07ANwWZu+4vMTxL2WjLvKZFyzW5z7ZA5KHnQp8DoP46wQREbUVmZYlhbRtyKD+5OAto1my4IKtWbi1tUW+tn43kSQJDQtBF1yF54E6CytjWpsUqFlLnWJ6JfI1mRVlVSPKKxGGIfEEMFEyBkBK1ftgq/0A/ZmqNFBVjchW32ersweSJCFpNpOUU6Sz2pKVeL7ikPeISVpKu5sxka22z4SZvKmUCZbbZGx9pxeYdEUYsM0aiNTkIcTKuEJIknE5ZuyyzCwHsemBcTG5Al/SNDoq/KhJ0RlZFdABkatMbqYZ11YAq2mflLYf2Jnk8yeGbb9JOjCq1DklhpHnbLRbgfUwkPvvxumPk3xN+6ICTN6Mx4x8I7EqYCZgYjLGyoWloYeBVgXKrwtU076TPBPPD6a23+yRbySkAyId0ABpk7zNC0zcpgBbn79bFSi/Loia562e79wk3/b7n9vdBQ0jb24XpRIjE8/3DxdxwD19sfWZeL7z8jpodzf9MU9uJPLSO0ThNOS5c9cLyuug8voNHXCPQt4lvzHiw6C0EqdaoDcluvqQ1opxIG7qzVslDzfQ911pRYeHVbHTMAypUI/FDTpXqb3VwfLMKKc8bT9wnqbCdiXm4QaIyVcUROuHYZhtvl3kzWPVgWeEMzazD7FA7LoOA6SZqtKKTK/MkrxtvWAMt/wI5IH+kOpW0nxvGvIu0vk+RMuPc4/HVGBa8kx8qpif5BISK2GSl9LrUWNe8oDT8rMAk7cZYhZTpQsD0xhvDau/eZmsWwEVF0vAz7vpHz1YHfscq6w2aNFPq8/LxRVUvQeTn4XZEPmaeG/bjHvVBdOqnKfbbh/yPQi+kWJWD8xjKUUtqnUjko5rQx/Z3lviOjBeeA9rkpcqDMDV7UPh+qSpRJ48HxBKSoR+rxYlVT6cAz7ydR95SQFJCfNGSr5+kz8cZCUG+r2yPCszMvmgoKgZUxZGUmWB0a3A6gVO/lz1GyaeV4CtPhF5VSMKCvYyiQTXwidlsaYnzO820oyhN2AiX49NHphs/WCMSh4YskKbxMfBrMh/FjCrZtIgngbmLYH87OXxdcj9n76f2cLCffr3Czh4lV7ee1t9OVX/ptcW/aVsMfQUadp/cdp3q3AW6Bx1EGyWUPW+81whw6vzJFgursCbpattOHi1PbX18+Dpd7m4Mttz4pvAHABcZwi9rb68thACgDkmfx2DGOgNPimM3o7YpzSIp+UK4Gan0S8froxzEnAyyP3O8n9mrGcHRGnmact/ODvNH+KZZCV5M76qVrcaM//HHzMTngOAzT/vAAAKW0S8leQdGctSDMofPYZVbqL4tAF6mipx8Xw1bVsspcKrbSrDJb94vopsa/tmG9Rq0BwA/PVH+sAve8DlqaZCKSX96DHgeT3C48rzxIqLJRSfNpyEXfJM9mYbF/+cosgvZvdnbif7Ad4k8usOoZFz/2leNsu+pAPALxb/Ae7MWVBLUySEAAAAAElFTkSuQmCC"

# ── Asset Configurations ──
# 같은 이미지에서 서로 다른 속성을 가진 두 개의 자산 정보를 정의합니다.
BULLET_ASSETS = {
    "player_bullet": {
        "data": SHEET_B64,
        "frame_size": (8, 8),
        "cols": 6,
        "total": 60,
        "anims": {"walk": [2]} # 플레이어 탄환 프레임 인덱스
    },
    "enemy_bullet": {
        "data": SHEET_B64,
        "frame_size": (8, 8),
        "cols": 6,
        "total": 60,
        "anims": {"walk": [3]} # 적 탄환 프레임 인덱스
    }
}

# ── Sprite Loading Logic ──
# 딕셔너리 설정을 기반으로 Pygame Surface 객체를 생성합니다.
def load_bullets():
    pygame.init()
    result = {}
    
    for key, info in BULLET_ASSETS.items():
        # Base64 디코딩 및 이미지 로드
        sheet_bytes = base64.b64decode(info["data"])
        sheet_surf = pygame.image.load(io.BytesIO(sheet_bytes)).convert_alpha()
        
        # 전체 프레임 자르기 (Subsurface 생성)
        temp_frames = []
        w, h = info["frame_size"]
        for i in range(info["total"]):
            row, col = divmod(i, info["cols"])
            rect = pygame.Rect(col * w, row * h, w, h)
            temp_frames.append(sheet_surf.subsurface(rect))
            
        # 정의된 애니메이션 순서에 맞게 프레임 리스트 할당
        anim_dict = {}
        for anim_name, indices in info["anims"].items():
            anim_dict[anim_name] = [temp_frames[idx] for idx in indices]
        
        result[key] = anim_dict
        
    return result

# ── Data Initialization ──
# 게임 루프에서 사용할 최종 스프라이트 데이터셋
loaded_data = load_bullets()

# 개별 접근 예시
player_walk_frames = loaded_data["player_bullet"]["walk"]
enemy_walk_frames = loaded_data["enemy_bullet"]["walk"]
