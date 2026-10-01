# -*- coding: utf-8 -*-
"""6 个新增维度的双语内容（C 组）：json_semi / fulltext / sp_proc / constraints / analytical_sql / matview.
CONTENT3_C[slug][dimkey] = {"zh": {"v","p","b"}, "en": {"v","p","b"}}
v = verdict（有/部分支持/无/不适用/未找到证据；Supported/Partial/Not supported/N/A/No evidence found），p = 10-25 字短语，b = markdown 正文。
正文沿用档案体例：`- ` 条目 + 反引号证据徽章（`官方文档`/`厂商口径`/`社区实测`/`社区共识`/`待验证`；英文 `(official docs)` 等）。
31 个产品 × 6 维度 × 2 语言 = 372 条目。
"""

CONTENT3_C = {}

# ---------------- alloydb ----------------
CONTENT3_C["alloydb"] = {
  "json_semi": {
    "zh": {"v": "有", "p": "jsonb 完整，GIN 索引",
           "b": "- jsonb 类型与 ->/->>/@>/jsonpath 算子完整，GIN（含 jsonb_path_ops）索引可用 `官方文档`。\n- 大 jsonb 文档更新为整行重写，频繁局部更新场景写放大明显 `社区共识`。"},
    "en": {"v": "Supported", "p": "Full jsonb with GIN indexing",
           "b": "- Complete jsonb with ->/->>/@>/jsonpath operators and GIN (incl. jsonb_path_ops) indexes `(official docs)`.\n- Large jsonb documents rewrite whole on update; heavy partial-update workloads see write amplification `(community consensus)`."}},
  "fulltext": {
    "zh": {"v": "有", "p": "tsvector/GIN；中文需分词插件",
           "b": "- tsvector/tsquery + GIN 全文检索完整，排名、加权、高亮开箱即用 `官方文档`。\n- 中文无内置分词，需 zhparser/jieba 等插件，分词质量决定召回 `社区共识`。"},
    "en": {"v": "Supported", "p": "tsvector/GIN; CJK needs plugins",
           "b": "- Full tsvector/tsquery + GIN with ranking, weighting, highlighting `(official docs)`.\n- No built-in Chinese tokenizer; zhparser/jieba plugins required, recall depends on segmentation quality `(community consensus)`."}},
  "sp_proc": {
    "zh": {"v": "有", "p": "plpgsql 完整；去 O 改写中等",
           "b": "- plpgsql 及多种过程语言完整，调试与异常处理成熟 `官方文档`。\n- 去 O 迁移：PL/SQL 包、自治事务等需改写，ora2pg/EDB 工具链可辅助评估 `社区共识`。"},
    "en": {"v": "Supported", "p": "Full plpgsql; moderate rewrite cost",
           "b": "- Complete plpgsql and multiple procedural languages with mature debugging `(official docs)`.\n- Oracle migration: packages and autonomous transactions need rewrites; ora2pg/EDB tooling helps assess `(community consensus)`."}},
  "constraints": {
    "zh": {"v": "有", "p": "约束语义最全：EXCLUDE/deferrable",
           "b": "- 外键、CHECK、唯一、EXCLUDE、deferrable 约束齐全，语义严格 `官方文档`。\n- 大表加带验证的外键/CHECK 会锁表，需分步或在线手段 `社区实测`。"},
    "en": {"v": "Supported", "p": "Full FK/CHECK/EXCLUDE/deferrable",
           "b": "- Full FK, CHECK, unique, EXCLUDE, deferrable constraints with strict semantics `(official docs)`.\n- Adding validated FK/CHECK on huge tables locks; use staged or online approaches `(community tested)`."}},
  "analytical_sql": {
    "zh": {"v": "有", "p": "窗口/CTE/递归完备，分析标杆",
           "b": "- 窗口函数、CTE（含递归）、GROUPING SETS/CUBE/ROLLUP 完备 `官方文档`。\n- 复杂分析查询优化器成熟，执行计划可读性好 `社区共识`。"},
    "en": {"v": "Supported", "p": "Complete windows/CTEs/recursion",
           "b": "- Complete window functions, CTEs (incl. recursive), GROUPING SETS/CUBE/ROLLUP `(official docs)`.\n- Mature optimizer for complex analytics with readable plans `(community consensus)`."}},
  "matview": {
    "zh": {"v": "有", "p": "物化视图手动刷新为主",
           "b": "- 支持物化视图，REFRESH（含 CONCURRENTLY）手动触发 `官方文档`。\n- 无原生增量自动刷新与查询自动改写，高频更新场景需自建调度 `社区共识`。"},
    "en": {"v": "Supported", "p": "Manual-refresh materialized views",
           "b": "- Materialized views with manual REFRESH (incl. CONCURRENTLY) `(official docs)`.\n- No native incremental auto-refresh or automatic query rewrite; schedule refreshes yourself for hot data `(community consensus)`."}},
}

# ---------------- aurora ----------------
CONTENT3_C["aurora"] = {
  "json_semi": {
    "zh": {"v": "有", "p": "MySQL 版 JSON；PG 版 jsonb",
           "b": "- Aurora MySQL：原生 JSON 二进制类型，虚拟生成列+索引，JSON_TABLE 可用 `官方文档`。\n- Aurora PG：jsonb 完整；两引擎 JSON 互不兼容，选型时按引擎看 `社区共识`。"},
    "en": {"v": "Supported", "p": "Native JSON (MySQL); jsonb (PG)",
           "b": "- Aurora MySQL: native binary JSON, virtual generated columns + indexes, JSON_TABLE `(official docs)`.\n- Aurora PG: full jsonb; JSON features differ by engine, evaluate per engine `(community consensus)`."}},
  "fulltext": {
    "zh": {"v": "有", "p": "ngram 中文分词；PG tsvector",
           "b": "- MySQL 版：FULLTEXT 索引 + ngram parser 中文分词 `官方文档`。\n- 相关性排序弱于专业检索引擎，大规模检索仍建议外挂 OpenSearch `社区共识`。"},
    "en": {"v": "Supported", "p": "FULLTEXT+ngram; tsvector on PG",
           "b": "- MySQL flavor: FULLTEXT + ngram parser for Chinese `(official docs)`.\n- Relevance ranking weaker than dedicated search engines; large-scale search still wants OpenSearch `(community consensus)`."}},
  "sp_proc": {
    "zh": {"v": "有", "p": "SP/触发器/事件完整",
           "b": "- MySQL 版支持存储过程、触发器、事件调度；PG 版 plpgsql 完整 `官方文档`。\n- MySQL 过程语言无包、调试弱，去 O 迁移改写成本高 `社区共识`。"},
    "en": {"v": "Supported", "p": "Full procedures/triggers/events",
           "b": "- MySQL flavor: procedures, triggers, event scheduler; PG flavor: full plpgsql `(official docs)`.\n- MySQL procedural language lacks packages and debugging; Oracle migration rewrites are costly `(community consensus)`."}},
  "constraints": {
    "zh": {"v": "有", "p": "InnoDB 约束完整",
           "b": "- InnoDB 外键、CHECK（8.0.16+ 强制）、唯一约束完整 `官方文档`。\n- 外键级联大批量删除易放大写入与锁等待 `社区实测`。"},
    "en": {"v": "Supported", "p": "Full InnoDB constraints",
           "b": "- Full InnoDB FK, enforced CHECK (8.0.16+), unique constraints `(official docs)`.\n- FK cascades on bulk deletes amplify writes and lock waits `(community tested)`."}},
  "analytical_sql": {
    "zh": {"v": "有", "p": "MySQL 8 窗口/CTE；PG 完整",
           "b": "- MySQL 版：8.0 窗口函数、CTE（含递归）可用 `官方文档`。\n- 复杂分析性能弱于 OLAP 引擎，大宽表关联仍是短板 `社区共识`。"},
    "en": {"v": "Supported", "p": "MySQL 8 windows/CTEs; full on PG",
           "b": "- MySQL flavor: 8.0 window functions and CTEs (incl. recursive) `(official docs)`.\n- Complex analytics lag OLAP engines; wide-table joins remain a weakness `(community consensus)`."}},
  "matview": {
    "zh": {"v": "部分支持", "p": "PG 版手动物化视图；MySQL 版无",
           "b": "- Aurora PG：物化视图手动 REFRESH（含 CONCURRENTLY）`官方文档`。\n- Aurora MySQL：无物化视图，靠汇总表+触发器/定时任务模拟 `社区共识`。"},
    "en": {"v": "Partial", "p": "Manual MVs on PG; none on MySQL",
           "b": "- Aurora PG: materialized views with manual REFRESH (incl. CONCURRENTLY) `(official docs)`.\n- Aurora MySQL: none; summary tables + triggers/jobs instead `(community consensus)`."}},
}

# ---------------- cassandra-scylladb ----------------
CONTENT3_C["cassandra-scylladb"] = {
  "json_semi": {
    "zh": {"v": "部分支持", "p": "集合类型；JSON 文本存取",
           "b": "- CQL 有 map/list/set 集合类型，可表达嵌套结构 `官方文档`。\n- 无原生 JSON 类型；ScyllaDB 支持 INSERT/SELECT JSON 语法糖，底层仍为文本/集合 `官方文档`。\n- 集合过大导致分区膨胀，生产建议控制元素数量 `社区共识`。"},
    "en": {"v": "Partial", "p": "Collections; JSON as text",
           "b": "- CQL map/list/set collections express nested structures `(official docs)`.\n- No native JSON type; ScyllaDB offers INSERT/SELECT JSON syntax over text/collections `(official docs)`.\n- Oversized collections bloat partitions; keep element counts bounded `(community consensus)`."}},
  "fulltext": {
    "zh": {"v": "部分支持", "p": "SASI 非分词；生产多外挂 ES",
           "b": "- SASI 二级索引支持前缀/contains 匹配，但非分词全文检索 `官方文档`。\n- 生产全文场景普遍外挂 ES/Solr，数据双写一致性自负 `社区共识`。"},
    "en": {"v": "Partial", "p": "SASI is not tokenized; ES common",
           "b": "- SASI secondary indexes do prefix/contains matching, not tokenized full-text `(official docs)`.\n- Production full-text usually offloads to ES/Solr; dual-write consistency is on you `(community consensus)`."}},
  "sp_proc": {
    "zh": {"v": "无", "p": "查证为无存储过程/触发器",
           "b": "- CQL 无存储过程、触发器、过程语言（查证为无）`官方文档`。\n- 逻辑只能放在应用层或 Spark/DSE Analytics 侧 `社区共识`。"},
    "en": {"v": "Not supported", "p": "Verified: no procedures/triggers",
           "b": "- No stored procedures, triggers, or procedural language in CQL (verified absent) `(official docs)`.\n- Logic lives in the app layer or Spark/DSE Analytics side `(community consensus)`."}},
  "constraints": {
    "zh": {"v": "无", "p": "无外键/CHECK；应用层保证",
           "b": "- 无外键、CHECK、唯一约束（轻量事务仅条件写入）`官方文档`。\n- 完整性靠应用层与反范式数据建模保证 `社区共识`。"},
    "en": {"v": "Not supported", "p": "No FK/CHECK; app-enforced",
           "b": "- No FK, CHECK, or unique constraints (LWT is conditional write only) `(official docs)`.\n- Integrity via app layer and denormalized modeling `(community consensus)`."}},
  "analytical_sql": {
    "zh": {"v": "无", "p": "CQL 无窗口函数/CTE",
           "b": "- CQL 无窗口函数、CTE、JOIN（查证为无）`官方文档`。\n- 分析靠 Spark 连接器或 DSE Analytics `社区共识`。"},
    "en": {"v": "Not supported", "p": "No windows/CTEs in CQL",
           "b": "- No window functions, CTEs, or JOINs in CQL (verified absent) `(official docs)`.\n- Analytics via Spark connector or DSE Analytics `(community consensus)`."}},
  "matview": {
    "zh": {"v": "部分支持", "p": "物化视图限制多，运维负担重",
           "b": "- 支持物化视图，但基表写入放大、修复运维负担重，限制多 `官方文档`。\n- 社区普遍建议用应用层双写宽表替代 `社区共识`。"},
    "en": {"v": "Partial", "p": "MVs with many limits",
           "b": "- Materialized views exist but amplify writes and burden repairs, with many limits `(official docs)`.\n- Community often prefers app-level dual-written wide tables `(community consensus)`."}},
}

