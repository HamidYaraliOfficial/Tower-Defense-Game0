import sys, math, random
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

# ─── TRANSLATIONS ────────────────────────────────────────────────────────────
TR = {
    'en': {
        'title': 'Tower Defense', 'start': 'Start', 'pause': 'Pause', 'resume': 'Resume',
        'restart': 'Restart', 'quit': 'Quit', 'theme': 'Theme', 'lang': 'Language',
        'dark': 'Dark', 'light': 'Light', 'wave': 'Wave', 'lives': 'Lives',
        'gold': 'Gold', 'score': 'Score', 'speed': 'Speed', 'sell': 'Sell',
        'upgrade': 'Upgrade', 'towers': 'Towers', 'game_over': 'GAME OVER',
        'victory': 'VICTORY!', 'paused': 'PAUSED', 'select_tower': 'Select Tower',
        'arrow': 'Arrow', 'cannon': 'Cannon', 'laser': 'Laser', 'freeze': 'Freeze',
        'missile': 'Missile', 'dmg': 'DMG', 'rng': 'RNG', 'spd': 'SPD',
        'cost': 'Cost', 'max_wave': 'Max Wave', 'next_wave': 'Next Wave',
        'lives_left': 'Lives', 'enemies': 'Enemies', 'lv': 'Lv',
        'sell_for': 'Sell for', 'upgrade_to': 'Upgrade to Lv',
        'place_tower': 'Click grid to place', 'info': 'Info',
    },
    'zh': {
        'title': '塔防游戏', 'start': '开始', 'pause': '暂停', 'resume': '继续',
        'restart': '重新开始', 'quit': '退出', 'theme': '主题', 'lang': '语言',
        'dark': '深色', 'light': '浅色', 'wave': '波次', 'lives': '生命',
        'gold': '金币', 'score': '分数', 'speed': '速度', 'sell': '出售',
        'upgrade': '升级', 'towers': '塔', 'game_over': '游戏结束',
        'victory': '胜利！', 'paused': '已暂停', 'select_tower': '选择塔',
        'arrow': '箭塔', 'cannon': '炮塔', 'laser': '激光塔', 'freeze': '冰冻塔',
        'missile': '导弹塔', 'dmg': '伤害', 'rng': '范围', 'spd': '速度',
        'cost': '费用', 'max_wave': '最大波次', 'next_wave': '下一波',
        'lives_left': '生命', 'enemies': '敌人', 'lv': '等级',
        'sell_for': '出售价格', 'upgrade_to': '升级到等级',
        'place_tower': '点击格子放置', 'info': '信息',
    },
    'fa': {
        'title': 'دفاع برج', 'start': 'شروع', 'pause': 'مکث', 'resume': 'ادامه',
        'restart': 'شروع مجدد', 'quit': 'خروج', 'theme': 'پوسته', 'lang': 'زبان',
        'dark': 'تیره', 'light': 'روشن', 'wave': 'موج', 'lives': 'جان',
        'gold': 'طلا', 'score': 'امتیاز', 'speed': 'سرعت', 'sell': 'فروش',
        'upgrade': 'ارتقا', 'towers': 'برج‌ها', 'game_over': 'بازی تمام شد',
        'victory': 'پیروزی!', 'paused': 'مکث', 'select_tower': 'انتخاب برج',
        'arrow': 'تیر', 'cannon': 'توپ', 'laser': 'لیزر', 'freeze': 'یخ',
        'missile': 'موشک', 'dmg': 'آسیب', 'rng': 'برد', 'spd': 'سرعت',
        'cost': 'هزینه', 'max_wave': 'موج آخر', 'next_wave': 'موج بعدی',
        'lives_left': 'جان', 'enemies': 'دشمنان', 'lv': 'سطح',
        'sell_for': 'فروش به', 'upgrade_to': 'ارتقا به سطح',
        'place_tower': 'روی خانه کلیک کن', 'info': 'اطلاعات',
    },
}

# ─── THEMES ──────────────────────────────────────────────────────────────────
THEMES = {
    'dark': {
        'bg': '#1a1a2e', 'panel': '#16213e', 'grid': '#0f3460',
        'path': '#533483', 'path_edge': '#7b52ab',
        'text': '#e0e0e0', 'sub': '#888', 'accent': '#e94560',
        'btn': '#0f3460', 'btn_hover': '#e94560',
        'hud_bg': '#16213e', 'border': '#0f3460',
        'grass': '#1a3a1a', 'grass2': '#1e4020',
        'selected': '#ffd700', 'range_fill': 'rgba(255,215,0,25)',
    },
    'light': {
        'bg': '#f0f4f8', 'panel': '#dce8f5', 'grid': '#b0c8e0',
        'path': '#c8a0d0', 'path_edge': '#9060a8',
        'text': '#1a1a2e', 'sub': '#555', 'accent': '#c0392b',
        'btn': '#4a90d9', 'btn_hover': '#c0392b',
        'hud_bg': '#dce8f5', 'border': '#90b0d0',
        'grass': '#c8e6c9', 'grass2': '#a5d6a7',
        'selected': '#e67e00', 'range_fill': 'rgba(230,126,0,30)',
    },
}

