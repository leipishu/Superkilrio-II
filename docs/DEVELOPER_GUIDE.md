# Superkilrio II 开发手册 / Developer Guide

---

## 中文版

### 1. 项目结构说明

```
Superkilrio II/
│
├─ docs/                # 多语言文档
├─ src/                 # 主代码目录
│  ├─ assets/           # 游戏资源
│  │  ├─ effects/       # 特效
│  │  │  ├─ hit.png
│  │  │  └─ kill.png
│  │  ├─ enemies/       # 敌人资源
│  │  │  ├─ level1_grunt/
│  │  │  │  ├─ attack_1.png
│  │  │  │  └─ attack_2.png
│  │  │  ├─ level2_grunt/
│  │  │  │  ├─ attack_1.png
│  │  │  │  └─ attack_2.png
│  │  │  ├─ level3_grunt/
│  │  │  │  ├─ attack_1.png
│  │  │  │  ├─ attack_2.png
│  │  │  │  └─ attack_3.png
│  │  │  └─ public/      # 共享资源
│  │  │     ├─ run_1.png
│  │  │     ├─ run_2.png
│  │  │     ├─ run_3.png
│  │  │     ├─ run_4.png
│  │  │     ├─ run_5.png
│  │  │     ├─ run_6.png
│  │  │     └─ stand.png
│  │  ├─ items/         # 物品资源
│  │  │  ├─ weapons/
│  │  │  │  ├─ firelock.png
│  │  │  │  └─ iron_hook.png
│  │  │  └─ quest_items/ # 任务物品...
│  │  ├─ npc/           # NPC资源
│  │  │  └─ trainer.png
│  │  └─ player/        # 玩家资源
│  │     ├─ attack_1.png
│  │     ├─ attack_2.png
│  │     ├─ jump.png
│  │     ├─ run_1.png
│  │     ├─ run_2.png
│  │     ├─ run_3.png
│  │     ├─ run_4.png
│  │     ├─ run_5.png
│  │     ├─ run_6.png
│  │     ├─ stand.png
│  │     ├─ firelock/
│  │     │  ├─ attack_1.png
│  │     │  ├─ attack_2.png
│  │     │  └─ attack_3.png
│  │     └─ iron_hook/
│  │        ├─ attack_1.png
│  │        └─ attack_2.png
│  ├─ ecs/              # ECS架构
│  │  ├─ entities/      # 实体定义
│  │  │  ├─ enemies/    # 敌人
│  │  │  │  ├─ level1_grunt.json
│  │  │  │  ├─ level1_grunt.py
│  │  │  │  ├─ level2_grunt.json
│  │  │  │  ├─ level2_grunt.py
│  │  │  │  ├─ level3_grunt.json
│  │  │  │  ├─ level3_grunt.py
│  │  │  │  └─ ...      # 可添加更多敌人
│  │  │  └─ npc/        # NPC
│  │  │     ├─ trainer.py
│  │  │     └─ ...      # 可添加更多NPC
│  │  ├─ systems/       # 系统
│  │  │  ├─ ai_system.py
│  │  │  └─ dialogue_system.py
│  │  └─ registry.py    # 实体注册表
│  ├─ items/            # 物品系统
│  │  ├─ weapons/       # 武器
│  │  │  ├─ firelock.json
│  │  │  ├─ firelock.py
│  │  │  ├─ iron_hook.json
│  │  │  ├─ iron_hook.py
│  │  │  └─ ...         # 可添加更多武器
│  │  ├─ quest_items/   # 任务物品...
│  │  ├─ base_item.py   # 物品基类
│  │  └─ registry.py    # 物品注册表
│  ├─ levels/           # 关卡系统
│  │  ├─ levels/        # 具体关卡
│  │  │  ├─ level_00.py
│  │  │  ├─ level_01.py
│  │  │  ├─ level_02.py
│  │  │  ├─ level_03.py
│  │  │  └─ ...         # 可添加更多关卡
│  │  └─ level_manager.py
│  ├─ systems/          # 游戏系统
│  │  ├─ audio_manager.py
│  │  ├─ combat_system.py
│  │  ├─ input_handler.py
│  │  ├─ interaction_system.py
│  │  ├─ particle_system.py
│  │  ├─ physics_system.py
│  │  └─ renderer.py
│  ├─ utils/            # 工具类
│  ├─ constants.py      # 全局常量
│  ├─ game_controller.py# 游戏控制器
│  ├─ main.py           # 程序入口
│  └─ player.py         # 玩家实现
├─ requirements.txt     # 依赖库
└─ README.md            # 项目说明
```