# ---------------- clickhouse ----------------
CONTENT3_C["clickhouse"] = {
  "json_semi": {
    "zh": {"v": "有", "p": "JSON/Object/Dynamic 类型强",
           "b": "- JSON/Object 类型 + JSONEachRow，Dynamic JSON 推断子列并可索引 `官方文档`。\n- 半结构化子列过多会导致 part 膨胀，生产需限制动态列数量 `社区实测`。"},
    "en": {"v": "Supported", "p": "Strong JSON/Object/Dynamic types",
           "b": "- JSON/Object types + JSONEachRow; Dynamic JSON infers subcolumns and indexes them `(official docs)`.\n- Too many dynamic subcolumns bloat parts; bound them in production `(community tested)`."}},
  "fulltext": {
    "zh": {"v": "部分支持", "p": "ngrambf/tokenbf 跳数索引",
           "b": "- ngrambf_v1/tokenbf_v1 跳数索引加速 LIKE/分词匹配 `官方文档`。\n- 无相关性排序、中文分词器等完整全文检索语义，重检索场景仍需 ES `社区共识`。"},
    "en": {"v": "Partial", "p": "Skip indexes; not a search engine",
           "b": "- ngrambf_v1/tokenbf_v1 skip indexes accelerate LIKE/token matching `(official docs)`.\n- No relevance ranking or CJK analyzers; heavy search still wants ES `(community consensus)`."}},
  "sp_proc": {
    "zh": {"v": "无", "p": "查证为无存储过程/触发器",
           "b": "- 无存储过程、触发器（查证为无）`官方文档`。\n- 逻辑放在 ETL/应用层，物化视图承担部分预计算 `社区共识`。"},
    "en": {"v": "Not supported", "p": "Verified: no procedures/triggers",
           "b": "- No stored procedures or triggers (verified absent) `(official docs)`.\n- Logic lives in ETL/app; materialized views cover some precomputation `(community consensus)`."}},
  "constraints": {
    "zh": {"v": "无", "p": "MergeTree 无外键/CHECK",
           "b": "- 无外键、CHECK、唯一约束（查证为无）`官方文档`。\n- 数据质量靠写入链路（Kafka/ETL）保证 `社区共识`。"},
    "en": {"v": "Not supported", "p": "No FK/CHECK on MergeTree",
           "b": "- No FK, CHECK, or unique constraints (verified absent) `(official docs)`.\n- Data quality enforced in the ingestion path (Kafka/ETL) `(community consensus)`."}},
  "analytical_sql": {
    "zh": {"v": "有", "p": "窗口/GROUPING SETS 完备",
           "b": "- 窗口函数、GROUPING SETS/CUBE/ROLLUP、数组/元组函数完备 `官方文档`。\n- 方言与标准 SQL 有差异，迁移时函数需适配 `社区共识`。"},
    "en": {"v": "Supported", "p": "Strong windows/GROUPING SETS",
           "b": "- Strong window functions, GROUPING SETS/CUBE/ROLLUP, array/tuple functions `(official docs)`.\n- Dialect differs from standard SQL; functions need porting `(community consensus)`."}},
  "matview": {
    "zh": {"v": "有", "p": "触发器式物化视图，语义特殊",
           "b": "- 物化视图为增量触发器语义（TO 内表），聚合预计算强大 `官方文档`。\n- 语义与传统 MV 差异大（无查询自动改写、写入即触发），误用易出错 `社区实测`。"},
    "en": {"v": "Supported", "p": "Trigger-style MVs, special semantics",
           "b": "- Trigger-style incremental MVs (TO inner table), strong for pre-aggregation `(official docs)`.\n- Semantics differ from classic MVs (no auto rewrite); misuse is error-prone `(community tested)`."}},
}

# ---------------- cockroachdb ----------------
CONTENT3_C["cockroachdb"] = {
  "json_semi": {
    "zh": {"v": "有", "p": "JSONB 类型，PG 算子兼容",
           "b": "- JSONB 类型，->/->>/@> 等 PG 兼容算子 `官方文档`。\n- GIN 索引支持弱于 PG，复杂 jsonb 查询性能注意 `待验证`。"},
    "en": {"v": "Supported", "p": "JSONB with PG-compatible operators",
           "b": "- JSONB type with PG-compatible ->/->>/@> operators `(official docs)`.\n- GIN indexing weaker than PG; watch complex jsonb query performance `(to be verified)`."}},
  "fulltext": {
    "zh": {"v": "无", "p": "查证为无，生产外挂检索",
           "b": "- 无全文索引（查证为无）`官方文档`。\n- 全文场景需外挂 ES/Typesense `社区共识`。"},
    "en": {"v": "Not supported", "p": "Verified absent; use external search",
           "b": "- No full-text indexes (verified absent) `(official docs)`.\n- Full-text needs external ES/Typesense `(community consensus)`."}},
  "sp_proc": {
    "zh": {"v": "无", "p": "查证为无存储过程/触发器",
           "b": "- 无存储过程、触发器（查证为无）`官方文档`。\n- 逻辑放应用层；去 O 迁移时 PL/SQL 需整体重写 `社区共识`。"},
    "en": {"v": "Not supported", "p": "Verified: no stored procedures",
           "b": "- No stored procedures or triggers (verified absent) `(official docs)`.\n- Logic in app layer; Oracle PL/SQL must be fully rewritten `(community consensus)`."}},
  "constraints": {
    "zh": {"v": "有", "p": "FK/CHECK 有，分布式下慎用",
           "b": "- 支持外键、CHECK、唯一约束 `官方文档`。\n- 跨 range 外键检查有分布式代价，高吞吐写入建议应用层保证 `官方文档`。"},
    "en": {"v": "Supported", "p": "FK/CHECK; careful when distributed",
           "b": "- FK, CHECK, unique constraints supported `(official docs)`.\n- Cross-range FK checks cost; high-throughput writes better enforced in app `(official docs)`."}},
  "analytical_sql": {
    "zh": {"v": "有", "p": "窗口/CTE 有；递归有限",
           "b": "- 窗口函数、CTE 可用，PG 兼容度高 `官方文档`。\n- 递归 CTE 与复杂分析性能弱于专用 OLAP `社区共识`。"},
    "en": {"v": "Supported", "p": "Windows/CTEs; limited recursion",
           "b": "- Window functions and CTEs with high PG compatibility `(official docs)`.\n- Recursive CTEs and heavy analytics lag dedicated OLAP `(community consensus)`."}},
  "matview": {
    "zh": {"v": "无", "p": "查证为无物化视图能力",
           "b": "- 无物化视图（查证为无）`官方文档`。\n- 预聚合靠应用层或下游 OLAP `社区共识`。"},
    "en": {"v": "Not supported", "p": "Verified: no materialized views",
           "b": "- No materialized views (verified absent) `(official docs)`.\n- Pre-aggregation via app layer or downstream OLAP `(community consensus)`."}},
}

# ---------------- databricks ----------------
CONTENT3_C["databricks"] = {
  "json_semi": {
    "zh": {"v": "有", "p": "VARIANT 类型，schema-on-read",
           "b": "- VARIANT 半结构化类型（Photon），schema-on-read，自动演进 `官方文档`。\n- VARIANT 查询性能弱于规整列，热点路径建议规整化 `官方文档`。"},
    "en": {"v": "Supported", "p": "VARIANT type, schema-on-read",
           "b": "- VARIANT semi-structured type (Photon) with schema-on-read and auto-evolution `(official docs)`.\n- VARIANT queries slower than regular columns; normalize hot paths `(official docs)`."}},
  "fulltext": {
    "zh": {"v": "部分支持", "p": "无原生全文索引；AI 检索另计",
           "b": "- Databricks SQL 无传统全文索引 `官方文档`。\n- 文本检索靠向量搜索/AI 检索，关键词精确检索弱 `社区共识`。"},
    "en": {"v": "Partial", "p": "No native FTS; AI search separate",
           "b": "- No classic full-text indexes in Databricks SQL `(official docs)`.\n- Text search via vector/AI retrieval; keyword-exact search is weak `(community consensus)`."}},
  "sp_proc": {
    "zh": {"v": "部分支持", "p": "SQL 脚本/工作流；无传统 SP",
           "b": "- 无传统存储过程；靠 Notebooks/Workflows 编排，DBSQL 有脚本能力 `官方文档`。\n- 去 O 迁移时 PL/SQL 逻辑需重写为作业流 `社区共识`。"},
    "en": {"v": "Partial", "p": "Scripts/workflows; no classic SPs",
           "b": "- No classic stored procedures; orchestration via Notebooks/Workflows `(official docs)`.\n- Oracle PL/SQL logic must be rewritten as job flows `(community consensus)`."}},
  "constraints": {
    "zh": {"v": "部分支持", "p": "Delta 约束有限；外键信息性",
           "b": "- Delta 支持 NOT NULL/CHECK（有限），主键/外键为信息性不强制 `官方文档`。\n- 完整性靠写入链路（DLT expectations）保证 `官方文档`。"},
    "en": {"v": "Partial", "p": "Limited Delta constraints",
           "b": "- Delta has limited NOT NULL/CHECK; PK/FK informational, not enforced `(official docs)`.\n- Integrity via ingestion (DLT expectations) `(official docs)`."}},
  "analytical_sql": {
    "zh": {"v": "有", "p": "Spark SQL 窗口/CTE 强",
           "b": "- Spark SQL 窗口函数、CTE 完备，分析函数丰富 `官方文档`。\n- 递归 CTE 支持有限，复杂递归改写为迭代作业 `社区共识`。"},
    "en": {"v": "Supported", "p": "Strong Spark SQL windows/CTEs",
           "b": "- Strong Spark SQL window functions and CTEs `(official docs)`.\n- Recursive CTEs limited; rewrite complex recursion as iterative jobs `(community consensus)`."}},
  "matview": {
    "zh": {"v": "有", "p": "物化视图+DLT，增量自动刷新",
           "b": "- Databricks SQL 物化视图与 DLT 管道，增量刷新、查询自动改写 `官方文档`。\n- 刷新按计算资源计费，频繁刷新小表注意成本 `厂商口径`。"},
    "en": {"v": "Supported", "p": "MVs + DLT, incremental refresh",
           "b": "- SQL materialized views and DLT pipelines with incremental refresh and auto rewrite `(official docs)`.\n- Refresh billed on compute; watch cost on frequently refreshed small tables `(vendor claim)`."}},
}

# ---------------- doris ----------------
CONTENT3_C["doris"] = {
  "json_semi": {
    "zh": {"v": "有", "p": "JSONB/Variant+倒排索引",
           "b": "- JSON/JSONB 类型，2.x Variant 半结构化，倒排索引加速 `官方文档`。\n- Variant 动态列过多膨胀 tablet，生产需设限 `社区实测`。"},
    "en": {"v": "Supported", "p": "JSONB/Variant + inverted index",
           "b": "- JSON/JSONB types, 2.x Variant semi-structured, inverted-index acceleration `(official docs)`.\n- Too many Variant dynamic columns bloat tablets; cap them `(community tested)`."}},
  "fulltext": {
    "zh": {"v": "有", "p": "倒排索引全文检索，中文 ngram",
           "b": "- 倒排索引支持全文检索，中文 ngram 分词 `官方文档`。\n- 相关性排序能力弱于 ES，MATCH 语义简单 `社区共识`。"},
    "en": {"v": "Supported", "p": "Inverted-index FTS, CJK ngram",
           "b": "- Inverted index full-text with Chinese ngram tokenization `(official docs)`.\n- Relevance ranking weaker than ES; simple MATCH semantics `(community consensus)`."}},
  "sp_proc": {
    "zh": {"v": "无", "p": "查证为无存储过程/触发器",
           "b": "- 无存储过程、触发器（查证为无）`官方文档`。\n- 逻辑在 ETL/应用层 `社区共识`。"},
    "en": {"v": "Not supported", "p": "Verified: no procedures/triggers",
           "b": "- No stored procedures or triggers (verified absent) `(official docs)`.\n- Logic in ETL/app layer `(community consensus)`."}},
  "constraints": {
    "zh": {"v": "无", "p": "OLAP 无外键/CHECK",
           "b": "- 无外键、CHECK（查证为无）`官方文档`。\n- 数据质量靠 Stream Load/Routine Load 前置校验 `社区共识`。"},
    "en": {"v": "Not supported", "p": "No FK/CHECK in OLAP",
           "b": "- No FK or CHECK (verified absent) `(official docs)`.\n- Quality enforced before Stream/Routine Load `(community consensus)`."}},
  "analytical_sql": {
    "zh": {"v": "有", "p": "窗口/GROUPING SETS 完备",
           "b": "- 窗口函数、GROUPING SETS/CUBE/ROLLUP 完备 `官方文档`。\n- 高基数精确去重等场景注意性能 `社区实测`。"},
    "en": {"v": "Supported", "p": "Complete windows/GROUPING SETS",
           "b": "- Complete window functions, GROUPING SETS/CUBE/ROLLUP `(official docs)`.\n- Watch performance on high-cardinality exact distinct counts `(community tested)`."}},
  "matview": {
    "zh": {"v": "有", "p": "同步/异步物化视图，自动改写",
           "b": "- 同步/异步物化视图，查询自动透明改写 `官方文档`。\n- 同步物化视图放大写入，宽表多 MV 注意导入性能 `社区实测`。"},
    "en": {"v": "Supported", "p": "Sync/async MVs, auto rewrite",
           "b": "- Sync/async materialized views with transparent query rewrite `(official docs)`.\n- Sync MVs amplify writes; many MVs on wide tables hurt load speed `(community tested)`."}},
}