# ─── TOWER DEFINITIONS ───────────────────────────────────────────────────────
TOWER_TYPES = {
    'arrow':   {'color': '#4caf50', 'cost': 50,  'dmg': 15,  'range': 120, 'rate': 30, 'bullet_speed': 6, 'splash': 0,   'slow': 0,   'icon': '🏹'},
    'cannon':  {'color': '#ff9800', 'cost': 100, 'dmg': 60,  'range': 100, 'rate': 60, 'bullet_speed': 5, 'splash': 35,  'slow': 0,   'icon': '💣'},
    'laser':   {'color': '#f44336', 'cost': 150, 'dmg': 8,   'range': 140, 'rate': 5,  'bullet_speed': 20,'splash': 0,   'slow': 0,   'icon': '🔴'},
    'freeze':  {'color': '#2196f3', 'cost': 120, 'dmg': 5,   'range': 110, 'rate': 45, 'bullet_speed': 7, 'splash': 30,  'slow': 0.4, 'icon': '❄️'},
    'missile': {'color': '#9c27b0', 'cost': 200, 'dmg': 120, 'range': 160, 'rate': 90, 'bullet_speed': 4, 'splash': 50,  'slow': 0,   'icon': '🚀'},
}

ENEMY_TYPES = [
    {'name': 'basic',  'hp': 80,   'speed': 1.2, 'reward': 10, 'color': '#e74c3c', 'size': 10},
    {'name': 'fast',   'hp': 50,   'speed': 2.2, 'reward': 15, 'color': '#f39c12', 'size': 8},
    {'name': 'tank',   'hp': 300,  'speed': 0.7, 'reward': 30, 'color': '#8e44ad', 'size': 14},
    {'name': 'flying', 'hp': 120,  'speed': 1.8, 'reward': 20, 'color': '#1abc9c', 'size': 9},
    {'name': 'boss',   'hp': 1000, 'speed': 0.5, 'reward': 100,'color': '#c0392b', 'size': 18},
]

MAX_WAVES = 20
COLS, ROWS = 20, 14
SIDE_W = 220

# ─── PATH GENERATION ─────────────────────────────────────────────────────────
def make_path():
    path = []
    r = ROWS // 2
    path.append((0, r))
    c = 0
    while c < COLS - 1:
        step = random.randint(3, 6)
        c2 = min(c + step, COLS - 1)
        for cc in range(c + 1, c2 + 1):
            path.append((cc, r))
        c = c2
        if c < COLS - 1:
            dr = random.choice([-1, 1]) * random.randint(1, 3)
            r2 = max(1, min(ROWS - 2, r + dr))
            if r2 != r:
                step_r = 1 if r2 > r else -1
                for rr in range(r + step_r, r2 + step_r, step_r):
                    path.append((c, rr))
                r = r2
    path.append((COLS - 1, r))
    seen = []
    for p in path:
        if p not in seen:
            seen.append(p)
    return seen


# ─── GAME OBJECTS ─────────────────────────────────────────────────────────────
class Enemy:
    def __init__(self, etype, path_cells, cell_w, cell_h, wave):
        d = ENEMY_TYPES[etype % len(ENEMY_TYPES)]
        scale = 1 + wave * 0.08
        self.hp = int(d['hp'] * scale)
        self.max_hp = self.hp
        self.speed = d['speed']
        self.reward = d['reward']
        self.color = QColor(d['color'])
        self.size = d['size']
        self.name = d['name']
        self.path = path_cells
        self.cell_w = cell_w
        self.cell_h = cell_h
        self.path_idx = 0
        self.progress = 0.0
        self.slow_timer = 0
        self.slow_factor = 1.0
        self.alive = True
        self.reached_end = False
        cx, cy = path_cells[0]
        self.x = cx * cell_w + cell_w / 2
        self.y = cy * cell_h + cell_h / 2

    def update(self):
        if not self.alive or self.reached_end:
            return
        if self.slow_timer > 0:
            self.slow_timer -= 1
            spd = self.speed * self.slow_factor
        else:
            spd = self.speed
            self.slow_factor = 1.0

        if self.path_idx >= len(self.path) - 1:
            self.reached_end = True
            return

        tx, ty = self.path[self.path_idx + 1]
        tx = tx * self.cell_w + self.cell_w / 2
        ty = ty * self.cell_h + self.cell_h / 2
        dx, dy = tx - self.x, ty - self.y
        dist = math.hypot(dx, dy)
        if dist < spd:
            self.x, self.y = tx, ty
            self.path_idx += 1
        else:
            self.x += dx / dist * spd
            self.y += dy / dist * spd

    def draw(self, p, ox, oy):
        x, y = self.x + ox, self.y + oy
        s = self.size
        # shadow
        p.setBrush(QColor(0, 0, 0, 60))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(QRectF(x - s + 2, y - s + 2, s * 2, s * 2))
        # body
        grad = QRadialGradient(x - s * 0.3, y - s * 0.3, s * 1.5)
        grad.setColorAt(0, self.color.lighter(140))
        grad.setColorAt(1, self.color.darker(130))
        p.setBrush(grad)
        p.setPen(QPen(self.color.darker(160), 1.5))
        p.drawEllipse(QRectF(x - s, y - s, s * 2, s * 2))
        # hp bar
        bar_w = s * 2.5
        bar_h = 4
        bx, by = x - bar_w / 2, y - s - 8
        p.setBrush(QColor(60, 0, 0))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(QRectF(bx, by, bar_w, bar_h), 2, 2)
        ratio = max(0, self.hp / self.max_hp)
        hp_col = QColor('#2ecc71') if ratio > 0.5 else QColor('#f39c12') if ratio > 0.25 else QColor('#e74c3c')
        p.setBrush(hp_col)
        p.drawRoundedRect(QRectF(bx, by, bar_w * ratio, bar_h), 2, 2)
        # slow indicator
        if self.slow_timer > 0:
            p.setBrush(QColor(100, 180, 255, 120))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(QRectF(x - s - 3, y - s - 3, (s + 3) * 2, (s + 3) * 2))


