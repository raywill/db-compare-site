# -*- coding: utf-8 -*-
# 13 AI prompt templates, v2: pre-filled default scenarios (2026-09-29).
# Scenario sections come PRE-FILLED with generic recommended defaults;
# the AI treats them as confirmed and starts directly, asking interactive
# questions only for lines the user deleted or marked unknown.
# 19-dimension update applied (大版本升级 removed, 6 new dims added).
# Anchors "用交互式选择题逐题提问" / "interactive multiple-choice questions"
# and the {{CANDIDATES}} placeholder are kept byte-identical.

AI_TEMPLATES_V2 = [
    {
        "title_zh": '通用选型对比',
        "title_en": 'General comparison',
        "use_zh": '适用：第一次选型，或在 2-4 个候选库之间做一次全面对比。',
        "use_en": 'Use when: selecting for the first time, or comparing 2-4 candidates head to head.',
        "cand_mode": 'multi',
        "candidates_hint_zh": '（填 2-4 个，如 PostgreSQL、TiDB、PolarDB）',
        "candidates_hint_en": '(2-4, e.g. PostgreSQL, TiDB, PolarDB)',
        "prompt_zh": """你是一名中立的数据库架构顾问，不代表任何厂商。请基于公开资料，帮我做一次数据库选型对比。

【我的业务场景】（以下已按通用推荐场景填好：不改可直接用，按你的实际情况修改会更准；删掉某一行或标注"未知"，AI 会针对该项向你提问确认）
- 业务类型与读写特征：电商下单，读写比约 7:3，写操作以事务型订单创建为主
- 数据规模与增速：当前 2TB，年增约 50%
- 峰值负载：写 2 万 TPS，读 20 万 QPS
- 团队规模与运维能力：3 名 DBA，可接受自建
- 部署环境：公有云（华东地域为主），满足国内合规要求
- 预算约束：license 成本敏感，人力成本同样敏感
- 否决项：必须支持同城多可用区高可用；等保三级为加分项而非硬性要求
（说明：将以上默认场景视为我已确认的场景，直接开始分析；仅对我删掉或标注"未知"的行再提问。）

【候选数据库】{{CANDIDATES}}

【输出要求】
1. 按这 19 个维度逐项对比：静态加密、传输加密、审计、认证与权限、备份恢复、可观测性、连接模型、事务与隔离级别、复制与一致性、扩展方式、兼容性、许可证与商业模式、中文资料丰富度、性能与延迟特征、合规与认证、成熟度与社区生态、标杆用户、生态工具链、云托管与 Serverless。
2. 每个关键结论标注证据等级：官方文档、厂商口径、社区实测、社区共识、待验证。严格区分"查证为无"和"未找到证据"，不要把没查到的写成不支持。
3. 每款候选库给出：最适合的场景、最可能踩的三个坑（从机制层面解释，并说明在什么负载或故障下会触发）。
4. 不做综合总分、不排名，只给带条件的判断，格式为"如果……那么……"。
5. 仅在用户删掉场景中的某一行或标注"未知"导致信息不足以下结论时，才主动向我提问：用交互式选择题逐题提问，一次只问一个关键问题，每个问题给出 3-4 个带字母编号的选项（A/B/C/D，外加 E. 其他，请说明），我只需回复字母即可作答；等我回答后再问下一题；不要一次把所有问题都列出来。所有关键问题问完后，再开始分析，不要编造。
6. 用中文回答。""",
        "prompt_en": """You are a neutral database architecture advisor, not affiliated with any vendor. Help me compare candidate databases based on public information.

【My scenario】(Pre-filled with generic recommended defaults: use as-is for instant results; edit to match your reality for better accuracy; delete a line or mark it "unknown" and the AI will ask about that item to confirm)
- Workload and read/write pattern: e-commerce ordering, roughly 7:3 read/write, writes dominated by transactional order creation
- Data size and growth: 2TB today, ~50% yearly growth
- Peak load: 20k write TPS, 200k read QPS
- Team size and ops capacity: 3 DBAs, self-hosting acceptable
- Deployment: public cloud (primary region in East China), meeting local compliance requirements
- Budget constraints: sensitive to license costs; headcount costs matter too
- Deal-breakers: must support multi-AZ high availability in the same metro; compliance certification is a plus, not a hard requirement
(Note: treat the default scenario above as confirmed and start the analysis directly; only ask again about lines I deleted or marked "unknown".)

【Candidate databases】{{CANDIDATES}}

【Output requirements】
1. Compare dimension by dimension across these 19 dimensions: encryption at rest, encryption in transit, auditing, authentication and authorization, backup and recovery, observability, connection model, transactions and isolation levels, replication and consistency, scaling approach, compatibility, license and business model, Chinese-language resources, performance & latency, compliance & certifications, maturity & community, notable adopters, ecosystem tooling, managed & serverless.
2. Tag each key claim with an evidence level: official docs, vendor claim, community-tested, community consensus, to-be-verified. Strictly distinguish "verified absent" from "no evidence found"; never present something you could not find as unsupported.
3. For each candidate: the scenarios it fits best, and the three most likely production pitfalls, explained at the mechanism level, including the load or failure conditions that trigger them.
4. No aggregate total score and no ranking. Give only conditional verdicts in "if ..., then ..." form.
5. Only when a scenario line was deleted or marked "unknown" and information is missing, proactively ask me targeted interactive multiple-choice questions, one key question per turn: each with 3-4 lettered options (A/B/C/D plus E. Other, please specify) that I can answer by simply replying with the letter; wait for my answer before asking the next question; do not list all questions at once. Start the analysis only after all key questions are answered, instead of inventing facts.
6. Answer in English.""",
    },
    {
        "title_zh": '去 O 迁移评估',
        "title_en": 'Migrating off Oracle',
        "use_zh": '适用：从 Oracle 迁出，评估目标库的真实兼容代价与迁移风险。',
        "use_en": 'Use when: migrating off Oracle and assessing the true compatibility cost and risk of a target database.',
        "cand_mode": 'multi',
        "candidates_hint_zh": '（填 1-2 个，如 PolarDB-O、EDB Postgres、OceanBase Oracle 模式）',
        "candidates_hint_en": '(1-2, e.g. PolarDB-O, EDB Postgres, OceanBase Oracle mode)',
        "prompt_zh": """你是一名中立的数据库架构顾问。请帮我评估"去 O"迁移（从 Oracle 迁出）的可行性与真实成本。

【现状】（以下已按典型去 O 场景填好：不改可直接用，按你的实际情况修改会更准；删掉某一行或标注"未知"，AI 会针对该项向你提问确认）
- Oracle 版本与部署：19c，两节点 RAC
- 强依赖特性：PL/SQL 存储过程包、分区表、DBLINK（计划逐步下线）
- 数据量与停机窗口：5TB，要求停机小于 4 小时
- 性能基线：核心交易峰值 8000 TPS，慢查询主要集中在报表类 SQL
（说明：将以上默认场景视为我已确认的场景，直接开始分析；仅对我删掉或标注"未知"的行再提问。）

【候选目标库】{{CANDIDATES}}

【输出要求】
1. 兼容性逐项核对：区分"语法能跑"和"语义等价"，这是两回事，必须分开写。每项标注证据等级：官方文档、厂商口径、社区实测、社区共识、待验证。
2. 迁移风险清单，按三档输出：一定会改的代码、可能要改的代码、必须做 POC 才能确认的项。
3. 给出数据校验策略（全量加增量对账思路）与回滚方案要点。
4. 不做综合评分。仅在用户删掉【现状】中的某一行或标注"未知"导致信息不足以下结论时，才主动向我提问：用交互式选择题逐题提问，一次只问一个关键问题，每个问题给出 3-4 个带字母编号的选项（A/B/C/D，外加 E. 其他，请说明），我只需回复字母即可作答；等我回答后再问下一题；不要一次把所有问题都列出来。所有关键问题问完后，再开始分析，不要编造。用中文回答。""",
        "prompt_en": """You are a neutral database architecture advisor. Help me assess the feasibility and true cost of migrating off Oracle.

【Current state】(Pre-filled with a typical Oracle-migration scenario: use as-is for instant results; edit to match your reality for better accuracy; delete a line or mark it "unknown" and the AI will ask about that item to confirm)
- Oracle version and topology: 19c, two-node RAC
- Hard dependencies: PL/SQL packages, partitioned tables, DBLINKs (planned for gradual decommission)
- Data size and downtime budget: 5TB, less than 4 hours of downtime
- Performance baseline: 8k peak TPS on core transactions; slow queries concentrated in reporting SQL
(Note: treat the default scenario above as confirmed and start the analysis directly; only ask again about lines I deleted or marked "unknown".)

【Candidate target databases】{{CANDIDATES}}

【Output requirements】
1. Check compatibility item by item, separating "syntax runs" from "semantically equivalent" — these are different things and must be written separately. Tag each item with an evidence level: official docs, vendor claim, community-tested, community consensus, to-be-verified.
2. A migration risk list in three tiers: code that will definitely change, code that may need changes, items that can only be confirmed with a POC.
3. A data-validation strategy (full plus incremental reconciliation approach) and the key points of a rollback plan.
4. No aggregate score. Only when a 【Current state】 line was deleted or marked "unknown" and information is missing, proactively ask me targeted interactive multiple-choice questions, one key question per turn: each with 3-4 lettered options (A/B/C/D plus E. Other, please specify) that I can answer by simply replying with the letter; wait for my answer before asking the next question; do not list all questions at once. Start the analysis only after all key questions are answered, instead of inventing facts. Answer in English.""",
    },
    {
        "title_zh": '读扩展架构选型',
        "title_en": 'Read-scaling architecture',
        "use_zh": '适用：一写多读架构，读压力大，需要搞清复制延迟与代理行为的真实边界。',
        "use_en": 'Use when: single-writer, multiple-reader architectures where read pressure is high and you need the real boundaries of replication lag and proxy behavior.',
        "cand_mode": 'multi',
        "candidates_hint_zh": '（如 MySQL 一主多从加代理、PolarDB 读写分离、TiDB、Aurora 读副本）',
        "candidates_hint_en": '(e.g. MySQL primary with replicas plus proxy, PolarDB read-write splitting, TiDB, Aurora read replicas)',
        "prompt_zh": """你是一名中立的数据库架构顾问。请帮我设计"一写多读"的读扩展架构，并对比候选方案。

【我的场景】（以下已按通用推荐场景填好：不改可直接用，按你的实际情况修改会更准；删掉某一行或标注"未知"，AI 会针对该项向你提问确认）
- 写负载：主库峰值写 1 万 TPS，写放大不明显
- 读负载：读 30 万 QPS，读写比约 30:1
- 一致性要求：核心读可接受 1 秒内旧数据；分布式事务非刚需
- 可用性要求：主库故障时 RTO 小于 5 分钟，RPO 接近 0
- 候选方案：{{CANDIDATES}}
（说明：将以上默认场景视为我已确认的场景，直接开始分析；仅对我删掉或标注"未知"的行再提问。）

【输出要求】
1. 对比各方案的：复制延迟的真实量级与放大的条件、代理或中间件在故障与事务中的行为（连接闪断、事务粘性）、只读节点的成本构成、写天花板在哪里。
2. 每个关键结论标注证据等级：官方文档、厂商口径、社区实测、社区共识、待验证；严格区分"查证为无"与"未找到证据"。
3. 给出 2-3 种架构组合建议，说明各自的取舍与翻车点，不做综合评分和排名。
4. 仅在用户删掉场景中的某一行或标注"未知"导致信息不足以下结论时，才主动向我提问：用交互式选择题逐题提问，一次只问一个关键问题，每个问题给出 3-4 个带字母编号的选项（A/B/C/D，外加 E. 其他，请说明），我只需回复字母即可作答；等我回答后再问下一题；不要一次把所有问题都列出来。所有关键问题问完后，再开始分析，不要编造。用中文回答。""",
        "prompt_en": """You are a neutral database architecture advisor. Help me design a single-writer, multiple-reader architecture and compare candidate approaches.

【My scenario】(Pre-filled with generic recommended defaults: use as-is for instant results; edit to match your reality for better accuracy; delete a line or mark it "unknown" and the AI will ask about that item to confirm)
- Write load: 10k write TPS on the primary, no significant write amplification
- Read load: 300k read QPS, read/write ratio about 30:1
- Consistency requirements: core reads tolerate up to 1 second of staleness; distributed transactions not a hard requirement
- Availability targets: RTO under 5 minutes, RPO near zero on primary failure
- Candidate approaches: {{CANDIDATES}}
(Note: treat the default scenario above as confirmed and start the analysis directly; only ask again about lines I deleted or marked "unknown".)

【Output requirements】
1. Compare: realistic replication-lag magnitude and the conditions that amplify it, proxy/middleware behavior during failures and inside transactions (connection blips, transaction stickiness), cost structure of read nodes, and where the write ceiling is.
2. Tag each key claim with an evidence level: official docs, vendor claim, community-tested, community consensus, to-be-verified. Strictly distinguish "verified absent" from "no evidence found".
3. Give 2-3 architecture combinations with their trade-offs and failure modes. No aggregate score, no ranking.
4. Only when a scenario line was deleted or marked "unknown" and information is missing, proactively ask me targeted interactive multiple-choice questions, one key question per turn: each with 3-4 lettered options (A/B/C/D plus E. Other, please specify) that I can answer by simply replying with the letter; wait for my answer before asking the next question; do not list all questions at once. Start the analysis only after all key questions are answered, instead of inventing facts. Answer in English.""",
    },
    {
        "title_zh": 'KV / 文档库选型',
        "title_en": 'KV and document store selection',
        "use_zh": '适用：在 Redis、MongoDB、DynamoDB、Cassandra 等之间按访问模式选型。',
        "use_en": 'Use when: choosing between Redis, MongoDB, DynamoDB, Cassandra and similar, driven by access patterns.',
        "cand_mode": 'multi',
        "candidates_hint_zh": '（填 2-3 个，如 Redis、Valkey、MongoDB、DynamoDB、Cassandra）',
        "candidates_hint_en": '(2-3, e.g. Redis, Valkey, MongoDB, DynamoDB, Cassandra)',
        "prompt_zh": """你是一名中立的数据库架构顾问。请帮我做 KV / 文档数据库选型。

【我的场景】（以下已按通用推荐场景填好：不改可直接用，按你的实际情况修改会更准；删掉某一行或标注"未知"，AI 会针对该项向你提问确认）
- 访问模式：高频点查为主，辅以计数器和会话存储
- 数据结构：以简单 KV 和哈希为主，少量 JSON 文档
- 规模与性能：key 量级 10 亿，峰值 50 万 QPS，P99 延迟要求 5ms
- 一致性与持久化：宕机可接受秒级数据丢失；不需要多副本强一致
- 运维方式：倾向云托管，Serverless 可接受
- 候选库：{{CANDIDATES}}
（说明：将以上默认场景视为我已确认的场景，直接开始分析；仅对我删掉或标注"未知"的行再提问。）

【输出要求】
1. 按访问模式逐项对比候选库的匹配度，指出"能用但别扭"的地方。
2. 重点对比：持久化与故障恢复的真实行为、大 key 与热 key 下的表现、集群扩缩容时的数据搬迁代价、托管服务的计费边界。
3. 每个关键结论标注证据等级：官方文档、厂商口径、社区实测、社区共识、待验证。
4. 只给带条件的判断，不做综合评分与排名；仅在用户删掉场景中的某一行或标注"未知"导致信息不足以下结论时，才主动向我提问：用交互式选择题逐题提问，一次只问一个关键问题，每个问题给出 3-4 个带字母编号的选项（A/B/C/D，外加 E. 其他，请说明），我只需回复字母即可作答；等我回答后再问下一题；不要一次把所有问题都列出来。所有关键问题问完后，再开始分析。用中文回答。""",
        "prompt_en": """You are a neutral database architecture advisor. Help me select a KV or document database.

【My scenario】(Pre-filled with generic recommended defaults: use as-is for instant results; edit to match your reality for better accuracy; delete a line or mark it "unknown" and the AI will ask about that item to confirm)
- Access patterns: mostly high-frequency point lookups, plus counters and session storage
- Data structures: mostly plain KV and hashes, some JSON documents
- Scale and performance: ~1B keys, 500k peak QPS, P99 latency target 5ms
- Consistency and durability: seconds of data loss tolerable on crash; strongly-consistent multi-replica not required
- Operations: lean toward managed cloud, serverless acceptable
- Candidates: {{CANDIDATES}}
(Note: treat the default scenario above as confirmed and start the analysis directly; only ask again about lines I deleted or marked "unknown".)

【Output requirements】
1. Compare each candidate against the access patterns item by item, and call out where something "works but feels wrong".
2. Focus on: real persistence and crash-recovery behavior, behavior under big keys and hot keys, data-movement cost during cluster scale-out/in, and billing boundaries of managed services.
3. Tag each key claim with an evidence level: official docs, vendor claim, community-tested, community consensus, to-be-verified.
4. Conditional verdicts only, no aggregate score and no ranking. Only when a scenario line was deleted or marked "unknown" and information is missing, proactively ask me targeted interactive multiple-choice questions, one key question per turn: each with 3-4 lettered options (A/B/C/D plus E. Other, please specify) that I can answer by simply replying with the letter; wait for my answer before asking the next question; do not list all questions at once. Start the analysis only after all key questions are answered. Answer in English.""",
    },
    {
        "title_zh": '单库深挖',
        "title_en": 'Single-database deep dive',
        "use_zh": '适用：锁定一款数据库后，把它推到极限，提前知道会在哪里翻车。',
        "use_en": 'Use when: you have shortlisted one database and want to push it to its limits before it pushes you.',
        "cand_mode": 'single',
        "candidates_hint_zh": '【候选库名称】',
        "candidates_hint_en": '【candidate database name】',
        "prompt_zh": """你是一名中立的数据库架构顾问，专长是把系统推到极限。请深入分析{{CANDIDATES}}：

1. 它的核心机制是什么？在什么负载、异常或故障下，这个机制会最先崩？
2. 列出 3 个最可能在生产环境踩到的坑，从机制层面解释，并说明触发条件。
3. 哪些场景是它的"甜蜜点"，哪些场景是"禁区"？为什么？
4. 每个关键结论标注证据等级：官方文档、厂商口径、社区实测、社区共识、待验证；不确定的请明确说不知道，不要编造。
5. 开始前先用一道交互式选择题问我最关心的 3-5 个维度：从 19 维中给出 3-4 组带字母编号的典型组合（A/B/C/D，外加 E. 其他，请说明），我只需回复字母即可勾选；等我回答后，再针对性深挖。不要一次抛出大段文字，也不要面面俱到地平铺。
6. 不做综合评分。用中文回答。
（建议：把本站该产品的档案页内容贴在下面，作为分析的起点）""",
        "prompt_en": """You are a neutral database architecture advisor who specializes in pushing systems to their limits. Analyze {{CANDIDATES}} in depth:

1. What is its core mechanism? Under what load, anomaly, or failure does this mechanism break first?
2. List the 3 most likely production pitfalls, explain them at the mechanism level, and state their trigger conditions.
3. Which scenarios are its sweet spot, and which are no-go zones? Why?
4. Tag each key claim with an evidence level: official docs, vendor claim, community-tested, community consensus, to-be-verified. Say "I don't know" explicitly where uncertain instead of inventing facts.
5. Before starting, ask me which 3-5 dimensions I care about most with one interactive multiple-choice question: offer 3-4 lettered bundles of typical dimension combinations (A/B/C/D plus E. Other, please specify) that I can answer by simply replying with the letter; go deep on those only after I answer. Do not dump a wall of text, and do not go a mile wide and an inch deep.
6. No aggregate score. Answer in English.
(Tip: paste this site's profile page for the product below as a starting point for the analysis.)""",
    },
]