# ---------------- duckdb ----------------
CONTENT3_C["duckdb"] = {
  "json_semi": {
    "zh": {"v": "有", "p": "JSON 扩展，自动推断",
           "b": "- JSON 扩展，JSON 类型，->> 提取，自动 schema 推断 `官方文档`。\n- 嵌入式分析定位，超大半结构化文件注意内存 `社区共识`。"},
    "en": {"v": "Supported", "p": "JSON extension, auto inference",
           "b": "- JSON extension with JSON type, ->> extraction, auto schema inference `(official docs)`.\n- Embedded analytics; watch memory on huge semi-structured files `(community consensus)`."}},
  "fulltext": {
    "zh": {"v": "部分支持", "p": "FTS 扩展尚实验性",
           "b": "- 官方 FTS 扩展提供全文检索，尚实验性 `官方文档`。\n- 生产关键词检索多靠 LIKE/正则或前置处理 `社区共识`。"},
    "en": {"v": "Partial", "p": "Experimental FTS extension",
           "b": "- Official FTS extension offers full-text, still experimental `(official docs)`.\n- Production keyword search often LIKE/regex or preprocessing `(community consensus)`."}},
  "sp_proc": {
    "zh": {"v": "无", "p": "查证为无存储过程/触发器",
           "b": "- 无存储过程、触发器（查证为无）`官方文档`。\n- 逻辑在宿主语言（Python/R）中 `社区共识`。"},
    "en": {"v": "Not supported", "p": "Verified: no procedures/triggers",
           "b": "- No stored procedures or triggers (verified absent) `(official docs)`.\n- Logic in host language (Python/R) `(community consensus)`."}},
  "constraints": {
    "zh": {"v": "有", "p": "单机主键/外键/CHECK 完整",
           "b": "- 主键、外键、CHECK、唯一约束完整（单机）`官方文档`。\n- 分析场景常关闭约束以提速，约束主要起语义作用 `社区共识`。"},
    "en": {"v": "Supported", "p": "Full single-node constraints",
           "b": "- Full PK, FK, CHECK, unique constraints (single-node) `(official docs)`.\n- Often disabled for speed in analytics; mainly semantic `(community consensus)`."}},
  "analytical_sql": {
    "zh": {"v": "有", "p": "分析 SQL 强项，窗口完备",
           "b": "- 窗口函数、CTE、PIVOT 等分析 SQL 为强项 `官方文档`。\n- 单机内存/磁盘上限是天花板 `社区共识`。"},
    "en": {"v": "Supported", "p": "Analytical SQL is its strength",
           "b": "- Window functions, CTEs, PIVOT — analytical SQL is its strength `(official docs)`.\n- Single-node memory/disk is the ceiling `(community consensus)`."}},
  "matview": {
    "zh": {"v": "无", "p": "查证为无；CTAS 模拟",
           "b": "- 无物化视图（查证为无）`官方文档`。\n- 用 CREATE TABLE AS + 定时重建模拟 `社区共识`。"},
    "en": {"v": "Not supported", "p": "Verified absent; CTAS instead",
           "b": "- No materialized views (verified absent) `(official docs)`.\n- Simulate with CREATE TABLE AS + scheduled rebuilds `(community consensus)`."}},
}

# ---------------- dynamodb ----------------
CONTENT3_C["dynamodb"] = {
  "json_semi": {
    "zh": {"v": "有", "p": "文档模型原生，Map/List 嵌套",
           "b": "- Map/List 嵌套文档原生，DynamoDB JSON 与 SDK 互转 `官方文档`。\n- 单 item 400KB 上限，深嵌套文档注意条目大小 `官方文档`。"},
    "en": {"v": "Supported", "p": "Native nested Map/List documents",
           "b": "- Native nested Map/List documents; DynamoDB JSON interop with SDKs `(official docs)`.\n- 400KB per-item cap; watch size on deeply nested docs `(official docs)`."}},
  "fulltext": {
    "zh": {"v": "无", "p": "查证为无；外挂 OpenSearch",
           "b": "- 无全文检索（查证为无）`官方文档`。\n- 标准方案 DynamoDB Streams + OpenSearch，延迟与成本自负 `官方文档`。"},
    "en": {"v": "Not supported", "p": "Verified absent; use OpenSearch",
           "b": "- No full-text search (verified absent) `(official docs)`.\n- Standard: DynamoDB Streams + OpenSearch; latency and cost on you `(official docs)`."}},
  "sp_proc": {
    "zh": {"v": "不适用", "p": "KV 无过程语言概念",
           "b": "- 无存储过程/触发器概念（不适用）`官方文档`。\n- 流处理靠 Streams + Lambda `官方文档`。"},
    "en": {"v": "N/A", "p": "No procedural concept in KV",
           "b": "- No stored-procedure/trigger concept (N/A) `(official docs)`.\n- Stream processing via Streams + Lambda `(official docs)`."}},
  "constraints": {
    "zh": {"v": "无", "p": "无外键/CHECK；条件写入",
           "b": "- 无外键、CHECK（查证为无），条件写入做乐观锁 `官方文档`。\n- 完整性应用层保证 `社区共识`。"},
    "en": {"v": "Not supported", "p": "No FK/CHECK; conditional writes",
           "b": "- No FK or CHECK (verified absent); conditional writes for optimistic locking `(official docs)`.\n- Integrity in app layer `(community consensus)`."}},
  "analytical_sql": {
    "zh": {"v": "不适用", "p": "PartiQL 有限；分析靠导出",
           "b": "- PartiQL 查询能力有限，无窗口函数（不适用分析 SQL）`官方文档`。\n- 分析靠导出 S3 + Athena/EMR `官方文档`。"},
    "en": {"v": "N/A", "p": "Limited PartiQL; export for analytics",
           "b": "- Limited PartiQL, no window functions (N/A for analytical SQL) `(official docs)`.\n- Analytics via export to S3 + Athena/EMR `(official docs)`."}},
  "matview": {
    "zh": {"v": "不适用", "p": "KV 无物化视图概念",
           "b": "- 无物化视图概念（不适用）`官方文档`。\n- 预聚合靠 Streams 物化到另一张表 `社区共识`。"},
    "en": {"v": "N/A", "p": "No MV concept in KV",
           "b": "- No materialized-view concept (N/A) `(official docs)`.\n- Pre-aggregate via Streams into another table `(community consensus)`."}},
}

# ---------------- edb ----------------
CONTENT3_C["edb"] = {
  "json_semi": {
    "zh": {"v": "有", "p": "PG jsonb 完整继承",
           "b": "- jsonb、GIN、jsonpath 完整继承 PG `官方文档`。\n- Oracle 兼容层对 JSON 语义以 PG 为准 `社区共识`。"},
    "en": {"v": "Supported", "p": "Full PG jsonb inheritance",
           "b": "- Full PG jsonb, GIN, jsonpath inheritance `(official docs)`.\n- JSON semantics follow PG even in Oracle-compat mode `(community consensus)`."}},
  "fulltext": {
    "zh": {"v": "有", "p": "tsvector 完整；中文需插件",
           "b": "- tsvector/tsquery 全文检索完整 `官方文档`。\n- 中文分词需第三方插件 `社区共识`。"},
    "en": {"v": "Supported", "p": "Full tsvector; CJK needs plugins",
           "b": "- Full tsvector/tsquery search `(official docs)`.\n- Chinese tokenization needs third-party plugins `(community consensus)`."}},
  "sp_proc": {
    "zh": {"v": "有", "p": "EPAS PL/SQL 高兼容，去 O 利器",
           "b": "- EPAS 兼容 Oracle PL/SQL（包、异常、自治事务），去 O 改写成本低是其卖点 `官方文档`。\n- 兼容非 100%，复杂包仍需逐个验证 `社区实测`。"},
    "en": {"v": "Supported", "p": "EPAS PL/SQL compatible",
           "b": "- EPAS Oracle PL/SQL compatible (packages, exceptions, autonomous txn); low rewrite cost is its pitch `(official docs)`.\n- Compatibility is not 100%; complex packages still need case-by-case validation `(community tested)`."}},
  "constraints": {
    "zh": {"v": "有", "p": "PG 约束完整+Oracle 兼容",
           "b": "- 外键、CHECK、deferrable 等 PG 约束完整，Oracle 语法兼容 `官方文档`。\n- 大表加约束同样注意锁表 `社区共识`。"},
    "en": {"v": "Supported", "p": "Full PG constraints + Oracle compat",
           "b": "- Full PG constraints (FK, CHECK, deferrable) with Oracle syntax compat `(official docs)`.\n- Same table-lock caution when adding constraints on huge tables `(community consensus)`."}},
  "analytical_sql": {
    "zh": {"v": "有", "p": "PG 分析 SQL 完整",
           "b": "- 窗口函数、CTE、GROUPING SETS 完整 `官方文档`。\n- 复杂分析优化器成熟 `社区共识`。"},
    "en": {"v": "Supported", "p": "Complete PG analytical SQL",
           "b": "- Complete window functions, CTEs, GROUPING SETS `(official docs)`.\n- Mature optimizer for complex analytics `(community consensus)`."}},
  "matview": {
    "zh": {"v": "有", "p": "PG 物化视图手动刷新",
           "b": "- 物化视图手动 REFRESH（含 CONCURRENTLY）`官方文档`。\n- 无自动增量刷新 `社区共识`。"},
    "en": {"v": "Supported", "p": "Manual-refresh PG MVs",
           "b": "- Manual-REFRESH materialized views (incl. CONCURRENTLY) `(official docs)`.\n- No automatic incremental refresh `(community consensus)`."}},
}

# ---------------- etcd ----------------
CONTENT3_C["etcd"] = {
  "json_semi": {
    "zh": {"v": "不适用", "p": "KV 字节值，无 JSON 语义",
           "b": "- value 为不透明字节，etcd 不解析 JSON（不适用）`官方文档`。\n- 如需 JSON 语义在客户端序列化/反序列化 `社区共识`。"},
    "en": {"v": "N/A", "p": "Byte values, no JSON semantics",
           "b": "- Values are opaque bytes; etcd does not parse JSON (N/A) `(official docs)`.\n- Serialize/deserialize JSON client-side if needed `(community consensus)`."}},
  "fulltext": {
    "zh": {"v": "不适用", "p": "KV 无全文检索概念",
           "b": "- 无全文检索概念（不适用）`官方文档`。\n- 键前缀查询（prefix/range）是其检索方式 `官方文档`。"},
    "en": {"v": "N/A", "p": "No full-text concept in KV",
           "b": "- No full-text concept (N/A) `(official docs)`.\n- Key prefix/range queries are its retrieval model `(official docs)`."}},
  "sp_proc": {
    "zh": {"v": "不适用", "p": "KV 无过程语言概念",
           "b": "- 无存储过程/触发器概念（不适用）`官方文档`。\n- 事务为多 key 原子 compare-and-swap，非过程逻辑 `官方文档`。"},
    "en": {"v": "N/A", "p": "No procedural concept in KV",
           "b": "- No stored-procedure/trigger concept (N/A) `(official docs)`.\n- Transactions are multi-key atomic compare-and-swap, not procedural logic `(official docs)`."}},
  "constraints": {
    "zh": {"v": "不适用", "p": "KV 无约束概念（不适用）",
           "b": "- 无外键/CHECK/唯一约束概念（不适用）`官方文档`。\n- 一致性靠 Raft 与租约（lease），非数据完整性约束 `官方文档`。"},
    "en": {"v": "N/A", "p": "No constraint concept in KV",
           "b": "- No FK/CHECK/unique concept (N/A) `(official docs)`.\n- Consistency via Raft and leases, not data-integrity constraints `(official docs)`."}},
  "analytical_sql": {
    "zh": {"v": "不适用", "p": "KV 无 SQL/分析概念",
           "b": "- 无 SQL，更无分析 SQL（不适用）`官方文档`。\n- 运维分析靠监控指标而非查询 `社区共识`。"},
    "en": {"v": "N/A", "p": "No SQL/analytics in KV",
           "b": "- No SQL, let alone analytical SQL (N/A) `(official docs)`.\n- Operational insight via metrics, not queries `(community consensus)`."}},
  "matview": {
    "zh": {"v": "不适用", "p": "KV 无物化视图概念",
           "b": "- 无物化视图概念（不适用）`官方文档`。\n- 缓存/配置场景不需要预聚合 `社区共识`。"},
    "en": {"v": "N/A", "p": "No MV concept in KV",
           "b": "- No materialized-view concept (N/A) `(official docs)`.\n- Cache/config use cases need no pre-aggregation `(community consensus)`."}},
}