class Bullet:
    def __init__(self, x, y, target, dmg, speed, splash, slow, slow_factor, color):
        self.x, self.y = x, y
        self.target = target
        self.dmg = dmg
        self.speed = speed
        self.splash = splash
        self.slow = slow
        self.slow_factor = slow_factor
        self.color = color
        self.alive = True
        self.trail = []

    def update(self, enemies):
        if not self.target.alive or self.target.reached_end:
            self.alive = False
            return None
        self.trail.append((self.x, self.y))
        if len(self.trail) > 6:
            self.trail.pop(0)
        dx, dy = self.target.x - self.x, self.target.y - self.y
        dist = math.hypot(dx, dy)
        if dist < self.speed + 2:
            self.alive = False
            hit = []
            if self.splash > 0:
                for e in enemies:
                    if e.alive and math.hypot(e.x - self.target.x, e.y - self.target.y) <= self.splash:
                        hit.append(e)
            else:
                hit.append(self.target)
            for e in hit:
                e.hp -= self.dmg
                if self.slow > 0:
                    e.slow_timer = 60
                    e.slow_factor = self.slow
                if e.hp <= 0:
                    e.alive = False
            return hit
        self.x += dx / dist * self.speed
        self.y += dy / dist * self.speed
        return None

    def draw(self, p, ox, oy):
        col = QColor(self.color)
        for i, (tx, ty) in enumerate(self.trail):
            alpha = int(180 * (i + 1) / len(self.trail))
            tc = QColor(col)
            tc.setAlpha(alpha)
            p.setBrush(tc)
            p.setPen(Qt.PenStyle.NoPen)
            r = 2 + i * 0.4
            p.drawEllipse(QRectF(tx + ox - r, ty + oy - r, r * 2, r * 2))
        p.setBrush(col)
        p.setPen(QPen(col.lighter(150), 1))
        p.drawEllipse(QRectF(self.x + ox - 4, self.y + oy - 4, 8, 8))


class Particle:
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-4, -1)
        self.life = random.randint(20, 40)
        self.max_life = self.life
        self.color = QColor(color)
        self.size = random.uniform(2, 5)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.15
        self.life -= 1

    def draw(self, p, ox, oy):
        alpha = int(255 * self.life / self.max_life)
        c = QColor(self.color)
        c.setAlpha(alpha)
        p.setBrush(c)
        p.setPen(Qt.PenStyle.NoPen)
        s = self.size * self.life / self.max_life
        p.drawEllipse(QRectF(self.x + ox - s, self.y + oy - s, s * 2, s * 2))


class Tower:
    def __init__(self, col, row, ttype):
        self.col, self.row = col, row
        self.ttype = ttype
        d = TOWER_TYPES[ttype]
        self.color = QColor(d['color'])
        self.base_cost = d['cost']
        self.dmg = d['dmg']
        self.range = d['range']
        self.rate = d['rate']
        self.bullet_speed = d['bullet_speed']
        self.splash = d['splash']
        self.slow = d['slow']
        self.slow_factor = 1.0 - d['slow']
        self.icon = d['icon']
        self.level = 1
        self.cooldown = 0
        self.angle = 0.0
        self.total_spent = d['cost']
        self.kills = 0
        self.x = self.y = 0.0

    def upgrade(self):
        if self.level < 3:
            self.level += 1
            cost = self.upgrade_cost()
            self.dmg = int(self.dmg * 1.5)
            self.range = int(self.range * 1.15)
            self.rate = max(3, int(self.rate * 0.8))
            self.total_spent += cost
            return cost
        return 0

    def upgrade_cost(self):
        return self.base_cost * self.level

    def sell_value(self):
        return int(self.total_spent * 0.6)

    def update(self, enemies, bullets):
        if self.cooldown > 0:
            self.cooldown -= 1
            return
        target = None
        best_prog = -1
        for e in enemies:
            if not e.alive or e.reached_end:
                continue
            dist = math.hypot(e.x - self.x, e.y - self.y)
            if dist <= self.range and e.path_idx > best_prog:
                best_prog = e.path_idx
                target = e
        if target:
            self.angle = math.atan2(target.y - self.y, target.x - self.x)
            self.cooldown = self.rate
            bullets.append(Bullet(
                self.x, self.y, target,
                self.dmg, self.bullet_speed,
                self.splash, self.slow > 0, self.slow_factor,
                self.color.name()
            ))

    def draw(self, p, ox, oy, cell_w, cell_h, selected=False, theme=None):
        cx = self.col * cell_w + cell_w / 2 + ox
        cy = self.row * cell_h + cell_h / 2 + oy
        self.x = cx - ox
        self.y = cy - oy
        r = min(cell_w, cell_h) * 0.42

        # range circle if selected
        if selected and theme:
            rc = QColor(theme['selected'])
            rc.setAlpha(30)
            p.setBrush(rc)
            p.setPen(QPen(QColor(theme['selected']), 1, Qt.PenStyle.DashLine))
            p.drawEllipse(QRectF(cx - self.range, cy - self.range, self.range * 2, self.range * 2))

        # base platform
        p.setBrush(QColor(40, 40, 40, 180))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(QRectF(cx - r * 1.1 + 2, cy - r * 1.1 + 2, r * 2.2, r * 2.2))

        grad = QRadialGradient(cx - r * 0.3, cy - r * 0.3, r * 1.8)
        grad.setColorAt(0, self.color.lighter(160))
        grad.setColorAt(0.6, self.color)
        grad.setColorAt(1, self.color.darker(150))
        p.setBrush(grad)
        border_col = QColor('#ffd700') if selected else self.color.darker(180)
        p.setPen(QPen(border_col, 2 if selected else 1.5))
        p.drawEllipse(QRectF(cx - r, cy - r, r * 2, r * 2))

        # barrel
        p.save()
        p.translate(cx, cy)
        p.rotate(math.degrees(self.angle))
        barrel_len = r * 1.3
        barrel_w = max(3, r * 0.35)
        p.setBrush(self.color.darker(130))
        p.setPen(QPen(self.color.darker(200), 1))
        p.drawRoundedRect(QRectF(0, -barrel_w / 2, barrel_len, barrel_w), 2, 2)
        p.restore()

        # level stars
        for i in range(self.level):
            sx = cx - (self.level - 1) * 5 + i * 10
            sy = cy + r + 5
            p.setBrush(QColor('#ffd700'))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(QRectF(sx - 3, sy - 3, 6, 6))


