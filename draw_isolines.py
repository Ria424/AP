# 등신호선 그리기
# 필요 패키지: numpy, matplotlib

import matplotlib.pyplot as plt
import numpy as np

# --- 환경 설정 (기숙사 평면) ---
width, height = 40, 20  # 전체 크기 (m) → 높이를 2배로 변경

# 방/복도 비율
# 아래 방: 0 ~ 7
# 복도: 7 ~ 11
# 위 방: 11 ~ 20

# AP 위치 (복도 중앙 = y=9)
aps = [(2.5, 9.0), (7.5, 9.0), (22.5, 9.0), (27.5, 9.0)]

# 등신호선 기준 RSSI (dBm)
thresholds_dbm = [-50, -60, -70]


# dBm → S(0~1) 정규화 함수
def dbm_to_S(dbm, r_min=-90, r_max=-40):
    S = (dbm - r_min) / (r_max - r_min)
    return np.clip(S, 1e-6, 1.0)


# S = 1 / (1 + d^2) → 반지름 계산
def S_to_radius(S):
    return np.sqrt(1.0 / S - 1.0) * 2.5


# --- 그림 설정 ---
fig, ax = plt.subplots(figsize=(12, 6))
ax.set_xlim(0, width)
ax.set_ylim(0, height)
ax.set_aspect("equal")
ax.set_title("Isolines")
ax.set_xlabel("Width (m)")
ax.set_ylabel("Height (m)")

# ---- 방 구조 그리기 ----

# 방 사이 세로 벽 (0~7 과 11~20)
for i in range(1, 8):
    x = i * 5
    # 아래쪽 방
    ax.plot([x, x], [0, 7], color="k", linewidth=1)
    # 위쪽 방
    ax.plot([x, x], [11, 20], color="k", linewidth=1)

# 복도 상·하 경계
ax.plot([0, 40], [7, 7], color="k", linewidth=1)
ax.plot([0, 40], [11, 11], color="k", linewidth=1)

# 외벽
ax.plot([0, 0], [0, 20], color="k", linewidth=2)
ax.plot([40, 40], [0, 20], color="k", linewidth=2)
ax.plot([0, 40], [0, 0], color="k", linewidth=2)
ax.plot([0, 40], [20, 20], color="k", linewidth=2)

# ---- 등신호선 그리기 ----
colors = ["red", "orange", "blue"]
for idx, ap in enumerate(aps):
    ax.scatter(ap[0], ap[1], color="white", edgecolors="black", s=80, zorder=5)
    ax.text(ap[0] + 0.3, ap[1] + 0.3, f"AP{idx + 1}", color="black")

    for dbm, col in zip(thresholds_dbm, colors):
        S = dbm_to_S(dbm)
        r = S_to_radius(S) * 2.2  # ← 원 크기 조정(2.2배 확대)

        theta = np.linspace(0, 2 * np.pi, 200)
        x_circle = ap[0] + r * np.cos(theta)
        y_circle = ap[1] + r * np.sin(theta)
        ax.plot(
            x_circle,
            y_circle,
            color=col,
            linestyle="--",
            linewidth=1,
            alpha=0.75,
            label=f"{dbm} dBm" if idx == 0 else "",
        )

# 범례
ax.legend(loc="upper right")

ax.grid(which="both", linestyle=":", linewidth=0.5, alpha=0.4)

plt.tight_layout()
plt.show()