# ---------------- mariadb ----------------
CONTENT3_C["mariadb"] = {
  "json_semi": {
    "zh": {"v": "有", "p": "JSON 为 LONGTEXT 别名，函数兼容",
           "b": "- JSON 为 LONGTEXT 别名（非二进制），JSON 函数与 MySQL 兼容 `官方文档`。\n- 无原生二进制存储与 JSON 路径索引，虚拟列可部分弥补 `社区共识`。"},
    "en": {"v": "Supported", "p": "JSON as LONGTEXT alias",
           "b": "- JSON is a LONGTEXT alias (not binary); functions MySQL-compatible `(official docs)`.\n- No native binary storage or JSON path indexes; virtual columns partly help `(community consensus)`."}},
  "fulltext": {
    "zh": {"v": "有", "p": "FULLTEXT+Mroonga 中文分词",
           "b": "- FULLTEXT 索引，Mroonga 引擎提供中文分词 `官方文档`。\n- Mroonga 为外部引擎，运维与主从复制需额外注意 `社区实测`。"},
    "en": {"v": "Supported", "p": "FULLTEXT + Mroonga CJK",
           "b": "- FULLTEXT indexes; Mroonga engine for Chinese tokenization `(official docs)`.\n- Mroonga is external; mind ops and replication `(community tested)`."}},
  "sp_proc": {
    "zh": {"v": "有", "p": "SP/触发器/事件；Oracle 模式",
           "b": "- 存储过程、触发器、事件完整，Oracle 模式兼容 PL/SQL 子集 `官方文档`。\n- Oracle 模式兼容有限，复杂包改写仍重 `社区共识`。"},
    "en": {"v": "Supported", "p": "SPs/triggers/events; Oracle mode",
           "b": "- Full procedures, triggers, events; Oracle mode covers a PL/SQL subset `(official docs)`.\n- Oracle-mode compatibility is limited; complex packages still heavy rewrites `(community consensus)`."}},
  "constraints": {
    "zh": {"v": "有", "p": "FK/CHECK 完整（10.2+）",
           "b": "- InnoDB 外键，10.2+ CHECK 约束 `官方文档`。\n- 外键级联大批量操作同样注意锁与写放大 `社区实测`。"},
    "en": {"v": "Supported", "p": "Full FK/CHECK (10.2+)",
           "b": "- InnoDB FKs, CHECK constraints (10.2+) `(official docs)`.\n- Same lock and write-amplification caution on FK cascades `(community tested)`."}},
  "analytical_sql": {
    "zh": {"v": "有", "p": "窗口/CTE（10.2+）",
           "b": "- 10.2+ 窗口函数、CTE `官方文档`。\n- 分析函数完备度弱于 PG/Oracle `社区共识`。"},
    "en": {"v": "Supported", "p": "Windows/CTEs (10.2+)",
           "b": "- Window functions, CTEs (10.2+) `(official docs)`.\n- Less complete than PG/Oracle analytics `(community consensus)`."}},
  "matview": {
    "zh": {"v": "无", "p": "查证为无原生；Flexviews 非内置",
           "b": "- 无原生（查证为无），Flexviews 等外部方案非内置 `社区共识`。\n- 汇总表+事件调度模拟 `社区共识`。"},
    "en": {"v": "Not supported", "p": "Verified absent; Flexviews external",
           "b": "- No native MVs (verified absent); Flexviews is external `(community consensus)`.\n- Simulate with summary tables + event scheduler `(community consensus)`."}},
}

# ---------------- milvus ----------------
CONTENT3_C["milvus"] = {
  "json_semi": {
    "zh": {"v": "部分支持", "p": "标量 JSON 字段；非核心",
           "b": "- 2.x 支持 JSON 标量字段，可做元数据过滤 `官方文档`。\n- 非文档查询主力，复杂嵌套查询弱 `社区共识`。"},
    "en": {"v": "Partial", "p": "JSON scalar fields; not core",
           "b": "- 2.x JSON scalar fields for metadata filtering `(official docs)`.\n- Not a document engine; nested queries weak `(community consensus)`."}},
  "fulltext": {
    "zh": {"v": "部分支持", "p": "Sparse 向量+BM25；非关键词检索引擎",
           "b": "- 2.4+ sparse 向量与 BM25 混合检索 `官方文档`。\n- 非传统全文检索引擎，中文分词依赖分词器接入 `待验证`。"},
    "en": {"v": "Partial", "p": "Sparse + BM25; not classic FTS",
           "b": "- 2.4+ sparse vectors with BM25 hybrid search `(official docs)`.\n- Not a classic full-text engine; CJK tokenization via plugged analyzers `(to be verified)`."}},
  "sp_proc": {
    "zh": {"v": "不适用", "p": "向量库无过程语言概念",
           "b": "- 无存储过程/触发器概念（不适用）`官方文档`。\n- 索引构建与检索逻辑在客户端/SDK `社区共识`。"},
    "en": {"v": "N/A", "p": "No procedural concept",
           "b": "- No stored-procedure/trigger concept (N/A) `(official docs)`.\n- Index build and query logic in client/SDK `(community consensus)`."}},
  "constraints": {
    "zh": {"v": "不适用", "p": "向量库无约束概念（不适用）",
           "b": "- 无外键/CHECK 概念（不适用）`官方文档`。\n- 主键为向量 id 去重，靠写入端保证 `社区共识`。"},
    "en": {"v": "N/A", "p": "No constraint concept",
           "b": "- No FK/CHECK concept (N/A) `(official docs)`.\n- Primary key dedups vector ids; enforced at write time `(community consensus)`."}},
  "analytical_sql": {
    "zh": {"v": "不适用", "p": "向量库无分析 SQL 概念",
           "b": "- 无 SQL/分析 SQL（不适用）`官方文档`。\n- 查询为向量相似度+标量过滤 `官方文档`。"},
    "en": {"v": "N/A", "p": "No analytical SQL concept",
           "b": "- No SQL/analytical SQL (N/A) `(official docs)`.\n- Queries are vector similarity + scalar filtering `(official docs)`."}},
  "matview": {
    "zh": {"v": "不适用", "p": "向量库无物化视图概念",
           "b": "- 无物化视图概念（不适用）`官方文档`。\n- 索引本身即预计算结构 `社区共识`。"},
    "en": {"v": "N/A", "p": "No MV concept",
           "b": "- No materialized-view concept (N/A) `(official docs)`.\n- Indexes themselves are the precomputed structure `(community consensus)`."}},
}

# ---------------- mongodb ----------------
CONTENT3_C["mongodb"] = {
  "json_semi": {
    "zh": {"v": "有", "p": "BSON 原生，文档模型本家",
           "b": "- BSON 文档原生，嵌套/数组一等公民 `官方文档`。\n- 16MB 文档上限，深嵌套注意 `官方文档`。"},
    "en": {"v": "Supported", "p": "Native BSON, document-native",
           "b": "- Native BSON documents; nesting/arrays first-class `(official docs)`.\n- 16MB document cap; watch deep nesting `(official docs)`."}},
  "fulltext": {
    "zh": {"v": "有", "p": "text 索引；中文分词弱",
           "b": "- text 索引多语言，中文按标点/空格切分效果弱 `官方文档`。\n- 生产中文检索多用 Atlas Search `社区共识`。"},
    "en": {"v": "Supported", "p": "Text indexes; weak CJK",
           "b": "- Multi-language text indexes; weak Chinese segmentation `(official docs)`.\n- Production Chinese search usually Atlas Search `(community consensus)`."}},
  "sp_proc": {
    "zh": {"v": "部分支持", "p": "无传统 SP；用 Trigger/Stream",
           "b": "- 无传统存储过程；Atlas Trigger + Change Stream 做事件驱动 `官方文档`。\n- 旧版 server-side JS 已弱化 `社区共识`。"},
    "en": {"v": "Partial", "p": "No classic SPs; Triggers/Streams",
           "b": "- No classic procedures; Atlas Triggers + Change Streams for events `(official docs)`.\n- Legacy server-side JS de-emphasized `(community consensus)`."}},
  "constraints": {
    "zh": {"v": "部分支持", "p": "无外键；schema validation 替代",
           "b": "- 无外键（查证为无）；schema validation（JSON Schema）做结构约束 `官方文档`。\n- 跨文档引用完整性应用层保证 `社区共识`。"},
    "en": {"v": "Partial", "p": "No FKs; schema validation instead",
           "b": "- No FKs (verified absent); schema validation (JSON Schema) for structure `(official docs)`.\n- Cross-document integrity in app layer `(community consensus)`."}},
  "analytical_sql": {
    "zh": {"v": "部分支持", "p": "聚合管道强；非 SQL",
           "b": "- 聚合管道表达力强，5.0+ $setWindowFields 支持窗口 `官方文档`。\n- 非 SQL，BI 需 Connector `社区共识`。"},
    "en": {"v": "Partial", "p": "Strong pipeline; not SQL",
           "b": "- Expressive aggregation pipeline; 5.0+ $setWindowFields windows `(official docs)`.\n- Not SQL; BI needs connectors `(community consensus)`."}},
  "matview": {
    "zh": {"v": "部分支持", "p": "On-Demand MV（$merge 模拟）",
           "b": "- 无原生 MV；On-Demand Materialized Views 用 $merge 聚合模拟 `官方文档`。\n- 刷新调度与一致性自建 `社区共识`。"},
    "en": {"v": "Partial", "p": "On-Demand MVs via $merge",
           "b": "- No native MVs; On-Demand MVs simulate via $merge `(official docs)`.\n- Scheduling and consistency DIY `(community consensus)`."}},
}

# ---------------- mysql ----------------
CONTENT3_C["mysql"] = {
  "json_semi": {
    "zh": {"v": "有", "p": "原生 JSON+虚拟列索引",
           "b": "- 原生二进制 JSON，->>/JSON_TABLE，虚拟生成列建索引 `官方文档`。\n- JSON 列无法直接建索引（需虚拟列），大 JSON 更新整列重写 `官方文档`。"},
    "en": {"v": "Supported", "p": "Native JSON + virtual-column indexes",
           "b": "- Native binary JSON, ->>/JSON_TABLE, indexes via virtual generated columns `(official docs)`.\n- No direct JSON indexes (need virtual columns); big JSON updates rewrite whole column `(official docs)`."}},
  "fulltext": {
    "zh": {"v": "有", "p": "FULLTEXT+ngram 中文分词",
           "b": "- FULLTEXT 索引，ngram parser 中文分词 `官方文档`。\n- 相关性算法简单，大规模检索弱于 ES `社区共识`。"},
    "en": {"v": "Supported", "p": "FULLTEXT + ngram CJK",
           "b": "- FULLTEXT with ngram parser for Chinese `(official docs)`.\n- Simple relevance; weaker than ES at scale `(community consensus)`."}},
  "sp_proc": {
    "zh": {"v": "有", "p": "SP/触发器有；语言弱，去 O 成本高",
           "b": "- 存储过程、触发器、事件调度完整 `官方文档`。\n- 无包、调试弱、异常处理简陋；去 O 迁移 PL/SQL 改写成本高 `社区共识`。"},
    "en": {"v": "Supported", "p": "SPs/triggers; weak language",
           "b": "- Full procedures, triggers, event scheduler `(official docs)`.\n- No packages, weak debugging; Oracle PL/SQL rewrites costly `(community consensus)`."}},
  "constraints": {
    "zh": {"v": "有", "p": "InnoDB FK/CHECK 完整",
           "b": "- InnoDB 外键、8.0.16+ CHECK 强制、唯一约束 `官方文档`。\n- 外键增加锁与级联写放大，高并发慎用 `社区实测`。"},
    "en": {"v": "Supported", "p": "Full InnoDB FK/CHECK",
           "b": "- InnoDB FKs, enforced CHECK (8.0.16+), unique constraints `(official docs)`.\n- FKs add locks and cascade write amplification; use carefully at scale `(community tested)`."}},
  "analytical_sql": {
    "zh": {"v": "有", "p": "8.0 窗口/CTE；分析非强项",
           "b": "- 8.0 窗口函数、CTE（含递归）`官方文档`。\n- 优化器对复杂分析弱，大关联/排序易慢 `社区共识`。"},
    "en": {"v": "Supported", "p": "8.0 windows/CTEs; not analytic",
           "b": "- 8.0 window functions, CTEs (incl. recursive) `(official docs)`.\n- Optimizer weak on complex analytics; big joins/sorts slow `(community consensus)`."}},
  "matview": {
    "zh": {"v": "无", "p": "查证为无；汇总表模拟",
           "b": "- 无物化视图（查证为无）`官方文档`。\n- 汇总表+触发器/定时任务模拟，一致性自负 `社区共识`。"},
    "en": {"v": "Not supported", "p": "Verified absent; summary tables",
           "b": "- No materialized views (verified absent) `(official docs)`.\n- Summary tables + triggers/jobs; consistency on you `(community consensus)`."}},
}