# ─── GAME CANVAS ─────────────────────────────────────────────────────────────
class GameCanvas(QWidget):
    state_changed = pyqtSignal(str)
    gold_changed = pyqtSignal(int)
    score_changed = pyqtSignal(int)
    wave_changed = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumSize(400, 300)
        self.theme = THEMES['dark']
        self.lang = 'en'
        self.state = 'idle'
        self.selected_tower_type = 'arrow'
        self.selected_tower = None
        self.speed_mult = 1
        self._init_game()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(16)
        self.setMouseTracking(True)
        self.hover_cell = None

    def t(self, k):
        return TR[self.lang].get(k, k)

    def set_theme(self, name):
        self.theme = THEMES[name]
        self.update()

    def set_lang(self, lang):
        self.lang = lang
        self.update()

    def _init_game(self):
        self.path_cells = make_path()
        self.path_set = set(self.path_cells)
        self.towers = []
        self.enemies = []
        self.bullets = []
        self.particles = []
        self.wave = 0
        self.lives = 20
        self.gold = 200
        self.score = 0
        self.spawn_queue = []
        self.spawn_timer = 0
        self.wave_active = False
        self.wave_cooldown = 0
        self.tick_count = 0

    def start_game(self):
        self._init_game()
        self.state = 'playing'
        self.state_changed.emit('playing')
        self._start_wave()
        self.setFocus()
        self.update()

    def _start_wave(self):
        self.wave += 1
        self.wave_changed.emit(self.wave)
        self.spawn_queue = self._build_wave(self.wave)
        self.spawn_timer = 0
        self.wave_active = True

    def _build_wave(self, w):
        q = []
        count = 8 + w * 3
        for i in range(count):
            if w >= 18 and i % 10 == 0:
                etype = 4  # boss
            elif w >= 10 and i % 5 == 0:
                etype = 2  # tank
            elif w >= 5 and i % 3 == 0:
                etype = 1  # fast
            elif w >= 8 and i % 4 == 0:
                etype = 3  # flying
            else:
                etype = 0
            q.append(etype)
        return q

    def _cell_size(self):
        w = self.width() - SIDE_W
        h = self.height()
        return w / COLS, h / ROWS

    def _tick(self):
        if self.state != 'playing':
            return
        for _ in range(self.speed_mult):
            self._update()

    def _update(self):
        self.tick_count += 1
        cw, ch = self._cell_size()

        # spawn
        if self.wave_active and self.spawn_queue:
            self.spawn_timer -= 1
            if self.spawn_timer <= 0:
                etype = self.spawn_queue.pop(0)
                e = Enemy(etype, self.path_cells, cw, ch, self.wave)
                self.enemies.append(e)
                self.spawn_timer = max(10, 40 - self.wave)

        # update enemies
        for e in self.enemies:
            e.update()
            if e.reached_end:
                self.lives -= 1
                e.alive = False
                if self.lives <= 0:
                    self.state = 'gameover'
                    self.state_changed.emit('gameover')
                    return
            if not e.alive and e.hp <= 0:
                self.gold += e.reward
                self.score += e.reward * self.wave
                self.gold_changed.emit(self.gold)
                self.score_changed.emit(self.score)
                for _ in range(8):
                    self.particles.append(Particle(e.x, e.y, e.color.name()))

        self.enemies = [e for e in self.enemies if e.alive and not e.reached_end]

        # update towers
        for t in self.towers:
            t.x = t.col * cw + cw / 2
            t.y = t.row * ch + ch / 2
            t.update(self.enemies, self.bullets)

        # update bullets
        new_bullets = []
        for b in self.bullets:
            b.update(self.enemies)
            if b.alive:
                new_bullets.append(b)
        self.bullets = new_bullets

        # particles
        self.particles = [p for p in self.particles if p.life > 0]
        for p in self.particles:
            p.update()

        # wave end check
        if self.wave_active and not self.spawn_queue and not self.enemies:
            self.wave_active = False
            if self.wave >= MAX_WAVES:
                self.state = 'victory'
                self.state_changed.emit('victory')
            else:
                self.wave_cooldown = 180
                self.gold += 25 + self.wave * 5

        if self.wave_cooldown > 0:
            self.wave_cooldown -= 1
            if self.wave_cooldown == 0:
                self._start_wave()

        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        game_w = w - SIDE_W
        cw, ch = self._cell_size()

        # background
        p.fillRect(0, 0, game_w, h, QColor(self.theme['bg']))

        # grid cells
        for row in range(ROWS):
            for col in range(COLS):
                x, y = col * cw, row * ch
                if (col, row) in self.path_set:
                    grad = QLinearGradient(x, y, x + cw, y + ch)
                    grad.setColorAt(0, QColor(self.theme['path']))
                    grad.setColorAt(1, QColor(self.theme['path_edge']))
                    p.fillRect(QRectF(x, y, cw, ch), grad)
                else:
                    col_c = QColor(self.theme['grass']) if (col + row) % 2 == 0 else QColor(self.theme['grass2'])
                    p.fillRect(QRectF(x, y, cw, ch), col_c)

        # grid lines
        p.setPen(QPen(QColor(self.theme['grid']), 0.5, Qt.PenStyle.SolidLine))
        for col in range(COLS + 1):
            p.drawLine(QPointF(col * cw, 0), QPointF(col * cw, h))
        for row in range(ROWS + 1):
            p.drawLine(QPointF(0, row * ch), QPointF(game_w, row * ch))

        # path arrows
        p.setPen(QPen(QColor(255, 255, 255, 40), 1))
        for i in range(len(self.path_cells) - 1):
            c1, r1 = self.path_cells[i]
            c2, r2 = self.path_cells[i + 1]
            x1 = c1 * cw + cw / 2
            y1 = r1 * ch + ch / 2
            x2 = c2 * cw + cw / 2
            y2 = r2 * ch + ch / 2
            p.drawLine(QPointF(x1, y1), QPointF(x2, y2))

        # start / end markers
        sc, sr = self.path_cells[0]
        ec, er = self.path_cells[-1]
        for (mc, mr, lbl, col) in [(sc, sr, 'S', '#2ecc71'), (ec, er, 'E', '#e74c3c')]:
            mx, my = mc * cw + cw / 2, mr * ch + ch / 2
            qc = QColor(col)
            qc.setAlpha(200)
            p.setBrush(qc)
            p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(QRectF(mx - 14, my - 14, 28, 28))
            p.setPen(QColor('#ffffff'))
            f = QFont('Arial', max(8, int(min(cw, ch) * 0.4)), QFont.Weight.Black)
            p.setFont(f)
            p.drawText(QRectF(mx - 14, my - 14, 28, 28), Qt.AlignmentFlag.AlignCenter, lbl)

        # hover highlight
        if self.hover_cell and self.state == 'playing':
            hc, hr = self.hover_cell
            if (hc, hr) not in self.path_set:
                occupied = any(t.col == hc and t.row == hr for t in self.towers)
                if not occupied:
                    hl = QColor(self.theme['selected'])
                    hl.setAlpha(60)
                    p.fillRect(QRectF(hc * cw, hr * ch, cw, ch), hl)
                    p.setPen(QPen(QColor(self.theme['selected']), 2))
                    p.setBrush(Qt.BrushStyle.NoBrush)
                    p.drawRect(QRectF(hc * cw, hr * ch, cw, ch))

        # towers
        for t in self.towers:
            is_sel = (self.selected_tower == t)
            t.draw(p, 0, 0, cw, ch, is_sel, self.theme)

        # bullets
        for b in self.bullets:
            b.draw(p, 0, 0)

        # particles
        for pt in self.particles:
            pt.draw(p, 0, 0)

        # enemies
        for e in self.enemies:
            e.draw(p, 0, 0)

        # side panel
        self._draw_side(p, game_w, w, h, cw, ch)

        # overlays
        if self.state == 'gameover':
            self._draw_overlay(p, game_w, h, self.t('game_over'), '#e74c3c')
        elif self.state == 'victory':
            self._draw_overlay(p, game_w, h, self.t('victory'), '#f1c40f')
        elif self.state == 'paused':
            self._draw_overlay(p, game_w, h, self.t('paused'), '#3498db')
        elif self.state == 'idle':
            self._draw_overlay(p, game_w, h, self.t('title'), '#2ecc71')

        p.end()

    def _draw_side(self, p, sx, w, h, cw, ch):
        # panel bg
        p.fillRect(sx, 0, w - sx, h, QColor(self.theme['panel']))
        p.setPen(QPen(QColor(self.theme['border']), 2))
        p.drawLine(sx, 0, sx, h)

        pad = 10
        x = sx + pad
        y = 14
        line = max(18, h // 28)

        # title
        f = QFont('Arial', max(12, (w - sx) // 14), QFont.Weight.Black)
        p.setFont(f)
        p.setPen(QColor(self.theme['accent']))
        p.drawText(QRect(x, y, w - sx - pad * 2, line + 6), Qt.AlignmentFlag.AlignHCenter, self.t('title'))
        y += line + 10

        # divider
        p.setPen(QPen(QColor(self.theme['border']), 1))
        p.drawLine(sx + pad, y, w - pad, y)
        y += 8

        # HUD stats
        stats = [
            (self.t('wave'),  f"{self.wave}/{MAX_WAVES}", '#3498db'),
            (self.t('lives'), str(self.lives),            '#2ecc71' if self.lives > 5 else '#e74c3c'),
            (self.t('gold'),  str(self.gold),             '#f1c40f'),
            (self.t('score'), str(self.score),            '#9b59b6'),
        ]
        f2 = QFont('Arial', max(9, (w - sx) // 20), QFont.Weight.Bold)
        p.setFont(f2)
        for label, val, col in stats:
            p.setPen(QColor(self.theme['sub']))
            p.drawText(QRect(x, y, (w - sx) // 2 - pad, line), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, label)
            p.setPen(QColor(col))
            p.drawText(QRect(sx + (w - sx) // 2, y, (w - sx) // 2 - pad, line), Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, val)
            y += line + 2

        y += 6
        p.setPen(QPen(QColor(self.theme['border']), 1))
        p.drawLine(sx + pad, y, w - pad, y)
        y += 10

        # tower select label
        f3 = QFont('Arial', max(8, (w - sx) // 22), QFont.Weight.Bold)
        p.setFont(f3)
        p.setPen(QColor(self.theme['text']))
        p.drawText(QRect(x, y, w - sx - pad * 2, line), Qt.AlignmentFlag.AlignHCenter, self.t('select_tower'))
        y += line + 4

        # tower buttons
        btn_w = w - sx - pad * 2
        btn_h = max(32, h // 18)
        for ttype, td in TOWER_TYPES.items():
            is_sel = self.selected_tower_type == ttype
            can_afford = self.gold >= td['cost']
            bg = QColor(td['color'])
            if is_sel:
                bg.setAlpha(220)
            else:
                bg.setAlpha(80 if can_afford else 40)
            p.setBrush(bg)
            border = QColor(td['color']) if is_sel else QColor(self.theme['border'])
            p.setPen(QPen(border, 2 if is_sel else 1))
            p.drawRoundedRect(QRectF(x, y, btn_w, btn_h), 6, 6)

            # tower name
            name_key = ttype
            f4 = QFont('Arial', max(8, btn_h // 3), QFont.Weight.Bold)
            p.setFont(f4)
            tc = QColor(self.theme['text']) if can_afford else QColor(self.theme['sub'])
            p.setPen(tc)
            label_txt = self.t(name_key)
            p.drawText(QRect(x + 6, y, btn_w // 2, btn_h), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, label_txt)

            # cost
            cost_col = QColor('#f1c40f') if can_afford else QColor('#888')
            p.setPen(cost_col)
            p.drawText(QRect(x, y, btn_w - 4, btn_h), Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, f"${td['cost']}")

            y += btn_h + 4

        y += 6
        p.setPen(QPen(QColor(self.theme['border']), 1))
        p.drawLine(sx + pad, y, w - pad, y)
        y += 8

        # selected tower info
        if self.selected_tower:
            t = self.selected_tower
            p.setPen(QColor(self.theme['accent']))
            f5 = QFont('Arial', max(8, (w - sx) // 22), QFont.Weight.Bold)
            p.setFont(f5)
            p.drawText(QRect(x, y, btn_w, line), Qt.AlignmentFlag.AlignHCenter, f"{self.t(t.ttype)}  {self.t('lv')}.{t.level}")
            y += line + 2

            p.setPen(QColor(self.theme['text']))
            f6 = QFont('Arial', max(7, (w - sx) // 25))
            p.setFont(f6)
            small_line = max(14, h // 36)
            infos = [
                f"{self.t('dmg')}: {t.dmg}   {self.t('rng')}: {int(t.range)}",
                f"{self.t('kills')}: {t.kills}   {self.t('sell_for')}: ${t.sell_value()}",
            ]
            for info in infos:
                p.drawText(QRect(x, y, btn_w, small_line), Qt.AlignmentFlag.AlignHCenter, info)
                y += small_line + 2

            # upgrade / sell buttons
            if y + btn_h * 2 + 12 < h - 10:
                # upgrade
                can_up = t.level < 3
                up_cost = t.upgrade_cost()
                can_afford_up = self.gold >= up_cost and can_up
                up_bg = QColor('#2ecc71') if can_afford_up else QColor('#555')
                up_bg.setAlpha(180)
                p.setBrush(up_bg)
                p.setPen(QPen(QColor('#2ecc71') if can_afford_up else QColor('#444'), 1.5))
                p.drawRoundedRect(QRectF(x, y, btn_w, btn_h), 6, 6)
                p.setPen(QColor('#fff'))
                p.setFont(f3)
                up_txt = f"{self.t('upgrade_to')} {t.level + 1} (${up_cost})" if can_up else "MAX"
                p.drawText(QRect(x, y, btn_w, btn_h), Qt.AlignmentFlag.AlignCenter, up_txt)
                self._upgrade_rect = QRect(x, y, btn_w, btn_h)
                y += btn_h + 4

                # sell
                p.setBrush(QColor('#e74c3c') if True else QColor('#555'))
                p.setPen(QPen(QColor('#e74c3c'), 1.5))
                p.drawRoundedRect(QRectF(x, y, btn_w, btn_h), 6, 6)
                p.setPen(QColor('#fff'))
                p.drawText(QRect(x, y, btn_w, btn_h), Qt.AlignmentFlag.AlignCenter,
                           f"{self.t('sell')} (${t.sell_value()})")
                self._sell_rect = QRect(x, y, btn_w, btn_h)
                y += btn_h + 4
        else:
            self._upgrade_rect = None
            self._sell_rect = None
            p.setPen(QColor(self.theme['sub']))
            f7 = QFont('Arial', max(7, (w - sx) // 26))
            p.setFont(f7)
            p.drawText(QRect(x, y, btn_w, line * 2), Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop,
                       self.t('place_tower'))

    def _draw_overlay(self, p, gw, h, title, color_hex):
        overlay = QColor(0, 0, 0, 150)
        p.fillRect(0, 0, gw, h, overlay)
        cx, cy = gw // 2, h // 2
        pw = max(280, gw // 2)
        ph = max(160, h // 3)
        bg = QColor(self.theme['panel'])
        bg.setAlpha(230)
        p.setBrush(bg)
        border = QColor(color_hex)
        p.setPen(QPen(border, 3))
        p.drawRoundedRect(cx - pw // 2, cy - ph // 2, pw, ph, 14, 14)

        fs = max(22, min(46, gw // 14))
        f = QFont('Arial', fs, QFont.Weight.Black)
        p.setFont(f)
        for off in range(3, 0, -1):
            g = QColor(color_hex)
            g.setAlpha(20 * off)
            p.setPen(g)
            p.drawText(QRect(cx - pw // 2, cy - ph // 2 - off * 2, pw, fs + 16),
                       Qt.AlignmentFlag.AlignHCenter, title)
        p.setPen(QColor(color_hex))
        p.drawText(QRect(cx - pw // 2, cy - ph // 2, pw, fs + 16),
                   Qt.AlignmentFlag.AlignHCenter, title)

        f2 = QFont('Arial', max(10, min(15, gw // 55)))
        p.setFont(f2)
        p.setPen(QColor(self.theme['text']))
        info_y = cy - ph // 2 + fs + 20
        p.drawText(QRect(cx - pw // 2, info_y, pw, 26),
                   Qt.AlignmentFlag.AlignHCenter,
                   f"{self.t('wave')}: {self.wave}/{MAX_WAVES}   {self.t('score')}: {self.score}")
        p.setPen(QColor(self.theme['sub']))
        f3 = QFont('Arial', max(8, min(12, gw // 65)))
        p.setFont(f3)
        p.drawText(QRect(cx - pw // 2, cy + ph // 2 - 28, pw, 24),
                   Qt.AlignmentFlag.AlignHCenter, "Use buttons below to continue")

    def mouseMoveEvent(self, e):
        cw, ch = self._cell_size()
        gx, gy = e.position().x(), e.position().y()
        if gx < self.width() - SIDE_W:
            col = int(gx // cw)
            row = int(gy // ch)
            if 0 <= col < COLS and 0 <= row < ROWS:
                self.hover_cell = (col, row)
            else:
                self.hover_cell = None
        else:
            self.hover_cell = None
        self.update()

    def mousePressEvent(self, e):
        if e.button() != Qt.MouseButton.LeftButton:
            return
        px, py = int(e.position().x()), int(e.position().y())
        gw = self.width() - SIDE_W

        # side panel clicks
        if px >= gw:
            # tower type buttons
            pad = 10
            sx = gw
            line = max(18, self.height() // 28)
            btn_h = max(32, self.height() // 18)
            # calculate y offset same as draw
            y = 14 + line + 10 + 8 + (line + 2) * 4 + 6 + 8 + line + 4
            for ttype in TOWER_TYPES:
                rect = QRect(sx + pad, y, self.width() - sx - pad * 2, btn_h)
                if rect.contains(px, py):
                    self.selected_tower_type = ttype
                    self.selected_tower = None
                    self.update()
                    return
                y += btn_h + 4

            # upgrade / sell
            if self.selected_tower:
                if self._upgrade_rect and self._upgrade_rect.contains(px, py):
                    t = self.selected_tower
                    cost = t.upgrade_cost()
                    if t.level < 3 and self.gold >= cost:
                        self.gold -= cost
                        t.upgrade()
                        self.gold_changed.emit(self.gold)
                        self.update()
                    return
                if self._sell_rect and self._sell_rect.contains(px, py):
                    val = self.selected_tower.sell_value()
                    self.gold += val
                    self.towers.remove(self.selected_tower)
                    self.selected_tower = None
                    self.gold_changed.emit(self.gold)
                    self.update()
                    return
            return

        if self.state != 'playing':
            return

        cw, ch = self._cell_size()
        col = int(px // cw)
        row = int(py // ch)

        if not (0 <= col < COLS and 0 <= row < ROWS):
            return

        # click on existing tower
        for t in self.towers:
            if t.col == col and t.row == row:
                self.selected_tower = t if self.selected_tower != t else None
                self.update()
                return

        # place new tower
        if (col, row) not in self.path_set:
            td = TOWER_TYPES[self.selected_tower_type]
            if self.gold >= td['cost']:
                self.gold -= td['cost']
                nt = Tower(col, row, self.selected_tower_type)
                self.towers.append(nt)
                self.selected_tower = nt
                self.gold_changed.emit(self.gold)
                self.update()
        else:
            self.selected_tower = None
            self.update()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_P or e.key() == Qt.Key.Key_Escape:
            if self.state == 'playing':
                self.state = 'paused'
                self.state_changed.emit('paused')
            elif self.state == 'paused':
                self.state = 'playing'
                self.state_changed.emit('playing')
            self.update()


# ─── MAIN WINDOW ─────────────────────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_theme = 'dark'
        self.current_lang = 'en'
        self.setWindowTitle('Tower Defense')
        self.setMinimumSize(700, 500)
        self.resize(1200, 720)
        self._build_ui()
        self._apply_theme()

    def t(self, k):
        return TR[self.current_lang].get(k, k)

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # top bar
        self.top_bar = QWidget()
        self.top_bar.setFixedHeight(46)
        tl = QHBoxLayout(self.top_bar)
        tl.setContentsMargins(12, 4, 12, 4)
        tl.setSpacing(8)

        self.title_lbl = QLabel(self.t('title'))
        self.title_lbl.setFont(QFont('Arial', 15, QFont.Weight.Black))
        tl.addWidget(self.title_lbl)
        tl.addStretch()

        self.lang_lbl = QLabel(self.t('lang') + ':')
        tl.addWidget(self.lang_lbl)
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(['English', '中文', 'فارسی'])
        self.lang_combo.setFixedWidth(90)
        self.lang_combo.currentIndexChanged.connect(self._on_lang)
        tl.addWidget(self.lang_combo)

        self.theme_lbl = QLabel(self.t('theme') + ':')
        tl.addWidget(self.theme_lbl)
        self.theme_combo = QComboBox()
        self.theme_combo.addItems([self.t('dark'), self.t('light')])
        self.theme_combo.setFixedWidth(80)
        self.theme_combo.currentIndexChanged.connect(self._on_theme)
        tl.addWidget(self.theme_combo)

        layout.addWidget(self.top_bar)

        # canvas
        self.canvas = GameCanvas()
        self.canvas.state_changed.connect(self._on_state)
        self.canvas.gold_changed.connect(self._on_gold)
        self.canvas.score_changed.connect(self._on_score)
        self.canvas.wave_changed.connect(self._on_wave)
        layout.addWidget(self.canvas, stretch=1)

        # bottom bar
        self.bot_bar = QWidget()
        self.bot_bar.setFixedHeight(50)
        bl = QHBoxLayout(self.bot_bar)
        bl.setContentsMargins(12, 6, 12, 6)
        bl.setSpacing(8)

        self.btn_start   = self._btn(self.t('start'),   self._do_start)
        self.btn_pause   = self._btn(self.t('pause'),   self._do_pause)
        self.btn_resume  = self._btn(self.t('resume'),  self._do_resume)
        self.btn_restart = self._btn(self.t('restart'), self._do_restart)
        self.btn_fast    = self._btn('2x',              self._do_speed)
        self.btn_quit    = self._btn(self.t('quit'),    self.close)

        for b in [self.btn_start, self.btn_pause, self.btn_resume,
                  self.btn_restart, self.btn_fast, self.btn_quit]:
            bl.addWidget(b)

        bl.addStretch()
        self.status_lbl = QLabel('')
        self.status_lbl.setFont(QFont('Arial', 10))
        bl.addWidget(self.status_lbl)

        layout.addWidget(self.bot_bar)
        self._refresh_buttons('idle')

    def _btn(self, text, slot):
        b = QPushButton(text)
        b.setFixedHeight(34)
        b.setMinimumWidth(80)
        b.setCursor(Qt.CursorShape.PointingHandCursor)
        b.clicked.connect(slot)
        return b

    def _refresh_buttons(self, state):
        self.btn_start.setVisible(state == 'idle')
        self.btn_pause.setVisible(state == 'playing')
        self.btn_resume.setVisible(state == 'paused')
        self.btn_restart.setVisible(state in ('paused', 'gameover', 'victory'))
        self.btn_fast.setVisible(state == 'playing')
        self.btn_quit.setVisible(True)

    def _do_start(self):
        self.canvas.start_game()
        self.canvas.setFocus()

    def _do_pause(self):
        self.canvas.state = 'paused'
        self.canvas.state_changed.emit('paused')

    def _do_resume(self):
        self.canvas.state = 'playing'
        self.canvas.state_changed.emit('playing')
        self.canvas.setFocus()

    def _do_restart(self):
        self.canvas.start_game()
        self.canvas.setFocus()

    def _do_speed(self):
        self.canvas.speed_mult = 1 if self.canvas.speed_mult == 2 else 2
        self.btn_fast.setText('1x' if self.canvas.speed_mult == 2 else '2x')

    def _on_state(self, state):
        self._refresh_buttons(state)
        msgs = {
            'paused': self.t('paused'),
            'gameover': self.t('game_over'),
            'victory': self.t('victory'),
        }
        self.status_lbl.setText(msgs.get(state, ''))

    def _on_gold(self, v):
        self.status_lbl.setText(f"{self.t('gold')}: {v}  {self.t('score')}: {self.canvas.score}")

    def _on_score(self, v):
        self.status_lbl.setText(f"{self.t('gold')}: {self.canvas.gold}  {self.t('score')}: {v}")

    def _on_wave(self, v):
        self.status_lbl.setText(f"{self.t('wave')}: {v}/{MAX_WAVES}")

    def _on_lang(self, idx):
        self.current_lang = ['en', 'zh', 'fa'][idx]
        self.canvas.set_lang(self.current_lang)
        self._update_texts()
        self._apply_theme()

    def _on_theme(self, idx):
        self.current_theme = 'dark' if idx == 0 else 'light'
        self.canvas.set_theme(self.current_theme)
        self._apply_theme()

    def _update_texts(self):
        self.title_lbl.setText(self.t('title'))
        self.lang_lbl.setText(self.t('lang') + ':')
        self.theme_lbl.setText(self.t('theme') + ':')
        self.btn_start.setText(self.t('start'))
        self.btn_pause.setText(self.t('pause'))
        self.btn_resume.setText(self.t('resume'))
        self.btn_restart.setText(self.t('restart'))
        self.btn_quit.setText(self.t('quit'))
        self.theme_combo.blockSignals(True)
        self.theme_combo.clear()
        self.theme_combo.addItems([self.t('dark'), self.t('light')])
        self.theme_combo.setCurrentIndex(0 if self.current_theme == 'dark' else 1)
        self.theme_combo.blockSignals(False)

    def _apply_theme(self):
        th = THEMES[self.current_theme]
        qss = f"""
        QMainWindow, QWidget {{
            background-color: {th['bg']};
            color: {th['text']};
            font-family: Arial;
        }}
        QLabel {{ color: {th['text']}; background: transparent; }}
        QPushButton {{
            background-color: {th['btn']};
            color: {th['text']};
            border: 1px solid {th['accent']};
            border-radius: 6px;
            padding: 4px 10px;
            font-weight: bold;
            font-size: 11px;
        }}
        QPushButton:hover {{
            background-color: {th['btn_hover']};
            color: #ffffff;
        }}
        QPushButton:pressed {{ background-color: {th['accent']}; }}
        QComboBox {{
            background-color: {th['panel']};
            color: {th['text']};
            border: 1px solid {th['sub']};
            border-radius: 5px;
            padding: 2px 6px;
            font-size: 11px;
        }}
        QComboBox:hover {{ border: 1px solid {th['accent']}; }}
        QComboBox QAbstractItemView {{
            background-color: {th['panel']};
            color: {th['text']};
            selection-background-color: {th['btn']};
            border: 1px solid {th['accent']};
        }}
        QComboBox::drop-down {{ border: none; width: 16px; }}
        QComboBox::down-arrow {{
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 5px solid {th['text']};
            margin-right: 4px;
        }}
        """
        self.setStyleSheet(qss)
        bar = f"background-color: {th['panel']}; border-bottom: 1px solid {th['border']};"
        bot = f"background-color: {th['panel']}; border-top: 1px solid {th['border']};"
        self.top_bar.setStyleSheet(bar)
        self.bot_bar.setStyleSheet(bot)
        self.title_lbl.setStyleSheet(f"color: {th['accent']}; font-weight: 900; background: transparent;")
        self.status_lbl.setStyleSheet(f"color: {th['sub']}; background: transparent;")


# ─── ENTRY POINT ─────────────────────────────────────────────────────────────
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
