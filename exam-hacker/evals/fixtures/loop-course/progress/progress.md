# 结构力学期末

## Goal and constraints

- Course ID: `structural-mechanics-final`
- Target: `75`
- Exam date: `2026-09-03`
- Timezone: `Asia/Shanghai`
- Legacy available minutes (not reconfirmed remaining): `600`
- Source index: [materials](materials.md)
- Prior decisions and source details: [complete historical fields](<history/imported-state.md>)

## Mastery and priorities

Imported ability claims (retain their evidence types and conditions):

### static-beam-internal-forces

- **topic_id**: static-beam-internal-forces
- **level**: 2
- **evidence_type**: self_report
- **evidence_ref**: U01:user-confirmed
- **confidence**: medium
- **observed_at**: 2026-08-31T10:00:00+08:00
- **notes**: 能独立完成标准题

### displacement-calculation

- **topic_id**: displacement-calculation
- **level**: 1
- **evidence_type**: self_report
- **evidence_ref**: U01:user-confirmed
- **confidence**: medium
- **observed_at**: 2026-08-31T10:00:00+08:00
- **notes**: 看答案能懂，闭卷不能复现

### force-method

- **topic_id**: force-method
- **level**: 1
- **evidence_type**: drill
- **evidence_ref**: event-force-method-001
- **confidence**: high
- **observed_at**: 2026-08-31T10:45:00+08:00
- **notes**: 首轮训练得 3/10；能识别力法，但不能独立写出兼容方程

### displacement-method

- **topic_id**: displacement-method
- **level**: 3
- **evidence_type**: self_report
- **evidence_ref**: U01:user-confirmed
- **confidence**: medium
- **observed_at**: 2026-08-31T10:00:00+08:00
- **notes**: 自报能限时完成变式，尚无实作证据

Observation details: [imported observations](<practice/imported-evidence.md>)

Legacy priorities (re-evaluate P0/P1/P2 from the current goal; do not map mechanically):

- 力法: must_win — 复习单明确占 30 分且当前自报完全空白
- 位移计算: must_win — 复习单明确占 25 分且当前只能看答案理解
- 静定梁内力: supporting — 复习单明确占 20 分且用户自报可以完成标准题
- 位移法: supporting — 复习单明确占 25 分但只有自报熟练，暂不直接跳过

## Current task

- Stage: resume gap; no exact pending question is established by this import.
- Answer exposure: unknown.
- Do not infer an unanswered task from an active/queued Session label.

### Legacy planned task session-force-method-repair

- **id**: session-force-method-repair
- **kind**: drill
- **state**: active
- **phase**: 修补暴露缺口
- **title**: 力法兼容方程定点修复
- **duration_minutes**: 90
- **objective**: 不借助答案，从基本体系独立写出兼容方程
- **success_criteria**: 闭卷完成一题并正确写出未知力、位移条件和兼容方程，关键三项全部命中
- **priority_id**: priority-force-method
- **knowledge_node_ids**:
  - Item 1:
    - force-method
- **depends_on**:
  - Item 1:
    - session-force-method-01
- **input_material_ids**:
  - Item 1:
    - review-sheet
- **input_artifact_ids**:
  - Item 1:
    - event-force-method-001
- **expected_outputs**:
  - Item 1:
    - **id**: evidence-force-method-repair
    - **label**: 力法兼容方程修复证据
    - **type**: practice_evidence
    - **status**: planned

## Next action

Recover any actual unfinished question and its exposure state from the learner or existing notes. If no pending question exists, verify present constraints and present a suitable new task. Do not ask the learner to choose a specialist.

## Recent changes

- 2026-09-30T08:44:20+00:00: Imported legacy files once into Markdown; see [complete historical fields](<history/imported-state.md>).
- Migration fixture: all historical fields are preserved in the linked Markdown history; byte-backup recovery is exercised by the automated tests.

## Import warnings

- Legacy planned Sessions do not prove a pending question or known answer exposure.
- Legacy source verification labels are imported, not independently reverified.
- Legacy available minutes may be stale; confirm before treating them as remaining capacity.