# ---------------- oceanbase ----------------
CONTENT3_C["oceanbase"] = {
  "json_semi": {
    "zh": {"v": "有", "p": "MySQL/Oracle 双模式 JSON",
           "b": "- MySQL 模式 JSON 类型兼容 MySQL；Oracle 模式 JSON 支持 `官方文档`。\n- JSON 索引能力弱于单机 MySQL/PG `待验证`。"},
    "en": {"v": "Supported", "p": "JSON in both MySQL/Oracle modes",
           "b": "- MySQL-mode JSON MySQL-compatible; Oracle-mode JSON supported `(official docs)`.\n- JSON indexing weaker than standalone MySQL/PG `(to be verified)`."}},
  "fulltext": {
    "zh": {"v": "部分支持", "p": "全文索引有限，细节待验证",
           "b": "- 企业版有全文索引，能力与限制需按版本确认 `厂商口径`。\n- 社区版全文能力弱，生产检索多外挂 `待验证`。"},
    "en": {"v": "Partial", "p": "Limited FTS; verify per version",
           "b": "- Enterprise has full-text; check limits per version `(vendor claim)`.\n- Community edition weak; production search often external `(to be verified)`."}},
  "sp_proc": {
    "zh": {"v": "有", "p": "Oracle 模式 PL/SQL 高兼容",
           "b": "- Oracle 模式 PL/SQL（包/触发器）高兼容，去 O 改写成本低是其主打 `官方文档`。\n- MySQL 模式 SP 兼容 MySQL；复杂包仍需验证 `社区实测`。"},
    "en": {"v": "Supported", "p": "Oracle-mode PL/SQL compatible",
           "b": "- Oracle-mode PL/SQL (packages/triggers) highly compatible; low rewrite cost is its pitch `(official docs)`.\n- MySQL-mode procedures MySQL-compatible; complex packages still need validation `(community tested)`."}},
  "constraints": {
    "zh": {"v": "有", "p": "双模式约束；分布式外键有代价",
           "b": "- 外键、CHECK、唯一约束双模式支持 `官方文档`。\n- 分布式下外键检查跨分区有代价，超大写入慎用 `官方文档`。"},
    "en": {"v": "Supported", "p": "Constraints both modes; FK costs",
           "b": "- FK, CHECK, unique in both modes `(official docs)`.\n- Distributed FK checks cross partitions; careful on huge writes `(official docs)`."}},
  "analytical_sql": {
    "zh": {"v": "有", "p": "Oracle 模式分析函数强",
           "b": "- Oracle 模式窗口函数、分析函数完备 `官方文档`。\n- MySQL 模式分析能力与 MySQL 对齐 `社区共识`。"},
    "en": {"v": "Supported", "p": "Strong analytics in Oracle mode",
           "b": "- Oracle-mode window/analytic functions complete `(official docs)`.\n- MySQL-mode analytics align with MySQL `(community consensus)`."}},
  "matview": {
    "zh": {"v": "部分支持", "p": "Oracle 模式 MV；MySQL 模式有限",
           "b": "- Oracle 模式支持物化视图 `官方文档`。\n- MySQL 模式物化视图能力有限，细节待验证 `待验证`。"},
    "en": {"v": "Partial", "p": "MVs in Oracle mode; limited else",
           "b": "- Oracle-mode materialized views `(official docs)`.\n- MySQL-mode MV support limited; details pending `(to be verified)`."}},
}

# ---------------- oracle ----------------
CONTENT3_C["oracle"] = {
  "json_semi": {
    "zh": {"v": "有", "p": "21c 原生二进制 JSON",
           "b": "- 21c+ 原生 JSON 数据类型（二进制），JSON 索引、JSON_TABLE `官方文档`。\n- 老版本 JSON 存 VARCHAR2/CLOB，函数式索引弥补 `社区共识`。"},
    "en": {"v": "Supported", "p": "Native binary JSON (21c+)",
           "b": "- 21c+ native binary JSON type, JSON indexes, JSON_TABLE `(official docs)`.\n- Older versions store JSON in VARCHAR2/CLOB with function-based indexes `(community consensus)`."}},
  "fulltext": {
    "zh": {"v": "有", "p": "Oracle Text 多语言含中文",
           "b": "- Oracle Text 全文检索，中文分词器（lexer）支持 `官方文档`。\n- 索引维护（同步/优化）运维负担重 `社区实测`。"},
    "en": {"v": "Supported", "p": "Oracle Text, multilingual",
           "b": "- Oracle Text with Chinese lexer support `(official docs)`.\n- Index maintenance (sync/optimize) is ops-heavy `(community tested)`."}},
  "sp_proc": {
    "zh": {"v": "有", "p": "PL/SQL 本家，包/调试完备",
           "b": "- PL/SQL 包、触发器、自治事务、DBMS 调试完备 `官方文档`。\n- 深度绑定 PL/SQL 是去 O 迁移的最大成本来源 `社区共识`。"},
    "en": {"v": "Supported", "p": "PL/SQL native, complete",
           "b": "- PL/SQL packages, triggers, autonomous transactions, DBMS debugging `(official docs)`.\n- Deep PL/SQL lock-in is the biggest Oracle-migration cost `(community consensus)`."}},
  "constraints": {
    "zh": {"v": "有", "p": "约束语义标杆，deferrable 完备",
           "b": "- 外键、CHECK、deferrable、NOVALIDATE 等语义最完备 `官方文档`。\n- 约束即文档，去 O 时注意目标库语义差异 `社区共识`。"},
    "en": {"v": "Supported", "p": "Constraint benchmark semantics",
           "b": "- Most complete constraint semantics: FK, CHECK, deferrable, NOVALIDATE `(official docs)`.\n- Constraints-as-documentation; mind target semantics when migrating `(community consensus)`."}},
  "analytical_sql": {
    "zh": {"v": "有", "p": "分析函数本家，MODEL 子句",
           "b": "- 窗口函数、分析函数、MODEL 子句，分析 SQL 标杆 `官方文档`。\n- 许可按功能包计费，OLAP 选件成本高 `社区共识`。"},
    "en": {"v": "Supported", "p": "Analytic functions benchmark",
           "b": "- Window/analytic functions, MODEL clause — the benchmark `(official docs)`.\n- Licensed per option pack; OLAP options costly `(community consensus)`."}},
  "matview": {
    "zh": {"v": "有", "p": "MV 本家：增量刷新+查询改写",
           "b": "- 物化视图日志增量刷新、查询自动改写，能力最完备 `官方文档`。\n- 刷新策略配错易致数据延迟或性能问题 `社区实测`。"},
    "en": {"v": "Supported", "p": "MVs: incremental + rewrite",
           "b": "- MV logs for incremental refresh, automatic query rewrite — most complete `(official docs)`.\n- Misconfigured refresh causes staleness or perf issues `(community tested)`."}},
}

# ---------------- polardb ----------------
CONTENT3_C["polardb"] = {
  "json_semi": {
    "zh": {"v": "有", "p": "MySQL/PG 版各自继承",
           "b": "- MySQL 版原生 JSON；PG 版 jsonb `官方文档`。\n- 能力与上游对齐，无额外增强 `社区共识`。"},
    "en": {"v": "Supported", "p": "Inherited per engine",
           "b": "- MySQL flavor native JSON; PG flavor jsonb `(official docs)`.\n- Aligned with upstream, no extra enhancements `(community consensus)`."}},
  "fulltext": {
    "zh": {"v": "有", "p": "FULLTEXT/tsvector 继承",
           "b": "- MySQL 版 FULLTEXT+ngram；PG 版 tsvector `官方文档`。\n- 大规模检索同样建议外挂 OpenSearch `社区共识`。"},
    "en": {"v": "Supported", "p": "Inherited FULLTEXT/tsvector",
           "b": "- MySQL flavor FULLTEXT+ngram; PG flavor tsvector `(official docs)`.\n- Large-scale search still wants OpenSearch `(community consensus)`."}},
  "sp_proc": {
    "zh": {"v": "有", "p": "SP/触发器继承；PG 版 plpgsql",
           "b": "- MySQL 版 SP/触发器/事件；PG 版 plpgsql 完整 `官方文档`。\n- 去 O 改写成本与上游一致 `社区共识`。"},
    "en": {"v": "Supported", "p": "Inherited SPs; plpgsql on PG",
           "b": "- MySQL flavor procedures/triggers/events; PG flavor full plpgsql `(official docs)`.\n- Oracle-migration rewrite cost same as upstream `(community consensus)`."}},
  "constraints": {
    "zh": {"v": "有", "p": "外键/CHECK 完整继承上游",
           "b": "- 外键、CHECK 等约束与上游一致 `官方文档`。\n- 云上大表加约束注意主从延迟与锁 `社区实测`。"},
    "en": {"v": "Supported", "p": "Fully inherited constraints",
           "b": "- FK, CHECK consistent with upstream `(official docs)`.\n- Mind replica lag and locks adding constraints on huge cloud tables `(community tested)`."}},
  "analytical_sql": {
    "zh": {"v": "有", "p": "分析 SQL 完整继承",
           "b": "- MySQL 版 8.0 窗口/CTE；PG 版分析 SQL 完整 `官方文档`。\n- HTAP 场景可搭配 PolarDB-X/IMCI 列存 `厂商口径`。"},
    "en": {"v": "Supported", "p": "Inherited analytical SQL",
           "b": "- MySQL flavor 8.0 windows/CTEs; PG flavor complete `(official docs)`.\n- HTAP via PolarDB-X/IMCI columnar `(vendor claim)`."}},
  "matview": {
    "zh": {"v": "部分支持", "p": "PG 版手动物化视图；MySQL 版无",
           "b": "- PG 版：物化视图手动 REFRESH `官方文档`。\n- MySQL 版：无，汇总表模拟 `社区共识`。"},
    "en": {"v": "Partial", "p": "Manual MVs on PG; none on MySQL",
           "b": "- PG flavor: manual-REFRESH materialized views `(official docs)`.\n- MySQL flavor: none; summary tables instead `(community consensus)`."}},
}

