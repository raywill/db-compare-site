# -*- coding: utf-8 -*-
"""6 个新增维度的数据：optimizer / tuning / lineage / storage_compute / multi_model / drivers.
CONTENT3_D[slug][dimkey] = {"zh": {"v","p","b"}, "en": {"v","p","b"}}
v = verdict（有/部分支持/无/不适用/未找到证据；Supported/Partial/Not supported/N/A/No evidence found），
p = 10-25 字短语，b = markdown 正文（`- ` 条目 + 反引号证据徽章）。
"""

CONTENT3_D = {}
CONTENT3_D["alloydb"] = {
  "optimizer": {
    "zh": {"v": "有", "p": "PG 衍生 CBO；列存引擎优化器适配",
           "b": "- 继承 PostgreSQL 的 CBO（GEQO、并行、分区裁剪），EXPLAIN 完备 `官方文档`。\n- 列存引擎查询会自动改写走列存路径，优化器层面透明 `官方文档`。\n- hint 仍需 pg_hint_plan 等扩展，非官方内置；统计信息过期同样导致计划翻转 `社区共识`。"},
    "en": {"v": "Supported", "p": "PG-derived CBO; columnar engine optimizer integration",
           "b": "- Inherits PostgreSQL's CBO (GEQO, parallelism, partition pruning) with full EXPLAIN support `(official docs)`.\n- Columnar engine queries are transparently rewritten to the columnar path at optimizer level `(official docs)`.\n- Hints still need extensions like pg_hint_plan (not built-in); stale statistics can flip plans as in PG `(community consensus)`."}},
  "tuning": {
    "zh": {"v": "有", "p": "自治调优强：自动列存与 autovacuum",
           "b": "- 参数大幅简化，自动列存按负载自动决定列存化 `官方文档`。\n- adaptive autovacuum、行列混存自适应减少手工调参 `官方文档`。\n- 深度调优仍需理解 PG 参数体系，极端负载下仍要人工介入 `社区共识`。"},
    "en": {"v": "Supported", "p": "Strong autonomous tuning: auto columnarization",
           "b": "- Greatly simplified parameters; automatic columnarization decides columnar storage by workload `(official docs)`.\n- Adaptive autovacuum and hybrid row/column storage cut manual tuning `(official docs)`.\n- Extreme workloads still need PG parameter knowledge and manual intervention `(community consensus)`."}},
  "lineage": {
    "zh": {"v": "部分支持", "p": "Dataplex 集成；无原生血缘",
           "b": "- 可通过 Dataplex/Data Catalog 采集元数据做血缘 `官方文档`。\n- 无数据库原生列级血缘，需第三方工具补齐 `社区共识`。"},
    "en": {"v": "Partial", "p": "Dataplex integration; no native lineage",
           "b": "- Metadata can feed lineage via Dataplex/Data Catalog `(official docs)`.\n- No native column-level lineage; third-party tools needed `(community consensus)`."}},
  "storage_compute": {
    "zh": {"v": "有", "p": "存算分离：计算与分布式存储分离",
           "b": "- 计算节点无状态，数据存于分布式存储，可独立扩缩 `官方文档`。\n- 故障恢复快：新计算节点直接挂载存储卷 `官方文档`。\n- 跨可用区存储复制带来写入延迟成本 `社区共识`。"},
    "en": {"v": "Supported", "p": "Disaggregated: stateless compute on distributed storage",
           "b": "- Stateless compute nodes on distributed storage; scale independently `(official docs)`.\n- Fast recovery: new compute attaches existing storage volumes `(official docs)`.\n- Cross-zone storage replication adds write-latency cost `(community consensus)`."}},
  "multi_model": {
    "zh": {"v": "部分支持", "p": "PG 生态多模：jsonb+pgvector 可用",
           "b": "- 继承 PG 的 jsonb、全文检索、PostGIS、pgvector 生态 `官方文档`。\n- 无原生图引擎；超大规模向量仍建议专用库 `社区共识`。"},
    "en": {"v": "Partial", "p": "PG multi-model: jsonb + pgvector available",
           "b": "- Inherits PG's jsonb, full-text, PostGIS, pgvector ecosystem `(official docs)`.\n- No native graph engine; hyperscale vectors still favor dedicated stores `(community consensus)`."}},
  "drivers": {
    "zh": {"v": "有", "p": "PG 协议兼容，驱动生态直接复用",
           "b": "- 标准 PG 协议，pgjdbc、psqlODBC、libpq 各语言驱动直接可用 `官方文档`。\n- IAM 数据库认证是 AlloyDB 特有接入方式，需驱动支持 `官方文档`。"},
    "en": {"v": "Supported", "p": "PG-protocol compatible; reuse PG drivers",
           "b": "- Standard PG protocol: pgjdbc, psqlODBC, libpq drivers work directly `(official docs)`.\n- IAM database authentication is AlloyDB-specific and needs driver support `(official docs)`."}}
}
CONTENT3_D["aurora"] = {
  "optimizer": {
    "zh": {"v": "有", "p": "引擎优化器同 MySQL/PG；存储层透明",
           "b": "- 查询优化器与对应引擎（MySQL 8 / PG）一致，hint、EXPLAIN 行为相同 `官方文档`。\n- Aurora 的存储层优化对优化器透明，不改变计划选择逻辑 `社区共识`。\n- 计划翻转的根因（统计信息、参数）与原生引擎相同 `社区共识`。"},
    "en": {"v": "Supported", "p": "Same optimizer as MySQL/PG engine; storage invisible",
           "b": "- Query optimizer matches the engine (MySQL 8 / PG): same hints and EXPLAIN behavior `(official docs)`.\n- Aurora's storage-layer optimizations are transparent to the optimizer `(community consensus)`.\n- Plan-flip root causes (statistics, parameters) mirror the native engine `(community consensus)`."}},
  "tuning": {
    "zh": {"v": "部分支持", "p": "参数组可调；Performance Insights 强",
           "b": "- 通过参数组调参，常用参数与原生引擎一致 `官方文档`。\n- Performance Insights、Enhanced Monitoring 诊断能力强 `官方文档`。\n- 无自动索引/自动重写，自治能力弱于 AlloyDB 等 `社区共识`。"},
    "en": {"v": "Partial", "p": "Parameter groups tunable; strong Performance Insights",
           "b": "- Tuned via parameter groups, same common parameters as native engines `(official docs)`.\n- Performance Insights and Enhanced Monitoring give strong diagnostics `(official docs)`.\n- No auto-indexing/rewrites; less autonomous than AlloyDB-class offerings `(community consensus)`."}},
  "lineage": {
    "zh": {"v": "部分支持", "p": "Glue 爬网元数据；无原生血缘",
           "b": "- Glue crawler 可抓取 Aurora 表元数据进 Data Catalog `官方文档`。\n- 无原生列级血缘，需第三方血缘工具 `社区共识`。"},
    "en": {"v": "Partial", "p": "Glue-crawled metadata; no native lineage",
           "b": "- Glue crawlers can catalog Aurora table metadata `(official docs)`.\n- No native column-level lineage; third-party tools needed `(community consensus)`."}},
  "storage_compute": {
    "zh": {"v": "有", "p": "存算分离标杆：分布式存储+计算分离",
           "b": "- 存储与计算分离，存储自动扩缩至 128TB，按使用量计费 `官方文档`。\n- 存储层 6 副本跨 3 AZ，故障切换秒级 `官方文档`。\n- 写入需经存储层仲裁，超高并发小事务延迟高于本地盘 `社区实测`。"},
    "en": {"v": "Supported", "p": "Disaggregation benchmark: distributed storage, split compute",
           "b": "- Storage/compute separated; storage auto-scales to 128TB, pay-per-use `(official docs)`.\n- 6 storage copies across 3 AZs; failover in seconds `(official docs)`.\n- Writes arbitrate through the storage layer; ultra-high-concurrency small transactions lag local disks `(community tested)`."}},
  "multi_model": {
    "zh": {"v": "部分支持", "p": "随引擎：MySQL JSON / PG 向量生态",
           "b": "- Aurora MySQL：JSON 类型+全文索引；Aurora PG：jsonb、pgvector（RDS 系支持）`官方文档`。\n- 无原生图/时序引擎 `社区共识`。"},
    "en": {"v": "Partial", "p": "Engine-dependent: MySQL JSON / PG vectors",
           "b": "- Aurora MySQL: JSON type + full-text; Aurora PG: jsonb, pgvector (RDS-family support) `(official docs)`.\n- No native graph/time-series engine `(community consensus)`."}},
  "drivers": {
    "zh": {"v": "有", "p": "原生协议兼容；RDS Proxy 增强",
           "b": "- 完全兼容 MySQL/PG 协议与驱动 `官方文档`。\n- RDS Proxy 提供连接池与故障切换加速 `官方文档`。"},
    "en": {"v": "Supported", "p": "Native protocol compatible; RDS Proxy enhanced",
           "b": "- Fully compatible with MySQL/PG protocols and drivers `(official docs)`.\n- RDS Proxy adds pooling and faster failover `(official docs)`."}}
}
CONTENT3_D["cassandra-scylladb"] = {
  "optimizer": {
    "zh": {"v": "部分支持", "p": "无 CBO：靠建模，计划简单可预测",
           "b": "- Cassandra 无代价优化器，查询性能由数据建模（分区键设计）决定，计划可预测但无自动优化 `官方文档`。\n- ALLOW FILTERING 全表扫描是经典生产事故源 `社区共识`。\n- ScyllaDB 保持 CQL 兼容，同样无 CBO `官方文档`。"},
    "en": {"v": "Partial", "p": "No CBO: modeling decides; simple predictable plans",
           "b": "- Cassandra has no cost-based optimizer; performance comes from data modeling (partition keys) — predictable but not auto-optimized `(official docs)`.\n- ALLOW FILTERING full scans are a classic production incident source `(community consensus)`.\n- ScyllaDB stays CQL-compatible, likewise no CBO `(official docs)`."}},
  "tuning": {
    "zh": {"v": "部分支持", "p": "Cassandra 参数上百；ScyllaDB 自调优",
           "b": "- cassandra.yaml 上百参数，调优高度依赖建模与 compaction 策略 `官方文档`。\n- ScyllaDB 按分片自动调优，运维负担明显更低 `官方文档`。\n- 诊断靠 nodetool/JMX，自治能力弱 `社区共识`。"},
    "en": {"v": "Partial", "p": "Cassandra: 100+ params; ScyllaDB self-tuning",
           "b": "- cassandra.yaml holds 100+ parameters; tuning hinges on modeling and compaction strategy `(official docs)`.\n- ScyllaDB self-tunes per shard, much lower ops burden `(official docs)`.\n- Diagnostics via nodetool/JMX; weak autonomy `(community consensus)`."}},
  "lineage": {
    "zh": {"v": "无", "p": "查证为无原生血缘",
           "b": "- 无原生数据血缘/目录功能 `官方文档`。\n- 需第三方数据治理平台对接 `社区共识`。"},
    "en": {"v": "Not supported", "p": "Verified: no native lineage",
           "b": "- No native data lineage/catalog features `(official docs)`.\n- Requires third-party data governance platforms `(community consensus)`."}},
  "storage_compute": {
    "zh": {"v": "有", "p": "存算一体：本地盘 LSM",
           "b": "- 经典存算一体：每节点本地盘存 SSTable，扩缩容需数据重分布 `官方文档`。\n- 本地盘带来高吞吐与低延迟，但弹性差 `社区共识`。"},
    "en": {"v": "Supported", "p": "Coupled: local-disk LSM",
           "b": "- Classic coupled design: each node keeps SSTables on local disks; scaling reshuffles data `(official docs)`.\n- Local disks give high throughput/low latency but poor elasticity `(community consensus)`."}},
  "multi_model": {
    "zh": {"v": "无", "p": "宽列+集合类型，无向量/全文/图",
           "b": "- 模型限宽列、集合/UDT，无原生向量、全文、图能力 `官方文档`。\n- Stargate 等网关可转协议但不改变模型 `社区共识`。"},
    "en": {"v": "Not supported", "p": "Wide-column + collections only",
           "b": "- Model limited to wide-column, collections/UDTs; no native vector, full-text, or graph `(official docs)`.\n- Gateways like Stargate translate protocols without changing the model `(community consensus)`."}},
  "drivers": {
    "zh": {"v": "有", "p": "DataStax 驱动矩阵全；JDBC 靠 Simba",
           "b": "- DataStax 官方 Java/Python/Node/Go/C# 驱动成熟 `官方文档`。\n- JDBC/ODBC 靠 Simba 等第三方驱动 `社区共识`。"},
    "en": {"v": "Supported", "p": "Full DataStax driver matrix; JDBC/ODBC via Simba",
           "b": "- Mature official Java/Python/Node/Go/C# drivers from DataStax `(official docs)`.\n- JDBC/ODBC rely on third-party drivers like Simba `(community consensus)`."}}
}
CONTENT3_D["clickhouse"] = {
  "optimizer": {
    "zh": {"v": "有", "p": "CBO 持续增强；SETTINGS 调优无 hint",
           "b": "- 24.x 起 CBO 大幅增强，EXPLAIN 完备 `官方文档`。\n- 无传统 hint 语法，靠 SETTINGS 逐查询调优 `官方文档`。\n- 分析场景计划翻转少，但 JOIN 顺序选错仍是慢查询主因 `社区共识`。"},
    "en": {"v": "Supported", "p": "Growing CBO; SETTINGS-based tuning, no classic hints",
           "b": "- CBO greatly improved since 24.x; full EXPLAIN `(official docs)`.\n- No classic hint syntax; per-query tuning via SETTINGS `(official docs)`.\n- Plan flips are rare in analytics, but bad JOIN order still tops slow-query causes `(community consensus)`."}},
  "tuning": {
    "zh": {"v": "部分支持", "p": "上百 settings；调优靠建模",
           "b": "- settings 上百，核心在建表（排序键、分区、TTL）而非运行时参数 `官方文档`。\n- parts 合并、内存配额是常规调优点，自治能力弱 `社区共识`。"},
    "en": {"v": "Partial", "p": "100+ settings; tuning lives in modeling",
           "b": "- 100+ settings, but the real tuning is table design (sorting key, partitioning, TTL) `(official docs)`.\n- Part merges and memory quotas are routine tuning; weak autonomy `(community consensus)`."}},
  "lineage": {
    "zh": {"v": "部分支持", "p": "无原生；OpenLineage 第三方集成",
           "b": "- 无原生血缘，需 OpenLineage/Marquez 等第三方集成 `社区共识`。\n- query_log 可作为血缘采集的数据源 `社区实测`。"},
    "en": {"v": "Partial", "p": "No native; third-party OpenLineage integration",
           "b": "- No native lineage; integrate OpenLineage/Marquez via third parties `(community consensus)`.\n- query_log can serve as a lineage data source `(community tested)`."}},
  "storage_compute": {
    "zh": {"v": "有", "p": "开源存算一体；Cloud 版存算分离",
           "b": "- 开源版经典存算一体：本地盘 MergeTree，高吞吐 `官方文档`。\n- ClickHouse Cloud 采用存算分离（对象存储）`官方文档`。\n- 自建分离存储方案成熟度不如云版 `社区共识`。"},
    "en": {"v": "Supported", "p": "OSS coupled; Cloud disaggregated",
           "b": "- OSS is classic coupled: local-disk MergeTree, high throughput `(official docs)`.\n- ClickHouse Cloud uses disaggregated object storage `(official docs)`.\n- Self-hosted disaggregated setups lag the cloud edition in maturity `(community consensus)`."}},
  "multi_model": {
    "zh": {"v": "部分支持", "p": "列存+JSON+倒排全文+向量索引",
           "b": "- JSON/Object 类型、倒排索引（全文）、向量索引（ANN）均已支持 `官方文档`。\n- 无图引擎；超大规模向量检索仍不如专用库 `社区共识`。"},
    "en": {"v": "Partial", "p": "Columnar + JSON + inverted full-text + vector index",
           "b": "- JSON/Object types, inverted indexes (full-text), and vector (ANN) indexes all supported `(official docs)`.\n- No graph engine; hyperscale vector search still favors dedicated stores `(community consensus)`."}},
  "drivers": {
    "zh": {"v": "有", "p": "HTTP 原生+JDBC/ODBC+各语言客户端",
           "b": "- HTTP 接口是一等公民，clickhouse-jdbc/ODBC 完备 `官方文档`。\n- Python/Go/Node/JS 官方或社区客户端成熟 `社区共识`。"},
    "en": {"v": "Supported", "p": "Native HTTP + JDBC/ODBC + language clients",
           "b": "- HTTP interface is first-class; clickhouse-jdbc/ODBC complete `(official docs)`.\n- Mature Python/Go/Node/JS official or community clients `(community consensus)`."}}
}
CONTENT3_D["cockroachdb"] = {
  "optimizer": {
    "zh": {"v": "有", "p": "自研 CBO；EXPLAIN 完备；hint 有限",
           "b": "- 自研分布式 CBO，支持 EXPLAIN (OPT/VERBOSE) `官方文档`。\n- hint 能力有限（不如 PG/Oracle），计划控制手段少 `官方文档`。\n- 统计信息自动收集，计划翻转多与统计过期相关 `社区共识`。"},
    "en": {"v": "Supported", "p": "Homegrown CBO; full EXPLAIN; limited hints",
           "b": "- Homegrown distributed CBO with EXPLAIN (OPT/VERBOSE) `(official docs)`.\n- Limited hint support (weaker than PG/Oracle), few plan-control levers `(official docs)`.\n- Statistics auto-collected; flips usually trace to stale stats `(community consensus)`."}},
  "tuning": {
    "zh": {"v": "部分支持", "p": "参数精简哲学；自动 rebalance",
           "b": "- 参数数量刻意精简，大量行为自动（副本 rebalance、range 分裂）`官方文档`。\n- DB Console 诊断完善，但深度调优点少 `社区共识`。"},
    "en": {"v": "Partial", "p": "Lean-parameter philosophy; strong auto-rebalance",
           "b": "- Deliberately few parameters; much is automatic (replica rebalance, range splits) `(official docs)`.\n- DB Console diagnostics are solid, but deep tuning levers are few `(community consensus)`."}},
  "lineage": {
    "zh": {"v": "无", "p": "查证为无原生血缘",
           "b": "- 无原生数据血缘/目录 `官方文档`。\n- 依赖第三方治理平台 `社区共识`。"},
    "en": {"v": "Not supported", "p": "Verified: no native lineage",
           "b": "- No native data lineage/catalog `(official docs)`.\n- Depends on third-party governance platforms `(community consensus)`."}},
  "storage_compute": {
    "zh": {"v": "有", "p": "存算一体：Pebble 本地盘",
           "b": "- 每节点 Pebble（RocksDB 衍生）本地存储，存算一体 `官方文档`。\n- 扩缩容自动 rebalance，但数据搬迁耗时 `社区共识`。"},
    "en": {"v": "Supported", "p": "Coupled: Pebble local disks",
           "b": "- Each node stores on local Pebble (RocksDB-derived); coupled `(official docs)`.\n- Scaling auto-rebalances, but data movement takes time `(community consensus)`."}},
  "multi_model": {
    "zh": {"v": "部分支持", "p": "PG 兼容多模：JSONB+全文+向量",
           "b": "- JSONB、全文检索、pgvector 兼容（PG 生态）`官方文档`。\n- 无原生图引擎 `社区共识`。"},
    "en": {"v": "Partial", "p": "PG-compatible multi-model: JSONB+full-text+vectors",
           "b": "- JSONB, full-text, pgvector-compatible (PG ecosystem) `(official docs)`.\n- No native graph engine `(community consensus)`."}},
  "drivers": {
    "zh": {"v": "有", "p": "PG 协议兼容，驱动直接复用",
           "b": "- PG 线协议兼容，pgjdbc/psqlODBC/libpq 直接可用 `官方文档`。\n- 部分 PG 高级特性驱动层需注意兼容 `社区共识`。"},
    "en": {"v": "Supported", "p": "PG-protocol compatible; reuse drivers",
           "b": "- PG wire-protocol compatible; pgjdbc/psqlODBC/libpq work directly `(official docs)`.\n- Some advanced PG features need driver-level compatibility care `(community consensus)`."}}
}
CONTENT3_D["databricks"] = {
  "optimizer": {
    "zh": {"v": "有", "p": "Photon+CBO+AQE；Spark hint 可用",
           "b": "- Photon 引擎 + Spark CBO，自适应查询执行（AQE）运行时调优 `官方文档`。\n- 支持 Spark SQL hint 干预计划 `官方文档`。\n- 计划翻转少于传统数仓，但 AQE 行为不透明难排查 `社区共识`。"},
    "en": {"v": "Supported", "p": "Photon + CBO + AQE; Spark hints available",
           "b": "- Photon engine + Spark CBO with adaptive query execution (AQE) runtime tuning `(official docs)`.\n- Spark SQL hints can steer plans `(official docs)`.\n- Fewer flips than legacy warehouses, but opaque AQE behavior is hard to debug `(community consensus)`."}},
  "tuning": {
    "zh": {"v": "有", "p": "自治调优强：Photon+自动 clustering",
           "b": "- Photon 自动向量化，Liquid Clustering 自动数据布局，调参极少 `官方文档`。\n- 自动优化（auto optimize/compaction）后台进行 `官方文档`。\n- 集群规格选择仍是成本主因 `社区共识`。"},
    "en": {"v": "Supported", "p": "Strong autonomy: Photon + auto liquid clustering",
           "b": "- Photon auto-vectorizes; Liquid Clustering auto-manages layout; minimal knobs `(official docs)`.\n- Auto-optimize/compaction runs in the background `(official docs)`.\n- Cluster sizing remains the main cost lever `(community consensus)`."}},
  "lineage": {
    "zh": {"v": "有", "p": "Unity Catalog 原生列级血缘",
           "b": "- Unity Catalog 提供表/列级血缘、数据发现，自动采集 `官方文档`。\n- 血缘覆盖 notebook/作业/SQL 全链路 `官方文档`。"},
    "en": {"v": "Supported", "p": "Unity Catalog native column-level lineage",
           "b": "- Unity Catalog provides table/column-level lineage and discovery, auto-captured `(official docs)`.\n- Lineage spans notebooks, jobs, and SQL end to end `(official docs)`."}},
  "storage_compute": {
    "zh": {"v": "有", "p": "存算分离：云存储+弹性集群",
           "b": "- 数据存云对象存储，计算集群弹性启停、独立扩缩 `官方文档`。\n- Serverless SQL 仓库进一步解耦 `官方文档`。\n- 跨云账户存储访问需网络配置 `社区共识`。"},
    "en": {"v": "Supported", "p": "Disaggregated: cloud storage + elastic clusters",
           "b": "- Data on cloud object storage; compute clusters start/stop and scale independently `(official docs)`.\n- Serverless SQL warehouses decouple further `(official docs)`.\n- Cross-account storage access needs network setup `(community consensus)`."}},
  "multi_model": {
    "zh": {"v": "有", "p": "Delta 多模：关系+JSON+向量+ML",
           "b": "- Delta Lake：结构化、半结构化 JSON、Vector Search、MLflow 模型 `官方文档`。\n- 无原生图/全文检索引擎 `社区共识`。"},
    "en": {"v": "Supported", "p": "Delta multi-model: relational + JSON + vectors + ML",
           "b": "- Delta Lake: structured, semi-structured JSON, Vector Search, MLflow models `(official docs)`.\n- No native graph/full-text engine `(community consensus)`."}},
  "drivers": {
    "zh": {"v": "有", "p": "JDBC/ODBC+Python 连接器+Spark",
           "b": "- 官方 JDBC/ODBC（Simba）、databricks-sql-connector（Python）`官方文档`。\n- BI 工具生态（dbt/PowerBI/Tableau）完备 `社区共识`。"},
    "en": {"v": "Supported", "p": "JDBC/ODBC + Python connector + Spark",
           "b": "- Official JDBC/ODBC (Simba), databricks-sql-connector (Python) `(official docs)`.\n- Full BI ecosystem (dbt/PowerBI/Tableau) `(community consensus)`."}}
}
CONTENT3_D["doris"] = {
  "optimizer": {
    "zh": {"v": "有", "p": "Nereids 新 CBO；hint 可用",
           "b": "- Nereids 新优化器替代旧 planner，CBO 能力持续增强 `官方文档`。\n- 支持 leading/shuffle hint 等干预 `官方文档`。\n- 老版本 planner 计划质量弱，升级 Nereids 是常规建议 `社区共识`。"},
    "en": {"v": "Supported", "p": "New Nereids CBO; hints available",
           "b": "- New Nereids optimizer replaces the legacy planner; CBO keeps improving `(official docs)`.\n- Supports leading/shuffle hints and similar steering `(official docs)`.\n- Legacy planner plans were weak; upgrading to Nereids is routine advice `(community consensus)`."}},
  "tuning": {
    "zh": {"v": "部分支持", "p": "参数可调；调优靠建模与分桶",
           "b": "- BE/FE 参数可调，核心调优点在建表（分区分桶、物化）`官方文档`。\n- 自治能力中等，无自动索引推荐 `社区共识`。"},
    "en": {"v": "Partial", "p": "Tunable params; tuning lives in modeling",
           "b": "- BE/FE parameters tunable, but real levers are table design (partitioning, bucketing, materialization) `(official docs)`.\n- Middling autonomy; no auto index advisor `(community consensus)`."}},
  "lineage": {
    "zh": {"v": "无", "p": "查证为无原生血缘",
           "b": "- 无原生数据血缘/目录 `官方文档`。\n- 需第三方治理平台 `社区共识`。"},
    "en": {"v": "Not supported", "p": "Verified: no native lineage",
           "b": "- No native data lineage/catalog `(official docs)`.\n- Requires third-party governance platforms `(community consensus)`."}},
  "storage_compute": {
    "zh": {"v": "有", "p": "2.x 起存算分离；默认存算一体",
           "b": "- 默认存算一体（本地盘）；2.x 起支持存算分离架构 `官方文档`。\n- 分离架构下计算节点无状态，弹性更好 `官方文档`。\n- 存算分离版本生态与稳定性待生产验证 `待验证`。"},
    "en": {"v": "Supported", "p": "Disaggregated since 2.x; coupled by default",
           "b": "- Coupled by default (local disks); disaggregated architecture since 2.x `(official docs)`.\n- Stateless compute nodes under disaggregation improve elasticity `(official docs)`.\n- Disaggregated edition's production maturity awaits validation `(to be verified)`."}},
  "multi_model": {
    "zh": {"v": "部分支持", "p": "关系+JSON+倒排全文+向量",
           "b": "- JSON 类型、倒排索引（全文）、向量索引均已支持 `官方文档`。\n- 无图引擎 `社区共识`。"},
    "en": {"v": "Partial", "p": "Relational + JSON + inverted full-text + vectors",
           "b": "- JSON type, inverted indexes (full-text), and vector indexes supported `(official docs)`.\n- No graph engine `(community consensus)`."}},
  "drivers": {
    "zh": {"v": "有", "p": "MySQL 协议兼容",
           "b": "- MySQL 线协议兼容，MySQL 驱动/JDBC/ODBC 直接可用 `官方文档`。\n- Flink/Spark Connector 生态成熟 `社区共识`。"},
    "en": {"v": "Supported", "p": "MySQL-protocol compatible",
           "b": "- MySQL wire-protocol compatible; MySQL drivers/JDBC/ODBC work directly `(official docs)`.\n- Mature Flink/Spark connector ecosystem `(community consensus)`."}}
}
CONTENT3_D["duckdb"] = {
  "optimizer": {
    "zh": {"v": "有", "p": "向量化 CBO；自动优化好，无 hint",
           "b": "- 向量化执行 + CBO，EXPLAIN 完备，小查询优化出色 `官方文档`。\n- 无 hint 机制，计划干预手段少 `官方文档`。\n- 嵌入式场景计划翻转风险低 `社区共识`。"},
    "en": {"v": "Supported", "p": "Vectorized CBO; great auto-optimization, no hints",
           "b": "- Vectorized execution + CBO, full EXPLAIN, excellent small-query optimization `(official docs)`.\n- No hint mechanism; few plan-steering levers `(official docs)`.\n- Low plan-flip risk in embedded scenarios `(community consensus)`."}},
  "tuning": {
    "zh": {"v": "有", "p": "零配置自治：PRAGMA 少量参数",
           "b": "- 开箱即用，PRAGMA 参数少且有合理默认 `官方文档`。\n- 内存/线程自动感知，自治程度在嵌入式库中突出 `社区共识`。"},
    "en": {"v": "Supported", "p": "Zero-config autonomy; few PRAGMAs",
           "b": "- Works out of the box; few PRAGMAs with sane defaults `(official docs)`.\n- Auto-detects memory/threads; notably autonomous among embedded DBs `(community consensus)`."}},
  "lineage": {
    "zh": {"v": "无", "p": "嵌入式场景无血缘，查证为无",
           "b": "- 无原生血缘；嵌入式定位通常不需要 `官方文档`。\n- 可通过上层工具链补齐 `社区共识`。"},
    "en": {"v": "Not supported", "p": "Verified none; embedded scope needs none",
           "b": "- No native lineage; embedded positioning rarely needs it `(official docs)`.\n- Upper toolchains can fill the gap `(community consensus)`."}},
  "storage_compute": {
    "zh": {"v": "有", "p": "存算一体：进程内嵌入式",
           "b": "- 进程内嵌入式，存储即本地文件，存算一体 `官方文档`。\n- 无网络开销，但无法独立扩展计算/存储 `社区共识`。"},
    "en": {"v": "Supported", "p": "Coupled: in-process embedded",
           "b": "- In-process embedded; storage is local files; coupled `(official docs)`.\n- No network overhead, but compute/storage can't scale independently `(community consensus)`."}},
  "multi_model": {
    "zh": {"v": "部分支持", "p": "关系+JSON+FTS/VSS 扩展",
           "b": "- JSON 类型，FTS（全文）、VSS（向量）为官方扩展 `官方文档`。\n- 无图引擎 `社区共识`。"},
    "en": {"v": "Partial", "p": "Relational + JSON + FTS/VSS extensions",
           "b": "- JSON type; FTS (full-text) and VSS (vector) as official extensions `(official docs)`.\n- No graph engine `(community consensus)`."}},
  "drivers": {
    "zh": {"v": "有", "p": "嵌入式驱动全：Python/R/JDBC/ODBC",
           "b": "- Python/R/Node/Java/JDBC/ODBC 官方驱动完备 `官方文档`。\n- 零依赖安装是开发体验优势 `社区共识`。"},
    "en": {"v": "Supported", "p": "Full embedded drivers: Python/R/JDBC/ODBC",
           "b": "- Complete official Python/R/Node/Java/JDBC/ODBC drivers `(official docs)`.\n- Zero-dependency install is a DX win `(community consensus)`."}}
}
CONTENT3_D["dynamodb"] = {
  "optimizer": {
    "zh": {"v": "不适用", "p": "无优化器：单表设计，查询固定",
           "b": "- 无 CBO/计划概念，性能由单表建模与 GSI 设计决定 `官方文档`。\n- 查询模式固定，可预测性强，但复杂查询需应用层组装 `社区共识`。"},
    "en": {"v": "N/A", "p": "No optimizer: single-table design, fixed patterns",
           "b": "- No CBO/plan concept; performance comes from single-table modeling and GSI design `(official docs)`.\n- Fixed access patterns are highly predictable, but complex queries need app-side assembly `(community consensus)`."}},
  "tuning": {
    "zh": {"v": "有", "p": "Serverless 自治：零调参",
           "b": "- 按需/预置+自动扩缩容，几乎零参数 `官方文档`。\n- 容量规划转为 WCU/RCU 成本规划 `社区共识`。"},
    "en": {"v": "Supported", "p": "Serverless autonomy: zero knobs",
           "b": "- On-demand/provisioned with auto scaling; near-zero parameters `(official docs)`.\n- Capacity planning becomes WCU/RCU cost planning `(community consensus)`."}},
  "lineage": {
    "zh": {"v": "部分支持", "p": "Glue Catalog 集成；无原生列级血缘",
           "b": "- 可导出/爬网至 Glue Data Catalog `官方文档`。\n- 无原生列级血缘 `社区共识`。"},
    "en": {"v": "Partial", "p": "Glue Catalog integration; no native column lineage",
           "b": "- Can export/crawl into Glue Data Catalog `(official docs)`.\n- No native column-level lineage `(community consensus)`."}},
  "storage_compute": {
    "zh": {"v": "有", "p": "全托管存算分离",
           "b": "- 全托管，存储自动分区扩缩，计算无感 `官方文档`。\n- 用户不感知架构，弹性由服务保证 `社区共识`。"},
    "en": {"v": "Supported", "p": "Fully managed disaggregation",
           "b": "- Fully managed; storage auto-partitions and scales invisibly `(official docs)`.\n- Architecture invisible to users; elasticity guaranteed by the service `(community consensus)`."}},
  "multi_model": {
    "zh": {"v": "无", "p": "纯 KV/文档，无多模",
           "b": "- 仅 KV/文档模型，无向量/全文/图原生能力 `官方文档`。"},
    "en": {"v": "Not supported", "p": "Pure KV/document; no multi-model",
           "b": "- KV/document only; no native vector/full-text/graph `(official docs)`."}},
  "drivers": {
    "zh": {"v": "有", "p": "AWS SDK 各语言；JDBC 靠 Simba",
           "b": "- AWS SDK（Java/Python/Node/Go）为一等接入 `官方文档`。\n- JDBC/ODBC 靠 Simba 第三方驱动 `社区共识`。"},
    "en": {"v": "Supported", "p": "AWS SDKs for all languages; JDBC/ODBC via Simba",
           "b": "- AWS SDKs (Java/Python/Node/Go) are first-class `(official docs)`.\n- JDBC/ODBC via third-party Simba drivers `(community consensus)`."}}
}
CONTENT3_D["edb"] = {
  "optimizer": {
    "zh": {"v": "有", "p": "PG 优化器+EDB 增强；Oracle 兼容 hint",
           "b": "- 继承 PG CBO，EDB 增加优化器增强与 Oracle 风格 hint 支持 `官方文档`。\n- Oracle 兼容模式下 hint 生态更丰富 `官方文档`。\n- 计划翻转治理仍依赖统计信息与 DBA 经验 `社区共识`。"},
    "en": {"v": "Supported", "p": "PG optimizer + EDB boosts; Oracle-style hints",
           "b": "- Inherits PG CBO plus EDB optimizer enhancements and Oracle-style hint support `(official docs)`.\n- Richer hint ecosystem in Oracle-compatibility mode `(official docs)`.\n- Plan-flip control still relies on statistics and DBA expertise `(community consensus)`."}},
  "tuning": {
    "zh": {"v": "部分支持", "p": "PG 参数体系+EDB 工具；自治中等",
           "b": "- 参数体系同 PG，EDB 提供 Postgres Enterprise Manager 诊断 `官方文档`。\n- 无全自治能力，调优仍需 DBA `社区共识`。"},
    "en": {"v": "Partial", "p": "PG parameters + EDB tooling; middling autonomy",
           "b": "- Same parameter system as PG, plus Postgres Enterprise Manager diagnostics `(official docs)`.\n- No full autonomy; tuning still needs DBAs `(community consensus)`."}},
  "lineage": {
    "zh": {"v": "部分支持", "p": "随 PG；第三方血缘集成",
           "b": "- 无原生血缘，靠 DataHub/Atlan 等第三方采集 PG 元数据 `社区共识`。"},
    "en": {"v": "Partial", "p": "As PG; third-party lineage integration",
           "b": "- No native lineage; relies on DataHub/Atlan harvesting PG metadata `(community consensus)`."}},
  "storage_compute": {
    "zh": {"v": "有", "p": "自建存算一体；BigAnimal 云版分离",
           "b": "- 自建部署经典存算一体 `官方文档`。\n- EDB BigAnimal 云版采用存算分离 `官方文档`。"},
    "en": {"v": "Supported", "p": "Self-hosted coupled; BigAnimal cloud disaggregated",
           "b": "- Self-hosted is classic coupled `(official docs)`.\n- EDB BigAnimal cloud uses disaggregated storage `(official docs)`."}},
  "multi_model": {
    "zh": {"v": "有", "p": "随 PG：jsonb+全文+PostGIS+pgvector",
           "b": "- 完整继承 PG 多模生态 `官方文档`。\n- Oracle 兼容模式不改变多模能力边界 `社区共识`。"},
    "en": {"v": "Supported", "p": "As PG: jsonb + full-text + PostGIS + pgvector",
           "b": "- Fully inherits PG's multi-model ecosystem `(official docs)`.\n- Oracle-compatibility mode doesn't change multi-model boundaries `(community consensus)`."}},
  "drivers": {
    "zh": {"v": "有", "p": "PG 驱动兼容+Oracle 兼容驱动",
           "b": "- PG 协议驱动全兼容，另提供 Oracle 兼容连接方式 `官方文档`。\n- JDBC/ODBC 完备 `社区共识`。"},
    "en": {"v": "Supported", "p": "PG-compatible + Oracle-compatible drivers",
           "b": "- Full PG-protocol driver compatibility plus Oracle-compatible connectivity `(official docs)`.\n- Complete JDBC/ODBC `(community consensus)`."}}
}
CONTENT3_D["etcd"] = {
  "optimizer": {
    "zh": {"v": "不适用", "p": "KV 存储无查询优化器",
           "b": "- 纯 KV 读写，无查询计划概念 `官方文档`。"},
    "en": {"v": "N/A", "p": "KV store has no query optimizer",
           "b": "- Pure KV reads/writes; no query-plan concept `(official docs)`."}},
  "tuning": {
    "zh": {"v": "部分支持", "p": "参数少：配额与压缩是调优点",
           "b": "- 参数精简，核心是 backend quota、compaction 周期 `官方文档`。\n- 大 value/高频 watch 是典型调优场景 `社区共识`。"},
    "en": {"v": "Partial", "p": "Few knobs: quota and compaction",
           "b": "- Lean parameters; the levers are backend quota and compaction intervals `(official docs)`.\n- Large values and high-frequency watches are the classic tuning cases `(community consensus)`."}},
  "lineage": {
    "zh": {"v": "不适用", "p": "KV 元数据存储，无血缘概念",
           "b": "- 定位是分布式 KV/配置中心，无数据血缘概念 `官方文档`。"},
    "en": {"v": "N/A", "p": "KV metadata store; no lineage concept",
           "b": "- A distributed KV/config store; no data-lineage concept `(official docs)`."}},
  "storage_compute": {
    "zh": {"v": "有", "p": "存算一体：Raft+bbolt 本地",
           "b": "- Raft 共识 + bbolt 本地存储，典型存算一体 `官方文档`。"},
    "en": {"v": "Supported", "p": "Coupled: Raft + bbolt local",
           "b": "- Raft consensus + bbolt local storage; classically coupled `(official docs)`."}},
  "multi_model": {
    "zh": {"v": "无", "p": "纯 KV，无多模",
           "b": "- 仅 KV 模型 `官方文档`。"},
    "en": {"v": "Not supported", "p": "Pure KV; no multi-model",
           "b": "- KV model only `(official docs)`."}},
  "drivers": {
    "zh": {"v": "有", "p": "gRPC 官方客户端：Go/Java/Python",
           "b": "- gRPC API，官方 Go/Java/Python 客户端 `官方文档`。\n- 无 JDBC/ODBC（KV 定位不需要）`社区共识`。"},
    "en": {"v": "Supported", "p": "Official gRPC clients: Go/Java/Python",
           "b": "- gRPC API with official Go/Java/Python clients `(official docs)`.\n- No JDBC/ODBC (unneeded for KV) `(community consensus)`."}}
}
CONTENT3_D["mariadb"] = {
  "optimizer": {
    "zh": {"v": "有", "p": "MySQL 衍生 CBO；hint 兼容",
           "b": "- 优化器源自 MySQL 并独立演进，EXPLAIN/hint 兼容 `官方文档`。\n- 统计信息引擎是差异点 `官方文档`。\n- 无计划冻结机制 `社区共识`。"},
    "en": {"v": "Supported", "p": "MySQL-derived CBO; compatible hints",
           "b": "- Optimizer forked from MySQL and evolved independently; EXPLAIN/hints compatible `(official docs)`.\n- Engine-independent statistics is a differentiator `(official docs)`.\n- No plan-freeze mechanism `(community consensus)`."}},
  "tuning": {
    "zh": {"v": "部分支持", "p": "参数多；调优复杂度同 MySQL",
           "b": "- 参数体系庞大，调优经验与 MySQL 通用 `社区共识`。\n- 自治能力弱 `社区共识`。"},
    "en": {"v": "Partial", "p": "Many parameters; MySQL-like tuning burden",
           "b": "- Large parameter surface; tuning knowledge transfers from MySQL `(community consensus)`.\n- Weak autonomy `(community consensus)`."}},
  "lineage": {
    "zh": {"v": "无", "p": "查证为无原生血缘",
           "b": "- 无原生血缘 `官方文档`。"},
    "en": {"v": "Not supported", "p": "Verified: no native lineage",
           "b": "- No native lineage `(official docs)`."}},
  "storage_compute": {
    "zh": {"v": "有", "p": "存算一体：本地盘架构",
           "b": "- 经典存算一体本地盘架构 `官方文档`。"},
    "en": {"v": "Supported", "p": "Coupled: local-disk architecture",
           "b": "- Classic coupled local-disk architecture `(official docs)`."}},
  "multi_model": {
    "zh": {"v": "部分支持", "p": "JSON 别名+全文；无向量",
           "b": "- JSON 为 LONGTEXT 别名，全文索引可用 `官方文档`。\n- 无原生向量/图 `社区共识`。"},
    "en": {"v": "Partial", "p": "JSON alias + full-text; no vectors",
           "b": "- JSON is a LONGTEXT alias; full-text indexes available `(official docs)`.\n- No native vector/graph `(community consensus)`."}},
  "drivers": {
    "zh": {"v": "有", "p": "MySQL 协议兼容，驱动通用",
           "b": "- MySQL 线协议兼容，Connector/J 等驱动通用 `官方文档`。"},
    "en": {"v": "Supported", "p": "MySQL-protocol compatible; shared drivers",
           "b": "- MySQL wire-protocol compatible; Connector/J and friends work `(official docs)`."}}
}
CONTENT3_D["milvus"] = {
  "optimizer": {
    "zh": {"v": "不适用", "p": "向量检索无传统 CBO；索引即计划",
           "b": "- 无 SQL 优化器；检索性能由索引类型（HNSW/IVF）与参数决定 `官方文档`。\n- 混合查询的过滤+向量顺序有内部启发式，非 CBO `社区共识`。"},
    "en": {"v": "N/A", "p": "No classic CBO for vector search; index is the plan",
           "b": "- No SQL optimizer; retrieval performance comes from index type (HNSW/IVF) and parameters `(official docs)`.\n- Hybrid filter-then-vector ordering uses internal heuristics, not a CBO `(community consensus)`."}},
  "tuning": {
    "zh": {"v": "部分支持", "p": "索引参数是核心调优点；门槛高",
           "b": "- HNSW 的 M/ef、IVF 的 nlist/nprobe 是核心调优点 `官方文档`。\n- 参数选错召回率/延迟断崖式下跌，调优门槛高 `社区共识`。"},
    "en": {"v": "Partial", "p": "Index params are the tuning surface; steep curve",
           "b": "- HNSW's M/ef and IVF's nlist/nprobe are the core levers `(official docs)`.\n- Wrong parameters crater recall/latency; steep tuning curve `(community consensus)`."}},
  "lineage": {
    "zh": {"v": "无", "p": "查证为无原生血缘",
           "b": "- 无原生数据血缘 `官方文档`。"},
    "en": {"v": "Not supported", "p": "Verified: no native lineage",
           "b": "- No native data lineage `(official docs)`."}},
  "storage_compute": {
    "zh": {"v": "有", "p": "存算分离：2.x 云原生架构",
           "b": "- 2.x 计算/存储/协调分离，对象存储存数据 `官方文档`。\n- 弹性扩缩计算节点不搬数据 `官方文档`。"},
    "en": {"v": "Supported", "p": "Disaggregated: 2.x cloud-native design",
           "b": "- 2.x separates compute/storage/coordination with object storage `(official docs)`.\n- Elastic compute scaling without data movement `(official docs)`."}},
  "multi_model": {
    "zh": {"v": "无", "p": "纯向量+标量过滤，无多模",
           "b": "- 纯向量检索引擎，标量字段仅作过滤 `官方文档`。"},
    "en": {"v": "Not supported", "p": "Pure vectors + scalar filtering",
           "b": "- Pure vector search engine; scalar fields for filtering only `(official docs)`."}},
  "drivers": {
    "zh": {"v": "有", "p": "PyMilvus/Java/Node/Go 官方 SDK",
           "b": "- 官方 Python/Java/Node.js/Go SDK 完备 `官方文档`。\n- RESTful API 可用 `官方文档`。"},
    "en": {"v": "Supported", "p": "Official PyMilvus/Java/Node/Go SDKs",
           "b": "- Complete official Python/Java/Node.js/Go SDKs `(official docs)`.\n- RESTful API available `(official docs)`."}}
}
CONTENT3_D["mongodb"] = {
  "optimizer": {
    "zh": {"v": "有", "p": "计划缓存+hint+索引过滤；8.0 改进",
           "b": "- 查询计划缓存，hint() 强制索引，index filters 可冻结计划 `官方文档`。\n- 8.0 查询引擎重写，复杂聚合计划质量提升 `官方文档`。\n- 计划缓存失效导致的抖动仍是排查难点 `社区共识`。"},
    "en": {"v": "Supported", "p": "Plan cache + hints + index filters; 8.0 rework",
           "b": "- Query plan cache, hint() to force indexes, index filters to pin plans `(official docs)`.\n- 8.0 query-engine rewrite improved complex aggregation plans `(official docs)`.\n- Jitter from plan-cache invalidation remains a debugging pain `(community consensus)`."}},
  "tuning": {
    "zh": {"v": "部分支持", "p": "参数少；Atlas 索引推荐部分自治",
           "b": "- 参数相对精简，调优核心在索引与 schema 设计 `官方文档`。\n- Atlas Performance Advisor 自动推荐索引 `官方文档`。\n- 分片键选错后期改造成本极高 `社区共识`。"},
    "en": {"v": "Partial", "p": "Few knobs; Atlas index advisor partly autonomous",
           "b": "- Lean parameters; tuning centers on indexes and schema design `(official docs)`.\n- Atlas Performance Advisor auto-recommends indexes `(official docs)`.\n- A wrong shard key is brutally expensive to fix later `(community consensus)`."}},
  "lineage": {
    "zh": {"v": "部分支持", "p": "无原生；Atlan/Manta 第三方集成",
           "b": "- 无原生血缘，靠 Atlan/Manta 等第三方 `社区共识`。\n- Atlas Data Federation 元数据可被采集 `官方文档`。"},
    "en": {"v": "Partial", "p": "No native; Atlan/Manta third-party integration",
           "b": "- No native lineage; third parties like Atlan/Manta `(community consensus)`.\n- Atlas Data Federation metadata can be harvested `(official docs)`."}},
  "storage_compute": {
    "zh": {"v": "有", "p": "默认存算一体；Atlas 有分离选项",
           "b": "- 副本集/分片本地盘，经典存算一体 `官方文档`。\n- Atlas 部分层级提供存算分离选项 `待验证`。"},
    "en": {"v": "Supported", "p": "Coupled by default; Atlas has separation options",
           "b": "- Replica sets/sharded clusters on local disks; classically coupled `(official docs)`.\n- Some Atlas tiers offer disaggregated options `(to be verified)`."}},
  "multi_model": {
    "zh": {"v": "有", "p": "文档+向量+全文+时序",
           "b": "- 文档原生，Atlas Vector Search、Atlas Search（全文）、时序集合 `官方文档`。\n- 无原生图引擎 `社区共识`。"},
    "en": {"v": "Supported", "p": "Document + vector + full-text + time-series",
           "b": "- Native documents, Atlas Vector Search, Atlas Search (full-text), time-series collections `(official docs)`.\n- No native graph engine `(community consensus)`."}},
  "drivers": {
    "zh": {"v": "有", "p": "官方驱动最全；BI Connector 给 JDBC",
           "b": "- 官方 Java/Python/Node/Go/C# 驱动业界最全之一 `官方文档`。\n- BI Connector 提供 JDBC/ODBC 给 BI 工具 `官方文档`。"},
    "en": {"v": "Supported", "p": "Most complete official drivers; BI Connector for JDBC",
           "b": "- Among the most complete official Java/Python/Node/Go/C# drivers `(official docs)`.\n- BI Connector exposes JDBC/ODBC for BI tools `(official docs)`."}}
}
CONTENT3_D["mysql"] = {
  "optimizer": {
    "zh": {"v": "有", "p": "CBO+丰富 hint；无计划冻结，翻转常见",
           "b": "- CBO + EXPLAIN，hint 丰富（STRAIGHT_JOIN、FORCE INDEX、SET_VAR、QB_NAME）`官方文档`。\n- 直方图统计信息弱，无 Oracle 式计划基线冻结 `官方文档`。\n- 统计信息过期/参数变更导致计划翻转是常见生产问题 `社区共识`。"},
    "en": {"v": "Supported", "p": "CBO + rich hints; no plan freeze, flips common",
           "b": "- CBO + EXPLAIN with rich hints (STRAIGHT_JOIN, FORCE INDEX, SET_VAR, QB_NAME) `(official docs)`.\n- Weak histogram statistics; no Oracle-style plan baseline freeze `(official docs)`.\n- Stale statistics/parameter changes causing plan flips are a common production issue `(community consensus)`."}},
  "tuning": {
    "zh": {"v": "部分支持", "p": "参数数百；performance_schema 强",
           "b": "- 可调参数数百，调优复杂度高是 DBA 共识 `社区共识`。\n- performance_schema + sys schema 诊断体系完善 `官方文档`。\n- 无自动索引/自动重写，自治能力弱 `官方文档`。"},
    "en": {"v": "Partial", "p": "Hundreds of params; strong performance_schema",
           "b": "- Hundreds of tunable parameters; tuning complexity is DBA consensus `(community consensus)`.\n- performance_schema + sys schema give a complete diagnostic stack `(official docs)`.\n- No auto-indexing/rewrites; weak autonomy `(official docs)`."}},
  "lineage": {
    "zh": {"v": "无", "p": "查证为无原生血缘",
           "b": "- 无原生数据血缘/目录 `官方文档`。\n- 靠 Atlas/DataHub 等第三方采集 binlog/元数据 `社区共识`。"},
    "en": {"v": "Not supported", "p": "Verified: no native lineage",
           "b": "- No native data lineage/catalog `(official docs)`.\n- Third parties like Atlas/DataHub harvest binlog/metadata `(community consensus)`."}},
  "storage_compute": {
    "zh": {"v": "有", "p": "存算一体：本地盘 InnoDB",
           "b": "- 经典存算一体：InnoDB 数据存本地盘 `官方文档`。\n- HeatWave 是 Oracle 云专属的存算分离形态，不计入开源版 `社区共识`。"},
    "en": {"v": "Supported", "p": "Coupled: local-disk InnoDB",
           "b": "- Classic coupled design: InnoDB data on local disks `(official docs)`.\n- HeatWave's disaggregation is Oracle-cloud-only, not in the OSS edition `(community consensus)`."}},
  "multi_model": {
    "zh": {"v": "部分支持", "p": "JSON+全文；无向量/图",
           "b": "- JSON 类型+多值索引/虚拟列，全文索引可用 `官方文档`。\n- 无原生向量、图能力 `官方文档`。"},
    "en": {"v": "Partial", "p": "JSON + full-text; no vector/graph",
           "b": "- JSON type with multi-valued indexes/generated columns; full-text indexes available `(official docs)`.\n- No native vector or graph `(official docs)`."}},
  "drivers": {
    "zh": {"v": "有", "p": "驱动生态最广：Connector 全家桶",
           "b": "- 官方 Connector/J、Connector/NET、Connector/Python、mysqlclient `官方文档`。\n- ORM/工具支持度业界最广 `社区共识`。"},
    "en": {"v": "Supported", "p": "Widest driver ecosystem: full Connector family",
           "b": "- Official Connector/J, Connector/NET, Connector/Python, mysqlclient `(official docs)`.\n- Broadest ORM/tool support in the industry `(community consensus)`."}}
}
CONTENT3_D["oceanbase"] = {
  "optimizer": {
    "zh": {"v": "有", "p": "CBO 双模式；Oracle hint+outline 绑定",
           "b": "- 自研 CBO，MySQL/Oracle 双模式，Oracle 兼容模式 hint 丰富 `官方文档`。\n- outline 机制可绑定/冻结执行计划 `官方文档`。\n- 分布式计划（分区裁剪、下推）的调优心智与单机不同 `社区共识`。"},
    "en": {"v": "Supported", "p": "Dual-mode CBO; Oracle hints + outline binding",
           "b": "- Homegrown CBO with MySQL/Oracle dual modes; rich hints in Oracle mode `(official docs)`.\n- Outline mechanism can bind/freeze execution plans `(official docs)`.\n- Distributed-plan tuning (partition pruning, pushdown) differs mentally from single-node `(community consensus)`."}},
  "tuning": {
    "zh": {"v": "部分支持", "p": "参数上千；OCP 诊断强，自治中等",
           "b": "- 参数上千，调优复杂度高 `官方文档`。\n- OCP 提供全链路诊断、SQL 限流 `官方文档`。\n- 自治能力中等，深度调优仍需专家 `社区共识`。"},
    "en": {"v": "Partial", "p": "1000+ params; strong OCP diagnostics, middling autonomy",
           "b": "- 1000+ parameters; high tuning complexity `(official docs)`.\n- OCP gives end-to-end diagnostics and SQL throttling `(official docs)`.\n- Middling autonomy; deep tuning still needs experts `(community consensus)`."}},
  "lineage": {
    "zh": {"v": "部分支持", "p": "DataWorks 集成；无原生列级血缘",
           "b": "- 可通过阿里 DataWorks 数据地图做血缘 `官方文档`。\n- 无数据库原生列级血缘 `社区共识`。"},
    "en": {"v": "Partial", "p": "DataWorks integration; no native column lineage",
           "b": "- Lineage via Alibaba DataWorks data map `(official docs)`.\n- No native database column-level lineage `(community consensus)`."}},
  "storage_compute": {
    "zh": {"v": "有", "p": "LSM 存算一体为主；4.x 分离版待验证",
           "b": "- 经典 LSM 本地盘存算一体 `官方文档`。\n- 4.x 推出存算分离版本，生产成熟度待验证 `待验证`。"},
    "en": {"v": "Supported", "p": "LSM-coupled primarily; 4.x separated edition TBD",
           "b": "- Classic LSM on local disks; coupled `(official docs)`.\n- 4.x introduced a disaggregated edition; production maturity to be verified `(to be verified)`."}},
  "multi_model": {
    "zh": {"v": "部分支持", "p": "关系+JSON+全文+向量（4.x AI）",
           "b": "- JSON、全文索引，4.x 增加向量检索能力 `官方文档`。\n- 无原生图引擎 `社区共识`。"},
    "en": {"v": "Partial", "p": "Relational + JSON + full-text + vectors (4.x AI)",
           "b": "- JSON, full-text indexes, and vector search added in 4.x `(official docs)`.\n- No native graph engine `(community consensus)`."}},
  "drivers": {
    "zh": {"v": "有", "p": "MySQL/Oracle 双协议驱动兼容",
           "b": "- MySQL 协议驱动直接兼容，Oracle 模式提供兼容驱动 `官方文档`。\n- JDBC/ODBC 完备 `社区共识`。"},
    "en": {"v": "Supported", "p": "Dual MySQL/Oracle protocol driver compatibility",
           "b": "- MySQL-protocol drivers work directly; Oracle mode ships compatible drivers `(official docs)`.\n- Complete JDBC/ODBC `(community consensus)`."}}
}
CONTENT3_D["oracle"] = {
  "optimizer": {
    "zh": {"v": "有", "p": "CBO 标杆；hint 最丰富；SPM 冻结",
           "b": "- CBO 业界标杆，hint 上百个，SQL Plan Baseline（SPM）冻结计划防翻转 `官方文档`。\n- AWR/ASH 让计划问题可追溯 `官方文档`。\n- 优化器行为版本间差异大，升级需 SPM 兜底 `社区共识`。"},
    "en": {"v": "Supported", "p": "CBO benchmark; richest hints; SPM plan freeze",
           "b": "- Industry-benchmark CBO, 100+ hints, SQL Plan Baselines (SPM) freeze plans against flips `(official docs)`.\n- AWR/ASH make plan issues traceable `(official docs)`.\n- Optimizer behavior varies across versions; upgrades need SPM as a safety net `(community consensus)`."}},
  "tuning": {
    "zh": {"v": "有", "p": "参数上千但 ADDM/AWR 自治最强",
           "b": "- 参数上千，复杂度最高一档 `官方文档`。\n- ADDM 自动诊断+建议，AWR 完备，自治数据库进一步自治 `官方文档`。\n- 工具强但学习曲线陡峭 `社区共识`。"},
    "en": {"v": "Supported", "p": "1000+ params but strongest ADDM/AWR autonomy",
           "b": "- 1000+ parameters; highest complexity tier `(official docs)`.\n- ADDM auto-diagnosis with advice, complete AWR; Autonomous DB goes further `(official docs)`.\n- Powerful tooling but a steep learning curve `(community consensus)`."}},
  "lineage": {
    "zh": {"v": "部分支持", "p": "OEM/Data Catalog；原生列级弱",
           "b": "- Oracle Enterprise Manager、Data Catalog 可做元数据管理 `官方文档`。\n- 原生列级血缘弱，靠第三方 `社区共识`。"},
    "en": {"v": "Partial", "p": "OEM/Data Catalog; weak native column lineage",
           "b": "- Oracle Enterprise Manager and Data Catalog cover metadata management `(official docs)`.\n- Weak native column-level lineage; third parties fill in `(community consensus)`."}},
  "storage_compute": {
    "zh": {"v": "有", "p": "混合：ASM 一体+Exadata 融合+云分离",
           "b": "- 传统 ASM 存算一体；Exadata 存储层计算下沉（Smart Scan）`官方文档`。\n- 云自治库底层存算分离 `官方文档`。"},
    "en": {"v": "Supported", "p": "Hybrid: ASM coupled + Exadata offload + cloud split",
           "b": "- Traditional ASM coupled; Exadata pushes compute to storage (Smart Scan) `(official docs)`.\n- Cloud Autonomous DB is disaggregated underneath `(official docs)`."}},
  "multi_model": {
    "zh": {"v": "有", "p": "关系+JSON+全文+空间+图+23ai 向量",
           "b": "- JSON、全文、空间、图，23ai 增加 AI Vector Search `官方文档`。\n- 一库多用能力最全之一 `社区共识`。"},
    "en": {"v": "Supported", "p": "Relational + JSON + text + spatial + graph + 23ai vectors",
           "b": "- JSON, full-text, spatial, graph, plus AI Vector Search in 23ai `(official docs)`.\n- Among the most complete multi-model offerings `(community consensus)`."}},
  "drivers": {
    "zh": {"v": "有", "p": "ojdbc/ODP.NET 官方驱动完备",
           "b": "- ojdbc、ODBC、ODP.NET、各语言驱动官方完备 `官方文档`。\n- 驱动版本与数据库版本匹配要求严格 `社区共识`。"},
    "en": {"v": "Supported", "p": "Complete ojdbc/ODP.NET official drivers",
           "b": "- Complete official ojdbc, ODBC, ODP.NET, and language drivers `(official docs)`.\n- Strict driver-to-database version matching required `(community consensus)`."}}
}
CONTENT3_D["polardb"] = {
  "optimizer": {
    "zh": {"v": "有", "p": "MySQL/PG 衍生+并行/HTAP 增强",
           "b": "- 继承引擎优化器，PolarDB 增加并行查询、IMCI 列存索引的优化器适配 `官方文档`。\n- hint 行为同原生引擎 `社区共识`。"},
    "en": {"v": "Supported", "p": "MySQL/PG-derived + parallel/HTAP boosts",
           "b": "- Inherits engine optimizers; PolarDB adds parallel query and IMCI columnar-index optimizer support `(official docs)`.\n- Hint behavior matches native engines `(community consensus)`."}},
  "tuning": {
    "zh": {"v": "有", "p": "DAS 自动诊断：索引推荐+SQL 优化",
           "b": "- 阿里云 DAS 提供自动 SQL 优化、索引推荐、空间分析 `官方文档`。\n- 参数组可调，自治能力在国产云库中突出 `社区共识`。"},
    "en": {"v": "Supported", "p": "DAS auto-diagnosis: index advisor + SQL tuning",
           "b": "- Alibaba DAS offers automatic SQL tuning, index recommendations, space analysis `(official docs)`.\n- Tunable parameter groups; notably autonomous among China cloud DBs `(community consensus)`."}},
  "lineage": {
    "zh": {"v": "部分支持", "p": "DataWorks 数据地图集成",
           "b": "- 通过 DataWorks 数据地图做血缘 `官方文档`。\n- 无数据库原生列级血缘 `社区共识`。"},
    "en": {"v": "Partial", "p": "DataWorks data-map integration",
           "b": "- Lineage via DataWorks data map `(official docs)`.\n- No native database column-level lineage `(community consensus)`."}},
  "storage_compute": {
    "zh": {"v": "有", "p": "存算分离：PolarStore 共享存储",
           "b": "- 计算与 PolarStore 分布式共享存储分离，一写多读 `官方文档`。\n- 只读节点秒级扩展不搬数据 `官方文档`。"},
    "en": {"v": "Supported", "p": "Disaggregated: PolarStore shared storage",
           "b": "- Compute separated from PolarStore distributed shared storage; single-write multi-read `(official docs)`.\n- Read replicas scale in seconds without data movement `(official docs)`."}},
  "multi_model": {
    "zh": {"v": "部分支持", "p": "随引擎：JSON/PG 向量生态",
           "b": "- PolarDB-PG 支持 pgvector 等 PG 生态 `官方文档`。\n- 无原生图/全文独立引擎 `社区共识`。"},
    "en": {"v": "Partial", "p": "Engine-dependent: JSON/PG vector ecosystem",
           "b": "- PolarDB-PG supports pgvector and the PG ecosystem `(official docs)`.\n- No standalone native graph/full-text engine `(community consensus)`."}},
  "drivers": {
    "zh": {"v": "有", "p": "MySQL/PG 协议兼容",
           "b": "- 完全兼容 MySQL/PG 协议与驱动 `官方文档`。"},
    "en": {"v": "Supported", "p": "MySQL/PG protocol compatible",
           "b": "- Fully compatible with MySQL/PG protocols and drivers `(official docs)`."}}
}
CONTENT3_D["postgresql"] = {
  "optimizer": {
    "zh": {"v": "有", "p": "CBO+GEQO；hint 需扩展；无冻结",
           "b": "- CBO 完备（GEQO 处理多表 JOIN），EXPLAIN (ANALYZE/BUFFERS) 业界标杆 `官方文档`。\n- hint 需 pg_hint_plan 扩展，非官方内置 `社区共识`。\n- 无计划冻结机制，统计信息过期致翻转是常见问题 `社区共识`。"},
    "en": {"v": "Supported", "p": "CBO + GEQO; hints need pg_hint_plan; no freeze",
           "b": "- Complete CBO (GEQO for many-table JOINs); EXPLAIN (ANALYZE/BUFFERS) is a benchmark `(official docs)`.\n- Hints need the pg_hint_plan extension, not built-in `(community consensus)`.\n- No plan-freeze mechanism; stale statistics flips are common `(community consensus)`."}},
  "tuning": {
    "zh": {"v": "有", "p": "参数约 350；autovacuum+诊断强",
           "b": "- 参数约 350 个，autovacuum 自动维护是亮点 `官方文档`。\n- pg_stat_statements、auto_explain 诊断生态完善 `社区共识`。\n- 无自动索引，自治弱于商业库 `社区共识`。"},
    "en": {"v": "Supported", "p": "~350 params; autovacuum + strong diagnostics",
           "b": "- ~350 parameters; autovacuum auto-maintenance is a highlight `(official docs)`.\n- pg_stat_statements and auto_explain give a complete diagnostic ecosystem `(community consensus)`.\n- No auto-indexing; less autonomous than commercial DBs `(community consensus)`."}},
  "lineage": {
    "zh": {"v": "部分支持", "p": "无原生；DataHub 采集 PG 元数据",
           "b": "- 无原生血缘，DataHub/Atlan 可采集 PG 元数据 `社区共识`。\n- pg_stat_statements 可作为血缘推断数据源 `社区实测`。"},
    "en": {"v": "Partial", "p": "No native; DataHub harvests PG metadata",
           "b": "- No native lineage; DataHub/Atlan can harvest PG metadata `(community consensus)`.\n- pg_stat_statements can feed lineage inference `(community tested)`."}},
  "storage_compute": {
    "zh": {"v": "有", "p": "开源版存算一体；云托管多分离",
           "b": "- 开源版经典本地盘存算一体 `官方文档`。\n- 云托管版（RDS/Aurora/AlloyDB）多为存算分离 `社区共识`。"},
    "en": {"v": "Supported", "p": "OSS coupled; cloud-hosted mostly split",
           "b": "- OSS edition is classic local-disk coupled `(official docs)`.\n- Cloud-hosted editions (RDS/Aurora/AlloyDB) are mostly disaggregated `(community consensus)`."}},
  "multi_model": {
    "zh": {"v": "有", "p": "一库多用标杆：jsonb+全文+GIS+向量",
           "b": "- jsonb(GIN)、全文检索、PostGIS、pgvector，扩展生态最强 `官方文档`。\n- 多模能力是 PG 护城河 `社区共识`。"},
    "en": {"v": "Supported", "p": "Multi-model benchmark: jsonb + FTS + PostGIS + vectors",
           "b": "- jsonb (GIN), full-text, PostGIS, pgvector; strongest extension ecosystem `(official docs)`.\n- Multi-model breadth is PG's moat `(community consensus)`."}},
  "drivers": {
    "zh": {"v": "有", "p": "libpq/pgjdbc/psqlODBC 完备",
           "b": "- libpq、pgjdbc、psqlODBC 官方完备 `官方文档`。\n- 各语言驱动质量高 `社区共识`。"},
    "en": {"v": "Supported", "p": "libpq/pgjdbc/psqlODBC; complete per-language",
           "b": "- Complete official libpq, pgjdbc, psqlODBC `(official docs)`.\n- High-quality drivers across languages `(community consensus)`."}}
}
CONTENT3_D["qdrant"] = {
  "optimizer": {
    "zh": {"v": "不适用", "p": "向量检索无传统 CBO",
           "b": "- 无 SQL 优化器；检索质量由 HNSW/量化配置决定 `官方文档`。"},
    "en": {"v": "N/A", "p": "No classic CBO for vector search",
           "b": "- No SQL optimizer; retrieval quality comes from HNSW/quantization config `(official docs)`."}},
  "tuning": {
    "zh": {"v": "部分支持", "p": "HNSW/量化参数是调优点",
           "b": "- m/ef_construct、量化、on_disk 等参数是调优核心 `官方文档`。\n- 参数语义清晰，调优门槛低于 Milvus `社区共识`。"},
    "en": {"v": "Partial", "p": "HNSW/quantization params are the levers",
           "b": "- m/ef_construct, quantization, and on_disk are the tuning core `(official docs)`.\n- Clear parameter semantics; gentler curve than Milvus `(community consensus)`."}},
  "lineage": {
    "zh": {"v": "无", "p": "查证为无原生血缘",
           "b": "- 无原生数据血缘 `官方文档`。"},
    "en": {"v": "Not supported", "p": "Verified: no native lineage",
           "b": "- No native data lineage `(official docs)`."}},
  "storage_compute": {
    "zh": {"v": "有", "p": "存算一体：本地盘 mmap",
           "b": "- 数据存本地（mmap），存算一体 `官方文档`。\n- 分布式模式分片仍在节点本地 `官方文档`。"},
    "en": {"v": "Supported", "p": "Coupled: local-disk mmap",
           "b": "- Data on local disks (mmap); coupled `(official docs)`.\n- Distributed-mode shards stay node-local `(official docs)`."}},
  "multi_model": {
    "zh": {"v": "无", "p": "纯向量+payload 过滤",
           "b": "- 纯向量检索引擎，payload 仅作过滤 `官方文档`。"},
    "en": {"v": "Not supported", "p": "Pure vectors + payload filtering",
           "b": "- Pure vector search engine; payloads for filtering only `(official docs)`."}},
  "drivers": {
    "zh": {"v": "有", "p": "Python/Rust/TS/Go 官方客户端",
           "b": "- 官方 Python/Rust/TypeScript/Go 客户端 `官方文档`。\n- REST/gRPC 双接口 `官方文档`。"},
    "en": {"v": "Supported", "p": "Official Python/Rust/TS/Go clients",
           "b": "- Official Python/Rust/TypeScript/Go clients `(official docs)`.\n- Dual REST/gRPC APIs `(official docs)`."}}
}
CONTENT3_D["redis-valkey"] = {
  "optimizer": {
    "zh": {"v": "不适用", "p": "命令式 KV，无查询优化器",
           "b": "- 命令式访问，无查询计划概念 `官方文档`。\n- RediSearch 查询有内部优化但非 CBO `社区共识`。"},
    "en": {"v": "N/A", "p": "Imperative KV; no query optimizer",
           "b": "- Imperative access; no query-plan concept `(official docs)`.\n- RediSearch queries have internal optimization but no CBO `(community consensus)`."}},
  "tuning": {
    "zh": {"v": "部分支持", "p": "参数少；调优靠内存与持久化",
           "b": "- redis.conf 参数精简，调优核心是 maxmemory 策略与 RDB/AOF `官方文档`。\n- 大 key/慢查询是常规治理项 `社区共识`。"},
    "en": {"v": "Partial", "p": "Few knobs; tune memory and persistence",
           "b": "- Lean redis.conf; tuning centers on maxmemory policy and RDB/AOF `(official docs)`.\n- Big keys/slow queries are routine governance `(community consensus)`."}},
  "lineage": {
    "zh": {"v": "不适用", "p": "KV 缓存定位，无血缘概念",
           "b": "- 定位缓存/KV，无数据血缘概念 `官方文档`。"},
    "en": {"v": "N/A", "p": "KV cache role; no lineage concept",
           "b": "- Positioned as cache/KV; no data-lineage concept `(official docs)`."}},
  "storage_compute": {
    "zh": {"v": "有", "p": "存算一体：内存+本地盘",
           "b": "- 内存为主+本地持久化，典型存算一体 `官方文档`。"},
    "en": {"v": "Supported", "p": "Coupled: memory + local disk",
           "b": "- Memory-first with local persistence; classically coupled `(official docs)`."}},
  "multi_model": {
    "zh": {"v": "部分支持", "p": "KV+JSON+向量+时序+图（模块）",
           "b": "- JSON、RediSearch（全文+向量）、时序、图靠模块扩展 `官方文档`。\n- Valkey 延续模块生态 `社区共识`。"},
    "en": {"v": "Partial", "p": "KV + JSON + vectors + time-series + graph (modules)",
           "b": "- JSON, RediSearch (full-text + vectors), time-series, and graph via modules `(official docs)`.\n- Valkey continues the module ecosystem `(community consensus)`."}},
  "drivers": {
    "zh": {"v": "有", "p": "客户端生态最全之一",
           "b": "- redis-py、Jedis、node-redis、go-redis 等，覆盖所有主流语言 `官方文档`。\n- RESP 协议简单，客户端质量高 `社区共识`。"},
    "en": {"v": "Supported", "p": "Among the fullest client ecosystems",
           "b": "- redis-py, Jedis, node-redis, go-redis covering all major languages `(official docs)`.\n- Simple RESP protocol; high client quality `(community consensus)`."}}
}
CONTENT3_D["snowflake"] = {
  "optimizer": {
    "zh": {"v": "有", "p": "云原生 CBO 全自动；无 hint",
           "b": "- 云原生 CBO，查询自动优化，EXPLAIN 可用 `官方文档`。\n- 无 hint 机制，计划干预手段少 `官方文档`。\n- 托管模式下计划翻转风险低 `社区共识`。"},
    "en": {"v": "Supported", "p": "Fully automatic cloud-native CBO; no hints",
           "b": "- Cloud-native CBO with automatic optimization; EXPLAIN available `(official docs)`.\n- No hint mechanism; few plan-steering levers `(official docs)`.\n- Low plan-flip risk under managed operation `(community consensus)`."}},
  "tuning": {
    "zh": {"v": "有", "p": "零调参标杆：自动 clustering/scaling",
           "b": "- 几乎零参数，自动微分区、自动 clustering、仓库自动扩缩 `官方文档`。\n- 调优转为仓库规格与成本管理 `社区共识`。"},
    "en": {"v": "Supported", "p": "Zero-knob benchmark: auto clustering/scaling",
           "b": "- Near-zero parameters; automatic micro-partitioning, clustering, warehouse scaling `(official docs)`.\n- Tuning becomes warehouse sizing and cost management `(community consensus)`."}},
  "lineage": {
    "zh": {"v": "有", "p": "原生血缘：DEPENDENCIES+ACCESS_HISTORY",
           "b": "- OBJECT_DEPENDENCIES、ACCESS_HISTORY 提供表/列级血缘 `官方文档`。\n- Horizon 目录统一治理 `官方文档`。"},
    "en": {"v": "Supported", "p": "Native lineage: OBJECT_DEPENDENCIES + ACCESS_HISTORY",
           "b": "- OBJECT_DEPENDENCIES and ACCESS_HISTORY give table/column lineage `(official docs)`.\n- Horizon catalog unifies governance `(official docs)`."}},
  "storage_compute": {
    "zh": {"v": "有", "p": "存算分离标杆：存储+虚拟仓库",
           "b": "- 集中存储层+独立虚拟仓库，存算分离标杆 `官方文档`。\n- 多集群共享同一份数据无拷贝 `官方文档`。"},
    "en": {"v": "Supported", "p": "Disaggregation benchmark: storage + virtual warehouses",
           "b": "- Centralized storage with independent virtual warehouses; the disaggregation benchmark `(official docs)`.\n- Multiple clusters share one data copy `(official docs)`."}},
  "multi_model": {
    "zh": {"v": "有", "p": "VARIANT 半结构化+全文+向量",
           "b": "- VARIANT 半结构化、全文搜索、Cortex 向量、非结构化文件 `官方文档`。\n- 无原生图引擎 `社区共识`。"},
    "en": {"v": "Supported", "p": "VARIANT semi-structured + FTS + vectors + unstructured",
           "b": "- VARIANT semi-structured, full-text search, Cortex vectors, unstructured files `(official docs)`.\n- No native graph engine `(community consensus)`."}},
  "drivers": {
    "zh": {"v": "有", "p": "JDBC/ODBC/Python/Go/Spark 官方全",
           "b": "- 官方 JDBC/ODBC/Python/Node.js/Go/.NET/Spark 连接器 `官方文档`。\n- BI 生态支持最全一档 `社区共识`。"},
    "en": {"v": "Supported", "p": "Full official JDBC/ODBC/Python/Node/Go/Spark",
           "b": "- Official JDBC/ODBC/Python/Node.js/Go/.NET/Spark connectors `(official docs)`.\n- Top-tier BI ecosystem support `(community consensus)`."}}
}
CONTENT3_D["spanner"] = {
  "optimizer": {
    "zh": {"v": "有", "p": "分布式 CBO；优化器版本化",
           "b": "- 分布式 CBO，查询优化器版本化可控升级 `官方文档`。\n- hint 有限（JOIN 方法/顺序）`官方文档`。\n- 计划翻转多与 interleaved 表设计相关 `社区共识`。"},
    "en": {"v": "Supported", "p": "Distributed CBO; versioned optimizer; limited hints",
           "b": "- Distributed CBO with versioned query optimizer for controlled upgrades `(official docs)`.\n- Limited hints (JOIN methods/order) `(official docs)`.\n- Flips often trace to interleaved-table design `(community consensus)`."}},
  "tuning": {
    "zh": {"v": "有", "p": "自治标杆：自动分片，零调参",
           "b": "- 自动分片、自动 rebalance，几乎无调参 `官方文档`。\n- 性能问题多源于 schema 设计而非参数 `社区共识`。"},
    "en": {"v": "Supported", "p": "Autonomy benchmark: auto-sharding, zero knobs",
           "b": "- Automatic sharding and rebalancing; near-zero knobs `(official docs)`.\n- Performance issues stem from schema design, not parameters `(community consensus)`."}},
  "lineage": {
    "zh": {"v": "有", "p": "Dataplex/Datastream 血缘集成",
           "b": "- 与 Dataplex 数据血缘、Data Catalog 集成 `官方文档`。"},
    "en": {"v": "Supported", "p": "Dataplex/Datastream lineage integration",
           "b": "- Integrates with Dataplex data lineage and Data Catalog `(official docs)`."}},
  "storage_compute": {
    "zh": {"v": "有", "p": "存算分离：Colossus+分布式计算",
           "b": "- 存储（Colossus）与计算分离的全球分布式架构 `官方文档`。"},
    "en": {"v": "Supported", "p": "Disaggregated: Colossus + distributed compute",
           "b": "- Globally distributed architecture separating Colossus storage from compute `(official docs)`."}},
  "multi_model": {
    "zh": {"v": "部分支持", "p": "关系+JSON+全文；向量待验证",
           "b": "- JSON 类型、全文搜索（2023+）`官方文档`。\n- 向量检索能力待验证 `待验证`。"},
    "en": {"v": "Partial", "p": "Relational + JSON + full-text; vectors TBD",
           "b": "- JSON type and full-text search (2023+) `(official docs)`.\n- Vector search capability to be verified `(to be verified)`."}},
  "drivers": {
    "zh": {"v": "有", "p": "官方多语言客户端；JDBC 靠 Simba",
           "b": "- 官方 Java/Python/Node/Go 客户端 `官方文档`。\n- JDBC/ODBC 靠 Simba 第三方 `社区共识`。"},
    "en": {"v": "Supported", "p": "Official multi-language clients; JDBC/ODBC via Simba",
           "b": "- Official Java/Python/Node/Go clients `(official docs)`.\n- JDBC/ODBC via third-party Simba `(community consensus)`."}}
}
CONTENT3_D["sqlserver"] = {
  "optimizer": {
    "zh": {"v": "有", "p": "CBO+Query Store 强制；自动修正",
           "b": "- CBO + hint（OPTION/USE PLAN），Query Store 可强制/冻结计划 `官方文档`。\n- Automatic Plan Correction 自动回退退化计划 `官方文档`。\n- 计划翻转治理在商业库中最成熟一档 `社区共识`。"},
    "en": {"v": "Supported", "p": "CBO + Query Store plan forcing; auto correction",
           "b": "- CBO + hints (OPTION/USE PLAN); Query Store can force/freeze plans `(official docs)`.\n- Automatic Plan Correction regresses degraded plans automatically `(official docs)`.\n- Among the most mature plan-flip controls in commercial DBs `(community consensus)`."}},
  "tuning": {
    "zh": {"v": "部分支持", "p": "参数精简；自动调优可建索引",
           "b": "- 参数相对精简，automatic tuning 可自动创建/删除索引 `官方文档`。\n- Query Store+扩展事件诊断完善 `官方文档`。\n- 深度调优仍需 DBA `社区共识`。"},
    "en": {"v": "Partial", "p": "Lean params; auto-tuning can build indexes",
           "b": "- Relatively lean parameters; automatic tuning can create/drop indexes `(official docs)`.\n- Query Store + Extended Events diagnostics are complete `(official docs)`.\n- Deep tuning still needs DBAs `(community consensus)`."}},
  "lineage": {
    "zh": {"v": "部分支持", "p": "Purview 集成；原生有限",
           "b": "- Microsoft Purview 做血缘与目录 `官方文档`。\n- 数据库原生血缘能力有限 `社区共识`。"},
    "en": {"v": "Partial", "p": "Purview integration; limited native",
           "b": "- Microsoft Purview covers lineage and catalog `(official docs)`.\n- Limited native database lineage `(community consensus)`."}},
  "storage_compute": {
    "zh": {"v": "有", "p": "传统存算一体；Hyperscale 分离",
           "b": "- 传统部署本地盘存算一体 `官方文档`。\n- Azure Hyperscale 采用存算分离 `官方文档`。"},
    "en": {"v": "Supported", "p": "Traditional coupled; Hyperscale split",
           "b": "- Traditional deployments are local-disk coupled `(official docs)`.\n- Azure Hyperscale uses disaggregated storage `(official docs)`."}},
  "multi_model": {
    "zh": {"v": "部分支持", "p": "关系+JSON+全文+空间+图；向量待验证",
           "b": "- JSON、全文、空间、图（2017+）`官方文档`。\n- 原生向量支持待验证 `待验证`。"},
    "en": {"v": "Partial", "p": "Relational + JSON + FTS + spatial + graph; vectors TBD",
           "b": "- JSON, full-text, spatial, graph (2017+) `(official docs)`.\n- Native vector support to be verified `(to be verified)`."}},
  "drivers": {
    "zh": {"v": "有", "p": "mssql-jdbc/ODBC/SqlClient 完备",
           "b": "- 官方 JDBC、ODBC、SqlClient（.NET）完备 `官方文档`。\n- 微软生态驱动质量高 `社区共识`。"},
    "en": {"v": "Supported", "p": "Complete mssql-jdbc/ODBC/SqlClient",
           "b": "- Complete official JDBC, ODBC, SqlClient (.NET) `(official docs)`.\n- High driver quality in the Microsoft ecosystem `(community consensus)`."}}
}
CONTENT3_D["starrocks"] = {
  "optimizer": {
    "zh": {"v": "有", "p": "OLAP CBO 标杆；hint 可用",
           "b": "- 自研 CBO 在 OLAP 场景计划质量突出 `官方文档`。\n- 支持 leading 等 hint 干预 `官方文档`。\n- 统计信息自动收集，翻转治理持续改进 `社区共识`。"},
    "en": {"v": "Supported", "p": "OLAP CBO benchmark; hints available",
           "b": "- Homegrown CBO with standout plan quality for OLAP `(official docs)`.\n- Supports leading and similar hints `(official docs)`.\n- Auto-collected statistics; flip controls keep improving `(community consensus)`."}},
  "tuning": {
    "zh": {"v": "部分支持", "p": "参数可调；调优靠建模",
           "b": "- BE/FE 参数可调，核心在建表与物化 `官方文档`。\n- 自治中等 `社区共识`。"},
    "en": {"v": "Partial", "p": "Tunable params; tuning lives in modeling",
           "b": "- BE/FE parameters tunable, but table design and materialization matter most `(official docs)`.\n- Middling autonomy `(community consensus)`."}},
  "lineage": {
    "zh": {"v": "无", "p": "查证为无原生血缘",
           "b": "- 无原生数据血缘 `官方文档`。"},
    "en": {"v": "Not supported", "p": "Verified: no native lineage",
           "b": "- No native data lineage `(official docs)`."}},
  "storage_compute": {
    "zh": {"v": "有", "p": "3.x 存算分离；默认存算一体",
           "b": "- 默认本地盘存算一体；3.x 起支持存算分离 `官方文档`。\n- 分离版生产成熟度持续验证中 `社区共识`。"},
    "en": {"v": "Supported", "p": "Disaggregated since 3.x; coupled by default",
           "b": "- Coupled on local disks by default; disaggregated since 3.x `(official docs)`.\n- Separated edition's production maturity still being proven `(community consensus)`."}},
  "multi_model": {
    "zh": {"v": "部分支持", "p": "关系+JSON+全文+向量",
           "b": "- JSON、全文索引、向量索引均已支持 `官方文档`。\n- 无图引擎 `社区共识`。"},
    "en": {"v": "Partial", "p": "Relational + JSON + full-text + vectors",
           "b": "- JSON, full-text, and vector indexes supported `(official docs)`.\n- No graph engine `(community consensus)`."}},
  "drivers": {
    "zh": {"v": "有", "p": "MySQL 协议兼容",
           "b": "- MySQL 线协议兼容，驱动直接复用 `官方文档`。"},
    "en": {"v": "Supported", "p": "MySQL-protocol compatible",
           "b": "- MySQL wire-protocol compatible; reuse drivers `(official docs)`."}}
}
CONTENT3_D["tdsql"] = {
  "optimizer": {
    "zh": {"v": "有", "p": "MySQL 衍生+分布式优化器",
           "b": "- 基于 MySQL 优化器扩展分布式计划 `官方文档`。\n- hint 兼容 MySQL `社区共识`。"},
    "en": {"v": "Supported", "p": "MySQL-derived + distributed optimizer",
           "b": "- Extends the MySQL optimizer with distributed plans `(official docs)`.\n- MySQL-compatible hints `(community consensus)`."}},
  "tuning": {
    "zh": {"v": "有", "p": "DBbrain 自动诊断：索引推荐+限流",
           "b": "- 腾讯云 DBbrain 提供 SQL 诊断、索引推荐、自治限流 `官方文档`。\n- 参数组可调 `官方文档`。"},
    "en": {"v": "Supported", "p": "DBbrain auto-diagnosis: index advisor + throttling",
           "b": "- Tencent DBbrain offers SQL diagnosis, index recommendations, autonomous throttling `(official docs)`.\n- Tunable parameter groups `(official docs)`."}},
  "lineage": {
    "zh": {"v": "部分支持", "p": "WeData 数据地图集成",
           "b": "- 通过 WeData 数据地图做血缘 `官方文档`。\n- 无原生列级血缘 `社区共识`。"},
    "en": {"v": "Partial", "p": "WeData data-map integration",
           "b": "- Lineage via WeData data map `(official docs)`.\n- No native column-level lineage `(community consensus)`."}},
  "storage_compute": {
    "zh": {"v": "有", "p": "存算分离架构",
           "b": "- 计算与存储分离设计 `官方文档`。"},
    "en": {"v": "Supported", "p": "Disaggregated architecture",
           "b": "- Compute/storage separated by design `(official docs)`."}},
  "multi_model": {
    "zh": {"v": "部分支持", "p": "随 MySQL：JSON+全文",
           "b": "- JSON、全文索引随 MySQL 引擎 `官方文档`。\n- 无向量/图 `社区共识`。"},
    "en": {"v": "Partial", "p": "As MySQL: JSON + full-text",
           "b": "- JSON and full-text follow the MySQL engine `(official docs)`.\n- No vector/graph `(community consensus)`."}},
  "drivers": {
    "zh": {"v": "有", "p": "MySQL 协议兼容",
           "b": "- MySQL 线协议兼容 `官方文档`。"},
    "en": {"v": "Supported", "p": "MySQL-protocol compatible",
           "b": "- MySQL wire-protocol compatible `(official docs)`."}}
}
CONTENT3_D["tidb"] = {
  "optimizer": {
    "zh": {"v": "有", "p": "CBO+丰富 hint；SPM 计划绑定",
           "b": "- CBO + 丰富 hint，SPM（SQL Plan Management）可绑定计划 `官方文档`。\n- 统计信息+Plan Cache，计划翻转有治理手段 `官方文档`。\n- 分布式计划调优心智与单机不同 `社区共识`。"},
    "en": {"v": "Supported", "p": "CBO + rich hints; SPM plan binding",
           "b": "- CBO with rich hints; SPM (SQL Plan Management) binds plans `(official docs)`.\n- Statistics + Plan Cache with flip-control tooling `(official docs)`.\n- Distributed-plan tuning differs mentally from single-node `(community consensus)`."}},
  "tuning": {
    "zh": {"v": "有", "p": "Dashboard 诊断强；auto-analyze 自治",
           "b": "- TiDB Dashboard 慢查询/热点可视化完善 `官方文档`。\n- auto-analyze 自动收集统计信息 `官方文档`。\n- 参数多，深度调优仍需专家 `社区共识`。"},
    "en": {"v": "Supported", "p": "Strong Dashboard diagnostics; auto-analyze",
           "b": "- TiDB Dashboard visualizes slow queries and hotspots well `(official docs)`.\n- auto-analyze collects statistics automatically `(official docs)`.\n- Many parameters; deep tuning still needs experts `(community consensus)`."}},
  "lineage": {
    "zh": {"v": "无", "p": "查证为无原生血缘",
           "b": "- 无原生数据血缘 `官方文档`。\n- 依赖第三方治理平台 `社区共识`。"},
    "en": {"v": "Not supported", "p": "Verified: no native lineage",
           "b": "- No native data lineage `(official docs)`.\n- Depends on third-party governance platforms `(community consensus)`."}},
  "storage_compute": {
    "zh": {"v": "有", "p": "存算分离：TiKV/TiFlash 独立扩缩",
           "b": "- TiDB/TiKV/TiFlash/PD 分离，可独立扩缩 `官方文档`。\n- 行列混存按需扩展 `官方文档`。"},
    "en": {"v": "Supported", "p": "Disaggregated: TiKV/TiFlash scale independently",
           "b": "- TiDB/TiKV/TiFlash/PD separated; scale independently `(official docs)`.\n- Row/column stores scale on demand `(official docs)`."}},
  "multi_model": {
    "zh": {"v": "部分支持", "p": "关系+JSON+向量；全文待验证",
           "b": "- JSON 类型，TiDB Vector Search 向量检索 `官方文档`。\n- 全文检索能力待验证 `待验证`。"},
    "en": {"v": "Partial", "p": "Relational + JSON + vectors; full-text TBD",
           "b": "- JSON type and TiDB Vector Search `(official docs)`.\n- Full-text capability to be verified `(to be verified)`."}},
  "drivers": {
    "zh": {"v": "有", "p": "MySQL 协议兼容",
           "b": "- MySQL 线协议兼容，驱动生态直接复用 `官方文档`。"},
    "en": {"v": "Supported", "p": "MySQL-protocol compatible",
           "b": "- MySQL wire-protocol compatible; reuse the driver ecosystem `(official docs)`."}}
}
CONTENT3_D["weaviate"] = {
  "optimizer": {
    "zh": {"v": "不适用", "p": "向量检索无传统 CBO",
           "b": "- 无 SQL 优化器；混合搜索（向量+BM25）的融合策略内部启发式 `官方文档`。"},
    "en": {"v": "N/A", "p": "No classic CBO for vector search",
           "b": "- No SQL optimizer; hybrid (vector+BM25) fusion uses internal heuristics `(official docs)`."}},
  "tuning": {
    "zh": {"v": "部分支持", "p": "参数少；HNSW 参数是调优点",
           "b": "- 参数精简，HNSW 的 ef/maxConnections 是调优核心 `官方文档`。\n- 模块（向量化）选择影响大 `社区共识`。"},
    "en": {"v": "Partial", "p": "Few knobs; HNSW params are the levers",
           "b": "- Lean parameters; HNSW ef/maxConnections are the tuning core `(official docs)`.\n- Module (vectorizer) choice matters greatly `(community consensus)`."}},
  "lineage": {
    "zh": {"v": "无", "p": "查证为无原生血缘",
           "b": "- 无原生数据血缘 `官方文档`。"},
    "en": {"v": "Not supported", "p": "Verified: no native lineage",
           "b": "- No native data lineage `(official docs)`."}},
  "storage_compute": {
    "zh": {"v": "有", "p": "存算一体：本地盘",
           "b": "- 单机/集群本地盘存储，存算一体 `官方文档`。"},
    "en": {"v": "Supported", "p": "Coupled: local disks",
           "b": "- Single-node/cluster local-disk storage; coupled `(official docs)`."}},
  "multi_model": {
    "zh": {"v": "部分支持", "p": "向量+对象+BM25 全文+生成式",
           "b": "- 向量+结构化对象+BM25 全文，生成式搜索模块 `官方文档`。\n- 无图/时序 `社区共识`。"},
    "en": {"v": "Partial", "p": "Vectors + objects + BM25 FTS + generative",
           "b": "- Vectors + structured objects + BM25 full-text with generative search modules `(official docs)`.\n- No graph/time-series `(community consensus)`."}},
  "drivers": {
    "zh": {"v": "有", "p": "Python/TS/Java/Go 官方客户端",
           "b": "- 官方 Python/TypeScript/Java/Go 客户端 `官方文档`。\n- GraphQL/REST API `官方文档`。"},
    "en": {"v": "Supported", "p": "Official Python/TS/Java/Go clients",
           "b": "- Official Python/TypeScript/Java/Go clients `(official docs)`.\n- GraphQL/REST APIs `(official docs)`."}}
}
CONTENT3_D["yugabytedb"] = {
  "optimizer": {
    "zh": {"v": "有", "p": "PG 衍生 CBO；分布式下推",
           "b": "- 继承 PG CBO，Yugabyte 增加分布式下推与分区感知 `官方文档`。\n- hint 随 PG（pg_hint_plan 扩展）`社区共识`。"},
    "en": {"v": "Supported", "p": "PG-derived CBO; distributed pushdown",
           "b": "- Inherits PG CBO; Yugabyte adds distributed pushdown and partition awareness `(official docs)`.\n- Hints follow PG (pg_hint_plan extension) `(community consensus)`."}},
  "tuning": {
    "zh": {"v": "部分支持", "p": "参数可调；YB UI 诊断；自治中等",
           "b": "- 参数可调，YB-Master Admin UI 诊断 `官方文档`。\n- 自动 tablet 分裂/搬迁部分自治 `官方文档`。"},
    "en": {"v": "Partial", "p": "Tunable; YB UI diagnostics; middling autonomy",
           "b": "- Tunable parameters; YB-Master Admin UI diagnostics `(official docs)`.\n- Automatic tablet splitting/movement is partly autonomous `(official docs)`."}},
  "lineage": {
    "zh": {"v": "无", "p": "查证为无原生血缘",
           "b": "- 无原生数据血缘 `官方文档`。"},
    "en": {"v": "Not supported", "p": "Verified: no native lineage",
           "b": "- No native data lineage `(official docs)`."}},
  "storage_compute": {
    "zh": {"v": "有", "p": "存算一体：DocDB 本地盘 LSM",
           "b": "- DocDB 本地盘 LSM，存算一体 `官方文档`。"},
    "en": {"v": "Supported", "p": "Coupled: DocDB local-disk LSM",
           "b": "- DocDB local-disk LSM; coupled `(official docs)`."}},
  "multi_model": {
    "zh": {"v": "部分支持", "p": "YCQL+YSQL 双 API；pgvector 可用",
           "b": "- YSQL（PG 兼容）支持 jsonb、pgvector `官方文档`。\n- YCQL（Cassandra 兼容）宽列 `官方文档`。"},
    "en": {"v": "Partial", "p": "Dual YCQL+YSQL APIs; pgvector available",
           "b": "- YSQL (PG-compatible) supports jsonb and pgvector `(official docs)`.\n- YCQL (Cassandra-compatible) wide-column `(official docs)`."}},
  "drivers": {
    "zh": {"v": "有", "p": "PG+Cassandra 双驱动生态",
           "b": "- YSQL 用 PG 驱动，YCQL 用 Cassandra 驱动 `官方文档`。\n- 拓扑感知智能驱动是特色 `官方文档`。"},
    "en": {"v": "Supported", "p": "Dual PG + Cassandra driver ecosystems",
           "b": "- YSQL uses PG drivers; YCQL uses Cassandra drivers `(official docs)`.\n- Topology-aware smart drivers are a highlight `(official docs)`."}}
}
CONTENT3_D["redshift"] = {
  "optimizer": {
    "zh": {"v": "有", "p": "PG8 衍生 CBO；无 hint；重统计",
           "b": "- 基于 PG8 的 CBO，EXPLAIN 可用 `官方文档`。\n- 无 hint 机制，计划干预靠改写 SQL 与表设计 `社区共识`。\n- 统计信息过期+错误的 distkey/sortkey 是计划劣化的主因 `社区共识`。"},
    "en": {"v": "Supported", "p": "PG8-derived CBO; no hints; stats + distkeys rule",
           "b": "- PG8-based CBO with EXPLAIN `(official docs)`.\n- No hint mechanism; steer plans by rewriting SQL and table design `(community consensus)`.\n- Stale statistics plus wrong distkey/sortkey are the top plan-degradation causes `(community consensus)`."}},
  "tuning": {
    "zh": {"v": "部分支持", "p": "WLM 队列调优；ATO 部分自治",
           "b": "- WLM 队列是核心调优点，参数组可调 `官方文档`。\n- Automatic Table Optimization、自动 vacuum、并发扩展部分自治 `官方文档`。\n- 深度调优仍依赖分布键/排序键设计 `社区共识`。"},
    "en": {"v": "Partial", "p": "WLM queue tuning; ATO partly autonomous",
           "b": "- WLM queues are the core lever; parameter groups tunable `(official docs)`.\n- Automatic Table Optimization, auto vacuum, and concurrency scaling are partly autonomous `(official docs)`.\n- Deep tuning still hinges on distkey/sortkey design `(community consensus)`."}},
  "lineage": {
    "zh": {"v": "部分支持", "p": "Glue Catalog 集成；第三方血缘",
           "b": "- 表元数据可进 Glue Data Catalog `官方文档`。\n- 列级血缘靠 Atlan/Alation 等第三方 `社区共识`。"},
    "en": {"v": "Partial", "p": "Glue Catalog integration; third-party lineage",
           "b": "- Table metadata can flow into Glue Data Catalog `(official docs)`.\n- Column-level lineage via third parties like Atlan/Alation `(community consensus)`."}},
  "storage_compute": {
    "zh": {"v": "有", "p": "RA3+RMS 存算分离；DC2 一体",
           "b": "- RA3 节点+Redshift Managed Storage：存算分离 `官方文档`。\n- DC2 节点本地 SSD：存算一体 `官方文档`。\n- 选型时节点类型决定架构范式 `社区共识`。"},
    "en": {"v": "Supported", "p": "RA3+RMS disaggregated; DC2 coupled",
           "b": "- RA3 nodes + Redshift Managed Storage: disaggregated `(official docs)`.\n- DC2 nodes with local SSDs: coupled `(official docs)`.\n- Node type decides the architecture paradigm `(community consensus)`."}},
  "multi_model": {
    "zh": {"v": "部分支持", "p": "SUPER 半结构化；无向量/全文/图",
           "b": "- SUPER 类型支持半结构化（JSON/Parquet）`官方文档`。\n- 无原生向量、全文、图能力 `官方文档`。"},
    "en": {"v": "Partial", "p": "SUPER semi-structured; no vector/FTS/graph",
           "b": "- SUPER type for semi-structured (JSON/Parquet) `(official docs)`.\n- No native vector, full-text, or graph `(official docs)`."}},
  "drivers": {
    "zh": {"v": "有", "p": "官方 JDBC/ODBC+Python 连接器",
           "b": "- 官方 JDBC/ODBC 驱动，redshift-connector（Python）`官方文档`。\n- PG 驱动部分兼容但有差异，不建议混用 `社区共识`。"},
    "en": {"v": "Supported", "p": "Official JDBC/ODBC + Python connector",
           "b": "- Official JDBC/ODBC drivers and redshift-connector (Python) `(official docs)`.\n- PG drivers are partly compatible but differ; mixing not advised `(community consensus)`."}}
}
CONTENT3_D["bigquery"] = {
  "optimizer": {
    "zh": {"v": "有", "p": "Dremel CBO 全自动；无 hint",
           "b": "- Dremel 架构 CBO 全自动优化，EXPLAIN 可用 `官方文档`。\n- 无 hint 机制，用户不干预计划 `官方文档`。\n- slot 自动调度使计划翻转风险极低 `社区共识`。"},
    "en": {"v": "Supported", "p": "Fully automatic Dremel CBO; no hints",
           "b": "- Dremel-architecture CBO fully automatic; EXPLAIN available `(official docs)`.\n- No hint mechanism; users don't steer plans `(official docs)`.\n- Automatic slot scheduling makes plan flips extremely rare `(community consensus)`."}},
  "tuning": {
    "zh": {"v": "有", "p": "Serverless 零调参自治标杆",
           "b": "- Serverless 模式零参数，autoscaling 自动扩缩 slot `官方文档`。\n- 调优转为 SQL 改写与成本（slot/字节计费）管理 `社区共识`。"},
    "en": {"v": "Supported", "p": "Serverless zero-knob autonomy benchmark",
           "b": "- Serverless mode has zero knobs; autoscaling scales slots automatically `(official docs)`.\n- Tuning becomes SQL rewriting plus cost (slot/byte billing) management `(community consensus)`."}},
  "lineage": {
    "zh": {"v": "有", "p": "Dataplex 列级血缘+目录，标杆",
           "b": "- Dataplex 自动采集列级血缘，Data Catalog 统一发现 `官方文档`。\n- 血缘覆盖查询/作业全链路 `官方文档`。"},
    "en": {"v": "Supported", "p": "Dataplex column-level lineage + Catalog; benchmark",
           "b": "- Dataplex auto-captures column-level lineage; Data Catalog unifies discovery `(official docs)`.\n- Lineage spans queries and jobs end to end `(official docs)`."}},
  "multi_model": {
    "zh": {"v": "部分支持", "p": "JSON+GEOGRAPHY+ML；向量有限",
           "b": "- JSON、GEOGRAPHY、BigQuery ML，VECTOR_SEARCH 有限支持 `官方文档`。\n- 无原生全文/图引擎 `社区共识`。"},
    "en": {"v": "Partial", "p": "JSON + GEOGRAPHY + ML; limited vectors",
           "b": "- JSON, GEOGRAPHY, BigQuery ML, and limited VECTOR_SEARCH `(official docs)`.\n- No native full-text/graph engine `(community consensus)`."}},
  "storage_compute": {
    "zh": {"v": "有", "p": "存算分离鼻祖：Colossus+Dremel",
           "b": "- Colossus 分布式存储 + Dremel 计算，存算分离的开创者 `官方文档`。\n- 计算资源按 slot 弹性，与存储完全解耦 `官方文档`。"},
    "en": {"v": "Supported", "p": "Disaggregation pioneer: Colossus + Dremel",
           "b": "- Colossus distributed storage + Dremel compute; the disaggregation pioneer `(official docs)`.\n- Compute scales in slots, fully decoupled from storage `(official docs)`."}},
  "drivers": {
    "zh": {"v": "有", "p": "官方多语言库；JDBC 靠 Simba",
           "b": "- 官方 Python/Java/Node/Go 客户端库 + REST API `官方文档`。\n- JDBC/ODBC 靠 Simba 官方合作驱动 `官方文档`。\n- dbt 等数仓工具链完备 `社区共识`。"},
    "en": {"v": "Supported", "p": "Official multi-language libs; JDBC/ODBC via Simba",
           "b": "- Official Python/Java/Node/Go client libraries plus REST API `(official docs)`.\n- JDBC/ODBC via official Simba-partnered drivers `(official docs)`.\n- Complete dbt-era warehouse toolchain `(community consensus)`."}}
}
