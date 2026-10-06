# compression-force-method-chain

得到满足协调条件与整体平衡的原结构最终内力。

## 来源

- review-sheet · Force Method Review Sheet — The source defines the basic-system, compatibility, solution, and superposition chain.

## 方法与推导

### 1. step-release-redundant

- 触发：题目给出一次超静定结构。
- 操作：解除一个多余约束，指定 X_1 的正方向。
- 依据：力法先把未知约束力转化为基本体系上的外加未知力。
- 检查：解除数量等于超静定次数，基本体系稳定。

### 2. step-compute-flexibility

- 触发：基本体系和 X_1 方向已经确定。
- 操作：分别计算 Delta_1P 与 delta_11。
- 依据：协调方程需要外荷载位移和单位未知力柔度。
- 检查：两个位移量对应同一释放方向且符号约定一致。

### 3. step-write-compatibility

- 触发：Delta_1P 与 delta_11 已知且原约束位移为零。
- 操作：写出 Delta_1P + delta_11 X_1 = 0。
- 依据：恢复多余约束后，释放方向的总位移必须满足原约束。
- 检查：方程每一项都是同方向位移，量纲一致。

### 4. step-solve-redundant

- 触发：协调方程已经闭合。
- 操作：解得 X_1 = -Delta_1P / delta_11。
- 依据：X_1 是恢复原约束所需的未知力。
- 检查：把 X_1 回代后协调残差为零。

### 5. step-superpose-forces

- 触发：X_1 已求出。
- 操作：叠加基本体系外荷载内力与 X_1 产生的内力。
- 依据：线弹性条件下可以恢复原结构内力。
- 检查：恢复后的结构满足整体平衡。

## 适用范围与省略

- 结构为线弹性且小变形。
- 基本体系稳定，位移与柔度采用同一符号约定。
- 存在支座沉降、温度变形或非零规定转角时，协调方程右端不能直接写零。
- 省略：Delta_1P 与 delta_11 的具体积分展开。；需要恢复时：题目要求分段积分、图乘法或存在变截面 EI 时。

## 核验

回代 X_1 检查协调残差为零，并检查叠加后整体平衡。

历史迁移样例；完整导入信息见 [迁移记录](../history/imported-state.md)。本笔记的存在不证明用户掌握。