# ---------------- postgresql ----------------
CONTENT3_C["postgresql"] = {
  "json_semi": {
    "zh": {"v": "有", "p": "jsonb 本家，GIN/jsonpath",
           "b": "- jsonb 二进制、GIN（含 jsonb_path_ops）、SQL/JSON 路径语言 `官方文档`。\n- 大 jsonb 局部更新整行重写，写放大注意 `社区共识`。"},
    "en": {"v": "Supported", "p": "jsonb native, GIN/jsonpath",
           "b": "- Native jsonb, GIN (incl. jsonb_path_ops), SQL/JSON path `(official docs)`.\n- Partial updates rewrite whole row; write amplification `(community consensus)`."}},
  "fulltext": {
    "zh": {"v": "有", "p": "tsvector 本家；中文需插件",
           "b": "- tsvector/tsquery/GIN，排名高亮完备 `官方文档`。\n- 中文分词需 zhparser 等插件 `社区共识`。"},
    "en": {"v": "Supported", "p": "tsvector native; CJK via plugins",
           "b": "- tsvector/tsquery/GIN with ranking and highlighting `(official docs)`.\n- Chinese needs zhparser-class plugins `(community consensus)`."}},
  "sp_proc": {
    "zh": {"v": "有", "p": "plpgsql 成熟，多过程语言",
           "b": "- plpgsql 异常处理、调试成熟，plpython/plperl 等多语言 `官方文档`。\n- 去 O 迁移：包/自治事务需改写，EDB/ora2pg 辅助 `社区共识`。"},
    "en": {"v": "Supported", "p": "Mature plpgsql, many languages",
           "b": "- Mature plpgsql with exceptions/debugging; plpython/plperl etc. `(official docs)`.\n- Oracle migration: packages/autonomous txn need rewrites; EDB/ora2pg help `(community consensus)`."}},
  "constraints": {
    "zh": {"v": "有", "p": "约束最完备：EXCLUDE/deferrable",
           "b": "- FK、CHECK、EXCLUDE、deferrable，语义最完备 `官方文档`。\n- 大表加带验证约束锁表是在线 DDL 话题 `社区共识`。"},
    "en": {"v": "Supported", "p": "Most complete: EXCLUDE/deferrable",
           "b": "- FK, CHECK, EXCLUDE, deferrable — most complete semantics `(official docs)`.\n- Validated constraints on huge tables lock; an online-DDL topic `(community consensus)`."}},
  "analytical_sql": {
    "zh": {"v": "有", "p": "分析 SQL 完备标杆",
           "b": "- 窗口函数、CTE（含递归）、GROUPING SETS 完备 `官方文档`。\n- 复杂分析优化器成熟 `社区共识`。"},
    "en": {"v": "Supported", "p": "Analytical SQL benchmark",
           "b": "- Window functions, CTEs (incl. recursive), GROUPING SETS `(official docs)`.\n- Mature optimizer for complex analytics `(community consensus)`."}},
  "matview": {
    "zh": {"v": "有", "p": "手动 REFRESH 为主",
           "b": "- 物化视图 REFRESH（含 CONCURRENTLY）手动 `官方文档`。\n- 无自动增量刷新/改写，pg_ivm 等扩展非官方 `社区共识`。"},
    "en": {"v": "Supported", "p": "Manual REFRESH mainly",
           "b": "- Manual REFRESH (incl. CONCURRENTLY) `(official docs)`.\n- No auto incremental refresh/rewrite; pg_ivm is third-party `(community consensus)`."}},
}

# ---------------- qdrant ----------------
CONTENT3_C["qdrant"] = {
  "json_semi": {
    "zh": {"v": "部分支持", "p": "payload JSON 过滤",
           "b": "- payload 为 JSON，可做标量过滤 `官方文档`。\n- 非文档查询引擎，嵌套查询弱 `社区共识`。"},
    "en": {"v": "Partial", "p": "JSON payload filtering",
           "b": "- JSON payloads for scalar filtering `(official docs)`.\n- Not a document engine; nested queries weak `(community consensus)`."}},
  "fulltext": {
    "zh": {"v": "不适用", "p": "向量检索；关键词非强项",
           "b": "- 关键词全文非其场景（不适用），文本靠向量/混合检索 `官方文档`。\n- full-text 索引类型主要用于 payload 精确/前缀匹配 `官方文档`。"},
    "en": {"v": "N/A", "p": "Vector search; not keyword FTS",
           "b": "- Keyword full-text N/A; text via vector/hybrid search `(official docs)`.\n- full-text index type is for exact/prefix payload matching `(official docs)`."}},
  "sp_proc": {
    "zh": {"v": "不适用", "p": "向量库无过程语言概念",
           "b": "- 无存储过程/触发器概念（不适用）`官方文档`。"},
    "en": {"v": "N/A", "p": "No procedural concept",
           "b": "- No stored-procedure/trigger concept (N/A) `(official docs)`."}},
  "constraints": {
    "zh": {"v": "不适用", "p": "向量库无约束概念（不适用）",
           "b": "- 无外键/CHECK 概念（不适用）`官方文档`。"},
    "en": {"v": "N/A", "p": "No constraint concept",
           "b": "- No FK/CHECK concept (N/A) `(official docs)`."}},
  "analytical_sql": {
    "zh": {"v": "不适用", "p": "向量库无分析 SQL 概念",
           "b": "- 无 SQL/分析 SQL（不适用）`官方文档`。"},
    "en": {"v": "N/A", "p": "No analytical SQL concept",
           "b": "- No SQL/analytical SQL (N/A) `(official docs)`."}},
  "matview": {
    "zh": {"v": "不适用", "p": "向量库无物化视图概念",
           "b": "- 无物化视图概念（不适用）`官方文档`。"},
    "en": {"v": "N/A", "p": "No MV concept",
           "b": "- No materialized-view concept (N/A) `(official docs)`."}},
}

# ---------------- redis-valkey ----------------
CONTENT3_C["redis-valkey"] = {
  "json_semi": {
    "zh": {"v": "部分支持", "p": "RedisJSON 模块；原生无",
           "b": "- RedisJSON（ReJSON）模块提供 JSON 类型与路径查询，Valkey 兼容 `官方文档`。\n- 模块非内核，云厂商支持度不一 `社区共识`。"},
    "en": {"v": "Partial", "p": "RedisJSON module; not native",
           "b": "- RedisJSON module for JSON types and path queries; Valkey-compatible `(official docs)`.\n- Module, not core; cloud support varies `(community consensus)`."}},
  "fulltext": {
    "zh": {"v": "有", "p": "RediSearch 模块；中文分词弱",
           "b": "- RediSearch 模块全文检索+聚合 `官方文档`。\n- 中文分词弱，内存占用高 `社区实测`。"},
    "en": {"v": "Supported", "p": "RediSearch module; weak CJK",
           "b": "- RediSearch module for full-text + aggregations `(official docs)`.\n- Weak Chinese tokenization; high memory `(community tested)`."}},
  "sp_proc": {
    "zh": {"v": "部分支持", "p": "Lua/Functions；无传统 SP",
           "b": "- Lua 脚本/Functions，无传统存储过程/触发器 `官方文档`。\n- 脚本长阻塞单线程，大 key 上禁用 `社区共识`。"},
    "en": {"v": "Partial", "p": "Lua/Functions; no classic SPs",
           "b": "- Lua scripts/Functions; no classic procedures/triggers `(official docs)`.\n- Long scripts block the single thread; avoid on big keys `(community consensus)`."}},
  "constraints": {
    "zh": {"v": "不适用", "p": "KV 无约束概念（不适用）",
           "b": "- 无外键/CHECK 概念（不适用）`官方文档`。"},
    "en": {"v": "N/A", "p": "No constraint concept in KV",
           "b": "- No FK/CHECK concept (N/A) `(official docs)`."}},
  "analytical_sql": {
    "zh": {"v": "不适用", "p": "RediSearch 聚合有限",
           "b": "- RediSearch 有限聚合，非分析 SQL（不适用）`官方文档`。"},
    "en": {"v": "N/A", "p": "Limited RediSearch aggregations",
           "b": "- Limited RediSearch aggregations; not analytical SQL (N/A) `(official docs)`."}},
  "matview": {
    "zh": {"v": "不适用", "p": "KV 无物化视图概念",
           "b": "- 无物化视图概念（不适用）`官方文档`。"},
    "en": {"v": "N/A", "p": "No MV concept in KV",
           "b": "- No materialized-view concept (N/A) `(official docs)`."}},
}

# ---------------- snowflake ----------------
CONTENT3_C["snowflake"] = {
  "json_semi": {
    "zh": {"v": "有", "p": "VARIANT 半结构化原生",
           "b": "- VARIANT/OBJECT/ARRAY 原生，schema-on-read，自动类型推断 `官方文档`。\n- 半结构化查询计费按扫描量，深层 FLATTEN 注意成本 `社区实测`。"},
    "en": {"v": "Supported", "p": "Native VARIANT semi-structured",
           "b": "- Native VARIANT/OBJECT/ARRAY, schema-on-read, auto inference `(official docs)`.\n- Billed on scanned bytes; deep FLATTEN costs `(community tested)`."}},
  "fulltext": {
    "zh": {"v": "部分支持", "p": "无传统全文索引；SEARCH 函数",
           "b": "- 无传统全文索引；SEARCH/文本函数 + Cortex Search（AI 检索另计）`官方文档`。\n- 关键词精确检索弱于 ES `社区共识`。"},
    "en": {"v": "Partial", "p": "No classic FTS; SEARCH funcs",
           "b": "- No classic full-text indexes; SEARCH functions + Cortex Search (separate AI service) `(official docs)`.\n- Keyword-exact search weaker than ES `(community consensus)`."}},
  "sp_proc": {
    "zh": {"v": "有", "p": "Scripting+多语言存储过程",
           "b": "- Snowflake Scripting（SQL 过程）+ JS/Python/Java 存储过程 `官方文档`。\n- 去 O 迁移 PL/SQL 需改写，语法差异大 `社区共识`。"},
    "en": {"v": "Supported", "p": "Scripting + multi-language SPs",
           "b": "- Snowflake Scripting + JS/Python/Java procedures `(official docs)`.\n- Oracle PL/SQL needs rewrites; syntax differs a lot `(community consensus)`."}},
  "constraints": {
    "zh": {"v": "部分支持", "p": "PK/FK/UNIQUE 信息性不强制",
           "b": "- 主键/外键/唯一为信息性约束，不强制执行 `官方文档`。\n- 靠 ETL 保证，误用会导致优化器误判 `社区实测`。"},
    "en": {"v": "Partial", "p": "Informational PK/FK/UNIQUE",
           "b": "- PK/FK/UNIQUE informational, not enforced `(official docs)`.\n- Enforced in ETL; wrong declarations mislead the optimizer `(community tested)`."}},
  "analytical_sql": {
    "zh": {"v": "有", "p": "分析 SQL 完备，MATCH_RECOGNIZE",
           "b": "- 窗口函数、CTE、递归、MATCH_RECOGNIZE 完备 `官方文档`。\n- 按计算计费，低效 SQL 直接变账单 `社区共识`。"},
    "en": {"v": "Supported", "p": "Complete analytics, MATCH_RECOGNIZE",
           "b": "- Complete windows, CTEs, recursion, MATCH_RECOGNIZE `(official docs)`.\n- Compute-billed; inefficient SQL becomes the bill `(community consensus)`."}},
  "matview": {
    "zh": {"v": "有", "p": "自动后台增量刷新+改写",
           "b": "- 物化视图后台自动增量刷新、查询自动改写 `官方文档`。\n- 刷新与存储计费，基表频繁更新成本高 `厂商口径`。"},
    "en": {"v": "Supported", "p": "Auto incremental refresh + rewrite",
           "b": "- Automatic background incremental refresh and query rewrite `(official docs)`.\n- Refresh + storage billed; costly on frequently updated base tables `(vendor claim)`."}},
}

# ---------------- spanner ----------------
CONTENT3_C["spanner"] = {
  "json_semi": {
    "zh": {"v": "有", "p": "JSON 类型；PG 方言 jsonb",
           "b": "- GoogleSQL JSON 类型，PG 接口 jsonb `官方文档`。\n- JSON 查询下推有限，复杂嵌套注意性能 `待验证`。"},
    "en": {"v": "Supported", "p": "JSON type; jsonb on PG dialect",
           "b": "- GoogleSQL JSON type; jsonb on PG interface `(official docs)`.\n- Limited JSON pushdown; watch nested-query perf `(to be verified)`."}},
  "fulltext": {
    "zh": {"v": "无", "p": "查证为无全文索引；外挂检索",
           "b": "- 无全文索引（查证为无）`官方文档`。\n- 全文场景外挂 Elasticsearch `社区共识`。"},
    "en": {"v": "Not supported", "p": "Verified absent; external search",
           "b": "- No full-text indexes (verified absent) `(official docs)`.\n- Full-text via external Elasticsearch `(community consensus)`."}},
  "sp_proc": {
    "zh": {"v": "无", "p": "查证为无存储过程/触发器",
           "b": "- 无存储过程、触发器（查证为无）`官方文档`。\n- 逻辑在应用层 `社区共识`。"},
    "en": {"v": "Not supported", "p": "Verified: no stored procedures",
           "b": "- No stored procedures or triggers (verified absent) `(official docs)`.\n- Logic in app layer `(community consensus)`."}},
  "constraints": {
    "zh": {"v": "有", "p": "FK/CHECK+交错表强制",
           "b": "- 外键、CHECK 强制，交错表（interleaved）物理共置 `官方文档`。\n- 跨 split 外键有延迟代价，建模建议共置 `官方文档`。"},
    "en": {"v": "Supported", "p": "Enforced FK/CHECK + interleaving",
           "b": "- Enforced FK and CHECK; interleaved tables co-locate `(official docs)`.\n- Cross-split FKs cost latency; model for co-location `(official docs)`."}},
  "analytical_sql": {
    "zh": {"v": "有", "p": "GoogleSQL 窗口函数",
           "b": "- GoogleSQL 窗口函数、CTE 可用 `官方文档`。\n- 非 OLAP 定位，重分析用 BigQuery `社区共识`。"},
    "en": {"v": "Supported", "p": "GoogleSQL window functions",
           "b": "- GoogleSQL window functions and CTEs `(official docs)`.\n- Not OLAP; heavy analytics belong in BigQuery `(community consensus)`."}},
  "matview": {
    "zh": {"v": "无", "p": "查证为无物化视图能力",
           "b": "- 无物化视图（查证为无）`官方文档`。\n- 预聚合在应用层或 BigQuery 侧 `社区共识`。"},
    "en": {"v": "Not supported", "p": "Verified: no materialized views",
           "b": "- No materialized views (verified absent) `(official docs)`.\n- Pre-aggregate in app or BigQuery `(community consensus)`."}},
}

