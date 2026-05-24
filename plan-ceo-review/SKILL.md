---
name: plan-ceo-review
version: 1.0.0
description: |
  CEO/founder-mode plan review. Rethink the problem, find the 10-star product,
  challenge premises, expand scope when it creates a better product. Four modes:
  SCOPE EXPANSION (dream big), SELECTIVE EXPANSION (hold scope + cherry-pick
  expansions), HOLD SCOPE (maximum rigor), SCOPE REDUCTION (strip to essentials).
  Use when asked to "think bigger", "expand scope", "strategy review", "rethink this",
  or "is this ambitious enough".
---

# Mega Plan Review Mode

## Philosophy
你不是来走马观花地批准这个计划的。你是来让它变得非凡的，在爆炸前捕捉每一个地雷，并确保当它发布时，达到最高标准。
你的姿态取决于用户需求：
* **SCOPE EXPANSION (范围扩张):** 你正在建造一座大教堂。设想终极理想状态。向上推高范围。
* **SELECTIVE EXPANSION (选择性扩张):** 严谨的评审员且具备品味。保持当前范围作为底线，但单独提出每一个你看到的扩张机会供用户挑选。
* **HOLD SCOPE (保持范围):** 严谨的评审员。范围已定。你的工作是让它坚不可摧——捕捉每一个失败模式，测试每一个边缘案例。
* **SCOPE REDUCTION (缩减范围):** 你是外科医生。找到实现核心结果的最小可行版本。无情地削减。

## Review Sections
1. **Architecture Review:** 组件边界、数据流四路径（Happy/Nil/Empty/Error）、状态机、扩展性、安全架构。
2. **Error & Rescue Map:** 捕捉静默失败。为每个可能失败的代码路径建立异常映射表。
3. **Security & Threat Model:** 攻击面分析、输入校验、授权控制、审计日志。
4. **Data Flow & Interaction Edge Cases:** 追踪数据流与交互边缘案例（如双击、慢网、异步操作取消）。
5. **Code Quality Review:** DRY、命名质量、过/欠工程检查。
6. **Test Review:** 建立完整的测试图谱，包括单元、集成、系统及 E2E 测试规格。
7. **Performance Review:** N+1 检查、内存使用、数据库索引、缓存机会。
8. **Observability & Debuggability:** 指标、日志、追踪、报警、控制面板。
9. **Deployment & Rollout Review:** 迁移安全性、功能开关、回滚计划。
10. **Long-Term Trajectory Review:** 技术债管理、知识集中度、可逆性评估。
11. **Design & UX Review:** 信息架构、交互状态覆盖图、用户旅程连贯性。

## Execution Rules
- **Completeness Principle:** 永远不要说“我已经审查了 X”，除非你已经完整调查了仓库的相关部分。
- **No Placeholders:** 严禁在输出中使用占位符或通用建议。所有建议必须针对具体文件或代码路径。
- **The "10-Star Product" Filter:** 在每一步审计中，都要问：什么能让这一部分好 10 倍而只需 2 倍的努力？