---

### 2. 关卡与实体注册机制

#### 2.1 关卡注册与加载
- 关卡基类：`src/levels/level_manager.py` 中的 `Level` 类
  - 关键属性：
    - `enemies`: 当前关卡敌人列表
    - `npcs`: 当前关卡NPC列表
    - `items`: 当前关卡物品列表
  - 必须实现方法：
    - `setup(self, player=None)`: 初始化关卡
      - 参数: player - 玩家实例(可选)
      - 返回: None
    - `update(self, delta_time)`: 更新关卡逻辑
      - 参数: delta_time - 帧间隔时间(秒)
      - 返回: None
    - `draw(self)`: 渲染关卡
      - 返回: None
- 关卡注册：`LevelManager` 自动扫描 `src/levels/levels/` 下所有 `level_*.py` 文件并注册
- 关卡命名规范：`level_<编号>.py` (如level_00.py, level_01.py...)
- 切换关卡：`level_manager.goto_level(level_num, player=player)`
  - 参数: 
    - level_num: 关卡编号(int)
    - player: 玩家实例(可选)
  - 返回: None

#### 2.2 实体注册与生成
- 注册表类：`src/ecs/registry.py` 中的 `EntityRegistry`
- 注册实体蓝图：
  ```python
  registry = EntityRegistry()
  registry.register_blueprint("level1_grunt", Level1Grunt)
  ```
- 生成实体：
  ```python
  entity = registry.spawn("level1_grunt", x=100, y=200)
  ```
- 批量更新/绘制实体：
  ```python
  registry.update_all(delta_time)
  registry.draw_all()
  ```

---

### 3. 日志系统用法
- 配置文件：`src/utils/logging_config.py`
- 初始化：`setup_logging()`（主入口自动调用）
- 获取 logger：
  ```python
  from src.utils.logging_config import logger
  my_logger = logger.getChild('模块名')
  my_logger.info("信息")
  my_logger.error("错误")
  ```
- 日志特性：
  - 日志文件自动轮转，最多保留5个历史日志。
  - 日志文件位于 `src/logs/`。
  - 控制台与文件双通道输出，支持 DEBUG/INFO 级别。

---

### 4. 主要系统与接口说明

#### 4.1 游戏主控制器
- 文件：`src/game_controller.py`
- 主要属性：`self.player`、`self.level_manager`、`self.dialogue_system`、`self.physics_system`、`self.interaction_system`、`self.input_handler`、`self.renderer`
- 主要方法：`setup()`、`on_draw()`、`on_update(delta_time)`、`on_key_press(key, modifiers)`、`on_key_release(key, modifiers)`、`run()`

#### 4.2 武器系统
- 基类：`src/items/base_item.py` 中的 `BaseItem`
  - 必须属性：`item_id`, `name`
  - 可选属性：`damage`, `attack_range`, `attack_speed`, `scale`
  - 方法：`load_from_json(json_file)` 从JSON加载配置
- 武器实现：
  - 继承 `BaseItem`
  - 必须实现 `use(player)` 方法
  - 示例：`src/items/weapons/iron_hook.py`, `src/items/weapons/firelock.py`
- 玩家接口：
  - `equip_weapon(weapon)`: 装备武器
  - `unequip_weapon()`: 取消装备
  - `equipped_weapon`: 当前装备的武器
- JSON配置：
  ```json
  {
    "item_id": "iron_hook",
    "name": "铁钩",
    "description": "一把锋利的铁钩",
    "damage": 15,
    "attack_range": 120,
    "attack_speed": 1.2,
    "texture": "items/weapons/iron_hook.png"
  }
  ```

