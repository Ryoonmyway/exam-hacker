# compression-compatibility-equation

写出与释放方向、符号约定和原支座位移条件一致的协调方程。

## 来源

- review-sheet · paragraph 2 — The source gives the zero-displacement compatibility equation.

## 方法与推导

### 1. step-assemble-compatibility

- 触发：已知释放方向的荷载位移和单位未知力柔度，且原支座不沉降。
- 操作：把同方向位移相加并令总位移等于零。
- 依据：恢复原约束后必须满足原结构的几何条件。
- 检查：各项方向、符号和位移量纲一致。

## 适用范围与省略

- 原释放方向位移规定值为零。
- Delta_1P 与 delta_11 使用同一方向约定。
- 存在支座沉降时，右端应改为规定位移而不是零。
- 省略：位移积分的具体求值过程。；需要恢复时：用户无法得到 Delta_1P 或 delta_11，而不只是不会组装方程时。

## 核验

检查每项均为同方向位移，并将无沉降条件代入右端为零。

历史迁移样例；完整导入信息见 [迁移记录](../history/imported-state.md)。本笔记的存在不证明用户掌握。