NEW_TEMPLATES_V2 = [
    {
        "group": 'olap',
        "title_zh": '离线数据仓库',
        "title_en": 'Batch data warehouse',
        "use_zh": '适用：T+1 或小时级批量 ETL，大扫描聚合为主的离线分析。',
        "use_en": 'Use when: T+1 or hourly batch ETL, offline analytics dominated by large scans and aggregations.',
        "cand_mode": 'multi',
        "candidates_hint_zh": '（如 Hive/Spark、ClickHouse、Apache Doris、StarRocks、Snowflake，填 2-3 个）',
        "candidates_hint_en": '(2-3, e.g. Hive/Spark, ClickHouse, Apache Doris, StarRocks, Snowflake)',
        "prompt_zh": """你是一名中立的数据架构顾问。请帮我做离线数据仓库（OLAP 批处理）选型。

【我的场景】（以下已按通用推荐场景填好：不改可直接用，按你的实际情况修改会更准；删掉某一行或标注"未知"，AI 会针对该项向你提问确认）
- 数据规模与增量：总量 200TB，日增 2TB
- ETL 窗口：每天凌晨 4 小时内必须跑完
- 查询特征：大表扫描聚合为主，偶发多表 JOIN；并发查询数约 20
- 数据更新需求：需要按天 UPDATE/DELETE 修正数据，每日一次
- 团队与运维：数据团队 8 人，可接受自建与调优
- 部署与成本：公有云；计算成本比存储更敏感
- 候选：{{CANDIDATES}}
（说明：将以上默认场景视为我已确认的场景，直接开始分析；仅对我删掉或标注"未知"的行再提问。）

【输出要求】
1. 按这些维度逐项对比：写入吞吐与 ETL 友好度、列存压缩与向量化扫描性能、大 JOIN 与复杂 SQL 能力、并发查询能力、数据更新与删除机制、运维复杂度（扩缩容、版本升级）、弹性扩展与存算分离、成本模型（存储与计算的计费边界）。
2. 每个关键结论标注证据等级：官方文档、厂商口径、社区实测、社区共识、待验证；严格区分"查证为无"与"未找到证据"。
3. 每款候选给出：甜蜜点、最可能踩的三个坑（从机制层面解释，如后台合并的写入放大、物化视图的刷新代价，并说明触发条件）。
4. 不做综合总分、不排名，只给"如果……那么……"的条件判断。
5. 仅在用户删掉场景中的某一行或标注"未知"导致信息不足以下结论时，才主动向我提问：用交互式选择题逐题提问，一次只问一个关键问题，每个问题给出 3-4 个带字母编号的选项（A/B/C/D，外加 E. 其他，请说明），我只需回复字母即可作答；等我回答后再问下一题；不要一次把所有问题都列出来。所有关键问题问完后，再开始分析，不要编造。用中文回答。""",
        "prompt_en": """You are a neutral data architecture advisor. Help me select an offline data warehouse (batch OLAP).

【My scenario】(Pre-filled with generic recommended defaults: use as-is for instant results; edit to match your reality for better accuracy; delete a line or mark it "unknown" and the AI will ask about that item to confirm)
- Data size and daily increment: 200TB total, 2TB per day
- ETL window: must finish within 4 hours every night
- Query pattern: mostly large-scan aggregations, occasional multi-table JOINs; ~20 concurrent queries
- Data updates: daily UPDATE/DELETE corrections, once per day
- Team and operations: 8-person data team, self-hosting and tuning acceptable
- Deployment and cost: public cloud; compute costs more sensitive than storage
- Candidates: {{CANDIDATES}}
(Note: treat the default scenario above as confirmed and start the analysis directly; only ask again about lines I deleted or marked "unknown".)

【Output requirements】
1. Compare dimension by dimension: write throughput and ETL friendliness, columnar compression and vectorized scan performance, large-JOIN and complex-SQL capability, concurrent query capacity, data update/delete mechanics, operational complexity (scaling, upgrades), elastic scaling and storage-compute separation, cost model (billing boundaries of storage vs compute).
2. Tag each key claim with an evidence level: official docs, vendor claim, community-tested, community consensus, to-be-verified. Strictly distinguish "verified absent" from "no evidence found".
3. For each candidate: its sweet spot and the three most likely pitfalls, explained at the mechanism level (e.g. write amplification from background merges, materialized-view refresh cost), with trigger conditions.
4. No aggregate total score and no ranking. Conditional verdicts only, in "if ..., then ..." form.
5. Only when a scenario line was deleted or marked "unknown" and information is missing, proactively ask me targeted interactive multiple-choice questions, one key question per turn: each with 3-4 lettered options (A/B/C/D plus E. Other, please specify) that I can answer by simply replying with the letter; wait for my answer before asking the next question; do not list all questions at once. Start the analysis only after all key questions are answered, instead of inventing facts. Answer in English.""",
    },
    {
        "group": 'olap',
        "title_zh": '实时数仓',
        "title_en": 'Real-time warehouse',
        "use_zh": '适用：秒级~分钟级延迟，流式写入、实时大屏、高并发查询。',
        "use_en": 'Use when: seconds-to-minutes latency, streaming ingestion, real-time dashboards, high-concurrency queries.',
        "cand_mode": 'multi',
        "candidates_hint_zh": '（如 ClickHouse、Apache Doris、StarRocks、Apache Pinot、Druid，填 2-3 个）',
        "candidates_hint_en": '(2-3, e.g. ClickHouse, Apache Doris, StarRocks, Apache Pinot, Druid)',
        "prompt_zh": """你是一名中立的数据架构顾问。请帮我做实时数仓选型（秒级~分钟级延迟）。

【我的场景】（以下已按通用推荐场景填好：不改可直接用，按你的实际情况修改会更准；删掉某一行或标注"未知"，AI 会针对该项向你提问确认）
- 数据源与写入：Kafka，峰值每秒写入 50 万条
- 端到端延迟 SLA：95% 的数据 1 分钟内可查
- 查询模式：实时大屏聚合为主，辅以高并发点查和明细下钻
- 语义要求：需要精确去重，exactly-once 非强需求
- 运维与成本约束：运维人力 2-3 人，倾向云托管，成本敏感
- 候选：{{CANDIDATES}}
（说明：将以上默认场景视为我已确认的场景，直接开始分析；仅对我删掉或标注"未知"的行再提问。）

【输出要求】
1. 按这些维度逐项对比：流式写入吞吐与延迟、去重与 exactly-once 语义的实现代价、实时 JOIN 能力、高并发查询下的稳定性、预聚合与物化视图、扩缩容与版本升级的运维成本、故障恢复（副本重建速度）。
2. 每个关键结论标注证据等级：官方文档、厂商口径、社区实测、社区共识、待验证；严格区分"查证为无"与"未找到证据"。
3. 每款候选给出：甜蜜点、最可能踩的三个坑（从机制层面解释，如写入放大的触发条件、副本同步延迟的放大路径）。
4. 不做综合总分、不排名，只给"如果……那么……"的条件判断。
5. 仅在用户删掉场景中的某一行或标注"未知"导致信息不足以下结论时，才主动向我提问：用交互式选择题逐题提问，一次只问一个关键问题，每个问题给出 3-4 个带字母编号的选项（A/B/C/D，外加 E. 其他，请说明），我只需回复字母即可作答；等我回答后再问下一题；不要一次把所有问题都列出来。所有关键问题问完后，再开始分析，不要编造。用中文回答。""",
        "prompt_en": """You are a neutral data architecture advisor. Help me select a real-time data warehouse (seconds-to-minutes latency).

【My scenario】(Pre-filled with generic recommended defaults: use as-is for instant results; edit to match your reality for better accuracy; delete a line or mark it "unknown" and the AI will ask about that item to confirm)
- Sources and ingestion: Kafka, peak 500k rows/sec
- End-to-end latency SLA: 95% of data queryable within 1 minute
- Query pattern: real-time dashboard aggregations, plus high-concurrency point lookups and drill-downs
- Semantics: exact deduplication required; exactly-once not a hard requirement
- Operations and cost constraints: 2-3 ops staff, lean toward managed services, cost-sensitive
- Candidates: {{CANDIDATES}}
(Note: treat the default scenario above as confirmed and start the analysis directly; only ask again about lines I deleted or marked "unknown".)

【Output requirements】
1. Compare dimension by dimension: streaming write throughput and latency, cost of implementing deduplication and exactly-once semantics, real-time JOIN capability, stability under high-concurrency queries, pre-aggregation and materialized views, operational cost of scaling and upgrades, failure recovery (replica rebuild speed).
2. Tag each key claim with an evidence level: official docs, vendor claim, community-tested, community consensus, to-be-verified. Strictly distinguish "verified absent" from "no evidence found".
3. For each candidate: its sweet spot and the three most likely pitfalls, explained at the mechanism level (e.g. trigger conditions of write amplification, amplification paths of replica-sync lag).
4. No aggregate total score and no ranking. Conditional verdicts only, in "if ..., then ..." form.
5. Only when a scenario line was deleted or marked "unknown" and information is missing, proactively ask me targeted interactive multiple-choice questions, one key question per turn: each with 3-4 lettered options (A/B/C/D plus E. Other, please specify) that I can answer by simply replying with the letter; wait for my answer before asking the next question; do not list all questions at once. Start the analysis only after all key questions are answered, instead of inventing facts. Answer in English.""",
    },
    {
        "group": 'olap',
        "title_zh": '交互式 BI 与即席查询',
        "title_en": 'Interactive BI and ad-hoc queries',
        "use_zh": '适用：分析师即席查询、BI 报表，要求亚秒响应、高并发。',
        "use_en": 'Use when: analyst ad-hoc queries and BI dashboards needing sub-second response and high concurrency.',
        "cand_mode": 'multi',
        "candidates_hint_zh": '（如 ClickHouse、Apache Doris、StarRocks、Trino/Presto、DuckDB，填 2-3 个）',
        "candidates_hint_en": '(2-3, e.g. ClickHouse, Apache Doris, StarRocks, Trino/Presto, DuckDB)',
        "prompt_zh": """你是一名中立的数据架构顾问。请帮我做交互式 BI 与即席查询引擎选型。

【我的场景】（以下已按通用推荐场景填好：不改可直接用，按你的实际情况修改会更准；删掉某一行或标注"未知"，AI 会针对该项向你提问确认）
- 用户规模与并发：200 名分析师，峰值并发查询 100
- 延迟要求：P95 在 2 秒内返回
- 数据量级与查询复杂度：多维下钻为主，每日约 30% 的查询会钻取明细
- BI 工具：Superset 为主，少量 Tableau
- 权限需求：需要行级权限，列级权限暂不需要
- 候选：{{CANDIDATES}}
（说明：将以上默认场景视为我已确认的场景，直接开始分析；仅对我删掉或标注"未知"的行再提问。）

【输出要求】
1. 按这些维度逐项对比：亚秒查询能力、高并发下的排队与资源隔离、BI 工具兼容性（SQL 方言、连接协议）、语义层与行列级权限、查询加速手段（缓存、预聚合）、运维复杂度与成本模型。
2. 每个关键结论标注证据等级：官方文档、厂商口径、社区实测、社区共识、待验证；严格区分"查证为无"与"未找到证据"。
3. 每款候选给出：甜蜜点、最可能踩的三个坑（从机制层面解释，如高并发下查询排队的触发条件、BI 生成 SQL 的方言坑）。
4. 不做综合总分、不排名，只给"如果……那么……"的条件判断。
5. 仅在用户删掉场景中的某一行或标注"未知"导致信息不足以下结论时，才主动向我提问：用交互式选择题逐题提问，一次只问一个关键问题，每个问题给出 3-4 个带字母编号的选项（A/B/C/D，外加 E. 其他，请说明），我只需回复字母即可作答；等我回答后再问下一题；不要一次把所有问题都列出来。所有关键问题问完后，再开始分析，不要编造。用中文回答。""",
        "prompt_en": """You are a neutral data architecture advisor. Help me select an engine for interactive BI and ad-hoc queries.

【My scenario】(Pre-filled with generic recommended defaults: use as-is for instant results; edit to match your reality for better accuracy; delete a line or mark it "unknown" and the AI will ask about that item to confirm)
- Users and concurrency: 200 analysts, 100 peak concurrent queries
- Latency target: P95 under 2 seconds
- Data size and query complexity: mostly multi-dimensional drill-downs; ~30% of daily queries drill through to detail rows
- BI tools: mainly Superset, some Tableau
- Authorization needs: row-level permissions required; column-level not needed yet
- Candidates: {{CANDIDATES}}
(Note: treat the default scenario above as confirmed and start the analysis directly; only ask again about lines I deleted or marked "unknown".)

【Output requirements】
1. Compare dimension by dimension: sub-second query capability, queuing and resource isolation under high concurrency, BI tool compatibility (SQL dialect, wire protocol), semantic layer and row/column-level permissions, acceleration techniques (caching, pre-aggregation), operational complexity and cost model.
2. Tag each key claim with an evidence level: official docs, vendor claim, community-tested, community consensus, to-be-verified. Strictly distinguish "verified absent" from "no evidence found".
3. For each candidate: its sweet spot and the three most likely pitfalls, explained at the mechanism level (e.g. trigger conditions of query queuing under high concurrency, SQL-dialect pitfalls from BI-generated queries).
4. No aggregate total score and no ranking. Conditional verdicts only, in "if ..., then ..." form.
5. Only when a scenario line was deleted or marked "unknown" and information is missing, proactively ask me targeted interactive multiple-choice questions, one key question per turn: each with 3-4 lettered options (A/B/C/D plus E. Other, please specify) that I can answer by simply replying with the letter; wait for my answer before asking the next question; do not list all questions at once. Start the analysis only after all key questions are answered, instead of inventing facts. Answer in English.""",
    },
    {
        "group": 'olap',
        "title_zh": '湖仓一体',
        "title_en": 'Lakehouse',
        "use_zh": '适用：已有数据湖，想统一批流、开放表格式、存算分离。',
        "use_en": 'Use when: you have a data lake and want unified batch/streaming, open table formats, and storage-compute separation.',
        "cand_mode": 'multi',
        "candidates_hint_zh": '（如 Iceberg 加 Trino、Hudi 加 Flink 等，填 1-2 组）',
        "candidates_hint_en": '(1-2, e.g. Iceberg plus Trino, Hudi plus Flink)',
        "prompt_zh": """你是一名中立的数据架构顾问。请帮我做湖仓一体架构选型。

【我的场景】（以下已按通用推荐场景填好：不改可直接用，按你的实际情况修改会更准；删掉某一行或标注"未知"，AI 会针对该项向你提问确认）
- 数据湖现状：对象存储，总量约 300TB
- 表格式倾向：尚未确定，倾向 Iceberg
- 计算引擎：Spark 跑批处理，Trino 跑即席查询
- 事务需求：需要 ACID 与 schema evolution，time travel 为加分项
- 流批一体需求：希望同一份数据同时服务离线与实时，但可分阶段落地
- 候选组合：{{CANDIDATES}}
（说明：将以上默认场景视为我已确认的场景，直接开始分析；仅对我删掉或标注"未知"的行再提问。）

【输出要求】
1. 按这些维度逐项对比：表格式能力（ACID、schema evolution、分区演进、time travel）、引擎生态与兼容性、元数据服务（catalog）选型、小文件问题与 compaction 代价、存算分离下的真实成本、流批一体的成熟度（区分"能跑"和"生产可用"）。
2. 每个关键结论标注证据等级：官方文档、厂商口径、社区实测、社区共识、待验证；严格区分"查证为无"与"未找到证据"。
3. 每组候选给出：甜蜜点、最可能踩的三个坑（从机制层面解释，如小文件放大的触发条件、compaction 的资源争抢）。
4. 不做综合总分、不排名，只给"如果……那么……"的条件判断。
5. 仅在用户删掉场景中的某一行或标注"未知"导致信息不足以下结论时，才主动向我提问：用交互式选择题逐题提问，一次只问一个关键问题，每个问题给出 3-4 个带字母编号的选项（A/B/C/D，外加 E. 其他，请说明），我只需回复字母即可作答；等我回答后再问下一题；不要一次把所有问题都列出来。所有关键问题问完后，再开始分析，不要编造。用中文回答。""",
        "prompt_en": """You are a neutral data architecture advisor. Help me select a lakehouse architecture.

【My scenario】(Pre-filled with generic recommended defaults: use as-is for instant results; edit to match your reality for better accuracy; delete a line or mark it "unknown" and the AI will ask about that item to confirm)
- Data lake status: object storage, ~300TB total
- Table format leaning: undecided, leaning toward Iceberg
- Compute engines: Spark for batch, Trino for ad-hoc queries
- Transactional needs: ACID and schema evolution required; time travel a plus
- Streaming-batch unification: want one dataset serving offline and real-time, phased rollout acceptable
- Candidate combinations: {{CANDIDATES}}
(Note: treat the default scenario above as confirmed and start the analysis directly; only ask again about lines I deleted or marked "unknown".)

【Output requirements】
1. Compare dimension by dimension: table-format capabilities (ACID, schema evolution, partition evolution, time travel), engine ecosystem and compatibility, metadata service (catalog) choice, small-files problem and compaction cost, real cost under storage-compute separation, maturity of streaming-batch unification (separate "it runs" from "production-ready").
2. Tag each key claim with an evidence level: official docs, vendor claim, community-tested, community consensus, to-be-verified. Strictly distinguish "verified absent" from "no evidence found".
3. For each candidate combination: its sweet spot and the three most likely pitfalls, explained at the mechanism level (e.g. trigger conditions of small-file amplification, resource contention from compaction).
4. No aggregate total score and no ranking. Conditional verdicts only, in "if ..., then ..." form.
5. Only when a scenario line was deleted or marked "unknown" and information is missing, proactively ask me targeted interactive multiple-choice questions, one key question per turn: each with 3-4 lettered options (A/B/C/D plus E. Other, please specify) that I can answer by simply replying with the letter; wait for my answer before asking the next question; do not list all questions at once. Start the analysis only after all key questions are answered, instead of inventing facts. Answer in English.""",
    },
    {
        "group": 'olap',
        "title_zh": '嵌入式与单机分析',
        "title_en": 'Embedded and single-node analytics',
        "use_zh": '适用：笔记本/单机/边缘的零运维分析，数据量 GB 到数 TB。',
        "use_en": 'Use when: zero-ops analytics on a laptop, single server, or edge, with GBs to a few TBs of data.',
        "cand_mode": 'multi',
        "candidates_hint_zh": '（如 DuckDB、ClickHouse 单机版、SQLite 相关方案，填 2-3 个）',
        "candidates_hint_en": '(2-3, e.g. DuckDB, single-node ClickHouse, SQLite-based options)',
        "prompt_zh": """你是一名中立的数据架构顾问。请帮我做嵌入式与单机 OLAP 选型。

【我的场景】（以下已按通用推荐场景填好：不改可直接用，按你的实际情况修改会更准；删掉某一行或标注"未知"，AI 会针对该项向你提问确认）
- 运行环境：单机服务器（64 核 / 256GB 内存）
- 数据量级：几百 GB，未来 2 年可能到 2TB
- 语言生态：Python/Arrow 为刚需
- 写入特征：单并发批量写入，每日一次
- 运维要求：要求零运维，嵌入应用分发
- 候选：{{CANDIDATES}}
（说明：将以上默认场景视为我已确认的场景，直接开始分析；仅对我删掉或标注"未知"的行再提问。）

【输出要求】
1. 按这些维度逐项对比：单机扫描性能天花板、内存管理与溢出行为、Python/Arrow 生态集成度、并发写入限制、文件格式与外部数据互操作、从单机扩展到集群的迁移路径。
2. 每个关键结论标注证据等级：官方文档、厂商口径、社区实测、社区共识、待验证；严格区分"查证为无"与"未找到证据"。
3. 每款候选给出：甜蜜点、最可能踩的三个坑（从机制层面解释），以及"出现什么信号就必须换成集群架构"的判断线。
4. 不做综合总分、不排名，只给"如果……那么……"的条件判断。
5. 仅在用户删掉场景中的某一行或标注"未知"导致信息不足以下结论时，才主动向我提问：用交互式选择题逐题提问，一次只问一个关键问题，每个问题给出 3-4 个带字母编号的选项（A/B/C/D，外加 E. 其他，请说明），我只需回复字母即可作答；等我回答后再问下一题；不要一次把所有问题都列出来。所有关键问题问完后，再开始分析，不要编造。用中文回答。""",
        "prompt_en": """You are a neutral data architecture advisor. Help me select an embedded or single-node OLAP engine.

【My scenario】(Pre-filled with generic recommended defaults: use as-is for instant results; edit to match your reality for better accuracy; delete a line or mark it "unknown" and the AI will ask about that item to confirm)
- Environment: single server (64 cores / 256GB RAM)
- Data size: hundreds of GB, possibly 2TB within 2 years
- Language ecosystem: Python/Arrow integration is a hard requirement
- Write pattern: single-writer batch loads, once daily
- Operations: zero-ops required, embedded distribution with the app
- Candidates: {{CANDIDATES}}
(Note: treat the default scenario above as confirmed and start the analysis directly; only ask again about lines I deleted or marked "unknown".)

【Output requirements】
1. Compare dimension by dimension: single-node scan performance ceiling, memory management and spilling behavior, Python/Arrow ecosystem integration, concurrent-write limits, file-format and external-data interoperability, migration path from single node to a cluster.
2. Tag each key claim with an evidence level: official docs, vendor claim, community-tested, community consensus, to-be-verified. Strictly distinguish "verified absent" from "no evidence found".
3. For each candidate: its sweet spot, the three most likely pitfalls explained at the mechanism level, and the tripwire — what signals mean you must move to a cluster architecture.
4. No aggregate total score and no ranking. Conditional verdicts only, in "if ..., then ..." form.
5. Only when a scenario line was deleted or marked "unknown" and information is missing, proactively ask me targeted interactive multiple-choice questions, one key question per turn: each with 3-4 lettered options (A/B/C/D plus E. Other, please specify) that I can answer by simply replying with the letter; wait for my answer before asking the next question; do not list all questions at once. Start the analysis only after all key questions are answered, instead of inventing facts. Answer in English.""",
    },
    {
        "group": 'aidb',
        "title_zh": 'RAG 向量库选型',
        "title_en": 'Vector DB for RAG',
        "use_zh": '适用：RAG 知识库，在专用向量库与通用库 AI 扩展之间做选择。',
        "use_en": 'Use when: building a RAG knowledge base and choosing between dedicated vector databases and AI extensions of general databases.',
        "cand_mode": 'multi',
        "candidates_hint_zh": '（如 Milvus、Weaviate、Qdrant、Pinecone、pgvector、OceanBase 向量、Elasticsearch，填 2-3 个）',
        "candidates_hint_en": '(2-3, e.g. Milvus, Weaviate, Qdrant, Pinecone, pgvector, OceanBase vector, Elasticsearch)',
        "prompt_zh": """你是一名中立的 AI 基础设施顾问。请帮我做 RAG 场景的向量数据库选型。

【我的场景】（以下已按通用推荐场景填好：不改可直接用，按你的实际情况修改会更准；删掉某一行或标注"未知"，AI 会针对该项向你提问确认）
- 向量规模：5000 万条，维度 1024
- embedding 模型：bge-m3，已固定
- 查询负载：峰值 2000 QPS，P99 延迟要求 100ms
- 过滤需求：需要标量过滤（按租户、时间、标签过滤后再做向量检索）
- 数据更新：每日新增约 1%，删除量小
- 部署方式：倾向云托管
- 候选：{{CANDIDATES}}
（说明：将以上默认场景视为我已确认的场景，直接开始分析；仅对我删掉或标注"未知"的行再提问。）

【输出要求】
1. 按 AI 数据库自己的维度对比（不要套用 OLTP 的维度）：向量索引算法（HNSW/IVF/DiskANN）与召回率-延迟权衡、标量过滤加向量混合检索（注意 pre-filtering 与 post-filtering 的正确性陷阱）、十亿级扩展（分片与分布式）、实时写入与删除的代价、embedding 流水线（切分与向量化谁来做、模型集成方式）、与现有技术栈的协同、成本模型。
2. 每个关键结论标注证据等级：官方文档、厂商口径、社区实测、社区共识、待验证；严格区分"查证为无"与"未找到证据"。
3. 每款候选给出：甜蜜点、最可能踩的三个坑（从机制层面解释，如 HNSW 参数调优空间、过滤导致召回率塌陷的条件）。
4. 不做综合总分、不排名，只给"如果……那么……"的条件判断。
5. 仅在用户删掉场景中的某一行或标注"未知"导致信息不足以下结论时，才主动向我提问：用交互式选择题逐题提问，一次只问一个关键问题，每个问题给出 3-4 个带字母编号的选项（A/B/C/D，外加 E. 其他，请说明），我只需回复字母即可作答；等我回答后再问下一题；不要一次把所有问题都列出来。所有关键问题问完后，再开始分析，不要编造。用中文回答。""",
        "prompt_en": """You are a neutral AI infrastructure advisor. Help me select a vector database for a RAG workload.

【My scenario】(Pre-filled with generic recommended defaults: use as-is for instant results; edit to match your reality for better accuracy; delete a line or mark it "unknown" and the AI will ask about that item to confirm)
- Vector scale: 50M vectors, 1024 dimensions
- Embedding model: bge-m3, fixed
- Query load: 2k peak QPS, P99 latency target 100ms
- Filtering needs: scalar filtering required (by tenant, time, tags before vector search)
- Data churn: ~1% daily inserts, few deletes
- Deployment: lean toward managed cloud
- Candidates: {{CANDIDATES}}
(Note: treat the default scenario above as confirmed and start the analysis directly; only ask again about lines I deleted or marked "unknown".)

【Output requirements】
1. Compare along dimensions native to AI databases (do not reuse OLTP dimensions): vector index algorithms (HNSW/IVF/DiskANN) and the recall-latency trade-off, scalar-filter plus vector hybrid search (watch the correctness trap of pre-filtering vs post-filtering), billion-scale-out (sharding and distribution), cost of real-time writes and deletes, the embedding pipeline (who does chunking and vectorization, model integration), fit with the existing stack, cost model.
2. Tag each key claim with an evidence level: official docs, vendor claim, community-tested, community consensus, to-be-verified. Strictly distinguish "verified absent" from "no evidence found".
3. For each candidate: its sweet spot and the three most likely pitfalls, explained at the mechanism level (e.g. HNSW parameter tuning headroom, conditions under which filtering collapses recall).
4. No aggregate total score and no ranking. Conditional verdicts only, in "if ..., then ..." form.
5. Only when a scenario line was deleted or marked "unknown" and information is missing, proactively ask me targeted interactive multiple-choice questions, one key question per turn: each with 3-4 lettered options (A/B/C/D plus E. Other, please specify) that I can answer by simply replying with the letter; wait for my answer before asking the next question; do not list all questions at once. Start the analysis only after all key questions are answered, instead of inventing facts. Answer in English.""",
    },
    {
        "group": 'aidb',
        "title_zh": '专用向量库 vs 通用库 AI 扩展',
        "title_en": 'Dedicated vector DB vs AI extensions',
        "use_zh": '适用：已有 PG/OceanBase/ES，想判断要不要引入专用向量库。',
        "use_en": 'Use when: you already run PG/OceanBase/ES and need to decide whether a dedicated vector database is warranted.',
        "cand_mode": 'first',
        "candidates_hint_zh": '（如 PostgreSQL 加 pgvector / OceanBase 向量 / Elasticsearch dense_vector / MongoDB Atlas Vector Search）',
        "candidates_hint_en": '(e.g. PostgreSQL with pgvector / OceanBase vector / Elasticsearch dense_vector / MongoDB Atlas Vector Search)',
        "prompt_zh": """你是一名中立的 AI 基础设施顾问。请帮我判断：RAG 场景下，继续用现有通用数据库的 AI 扩展，还是引入专用向量数据库？

【我的现状】（以下已按通用推荐场景填好：不改可直接用，按你的实际情况修改会更准；删掉某一行或标注"未知"，AI 会针对该项向你提问确认）
- 现有数据库：{{CANDIDATES}}
- 向量规模与增长预期：当前 2000 万条，维度 1024，未来一年预计增长到 1 亿
- 当前痛点：召回率不达标（Top10 召回率约 85%），过滤查询写起来别扭
- 团队对引入新组件的接受度：可以接受，但希望运维负担可控
（说明：将以上默认场景视为我已确认的场景，直接开始分析；仅对我删掉或标注"未知"的行再提问。）

【输出要求】
1. 对比通用库 AI 扩展与专用向量库（Milvus、Qdrant、Weaviate）在五个方面的差异：索引算法丰富度、规模天花板、混合检索能力、运维负担、生态集成。
2. 给出明确的取舍线：什么规模与什么信号出现之前，通用库的 AI 扩展够用；出现哪些信号，就必须迁到专用向量库。
3. 如果建议迁移，给出迁移代价评估（数据迁移、双写、回滚方案）。
4. 每个关键结论标注证据等级：官方文档、厂商口径、社区实测、社区共识、待验证；严格区分"查证为无"与"未找到证据"。
5. 不做综合总分、不排名；仅在用户删掉【我的现状】中的某一行或标注"未知"导致信息不足以下结论时，才主动向我提问：用交互式选择题逐题提问，一次只问一个关键问题，每个问题给出 3-4 个带字母编号的选项（A/B/C/D，外加 E. 其他，请说明），我只需回复字母即可作答；等我回答后再问下一题；不要一次把所有问题都列出来。所有关键问题问完后，再开始分析，不要编造。用中文回答。""",
        "prompt_en": """You are a neutral AI infrastructure advisor. Help me decide: for a RAG workload, should I stay on my general-purpose database's AI extension or adopt a dedicated vector database?

【Current state】(Pre-filled with generic recommended defaults: use as-is for instant results; edit to match your reality for better accuracy; delete a line or mark it "unknown" and the AI will ask about that item to confirm)
- Existing database: {{CANDIDATES}}
- Vector scale and growth outlook: 20M vectors at 1024 dims today, expected to reach 100M within a year
- Current pain points: recall below bar (~85% Top-10 recall), filtered queries awkward to write
- Team appetite for adding a new component: acceptable if operational burden stays manageable
(Note: treat the default scenario above as confirmed and start the analysis directly; only ask again about lines I deleted or marked "unknown".)

【Output requirements】
1. Contrast general-purpose AI extensions against dedicated vector databases (Milvus, Qdrant, Weaviate) on five axes: index-algorithm richness, scale ceiling, hybrid-search capability, operational burden, ecosystem integration.
2. Draw an explicit line: below what scale and signals the general-purpose extension is enough; which signals mean you must move to a dedicated vector database.
3. If migration is advised, assess the migration cost (data migration, dual writes, rollback plan).
4. Tag each key claim with an evidence level: official docs, vendor claim, community-tested, community consensus, to-be-verified. Strictly distinguish "verified absent" from "no evidence found".
5. No aggregate total score and no ranking. Only when a 【Current state】 line was deleted or marked "unknown" and information is missing, proactively ask me targeted interactive multiple-choice questions, one key question per turn: each with 3-4 lettered options (A/B/C/D plus E. Other, please specify) that I can answer by simply replying with the letter; wait for my answer before asking the next question; do not list all questions at once. Start the analysis only after all key questions are answered, instead of inventing facts. Answer in English.""",
    },
    {
        "group": 'aidb',
        "title_zh": '混合检索与召回质量',
        "title_en": 'Hybrid search and recall quality',
        "use_zh": '适用：RAG 检索质量不达标，需要深水区诊断与调优。',
        "use_en": 'Use when: RAG retrieval quality is below bar and you need deep diagnosis and tuning.',
        "prompt_zh": """你是一名中立的 AI 基础设施顾问，专长检索质量调优。我的 RAG 检索质量不达标，请帮我做混合检索与召回质量的深水区诊断。

【我的现状】（以下已按通用推荐场景填好：不改可直接用，按你的实际情况修改会更准；删掉某一行或标注"未知"，AI 会针对该项向你提问确认）
- 当前方案：单一向量检索
- 症状：召回率低（Top10 召回率约 80%），相关文档排不上
- 数据特征：中英文混合，长文档，结构化字段多（租户、时间、标签）
（说明：将以上默认场景视为我已确认的场景，直接开始分析；仅对我删掉或标注"未知"的行再提问。）

【输出要求】
1. 给出诊断框架：先判断是 embedding 模型问题、索引参数问题、切分策略问题，还是过滤写法问题，并说明每种的判别方法。
2. 对比混合检索策略：多路召回（向量加全文加稀疏）与结果融合（RRF 这类方法）、重排（rerank）模型的取舍与代价。
3. 给出离线评测方法：如何构建评测集、用什么指标（召回率、MRR、nDCG）验证优化真的有效。
4. 说明 GraphRAG 这类方案在什么条件下值得上、什么条件下是过度设计。
5. 每个关键结论标注证据等级：官方文档、厂商口径、社区实测、社区共识、待验证；不确定的明确说不知道，不要编造。
6. 若用户删掉【我的现状】中的行或标注"未知"，像医生问诊一样先向我提问：交互式逐题进行，一次只问一个关键症状，每个症状给出 3-4 个带字母编号的选项（A/B/C/D，外加 E. 其他，请说明），我只需回复字母即可作答；等我回答后再问下一个，所有关键症状问完后，再开始诊断。不要一次把所有问题都列出来，也不要编造。问诊时优先覆盖：召回不达标的具体症状（查全/查准/排序哪个环节）、向量规模与索引类型、标量过滤复杂度、查询模式（TopK 取值）、已尝试过的优化手段。用中文回答。""",
        "prompt_en": """You are a neutral AI infrastructure advisor specializing in retrieval-quality tuning. My RAG retrieval quality is below bar — help me with a deep diagnosis of hybrid search and recall quality.

【Current state】(Pre-filled with generic recommended defaults: use as-is for instant results; edit to match your reality for better accuracy; delete a line or mark it "unknown" and the AI will ask about that item to confirm)
- Current approach: pure vector search
- Symptoms: low recall (~80% Top-10 recall), relevant documents not ranking
- Data characteristics: mixed Chinese-English, long documents, many structured fields (tenant, time, tags)
(Note: treat the default scenario above as confirmed and start the analysis directly; only ask again about lines I deleted or marked "unknown".)

【Output requirements】
1. A diagnostic framework: determine first whether it is an embedding-model problem, an index-parameter problem, a chunking-strategy problem, or a filter-writing problem — with a discrimination method for each.
2. Compare hybrid strategies: multi-path retrieval (vector plus full-text plus sparse) with result fusion (methods like RRF), and the trade-offs and costs of rerank models.
3. An offline evaluation method: how to build an eval set and which metrics (recall, MRR, nDCG) prove an optimization actually worked.
4. When GraphRAG-style approaches are worth it and when they are over-engineering.
5. Tag each key claim with an evidence level: official docs, vendor claim, community-tested, community consensus, to-be-verified. Say explicitly where uncertain instead of inventing facts.
6. If the user deleted 【Current state】 lines or marked them "unknown", take a doctor-like history first, interactively one symptom at a time: each step ask one key symptom with 3-4 lettered options (A/B/C/D plus E. Other, please specify) that I can answer by simply replying with the letter; wait for my answer before asking the next one, and start the diagnosis only after the history is complete. Do not list all questions at once, and do not invent facts. Prioritize asking about: which stage underperforms (recall/precision/ranking), vector scale and index type, scalar-filter complexity, query pattern (TopK value), optimizations already tried. Answer in English.""",
    },
]