# ---------------- sqlserver ----------------
CONTENT3_C["sqlserver"] = {
  "json_semi": {
    "zh": {"v": "有", "p": "JSON 函数层；无原生类型",
           "b": "- 2016+ JSON 函数（FOR JSON/OPENJSON），存 nvarchar，无原生 JSON 类型 `官方文档`。\n- 计算列+索引可加速路径查询 `官方文档`。"},
    "en": {"v": "Supported", "p": "JSON functions; no native type",
           "b": "- 2016+ JSON functions (FOR JSON/OPENJSON) over nvarchar; no native type `(official docs)`.\n- Computed columns + indexes accelerate path queries `(official docs)`."}},
  "fulltext": {
    "zh": {"v": "有", "p": "Full-Text Search；中文分词器",
           "b": "- Full-Text Search，中文 word breaker `官方文档`。\n- 全文目录维护与备份恢复联动，运维注意 `社区实测`。"},
    "en": {"v": "Supported", "p": "Full-Text Search with CJK breaker",
           "b": "- Full-Text Search with Chinese word breaker `(official docs)`.\n- Catalog maintenance ties into backup/restore ops `(community tested)`."}},
  "sp_proc": {
    "zh": {"v": "有", "p": "T-SQL 完备，SSMS 调试",
           "b": "- T-SQL 存储过程、触发器、CLR 完备，SSMS 调试 `官方文档`。\n- 去 O 迁移 T-SQL 与 PL/SQL 双向改写成本都高 `社区共识`。"},
    "en": {"v": "Supported", "p": "Complete T-SQL, SSMS debugging",
           "b": "- Complete T-SQL procedures, triggers, CLR with SSMS debugging `(official docs)`.\n- Oracle migration rewrites costly both ways `(community consensus)`."}},
  "constraints": {
    "zh": {"v": "有", "p": "外键/CHECK/唯一/默认完备",
           "b": "- 外键、CHECK、唯一、默认约束完备 `官方文档`。\n- 大表加约束注意锁与在线操作 `社区实测`。"},
    "en": {"v": "Supported", "p": "Complete constraints",
           "b": "- Full FK, CHECK, unique, default constraints `(official docs)`.\n- Mind locks and online ops adding constraints on huge tables `(community tested)`."}},
  "analytical_sql": {
    "zh": {"v": "有", "p": "T-SQL 分析函数完备",
           "b": "- 窗口函数、CTE、GROUPING SETS 完备 `官方文档`。\n- 列存索引（columnstore）加持分析性能 `官方文档`。"},
    "en": {"v": "Supported", "p": "Complete T-SQL analytics",
           "b": "- Complete window functions, CTEs, GROUPING SETS `(official docs)`.\n- Columnstore indexes boost analytics `(official docs)`."}},
  "matview": {
    "zh": {"v": "有", "p": "索引视图自动维护+改写",
           "b": "- 索引视图（indexed views）自动维护、查询自动改写 `官方文档`。\n- 限制多（SCHEMABINDING、确定性函数），滥用拖慢写入 `社区实测`。"},
    "en": {"v": "Supported", "p": "Indexed views, auto-maintained",
           "b": "- Indexed views auto-maintained with automatic rewrite `(official docs)`.\n- Many limits (SCHEMABINDING, deterministic funcs); abuse slows writes `(community tested)`."}},
}

# ---------------- starrocks ----------------
CONTENT3_C["starrocks"] = {
  "json_semi": {
    "zh": {"v": "有", "p": "JSON/Variant+倒排索引",
           "b": "- JSON 类型，3.x Variant 半结构化，倒排索引加速 `官方文档`。\n- 动态列过多同样注意 tablet 膨胀 `社区实测`。"},
    "en": {"v": "Supported", "p": "JSON/Variant + inverted index",
           "b": "- JSON type, 3.x Variant semi-structured, inverted-index acceleration `(official docs)`.\n- Too many dynamic columns bloat tablets likewise `(community tested)`."}},
  "fulltext": {
    "zh": {"v": "有", "p": "倒排索引全文检索+ngram",
           "b": "- 倒排索引全文检索，ngram 中文分词 `官方文档`。\n- 相关性排序弱于 ES `社区共识`。"},
    "en": {"v": "Supported", "p": "Inverted-index full-text",
           "b": "- Inverted-index full-text with ngram CJK tokenization `(official docs)`.\n- Relevance ranking weaker than ES `(community consensus)`."}},
  "sp_proc": {
    "zh": {"v": "无", "p": "查证为无存储过程/触发器",
           "b": "- 无存储过程、触发器（查证为无）`官方文档`。\n- 逻辑在 ETL/应用层 `社区共识`。"},
    "en": {"v": "Not supported", "p": "Verified: no procedures/triggers",
           "b": "- No stored procedures or triggers (verified absent) `(official docs)`.\n- Logic in ETL/app layer `(community consensus)`."}},
  "constraints": {
    "zh": {"v": "无", "p": "OLAP 无外键/CHECK",
           "b": "- 无外键、CHECK（查证为无）`官方文档`。\n- 数据质量靠导入前校验 `社区共识`。"},
    "en": {"v": "Not supported", "p": "No FK/CHECK in OLAP",
           "b": "- No FK or CHECK (verified absent) `(official docs)`.\n- Quality enforced before loading `(community consensus)`."}},
  "analytical_sql": {
    "zh": {"v": "有", "p": "窗口/GROUPING SETS 完备",
           "b": "- 窗口函数、GROUPING SETS/CUBE/ROLLUP 完备 `官方文档`。\n- 向量化执行加持复杂分析 `官方文档`。"},
    "en": {"v": "Supported", "p": "Complete windows/GROUPING SETS",
           "b": "- Complete window functions, GROUPING SETS/CUBE/ROLLUP `(official docs)`.\n- Vectorized execution boosts complex analytics `(official docs)`."}},
  "matview": {
    "zh": {"v": "有", "p": "同步/异步 MV，自动改写",
           "b": "- 同步/异步物化视图，查询自动透明改写 `官方文档`。\n- 异步 MV 刷新延迟与资源消耗需评估 `社区实测`。"},
    "en": {"v": "Supported", "p": "Sync/async MVs, auto rewrite",
           "b": "- Sync/async materialized views with transparent query rewrite `(official docs)`.\n- Evaluate async MV refresh lag and resource cost `(community tested)`."}},
}

# ---------------- tdsql ----------------
CONTENT3_C["tdsql"] = {
  "json_semi": {
    "zh": {"v": "有", "p": "MySQL 版 JSON 继承",
           "b": "- MySQL 版原生 JSON 类型与函数 `官方文档`。\n- 能力与上游 MySQL 对齐 `社区共识`。"},
    "en": {"v": "Supported", "p": "Inherited MySQL JSON",
           "b": "- MySQL flavor native JSON types and functions `(official docs)`.\n- Aligned with upstream MySQL `(community consensus)`."}},
  "fulltext": {
    "zh": {"v": "有", "p": "FULLTEXT 继承",
           "b": "- MySQL 版 FULLTEXT 索引 `官方文档`。\n- 大规模检索同样建议外挂 ES `社区共识`。"},
    "en": {"v": "Supported", "p": "Inherited FULLTEXT",
           "b": "- MySQL flavor FULLTEXT indexes `(official docs)`.\n- Large-scale search still wants ES `(community consensus)`."}},
  "sp_proc": {
    "zh": {"v": "有", "p": "SP/触发器继承 MySQL",
           "b": "- 存储过程、触发器、事件与 MySQL 一致 `官方文档`。\n- 去 O 改写成本与 MySQL 一致 `社区共识`。"},
    "en": {"v": "Supported", "p": "Inherited MySQL SPs",
           "b": "- Procedures, triggers, events same as MySQL `(official docs)`.\n- Oracle-migration cost same as MySQL `(community consensus)`."}},
  "constraints": {
    "zh": {"v": "有", "p": "FK/CHECK 继承",
           "b": "- 外键、CHECK 与 MySQL 一致 `官方文档`。\n- 分布式下外键使用注意 shard 键对齐 `社区实测`。"},
    "en": {"v": "Supported", "p": "Inherited FK/CHECK",
           "b": "- FK, CHECK same as MySQL `(official docs)`.\n- Mind shard-key alignment for FKs when distributed `(community tested)`."}},
  "analytical_sql": {
    "zh": {"v": "有", "p": "窗口函数/CTE 完整继承",
           "b": "- 8.0 窗口函数、CTE `官方文档`。\n- 复杂分析非其主场景 `社区共识`。"},
    "en": {"v": "Supported", "p": "Inherited windows/CTEs",
           "b": "- 8.0 window functions, CTEs `(official docs)`.\n- Complex analytics not its main scene `(community consensus)`."}},
  "matview": {
    "zh": {"v": "无", "p": "查证为无物化视图能力",
           "b": "- 无物化视图（查证为无）`官方文档`。\n- 汇总表模拟 `社区共识`。"},
    "en": {"v": "Not supported", "p": "Verified: no materialized views",
           "b": "- No materialized views (verified absent) `(official docs)`.\n- Summary tables instead `(community consensus)`."}},
}

# ---------------- tidb ----------------
CONTENT3_C["tidb"] = {
  "json_semi": {
    "zh": {"v": "有", "p": "JSON 类型 MySQL 兼容",
           "b": "- JSON 类型与函数 MySQL 兼容 `官方文档`。\n- JSON 索引经虚拟列，分布式下注意 `社区共识`。"},
    "en": {"v": "Supported", "p": "MySQL-compatible JSON",
           "b": "- MySQL-compatible JSON types and functions `(official docs)`.\n- JSON indexes via virtual columns; mind distribution `(community consensus)`."}},
  "fulltext": {
    "zh": {"v": "无", "p": "查证为无 FULLTEXT",
           "b": "- 不支持 FULLTEXT 索引（MySQL 兼容性缺口，查证为无）`官方文档`。\n- 全文场景外挂 ES `社区共识`。"},
    "en": {"v": "Not supported", "p": "Verified: no FULLTEXT",
           "b": "- No FULLTEXT indexes (MySQL compat gap, verified absent) `(official docs)`.\n- Full-text via external ES `(community consensus)`."}},
  "sp_proc": {
    "zh": {"v": "无", "p": "查证为无存储过程/触发器",
           "b": "- 不支持存储过程、触发器（查证为无）`官方文档`。\n- 去 O/去 MySQL 迁移时 SP 需重写为应用逻辑 `社区共识`。"},
    "en": {"v": "Not supported", "p": "Verified: no procedures/triggers",
           "b": "- No stored procedures or triggers (verified absent) `(official docs)`.\n- Procedures must move to app logic when migrating `(community consensus)`."}},
  "constraints": {
    "zh": {"v": "部分支持", "p": "FK 曾长期缺失；现逐步完善",
           "b": "- 外键曾长期不支持，现版本逐步完善，仍有诸多限制 `官方文档`。\n- CHECK 支持；生产使用外键前按版本核对限制清单 `社区实测`。"},
    "en": {"v": "Partial", "p": "FKs long missing; maturing",
           "b": "- FKs long unsupported, now maturing with many limits `(official docs)`.\n- CHECK supported; check the per-version limit list before using FKs `(community tested)`."}},
  "analytical_sql": {
    "zh": {"v": "有", "p": "窗口/CTE MySQL 8 对齐",
           "b": "- 窗口函数、CTE 与 MySQL 8 对齐 `官方文档`。\n- MPP 下复杂分析可用 TiFlash 加速 `官方文档`。"},
    "en": {"v": "Supported", "p": "Windows/CTEs aligned to MySQL 8",
           "b": "- Window functions, CTEs aligned with MySQL 8 `(official docs)`.\n- TiFlash accelerates complex MPP analytics `(official docs)`."}},
  "matview": {
    "zh": {"v": "无", "p": "查证为无物化视图能力",
           "b": "- 无物化视图（查证为无）`官方文档`。\n- 预聚合靠应用层或下游 OLAP `社区共识`。"},
    "en": {"v": "Not supported", "p": "Verified: no materialized views",
           "b": "- No materialized views (verified absent) `(official docs)`.\n- Pre-aggregate in app or downstream OLAP `(community consensus)`."}},
}