#### 4.3 玩家与敌人
- 玩家类：`src/player.py`，继承自 `arcade.Sprite`
- 敌人类：如 `src/ecs/entities/enemies/level1_grunt.py`
- 动画与物理属性：均在各自类的 `__init__` 中初始化

#### 4.3 输入系统
- 文件：`src/systems/input_handler.py`
- 接口：`on_key_press(key, modifiers)`、`on_key_release(key, modifiers)`

#### 4.4 交互系统
- 文件：`src/systems/interaction_system.py`
- 接口：`check_npc_proximity()`、`handle_interaction(key)`

#### 4.5 对话系统
- 文件：`src/ecs/systems/dialogue_system.py`
- 接口：`start_dialogue(lines: List[str])`、`next_line()`、`draw()`

#### 4.6 渲染系统
- 文件：`src/systems/renderer.py`
- 接口：`draw()`

---

### 5. 常用全局常量
- 文件：`src/constants.py`
- 示例：`SCREEN_WIDTH`、`PLAYER_SPEED`、`ENEMY_SCALE`、`GROUND_Y`、`get_asset_path(relative_path)`

---

### 6. 开发流程示例

#### 6.1 关卡开发
1. 在 `src/levels/levels/` 新建 `level_xx.py`，定义 `LEVEL_NUM` 和 `Level` 类。
2. 在 `Level.setup(self, player=None)` 中生成敌人/NPC，添加到 `self.enemies` 或 `self.npcs`。
3. 在 `update`/`draw` 方法中实现关卡逻辑与渲染。
4. 关卡会被 `LevelManager` 自动注册和加载。

#### 6.2 武器开发
1. 在 `src/items/weapons/` 下新建武器文件（如 `new_weapon.py`）
2. 创建继承 `BaseItem` 的类：
   ```python
   class NewWeapon(BaseItem):
       def __init__(self):
           json_path = os.path.join(os.path.dirname(__file__), "new_weapon.json")
           super().__init__(json_path)
       
       def use(self, player):
           # 装备/取消装备逻辑
           pass
   ```
3. 创建对应的JSON配置文件（如 `new_weapon.json`）
4. 添加武器纹理到 `src/assets/items/weapons/`
5. 在关卡或NPC中生成武器实例

---

### 7. 依赖与运行
- 依赖：见 `requirements.txt`（主要为 `arcade`、`pillow`）
- 运行入口：`src/main.py`
  ```bash
  python src/main.py
  ```

---

### 8. 贡献与协作建议
- 遵循已有模块结构，新增关卡、实体、系统时保持接口一致。
- 日志充分，便于调试和问题定位。
- 关卡、实体、系统均建议写好注释和类型标注。
- 资源文件统一放在 `src/assets/` 下，使用 `get_asset_path` 获取路径。

---

如需更详细的函数参数、类继承关系、具体用法，可查阅对应源码文件，或在此文档基础上补充。欢迎协作开发！


---

## English Version

### 1. Project Structure

```
Superkilrio II/
│
├─ docs/                # Documentation (multi-language)
├─ src/                 # Main source code
│  ├─ assets/           # Game assets (images, characters, enemies, etc.)
│  ├─ ecs/              # Entity-Component-System
│  │  ├─ entities/      # Enemy, NPC entity definitions
│  │  ├─ systems/       # AI, dialogue, etc.
│  │  └─ registry.py    # Entity registry
│  ├─ levels/           # Level management and implementations
│  │  ├─ level_manager.py
│  │  └─ levels/        # Level implementations (level_00.py, level_01.py, ...)
│  ├─ systems/          # Game systems (input, physics, rendering, interaction)
│  ├─ utils/            # Utilities (e.g., logging config)
│  ├─ constants.py      # Global constants
│  ├─ game_controller.py# Main game controller
│  ├─ main.py           # Entry point
│  └─ player.py         # Player implementation
├─ requirements.txt     # Dependencies
└─ README.md            # Project intro
```