# ---------------- weaviate ----------------
CONTENT3_C["weaviate"] = {
  "json_semi": {
    "zh": {"v": "部分支持", "p": "object 属性；GraphQL 过滤",
           "b": "- 属性支持 object/object[] 类型，GraphQL 可过滤 `官方文档`。\n- 非文档查询主力 `社区共识`。"},
    "en": {"v": "Partial", "p": "object props; GraphQL filters",
           "b": "- object/object[] properties filterable via GraphQL `(official docs)`.\n- Not a document query engine `(community consensus)`."}},
  "fulltext": {
    "zh": {"v": "部分支持", "p": "BM25 关键词混合检索",
           "b": "- BM25 关键词混合检索（hybrid）`官方文档`。\n- 非传统全文检索引擎 `社区共识`。"},
    "en": {"v": "Partial", "p": "BM25 hybrid search",
           "b": "- BM25 keyword hybrid search `(official docs)`.\n- Not a classic full-text engine `(community consensus)`."}},
  "sp_proc": {
    "zh": {"v": "不适用", "p": "向量库无过程语言概念",
           "b": "- 无存储过程/触发器概念（不适用）`官方文档`。"},
    "en": {"v": "N/A", "p": "No procedural concept",
           "b": "- No stored-procedure/trigger concept (N/A) `(official docs)`."}},
  "constraints": {
    "zh": {"v": "不适用", "p": "向量库无约束概念（不适用）",
           "b": "- 无外键/CHECK 概念（不适用）`官方文档`。"},
    "en": {"v": "N/A", "p": "No constraint concept",
           "b": "- No FK/CHECK concept (N/A) `(official docs)`."}},
  "analytical_sql": {
    "zh": {"v": "不适用", "p": "向量库无分析 SQL 概念",
           "b": "- 无 SQL/分析 SQL（不适用）`官方文档`。"},
    "en": {"v": "N/A", "p": "No analytical SQL concept",
           "b": "- No SQL/analytical SQL (N/A) `(official docs)`."}},
  "matview": {
    "zh": {"v": "不适用", "p": "向量库无物化视图概念",
           "b": "- 无物化视图概念（不适用）`官方文档`。"},
    "en": {"v": "N/A", "p": "No MV concept",
           "b": "- No materialized-view concept (N/A) `(official docs)`."}},
}

# ---------------- yugabytedb ----------------
CONTENT3_C["yugabytedb"] = {
  "json_semi": {
    "zh": {"v": "有", "p": "YSQL jsonb；YCQL 集合",
           "b": "- YSQL jsonb（PG 兼容），YCQL 集合类型 `官方文档`。\n- YSQL GIN 索引支持弱于 PG `待验证`。"},
    "en": {"v": "Supported", "p": "YSQL jsonb; YCQL collections",
           "b": "- YSQL jsonb (PG-compatible); YCQL collections `(official docs)`.\n- YSQL GIN weaker than PG `(to be verified)`."}},
  "fulltext": {
    "zh": {"v": "部分支持", "p": "tsvector 有限，待验证",
           "b": "- YSQL 继承 PG 部分全文能力，tsvector 支持有限 `待验证`。\n- 生产全文多外挂 ES `社区共识`。"},
    "en": {"v": "Partial", "p": "Limited tsvector; verify",
           "b": "- Partial PG full-text inheritance; tsvector limited `(to be verified)`.\n- Production full-text often external ES `(community consensus)`."}},
  "sp_proc": {
    "zh": {"v": "有", "p": "YSQL plpgsql；触发器部分",
           "b": "- YSQL plpgsql 可用，触发器部分支持 `官方文档`。\n- 分布式下触发器语义注意 `待验证`。"},
    "en": {"v": "Supported", "p": "YSQL plpgsql; partial triggers",
           "b": "- YSQL plpgsql works; triggers partially supported `(official docs)`.\n- Mind trigger semantics under distribution `(to be verified)`."}},
  "constraints": {
    "zh": {"v": "部分支持", "p": "FK/CHECK 有；分布式代价",
           "b": "- YSQL 外键、CHECK 支持 `官方文档`。\n- 跨 tablet 外键检查有分布式代价，高吞吐慎用 `官方文档`。"},
    "en": {"v": "Partial", "p": "FK/CHECK; distributed cost",
           "b": "- YSQL FK and CHECK supported `(official docs)`.\n- Cross-tablet FK checks cost; careful at high throughput `(official docs)`."}},
  "analytical_sql": {
    "zh": {"v": "有", "p": "YSQL 窗口函数 PG 兼容",
           "b": "- YSQL 窗口函数、CTE（PG 兼容）`官方文档`。\n- 复杂分析性能弱于专用 OLAP `社区共识`。"},
    "en": {"v": "Supported", "p": "YSQL windows, PG-compatible",
           "b": "- YSQL window functions, CTEs (PG-compatible) `(official docs)`.\n- Complex analytics weaker than dedicated OLAP `(community consensus)`."}},
  "matview": {
    "zh": {"v": "有", "p": "YSQL 物化视图手动刷新",
           "b": "- YSQL 物化视图（PG 兼容，手动 REFRESH）`官方文档`。\n- 无自动增量刷新 `社区共识`。"},
    "en": {"v": "Supported", "p": "YSQL MVs, manual refresh",
           "b": "- YSQL materialized views (PG-compatible, manual REFRESH) `(official docs)`.\n- No automatic incremental refresh `(community consensus)`."}},
}

# ---------------- redshift ----------------
CONTENT3_C["redshift"] = {
  "json_semi": {
    "zh": {"v": "有", "p": "SUPER 类型半结构化原生",
           "b": "- SUPER 类型原生半结构化，PartiQL 导航查询 `官方文档`。\n- SUPER 列无统计信息时查询规划弱，热点路径建议规整化 `社区实测`。"},
    "en": {"v": "Supported", "p": "Native SUPER semi-structured",
           "b": "- Native SUPER semi-structured type with PartiQL navigation `(official docs)`.\n- Weak stats on SUPER columns hurt planning; normalize hot paths `(community tested)`."}},
  "fulltext": {
    "zh": {"v": "部分支持", "p": "无原生全文索引；文本函数",
           "b": "- 无原生全文索引（查证为无），靠文本函数/模糊匹配 `官方文档`。\n- 全文场景集成 OpenSearch `社区共识`。"},
    "en": {"v": "Partial", "p": "No native FTS; text functions",
           "b": "- No native full-text indexes (verified absent); text functions/fuzzy matching `(official docs)`.\n- Full-text via OpenSearch integration `(community consensus)`."}},
  "sp_proc": {
    "zh": {"v": "有", "p": "存储过程（PL/pgSQL 子集）",
           "b": "- 支持存储过程（PL/pgSQL 子集），游标/异常处理有限 `官方文档`。\n- 与 PG/Oracle 过程语言差异大，迁移需改写 `社区共识`。"},
    "en": {"v": "Supported", "p": "Procedures (PL/pgSQL subset)",
           "b": "- Stored procedures (PL/pgSQL subset) with limited cursors/exceptions `(official docs)`.\n- Differs a lot from PG/Oracle; migrations need rewrites `(community consensus)`."}},
  "constraints": {
    "zh": {"v": "部分支持", "p": "PK/FK/UNIQUE 信息性不强制",
           "b": "- 主键/外键/唯一为信息性约束，不强制执行 `官方文档`。\n- 用于查询优化，错误声明误导优化器 `社区实测`。"},
    "en": {"v": "Partial", "p": "Informational PK/FK/UNIQUE",
           "b": "- PK/FK/UNIQUE informational, not enforced `(official docs)`.\n- Used for optimization; wrong declarations mislead the planner `(community tested)`."}},
  "analytical_sql": {
    "zh": {"v": "有", "p": "窗口/GROUPING SETS 完备",
           "b": "- 窗口函数、GROUPING SETS 等分析 SQL 完备 `官方文档`。\n- 基于 PG 8 系，部分新语法缺失 `社区共识`。"},
    "en": {"v": "Supported", "p": "Complete windows/GROUPING SETS",
           "b": "- Complete window functions, GROUPING SETS `(official docs)`.\n- PG 8-based; some newer syntax missing `(community consensus)`."}},
  "matview": {
    "zh": {"v": "有", "p": "自动增量刷新+自动改写",
           "b": "- 物化视图自动增量刷新、查询自动改写 `官方文档`。\n- 仅支持部分增量场景，基表大变更回退全量 `官方文档`。"},
    "en": {"v": "Supported", "p": "Auto incremental refresh + rewrite",
           "b": "- Automatic incremental refresh and query rewrite `(official docs)`.\n- Only some incremental cases; big base changes fall back to full `(official docs)`."}},
}

# ---------------- bigquery ----------------
CONTENT3_C["bigquery"] = {
  "json_semi": {
    "zh": {"v": "有", "p": "JSON 类型原生，函数丰富",
           "b": "- 原生 JSON 数据类型，JSON_QUERY/JSON_VALUE 等函数丰富 `官方文档`。\n- 按扫描计费，SELECT * 大 JSON 费用惊人 `社区实测`。"},
    "en": {"v": "Supported", "p": "Native JSON, rich functions",
           "b": "- Native JSON type with rich JSON_QUERY/JSON_VALUE functions `(official docs)`.\n- Billed per scanned byte; SELECT * on big JSON is shockingly expensive `(community tested)`."}},
  "fulltext": {
    "zh": {"v": "有", "p": "SEARCH 函数+search index",
           "b": "- SEARCH 函数与 search index 支持全文检索 `官方文档`。\n- 索引有配额与延迟，非实时 `官方文档`。"},
    "en": {"v": "Supported", "p": "SEARCH functions + search index",
           "b": "- SEARCH functions and search index for full-text `(official docs)`.\n- Index has quotas and lag; not real-time `(official docs)`."}},
  "sp_proc": {
    "zh": {"v": "有", "p": "SQL 脚本/存储过程+调度查询",
           "b": "- 多语句脚本、存储过程（procedures），scheduled queries 定时调度 `官方文档`。\n- 去 O 迁移 PL/SQL 需改写 `社区共识`。"},
    "en": {"v": "Supported", "p": "Scripting/procedures/scheduling",
           "b": "- Multi-statement scripting, procedures, scheduled queries `(official docs)`.\n- Oracle PL/SQL needs rewrites `(community consensus)`."}},
  "constraints": {
    "zh": {"v": "部分支持", "p": "PK/FK 信息性不强制",
           "b": "- 主键/外键为 not enforced 信息性约束 `官方文档`。\n- 靠上游保证，错误声明影响优化 `社区共识`。"},
    "en": {"v": "Partial", "p": "Informational PK/FK",
           "b": "- PK/FK not enforced, informational `(official docs)`.\n- Guaranteed upstream; wrong declarations affect optimization `(community consensus)`."}},
  "analytical_sql": {
    "zh": {"v": "有", "p": "分析 SQL 强项，函数极全",
           "b": "- 窗口函数、CTE、PIVOT、ML 函数，分析 SQL 为强项 `官方文档`。\n- 方言（GoogleSQL）与标准 SQL 差异，迁移注意 `社区共识`。"},
    "en": {"v": "Supported", "p": "Analytical SQL strength",
           "b": "- Window functions, CTEs, PIVOT, ML functions — analytical SQL is its strength `(official docs)`.\n- GoogleSQL dialect differs from standard SQL `(community consensus)`."}},
  "matview": {
    "zh": {"v": "有", "p": "增量刷新+自动改写；需分区对齐",
           "b": "- 物化视图增量刷新、查询自动改写 `官方文档`。\n- 需基表分区对齐等前提，不满足则不增量 `官方文档`。"},
    "en": {"v": "Supported", "p": "Incremental + rewrite; needs alignment",
           "b": "- Incremental refresh and automatic rewrite `(official docs)`.\n- Requires partition alignment etc.; otherwise no incremental `(official docs)`."}},
}