---

### 2. Level & Entity Registration

#### 2.1 Level Registration & Loading
- Base class: `Level` in `src/levels/level_manager.py`.
- Registration: `LevelManager` auto-scans `src/levels/levels/` for `level_*.py` and registers them.
- Implementation: Each level must define `LEVEL_NUM` and a `Level` class (subclass of `level_manager.Level`), with `setup(self, player=None)`, `update(self, delta_time)`, `draw(self)`.
- Switch level: `level_manager.goto_level(level_num, player=player)`

#### 2.2 Entity Registration & Spawning
- Registry: `EntityRegistry` in `src/ecs/registry.py`
- Register blueprint:
  ```python
  registry = EntityRegistry()
  registry.register_blueprint("level1_grunt", Level1Grunt)
  ```
- Spawn entity:
  ```python
  entity = registry.spawn("level1_grunt", x=100, y=200)
  ```
- Batch update/draw:
  ```python
  registry.update_all(delta_time)
  registry.draw_all()
  ```

---

### 3. Logging System
- Config: `src/utils/logging_config.py`
- Init: `setup_logging()` (auto-called in main entry)
- Get logger:
  ```python
  from src.utils.logging_config import logger
  my_logger = logger.getChild('ModuleName')
  my_logger.info("Info")
  my_logger.error("Error")
  ```
- Features:
  - Log files auto-rotate, keep up to 5 history logs.
  - Logs in `src/logs/`.
  - Console & file output, supports DEBUG/INFO.

---

### 4. Main Systems & Interfaces

#### 4.1 Game Controller
- File: `src/game_controller.py`
- Main attributes: `self.player`, `self.level_manager`, `self.dialogue_system`, `self.physics_system`, `self.interaction_system`, `self.input_handler`, `self.renderer`
- Main methods: `setup()`, `on_draw()`, `on_update(delta_time)`, `on_key_press(key, modifiers)`, `on_key_release(key, modifiers)`, `run()`

#### 4.2 Player & Enemies
- Player: `src/player.py`, subclass of `arcade.Sprite`
- Enemy: e.g. `src/ecs/entities/enemies/level1_grunt.py`
- Animation & physics: initialized in each class's `__init__`

#### 4.3 Input System
- File: `src/systems/input_handler.py`
- Interfaces: `on_key_press(key, modifiers)`, `on_key_release(key, modifiers)`

#### 4.4 Interaction System
- File: `src/systems/interaction_system.py`
- Interfaces: `check_npc_proximity()`, `handle_interaction(key)`

#### 4.5 Dialogue System
- File: `src/ecs/systems/dialogue_system.py`
- Interfaces: `start_dialogue(lines: List[str])`, `next_line()`, `draw()`

#### 4.6 Renderer
- File: `src/systems/renderer.py`
- Interface: `draw()`

---

### 5. Global Constants
- File: `src/constants.py`
- Examples: `SCREEN_WIDTH`, `PLAYER_SPEED`, `ENEMY_SCALE`, `GROUND_Y`, `get_asset_path(relative_path)`

---

### 6. Level Development Example
1. Create `level_xx.py` in `src/levels/levels/`, define `LEVEL_NUM` and `Level` class.
2. In `Level.setup(self, player=None)`, spawn enemies/NPCs, add to `self.enemies` or `self.npcs`.
3. Implement logic/rendering in `update`/`draw`.
4. Level will be auto-registered and loaded by `LevelManager`.

---

### 7. Dependencies & Running
- Dependencies: see `requirements.txt` (mainly `arcade`, `pillow`)
- Entry: `src/main.py`
  ```bash
  python src/main.py
  ```

---

### 8. Contribution & Collaboration
- Follow existing module structure, keep interface consistency for new levels/entities/systems.
- Use logging for debugging and issue tracking.
- Comment and type-annotate levels/entities/systems.
- Place assets in `src/assets/`, use `get_asset_path` for paths.

---

For more details, check the source code or extend this document. Contributions welcome! 