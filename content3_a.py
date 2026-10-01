# -*- coding: utf-8 -*-
"""6 个新增维度的数据（A 组）：ttl / online_ddl / multitenant / multi_region / ha_rto / multi_cloud.
CONTENT3_A[slug][dimkey] = {"zh": {"v","p","b"}, "en": {"v","p","b"}}
v = verdict（有/部分支持/无/不适用/未找到证据；Supported/Partial/Not supported/N/A/No evidence found），p = 短语，b = markdown 正文。
正文沿用档案体例：`- ` 条目 + 反引号证据徽章（`官方文档`/`厂商口径`/`社区实测`/`社区共识`/`待验证`）。
"""

CONTENT3_A = {}

# ---------------- 维度 ttl：TTL 与数据生命周期管理 ----------------
# scope: 行级/分区级自动过期删除、冷热分层、归档策略。不含备份保留。
CONTENT3_A.setdefault("alloydb", {})["ttl"] = {
  "zh": {"v": "部分支持", "p": "分区表+pg_cron；无原生行级TTL",
         "b": "- PG 分区表 + pg_partman/pg_cron 定时清理过期分区是常规做法 `社区共识`。\n- AlloyDB 备份保留策略管的是备份，不管业务数据过期 `官方文档`。\n- 大分区表 DROP 分区是 O(1) 元数据操作，比 DELETE 高效得多 `社区共识`。"},
  "en": {"v": "Partial", "p": "Partitioning + pg_cron; no native row-level TTL",
         "b": "- Partitioned tables with pg_partman/pg_cron dropping expired partitions is the standard pattern `(community consensus)`.\n- AlloyDB backup retention governs backups, not business-data expiry `(official docs)`.\n- Dropping a partition is an O(1) metadata operation, far cheaper than DELETE `(community consensus)`."}}
CONTENT3_A.setdefault("aurora", {})["ttl"] = {
  "zh": {"v": "部分支持", "p": "分区+event 定时清理；无原生行级TTL",
         "b": "- MySQL 版：分区表 + event scheduler 定时删过期分区 `社区共识`。\n- PG 版：pg_cron + 分区裁剪，沿用 PG 生态做法 `官方文档`。\n- 无原生行级 TTL；大表逐行 DELETE 又慢又胀 undo `社区共识`。"},
  "en": {"v": "Partial", "p": "Partitions + scheduled events; no native row-level TTL",
         "b": "- MySQL flavor: partitioned tables + event scheduler to drop expired partitions `(community consensus)`.\n- PG flavor: pg_cron + partition pruning, same as the PG ecosystem `(official docs)`.\n- No native row-level TTL; row-by-row DELETE on huge tables is slow and bloats undo `(community consensus)`."}}
CONTENT3_A.setdefault("cassandra-scylladb", {})["ttl"] = {
  "zh": {"v": "有", "p": "列级/表级原生 TTL，写入时指定",
         "b": "- INSERT/UPDATE 可带 USING TTL（列级过期），表级 default_time_to_live `官方文档`。\n- 过期数据靠 compaction 回收，墓碑（tombstone）堆积会拖慢读 `社区共识`。\n- TTL 重度场景建议调小 gc_grace_seconds 并监控 tombstone 比例 `社区实测`。"},
  "en": {"v": "Supported", "p": "Native column-/table-level TTL set at write time",
         "b": "- INSERT/UPDATE accept USING TTL per column; default_time_to_live per table `(official docs)`.\n- Expired data is reclaimed by compaction; tombstone buildup hurts read performance `(community consensus)`.\n- For TTL-heavy workloads lower gc_grace_seconds and watch tombstone ratios `(community tested)`."}}
CONTENT3_A.setdefault("clickhouse", {})["ttl"] = {
  "zh": {"v": "有", "p": "TTL 表达式（列级/表级），后台自动清理",
         "b": "- 建表时 TTL datetime_col + INTERVAL，后台线程自动删过期分区/行 `官方文档`。\n- 可配到列级（只删某列）或整行，TO DISK/VOLUME 支持冷热分层 `官方文档`。\n- 清理依赖 merge，不能保证精确时刻删除，延迟分钟到小时级 `社区共识`。"},
  "en": {"v": "Supported", "p": "TTL expressions (column-/table-level), cleaned in background",
         "b": "- TTL datetime_col + INTERVAL at CREATE TABLE; a background thread removes expired parts/rows `(official docs)`.\n- Column-level (drop one column) or row-level TTL, plus TO DISK/VOLUME for hot-cold tiering `(official docs)`.\n- Cleanup rides on merges, so expiry is not exact — minutes to hours of lag `(community consensus)`."}}
CONTENT3_A.setdefault("cockroachdb", {})["ttl"] = {
  "zh": {"v": "部分支持", "p": "无原生 TTL；靠 scheduled job 定时删",
         "b": "- 无原生行级 TTL，需用 scheduled job 机制跑定时 DELETE `官方文档`。\n- 大表定时删注意拆批，避免长事务拖慢 MVCC GC `社区共识`。\n- 原生 TTL 的 feature request 长期 open，短期别指望 `社区共识`。"},
  "en": {"v": "Partial", "p": "No native TTL; scheduled jobs for periodic deletes",
         "b": "- No native row-level TTL; use scheduled jobs running periodic DELETEs `(official docs)`.\n- Batch large deletes to avoid long transactions slowing MVCC GC `(community consensus)`.\n- The native-TTL feature request has been open for years; don't count on it soon `(community consensus)`."}}
CONTENT3_A.setdefault("databricks", {})["ttl"] = {
  "zh": {"v": "有", "p": "Delta 表保留期+VACUUM；流式需自建清理",
         "b": "- Delta 表可设保留期，VACUUM 按保留期清理旧文件版本 `官方文档`。\n- 流式表/物化视图的增量过期逻辑需自己写清理任务 `官方文档`。\n- VACUUM 默认 7 天保留期防并发读写冲突，调小有风险 `社区共识`。"},
  "en": {"v": "Supported", "p": "Delta retention + VACUUM; custom cleanup for streaming",
         "b": "- Delta tables support retention periods; VACUUM reclaims old file versions per retention `(official docs)`.\n- Streaming tables/materialized views need custom cleanup jobs for expiry logic `(official docs)`.\n- VACUUM defaults to 7-day retention to protect concurrent readers; lowering it is risky `(community consensus)`."}}
CONTENT3_A.setdefault("doris", {})["ttl"] = {
  "zh": {"v": "部分支持", "p": "动态分区+分区过期；无行级 TTL",
         "b": "- 动态分区按时间自动建分区，配分区保留个数实现滚动过期 `官方文档`。\n- 无原生行级 TTL，行级过期走 DELETE（Doris 的 DELETE 走导入链路，代价高）`官方文档`。\n- 冷热分层（storage policy）可把老分区沉到对象存储降成本 `官方文档`。"},
  "en": {"v": "Partial", "p": "Dynamic partitions with retention; no row-level TTL",
         "b": "- Dynamic partitions auto-create time partitions; a retention count gives rolling expiry `(official docs)`.\n- No native row-level TTL; row deletes go through the load path and are expensive `(official docs)`.\n- Tiered storage policies can sink old partitions to object storage to cut cost `(official docs)`."}}
CONTENT3_A.setdefault("duckdb", {})["ttl"] = {
  "zh": {"v": "无", "p": "嵌入式单机，无 TTL 机制",
         "b": "- 无原生 TTL/分区过期，需应用层 WHERE 过滤或定期 DELETE `官方文档`。\n- 定位是嵌入式分析引擎，数据生命周期由宿主应用管理 `社区共识`。\n- 大删后需 VACUUM/重写回收空间 `社区共识`。"},
  "en": {"v": "Not supported", "p": "Embedded single-node; no TTL mechanism",
         "b": "- No native TTL or partition expiry; filter in the app layer or run periodic DELETEs `(official docs)`.\n- As an embedded engine, lifecycle is owned by the host application `(community consensus)`.\n- Reclaim space after big deletes via VACUUM/rewrite `(community consensus)`."}}
CONTENT3_A.setdefault("dynamodb", {})["ttl"] = {
  "zh": {"v": "有", "p": "表级 TTL 属性，后台自动删不耗 WCU",
         "b": "- 表上指定 TTL 属性（epoch 秒），过期项后台自动删，不消耗写容量 `官方文档`。\n- 删除延迟通常几小时内，不保证精确时刻 `官方文档`。\n- TTL 删除会产生 DynamoDB Streams 记录，可触发下游清理 `官方文档`。"},
  "en": {"v": "Supported", "p": "Table-level TTL attribute; background deletes free of WCU",
         "b": "- Designate a TTL attribute (epoch seconds); expired items are deleted in the background with no write-capacity cost `(official docs)`.\n- Deletion lags by hours typically; not exact `(official docs)`.\n- TTL deletions emit DynamoDB Streams records, useful for downstream cleanup `(official docs)`."}}
CONTENT3_A.setdefault("edb", {})["ttl"] = {
  "zh": {"v": "部分支持", "p": "PG 分区+pg_cron；无原生行级 TTL",
         "b": "- 继承 PG 生态：分区表 + pg_partman/pg_cron 做滚动过期 `官方文档`。\n- 无原生行级 TTL，大表逐行删同样面临膨胀问题 `社区共识`。"},
  "en": {"v": "Partial", "p": "PG partitioning + pg_cron; no native row-level TTL",
         "b": "- Inherits the PG ecosystem: partitioned tables with pg_partman/pg_cron for rolling expiry `(official docs)`.\n- No native row-level TTL; row-by-row deletes on huge tables bloat the same way `(community consensus)`."}}
CONTENT3_A.setdefault("etcd", {})["ttl"] = {
  "zh": {"v": "有", "p": "key 租约（lease）TTL，原生机制",
         "b": "- key 可绑定 lease，lease 过期则 key 自动删除，是原生设计 `官方文档`。\n- lease 需客户端 keepalive 续约，网络分区时可能误删 `社区共识`。\n- 定位是元数据/配置存储，不适合海量业务数据过期 `社区共识`。"},
  "en": {"v": "Supported", "p": "Key leases with TTL; native mechanism",
         "b": "- Keys attach to leases; lease expiry auto-deletes the keys — native by design `(official docs)`.\n- Leases need client keepalive; network partitions can cause premature deletion `(community consensus)`.\n- Built for metadata/config, not bulk business-data expiry `(community consensus)`."}}
CONTENT3_A.setdefault("mariadb", {})["ttl"] = {
  "zh": {"v": "部分支持", "p": "分区+event；无原生行级 TTL",
         "b": "- 分区表 + event scheduler 定时清理是标准做法 `社区共识`。\n- 与 MySQL 同源限制，无原生行级 TTL `社区共识`。"},
  "en": {"v": "Partial", "p": "Partitions + events; no native row-level TTL",
         "b": "- Partitioned tables + event scheduler is the standard expiry pattern `(community consensus)`.\n- Same lineage limits as MySQL; no native row-level TTL `(community consensus)`."}}
CONTENT3_A.setdefault("milvus", {})["ttl"] = {
  "zh": {"v": "有", "p": "集合级 TTL（ttl.seconds），后台清理",
         "b": "- 集合可配 ttl.seconds，过期数据后台自动清理 `官方文档`。\n- 清理是异步的，不保证精确时刻，配合 compaction 回收 `待验证`。"},
  "en": {"v": "Supported", "p": "Collection-level TTL (ttl.seconds), background cleanup",
         "b": "- Collections accept ttl.seconds; expired data is cleaned in the background `(official docs)`.\n- Cleanup is asynchronous, not exact-time; reclaimed with compaction `(to be verified)`."}}
CONTENT3_A.setdefault("mongodb", {})["ttl"] = {
  "zh": {"v": "有", "p": "TTL 索引原生，分钟级精度后台删",
         "b": "- TTL 索引按日期字段过期自动删文档，精度约 60 秒 `官方文档`。\n- 后台线程单线程删除，大批量过期可能积压 `社区共识`。\n- capped collection 是固定容量淘汰，不是 TTL 语义 `社区共识`。"},
  "en": {"v": "Supported", "p": "Native TTL indexes; background deletes at ~minute precision",
         "b": "- TTL indexes auto-delete documents by date field, roughly 60-second precision `(official docs)`.\n- A single background thread does the deletes; massive expiries can backlog `(community consensus)`.\n- Capped collections are fixed-size eviction, a different mechanism `(community consensus)`."}}
CONTENT3_A.setdefault("mysql", {})["ttl"] = {
  "zh": {"v": "部分支持", "p": "分区交换+event；无原生行级 TTL",
         "b": "- 分区表 + event 定时 DROP 分区是生产标准做法 `社区共识`。\n- 无原生行级 TTL；大表 DELETE 慢且产生大量 undo/redo `社区共识`。"},
  "en": {"v": "Partial", "p": "Partition exchange + events; no native row-level TTL",
         "b": "- Partitioned tables + scheduled events dropping partitions is the production standard `(community consensus)`.\n- No native row-level TTL; big-table DELETEs are slow and generate heavy undo/redo `(community consensus)`."}}
CONTENT3_A.setdefault("oceanbase", {})["ttl"] = {
  "zh": {"v": "部分支持", "p": "分区表滚动过期；行级 TTL 有限",
         "b": "- 分区表 + 定时任务删分区是常用做法 `社区共识`。\n- 行级自动过期能力弱于 Cassandra 系，需应用层配合 `待验证`。"},
  "en": {"v": "Partial", "p": "Rolling partition expiry; limited row-level TTL",
         "b": "- Partitioned tables with scheduled partition drops are the common pattern `(community consensus)`.\n- Row-level auto-expiry is weaker than the Cassandra family; app-layer help needed `(to be verified)`."}}
CONTENT3_A.setdefault("oracle", {})["ttl"] = {
  "zh": {"v": "有", "p": "ILM/ADO 自动数据优化，生命周期最完整",
         "b": "- ILM + Heat Map 自动识别冷数据，ADO 策略自动压缩/分层/置只读 `官方文档`。\n- 分区表滚动 + 在线重定义配合，生命周期管理覆盖最完整 `官方文档`。\n- 功能多在企业版，授权成本高 `社区共识`。"},
  "en": {"v": "Supported", "p": "ILM/ADO automatic data optimization; most complete lifecycle",
         "b": "- ILM with Heat Map auto-detects cold data; ADO policies auto-compress/tier/set read-only `(official docs)`.\n- Rolling partitions plus online redefinition make lifecycle coverage the most complete `(official docs)`.\n- Mostly Enterprise Edition features with high license cost `(community consensus)`."}}
CONTENT3_A.setdefault("polardb", {})["ttl"] = {
  "zh": {"v": "部分支持", "p": "同源分区+定时任务；无原生行级 TTL",
         "b": "- MySQL/PG 版继承各自生态的分区过期做法 `官方文档`。\n- 无原生行级 TTL `社区共识`。"},
  "en": {"v": "Partial", "p": "Same-lineage partition expiry; no native row-level TTL",
         "b": "- MySQL/PG flavors inherit their ecosystems' partition-expiry patterns `(official docs)`.\n- No native row-level TTL `(community consensus)`."}}
CONTENT3_A.setdefault("postgresql", {})["ttl"] = {
  "zh": {"v": "部分支持", "p": "声明式分区+pg_cron；无原生行级 TTL",
         "b": "- 声明式分区 + pg_partman/pg_cron 滚动删分区是标准答案 `社区共识`。\n- 无原生行级 TTL；pg_cron 需装扩展，托管版一般自带 `官方文档`。"},
  "en": {"v": "Partial", "p": "Declarative partitioning + pg_cron; no native row-level TTL",
         "b": "- Declarative partitioning with pg_partman/pg_cron for rolling drops is the standard answer `(community consensus)`.\n- No native row-level TTL; pg_cron needs the extension (usually bundled in managed offerings) `(official docs)`."}}
CONTENT3_A.setdefault("qdrant", {})["ttl"] = {
  "zh": {"v": "部分支持", "p": "无原生 TTL；按 payload 时间字段批量删",
         "b": "- 无原生 TTL 机制，需定时按 payload 时间字段 filter 删除 `待验证`。\n- 向量库场景 TTL 需求弱，官方优先级不高 `社区共识`。"},
  "en": {"v": "Partial", "p": "No native TTL; batch-delete by payload timestamp",
         "b": "- No native TTL; schedule filtered deletes on a payload timestamp field `(to be verified)`.\n- TTL demand is weak in vector-DB scenarios; low official priority `(community consensus)`."}}
CONTENT3_A.setdefault("redis-valkey", {})["ttl"] = {
  "zh": {"v": "有", "p": "EXPIRE/TTL 原生，键级精确过期",
         "b": "- EXPIRE/PEXPIRE/EXPIREAT 精确到毫秒，后台+惰性双删策略 `官方文档`。\n- 大量 key 同时过期可能引发延迟毛刺，生产上打散过期时间是常识 `社区共识`。"},
  "en": {"v": "Supported", "p": "Native EXPIRE/TTL; exact per-key expiry",
         "b": "- EXPIRE/PEXPIRE/EXPIREAT with millisecond precision; active + lazy expiry `(official docs)`.\n- Mass simultaneous expiries can cause latency spikes — scattering expiry times is standard practice `(community consensus)`."}}
CONTENT3_A.setdefault("snowflake", {})["ttl"] = {
  "zh": {"v": "有", "p": "保留期+Time Travel，表级可配",
         "b": "- DATA_RETENTION_TIME_IN_DAYS 表级保留期，过期自动清理 `官方文档`。\n- Time Travel/Fail-safe 是保留期的延伸，不是业务 TTL 语义 `官方文档`。\n- 保留期产生存储费用，设太长烧钱 `社区共识`。"},
  "en": {"v": "Supported", "p": "Retention periods + Time Travel, configurable per table",
         "b": "- DATA_RETENTION_TIME_IN_DAYS per-table retention with automatic cleanup `(official docs)`.\n- Time Travel/Fail-safe extend retention; they are not business TTL `(official docs)`.\n- Retention consumes storage billing — long periods get expensive `(community consensus)`."}}
CONTENT3_A.setdefault("spanner", {})["ttl"] = {
  "zh": {"v": "部分支持", "p": "无原生 TTL；靠定时删或分区设计",
         "b": "- 无原生行级 TTL，需应用定时批量删 `社区共识`。\n- 交错表/分区键设计可让过期删除更高效 `社区共识`。"},
  "en": {"v": "Partial", "p": "No native TTL; scheduled deletes or partitioning",
         "b": "- No native row-level TTL; application-scheduled batch deletes `(community consensus)`.\n- Interleaved tables/partition-key design can make expiry deletes cheaper `(community consensus)`."}}
CONTENT3_A.setdefault("sqlserver", {})["ttl"] = {
  "zh": {"v": "部分支持", "p": "分区切换+SQL Agent；Stretch 已弃用",
         "b": "- 分区切换（SWITCH）实现快速过期，SQL Agent 定时作业 `官方文档`。\n- Stretch Database（冷热分层到 Azure）已弃用，不要再规划 `官方文档`。\n- 无原生行级 TTL `社区共识`。"},
  "en": {"v": "Partial", "p": "Partition switching + SQL Agent; Stretch deprecated",
         "b": "- Partition SWITCH for fast expiry with SQL Agent jobs `(official docs)`.\n- Stretch Database (tiering to Azure) is deprecated — do not plan on it `(official docs)`.\n- No native row-level TTL `(community consensus)`."}}
CONTENT3_A.setdefault("starrocks", {})["ttl"] = {
  "zh": {"v": "有", "p": "动态分区+partition_ttl_number 自动过期",
         "b": "- 动态分区配 partition_ttl_number，过期分区自动删 `官方文档`。\n- 无行级 TTL；主键模型 DELETE 代价高 `官方文档`。\n- 存储分层（storage medium）可做冷热分离 `官方文档`。"},
  "en": {"v": "Supported", "p": "Dynamic partitions + partition_ttl_number auto-expiry",
         "b": "- Dynamic partitions with partition_ttl_number auto-drop expired partitions `(official docs)`.\n- No row-level TTL; DELETE on primary-key models is costly `(official docs)`.\n- Storage-medium tiering supports hot-cold separation `(official docs)`."}}
CONTENT3_A.setdefault("tdsql", {})["ttl"] = {
  "zh": {"v": "部分支持", "p": "同源分区过期；无原生行级 TTL",
         "b": "- MySQL 版分区 + event，PG 版分区 + 定时任务 `社区共识`。\n- 无原生行级 TTL `社区共识`。"},
  "en": {"v": "Partial", "p": "Same-lineage partition expiry; no native row-level TTL",
         "b": "- MySQL flavor: partitions + events; PG flavor: partitions + scheduled jobs `(community consensus)`.\n- No native row-level TTL `(community consensus)`."}}
CONTENT3_A.setdefault("tidb", {})["ttl"] = {
  "zh": {"v": "有", "p": "表级 TTL 属性（TTL='x'），原生支持",
         "b": "- 建表时 TTL=\"3 MONTH\" 等，过期行后台自动删 `官方文档`。\n- TTL 作业与 GC 配合，大表过期删对前台影响小 `官方文档`。\n- TTL 列要求有索引，设计表时要注意 `社区共识`。"},
  "en": {"v": "Supported", "p": "Native table-level TTL attribute (TTL='x')",
         "b": "- TTL=\"3 MONTH\" at CREATE TABLE; expired rows deleted in background `(official docs)`.\n- TTL jobs coordinate with GC; expiry deletes barely affect foreground traffic `(official docs)`.\n- The TTL column needs an index — design tables accordingly `(community consensus)`."}}
CONTENT3_A.setdefault("weaviate", {})["ttl"] = {
  "zh": {"v": "无", "p": "无原生 TTL，需应用层删",
         "b": "- 无原生 TTL 机制，过期对象需应用定时删 `待验证`。\n- 向量场景 TTL 需求弱 `社区共识`。"},
  "en": {"v": "Not supported", "p": "No native TTL; app-layer deletes",
         "b": "- No native TTL; expired objects need app-scheduled deletes `(to be verified)`.\n- TTL demand is weak in vector scenarios `(community consensus)`."}}
CONTENT3_A.setdefault("yugabytedb", {})["ttl"] = {
  "zh": {"v": "有", "p": "YCQL/YSQL 表级 TTL",
         "b": "- YCQL 继承 Cassandra 语义：USING TTL / default_time_to_live `官方文档`。\n- YSQL 也支持表级 TTL 属性，过期后台清理 `官方文档`。\n- 墓碑与 compaction 行为同 Cassandra 系，需同样运维 `社区共识`。"},
  "en": {"v": "Supported", "p": "Table-level TTL (default_time_to_live) + PG partitioning",
         "b": "- YCQL inherits Cassandra semantics: USING TTL / default_time_to_live `(official docs)`.\n- YSQL also supports a table-level TTL attribute with background cleanup `(official docs)`.\n- Tombstone/compaction behavior matches the Cassandra family; same ops care needed `(community consensus)`."}}
CONTENT3_A.setdefault("redshift", {})["ttl"] = {
  "zh": {"v": "部分支持", "p": "无原生 TTL；定时 DELETE+VACUUM",
         "b": "- 无原生 TTL/分区过期，需定时 DELETE + VACUUM 回收 `社区共识`。\n- 大表 DELETE 代价高，设计时多用时间序分区表轮换 `社区共识`。\n- Spectrum 外表生命周期由 S3 生命周期策略管 `官方文档`。"},
  "en": {"v": "Partial", "p": "No native TTL; scheduled DELETE + VACUUM",
         "b": "- No native TTL or partition expiry; scheduled DELETE + VACUUM to reclaim `(community consensus)`.\n- Big-table DELETEs are costly — design time-ordered table rotation instead `(community consensus)`.\n- Spectrum external-table lifecycle is governed by S3 lifecycle policies `(official docs)`."}}
CONTENT3_A.setdefault("bigquery", {})["ttl"] = {
  "zh": {"v": "有", "p": "表/分区过期时间原生",
         "b": "- 表级 expiration_time、数据集默认过期、分区表 partition_expiration_days `官方文档`。\n- 过期自动删且不收删除费，是成本治理常用手段 `官方文档`。\n- 过期是整表/整分区粒度，无行级 TTL `官方文档`。"},
  "en": {"v": "Supported", "p": "Native table/partition expiration; partition_expiration_days",
         "b": "- Table expiration_time, dataset default expiration, partition_expiration_days `(official docs)`.\n- Expiry auto-deletes at no deletion cost — a standard cost-governance lever `(official docs)`.\n- Expiry is table-/partition-granular; no row-level TTL `(official docs)`."}}

# ---------------- 维度 online_ddl：在线 DDL 与 Schema 演进 ----------------
# scope: 加列/改列/建索引是否锁表、在线变更机制、大表 DDL 风险与工具（gh-ost/pt-osc）。
CONTENT3_A.setdefault("alloydb", {})["online_ddl"] = {
  "zh": {"v": "有", "p": "PG 原生在线 DDL，加列/建索引不锁表",
         "b": "- 继承 PG：加 nullable 列是元数据操作，CREATE INDEX CONCURRENTLY 不阻塞写 `官方文档`。\n- 改列类型/加非空约束仍需重写或全表扫描，大表要规划窗口 `社区共识`。"},
  "en": {"v": "Supported", "p": "Native PG online DDL; add-column/index without locking",
         "b": "- Inherits PG: adding a nullable column is a metadata op; CREATE INDEX CONCURRENTLY doesn't block writes `(official docs)`.\n- Changing column types / adding NOT NULL still rewrites or scans the table — plan windows for huge tables `(community consensus)`."}}
CONTENT3_A.setdefault("aurora", {})["online_ddl"] = {
  "zh": {"v": "部分支持", "p": "MySQL 版在线 DDL 有限；PG 版原生",
         "b": "- Aurora MySQL：InnoDB online DDL，加列多可在线，但改主键/列类型仍重建，大表用 gh-ost 更稳 `社区共识`。\n- Aurora PG：同 PG 原生在线 DDL `官方文档`。\n- 快照恢复/回溯（backtrack）可作为 DDL 翻车后的兜底 `官方文档`。"},
  "en": {"v": "Partial", "p": "Limited online DDL on MySQL flavor; native on PG flavor",
         "b": "- Aurora MySQL: InnoDB online DDL covers many add-column cases, but PK changes / type changes still rebuild — gh-ost is safer for huge tables `(community consensus)`.\n- Aurora PG: native PG online DDL `(official docs)`.\n- Snapshot restore / backtrack can bail out a failed DDL `(official docs)`."}}
CONTENT3_A.setdefault("cassandra-scylladb", {})["online_ddl"] = {
  "zh": {"v": "部分支持", "p": "加列轻量但 schema 变更最终一致",
         "b": "- 加列是轻量元数据操作，但 schema 变更在集群内最终一致，混合版本期读写可能异常 `官方文档`。\n- 不支持删列后重建同名列等操作，schema 演进约束多 `社区共识`。\n- ScyllaDB 的 schema 变更做了 Raft 化改进，一致性更好 `官方文档`。"},
  "en": {"v": "Partial", "p": "Lightweight add-column but eventually-consistent schema changes",
         "b": "- Adding a column is a lightweight metadata op, but schema changes propagate eventually — mixed-version reads/writes can misbehave `(official docs)`.\n- Many restrictions (e.g. no re-adding a dropped column name); schema evolution is constrained `(community consensus)`.\n- ScyllaDB Raft-ified schema changes for better consistency `(official docs)`."}}
CONTENT3_A.setdefault("clickhouse", {})["online_ddl"] = {
  "zh": {"v": "部分支持", "p": "ALTER 元数据轻量；mutation 重写代价高",
         "b": "- ADD COLUMN 等是元数据操作，瞬间完成 `官方文档`。\n- ALTER UPDATE/DELETE（mutation）是后台重写 parts，大表极慢且耗资源 `社区共识`。\n- 建索引（skip index）需物化 projection，重建代价看数据量 `社区共识`。"},
  "en": {"v": "Partial", "p": "Lightweight ALTER metadata ops; costly mutation rewrites",
         "b": "- ADD COLUMN and friends are metadata ops, instant `(official docs)`.\n- ALTER UPDATE/DELETE (mutations) rewrite parts in the background — very slow and resource-hungry on huge tables `(community consensus)`.\n- Skip indexes need materialized projections; rebuild cost scales with data `(community consensus)`."}}
CONTENT3_A.setdefault("cockroachdb", {})["online_ddl"] = {
  "zh": {"v": "有", "p": "声明式在线 schema 变更，并发友好",
         "b": "- schema 变更是在线声明式的，多语句可并发执行不阻塞读写 `官方文档`。\n- 大表加索引是后台分布式回填，前台无感 `官方文档`。\n- 极端场景下 schema 变更仍可能排队，变更期间避免混用 DDL+DML 大事务 `社区共识`。"},
  "en": {"v": "Supported", "p": "Declarative online schema changes; concurrency-friendly",
         "b": "- Schema changes are declarative and online; multiple statements run concurrently without blocking reads/writes `(official docs)`.\n- Index backfills on huge tables are distributed background work, invisible to foreground traffic `(official docs)`.\n- In edge cases schema changes can queue; avoid mixing DDL with huge DML transactions during changes `(community consensus)`."}}
CONTENT3_A.setdefault("databricks", {})["online_ddl"] = {
  "zh": {"v": "有", "p": "Delta schema 在线演进",
         "b": "- Delta Lake 支持 schema 自动演进与 mergeSchema，流批写入加列不中断 `官方文档`。\n- 列改名/改类型需 overwrite 或 column mapping，有代价 `官方文档`。\n- Unity Catalog 下表结构变更可审计 `官方文档`。"},
  "en": {"v": "Supported", "p": "Delta schema evolution / mergeSchema",
         "b": "- Delta Lake supports automatic schema evolution and mergeSchema; streaming/batch writes tolerate new columns `(official docs)`.\n- Renames / type changes need overwrite or column mapping, at a cost `(official docs)`.\n- Schema changes are auditable under Unity Catalog `(official docs)`."}}
CONTENT3_A.setdefault("doris", {})["online_ddl"] = {
  "zh": {"v": "部分支持", "p": "Light schema change 加列轻量",
         "b": "- Light schema change 让加列/加分区走轻量路径，不阻塞导入 `官方文档`。\n- 改列类型、改 key 列等仍需重写 tablet，大表代价高 `官方文档`。\n- 建 rollup/物化视图是异步 job，不影响前台 `社区共识`。"},
  "en": {"v": "Partial", "p": "Light schema change for lightweight add-column",
         "b": "- Light schema change puts add-column/add-partition on a lightweight path without blocking loads `(official docs)`.\n- Type changes / key-column changes still rewrite tablets — expensive on huge tables `(official docs)`.\n- Building rollups/materialized views runs as async jobs, invisible to foreground `(community consensus)`."}}
CONTENT3_A.setdefault("duckdb", {})["online_ddl"] = {
  "zh": {"v": "不适用", "p": "嵌入式单机，无并发 DDL 问题",
         "b": "- 单进程嵌入式，DDL 直接执行，无锁表/在线概念 `官方文档`。\n- 大文件加列是重写，耗时看 IO `社区共识`。"},
  "en": {"v": "N/A", "p": "Embedded single-process; no concurrent-DDL concern",
         "b": "- Single-process embedded; DDL runs directly with no locking/online distinction `(official docs)`.\n- Add-column on huge files rewrites data; time depends on IO `(community consensus)`."}}
CONTENT3_A.setdefault("dynamodb", {})["online_ddl"] = {
  "zh": {"v": "不适用", "p": "schemaless，无 DDL 概念",
         "b": "- 无 schema，属性随时增减，无 DDL 痛点 `官方文档`。\n- 加 GSI 是在线后台构建，大表回填耗时但不阻塞 `官方文档`。\n- GSI 回填期间写放大，WCU 规划要留余量 `社区共识`。"},
  "en": {"v": "N/A", "p": "Schemaless; no DDL concept",
         "b": "- No schema; attributes come and go with no DDL pain `(official docs)`.\n- Adding a GSI builds online in the background; backfills take time on huge tables but don't block `(official docs)`.\n- GSI backfill amplifies writes — leave WCU headroom `(community consensus)`."}}
CONTENT3_A.setdefault("edb", {})["online_ddl"] = {
  "zh": {"v": "有", "p": "PG 原生在线 DDL",
         "b": "- 同 PG：加列元数据操作，并发建索引不阻塞 `官方文档`。\n- EDB 工具链（Migration Portal）辅助 Oracle 迁移时的 DDL 改写 `厂商口径`。"},
  "en": {"v": "Supported", "p": "Native PG online DDL",
         "b": "- Same as PG: metadata-only add-column; concurrent index builds don't block `(official docs)`.\n- EDB tooling (Migration Portal) assists DDL rewriting in Oracle migrations `(vendor claim)`."}}
CONTENT3_A.setdefault("etcd", {})["online_ddl"] = {
  "zh": {"v": "不适用", "p": "KV 存储，无 schema/DDL",
         "b": "- 纯 KV，无表结构，无 DDL 概念 `官方文档`。\n- 数据格式变更由应用版本管理，与存储无关 `社区共识`。"},
  "en": {"v": "N/A", "p": "KV store; no schema/DDL",
         "b": "- Pure KV, no table structure, no DDL concept `(official docs)`.\n- Data-format changes are managed by app versioning, unrelated to storage `(community consensus)`."}}
CONTENT3_A.setdefault("mariadb", {})["online_ddl"] = {
  "zh": {"v": "部分支持", "p": "在线 DDL 有限，大表仍有风险",
         "b": "- InnoDB online DDL 覆盖加列等常见操作，但部分仍锁表/重建 `官方文档`。\n- 大表生产上常用 pt-osc/gh-ost 做无锁变更 `社区共识`。"},
  "en": {"v": "Partial", "p": "Limited online DDL; risky on huge tables",
         "b": "- InnoDB online DDL covers common add-column cases, but some ops still lock/rebuild `(official docs)`.\n- pt-osc/gh-ost remain the production choice for lock-free changes on huge tables `(community consensus)`."}}
CONTENT3_A.setdefault("milvus", {})["online_ddl"] = {
  "zh": {"v": "部分支持", "p": "动态字段；集合 schema 相对固定",
         "b": "- 支持动态字段（dynamic field）容纳新增属性 `官方文档`。\n- 集合 schema（向量维度、度量类型）建后基本不可改，改需重建 `官方文档`。\n- 加索引是在线后台构建 `官方文档`。"},
  "en": {"v": "Partial", "p": "Dynamic fields; collection schema largely fixed",
         "b": "- Dynamic fields absorb new attributes `(official docs)`.\n- Collection schema (vector dim, metric type) is effectively immutable after creation — changes need rebuild `(official docs)`.\n- Index building runs online in the background `(official docs)`."}}
CONTENT3_A.setdefault("mongodb", {})["online_ddl"] = {
  "zh": {"v": "有", "p": "schemaless；索引后台构建",
         "b": "- 无 schema，文档结构随时变，无 DDL 锁表问题 `官方文档`。\n- 建索引后台执行，大集合耗时但不阻塞读写 `官方文档`。\n- 4.2+ 支持 rolling 之外的 resharding 在线重分片 `官方文档`。"},
  "en": {"v": "Supported", "p": "Schemaless; background index builds",
         "b": "- No schema; document shape evolves freely with no DDL locking `(official docs)`.\n- Index builds run in the background; slow on huge collections but non-blocking `(official docs)`.\n- 4.2+ supports online resharding `(official docs)`."}}
CONTENT3_A.setdefault("mysql", {})["online_ddl"] = {
  "zh": {"v": "部分支持", "p": "InnoDB 在线 DDL 有限；gh-ost 生态",
         "b": "- InnoDB online DDL：加 nullable 列多可在线，但改列类型/主键/字符集仍重建锁表 `官方文档`。\n- 大表生产标准是 gh-ost/pt-online-schema-change 做无锁变更，有主从延迟与触发器风险 `社区共识`。\n- 8.0 的 instant add column 只覆盖末尾加列，场景有限 `官方文档`。"},
  "en": {"v": "Partial", "p": "Limited InnoDB online DDL; gh-ost/pt-osc ecosystem",
         "b": "- InnoDB online DDL: many add-column cases are online, but type/PK/charset changes still rebuild and lock `(official docs)`.\n- Production standard for huge tables is gh-ost/pt-online-schema-change — watch replica lag and trigger risks `(community consensus)`.\n- 8.0 instant add column only covers trailing columns; limited scope `(official docs)`."}}
CONTENT3_A.setdefault("oceanbase", {})["online_ddl"] = {
  "zh": {"v": "有", "p": "分布式在线 DDL",
         "b": "- 多数 DDL 在线执行，加列/建索引不阻塞业务 `官方文档`。\n- 分布式场景下 DDL 有全局协调，大表建索引是后台任务 `社区共识`。"},
  "en": {"v": "Supported", "p": "Distributed online DDL",
         "b": "- Most DDL runs online; add-column/index builds don't block traffic `(official docs)`.\n- Distributed DDL needs global coordination; huge-table index builds are background jobs `(community consensus)`."}}
CONTENT3_A.setdefault("oracle", {})["online_ddl"] = {
  "zh": {"v": "有", "p": "在线重定义/Edition，在线 DDL 标杆",
         "b": "- DBMS_REDEFINITION 在线重定义表、Edition 在线升级应用，业界标杆 `官方文档`。\n- 加列（尤其 nullable）多是在线元数据操作 `官方文档`。\n- 功能强但操作复杂，对 DBA 功力要求高 `社区共识`。"},
  "en": {"v": "Supported", "p": "Online redefinition / Editions; the online-DDL benchmark",
         "b": "- DBMS_REDEFINITION online table redefinition and Edition-based app upgrades are the industry benchmark `(official docs)`.\n- Add-column (especially nullable) is usually an online metadata op `(official docs)`.\n- Powerful but operationally complex; demands skilled DBAs `(community consensus)`."}}
CONTENT3_A.setdefault("polardb", {})["online_ddl"] = {
  "zh": {"v": "部分支持", "p": "同源在线 DDL 能力",
         "b": "- MySQL 版同 InnoDB online DDL 限制，大表建议 gh-ost `社区共识`。\n- PG 版同 PG 原生在线 DDL `官方文档`。"},
  "en": {"v": "Partial", "p": "Same-lineage online DDL capabilities",
         "b": "- MySQL flavor shares InnoDB online-DDL limits; gh-ost advised for huge tables `(community consensus)`.\n- PG flavor has native PG online DDL `(official docs)`."}}
CONTENT3_A.setdefault("postgresql", {})["online_ddl"] = {
  "zh": {"v": "有", "p": "原生在线 DDL，加列/并发建索引",
         "b": "- 加 nullable 列是元数据操作（PG11+ 带默认值也快），CREATE INDEX CONCURRENTLY 不阻塞写 `官方文档`。\n- 改列类型需 ACCESS EXCLUSIVE 锁重写，大表是经典痛点 `社区共识`。\n- pg_repack 等工具可做在线重组 `社区共识`。"},
  "en": {"v": "Supported", "p": "Native online DDL; add-column / concurrent index builds",
         "b": "- Adding a nullable column is a metadata op (fast even with defaults since PG11); CREATE INDEX CONCURRENTLY doesn't block writes `(official docs)`.\n- Type changes take ACCESS EXCLUSIVE and rewrite — the classic huge-table pain `(community consensus)`.\n- Tools like pg_repack do online reorganization `(community consensus)`."}}
CONTENT3_A.setdefault("qdrant", {})["online_ddl"] = {
  "zh": {"v": "有", "p": "无传统 DDL；payload 索引在线建",
         "b": "- 无表结构，payload 字段随时增减 `官方文档`。\n- payload 索引可在线创建，大集合构建耗时 `官方文档`。"},
  "en": {"v": "Supported", "p": "No traditional DDL; payload indexes built online",
         "b": "- No table structure; payload fields come and go `(official docs)`.\n- Payload indexes can be created online; builds take time on huge collections `(official docs)`."}}
CONTENT3_A.setdefault("redis-valkey", {})["online_ddl"] = {
  "zh": {"v": "不适用", "p": "无 schema，无 DDL",
         "b": "- KV/数据结构无 schema，无 DDL 概念 `官方文档`。\n- RediSearch 索引 schema 变更需重建 `社区共识`。"},
  "en": {"v": "N/A", "p": "No schema, no DDL",
         "b": "- KV/data structures have no schema and no DDL concept `(official docs)`.\n- RediSearch index schema changes need rebuilds `(community consensus)`."}}
CONTENT3_A.setdefault("snowflake", {})["online_ddl"] = {
  "zh": {"v": "有", "p": "元数据操作在线，无锁表概念",
         "b": "- 加列/改列多是元数据操作，在线完成 `官方文档`。\n- 微分区存储下无传统'锁表'概念，并发 DDL 友好 `社区共识`。"},
  "en": {"v": "Supported", "p": "Online metadata ops; no table-lock concept",
         "b": "- Add/alter column are mostly metadata ops, done online `(official docs)`.\n- Micro-partition storage has no traditional table-lock concept; DDL is concurrency-friendly `(community consensus)`."}}
CONTENT3_A.setdefault("spanner", {})["online_ddl"] = {
  "zh": {"v": "有", "p": "schema 更新后台长操作",
         "b": "- schema 更新是在线长操作，后台分阶段执行不阻塞读写 `官方文档`。\n- 大表加二级索引回填耗时，期间注意资源 `官方文档`。"},
  "en": {"v": "Supported", "p": "Schema updates as background long operations",
         "b": "- Schema updates are online long-running operations executed in staged background phases `(official docs)`.\n- Secondary-index backfills on huge tables take time; watch resources `(official docs)`."}}
CONTENT3_A.setdefault("sqlserver", {})["online_ddl"] = {
  "zh": {"v": "部分支持", "p": "企业版在线索引；部分 DDL 在线",
         "b": "- 企业版支持在线建索引/重建（ONLINE=ON），部分版本/操作受限 `官方文档`。\n- 在线操作仍需短暂锁（Sch-M），高并发下可能排队 `社区共识`。\n- 标准版在线能力弱，版本差异大 `社区共识`。"},
  "en": {"v": "Partial", "p": "Online indexing on Enterprise; partial online DDL",
         "b": "- Enterprise supports online index create/rebuild (ONLINE=ON), with version/operation limits `(official docs)`.\n- Online ops still need brief Sch-M locks and can queue under high concurrency `(community consensus)`.\n- Standard Edition is much weaker; big version skew `(community consensus)`."}}
CONTENT3_A.setdefault("starrocks", {})["online_ddl"] = {
  "zh": {"v": "部分支持", "p": "Light schema change 加列轻量",
         "b": "- Light schema change 加列走轻量路径 `官方文档`。\n- 改列类型/key 列需重写，大表代价高 `官方文档`。"},
  "en": {"v": "Partial", "p": "Light schema change for add-column",
         "b": "- Light schema change puts add-column on a lightweight path `(official docs)`.\n- Type/key-column changes rewrite data — expensive on huge tables `(official docs)`."}}
CONTENT3_A.setdefault("tdsql", {})["online_ddl"] = {
  "zh": {"v": "部分支持", "p": "同源在线 DDL",
         "b": "- MySQL 版同 InnoDB online DDL 限制 `社区共识`。\n- PG 版同 PG 原生在线 DDL `官方文档`。"},
  "en": {"v": "Partial", "p": "Same-lineage online DDL",
         "b": "- MySQL flavor shares InnoDB online-DDL limits `(community consensus)`.\n- PG flavor has native PG online DDL `(official docs)`."}}
CONTENT3_A.setdefault("tidb", {})["online_ddl"] = {
  "zh": {"v": "有", "p": "在线 DDL（F1 机制），分布式强项",
         "b": "- 基于 Google F1 论文的在线 DDL，加列/加索引不阻塞读写 `官方文档`。\n- DDL 是集群级串行队列，大量并发 DDL 会排队 `社区共识`。\n- 加索引是分布式回填，大表耗时但前台无感 `官方文档`。"},
  "en": {"v": "Supported", "p": "Online DDL (F1 mechanism); distributed strength",
         "b": "- Google-F1-paper online DDL; add-column/index never blocks reads/writes `(official docs)`.\n- DDL uses a cluster-wide serial queue; heavy concurrent DDL queues up `(community consensus)`.\n- Index adds are distributed backfills — slow on huge tables but invisible to foreground `(official docs)`."}}
CONTENT3_A.setdefault("weaviate", {})["online_ddl"] = {
  "zh": {"v": "有", "p": "class 属性可加；无传统 DDL",
         "b": "- class 的 property 可随时新增，无锁表概念 `官方文档`。\n- 已有属性类型不可改，改需重建 class `社区共识`。"},
  "en": {"v": "Supported", "p": "Class properties addable; no traditional DDL",
         "b": "- Class properties can be added anytime; no table-lock concept `(official docs)`.\n- Existing property types are immutable — rebuild the class to change `(community consensus)`."}}
CONTENT3_A.setdefault("yugabytedb", {})["online_ddl"] = {
  "zh": {"v": "有", "p": "PG 兼容在线 DDL；分布式协调有延迟",
         "b": "- YSQL 兼容 PG 在线 DDL 语义，加列/并发建索引可用 `官方文档`。\n- 分布式下 DDL 需跨节点协调，完成延迟高于单机 PG `社区共识`。"},
  "en": {"v": "Supported", "p": "PG-compatible online DDL; cross-node coordination lag",
         "b": "- YSQL matches PG online-DDL semantics; add-column/concurrent index builds work `(official docs)`.\n- Distributed DDL needs cross-node coordination — slower to complete than single-node PG `(community consensus)`."}}
CONTENT3_A.setdefault("redshift", {})["online_ddl"] = {
  "zh": {"v": "部分支持", "p": "部分 ALTER 锁表；大表变更代价高",
         "b": "- ADD COLUMN 等轻量，但 DISTKEY/SORTKEY 变更需建新表+导数据 `官方文档`。\n- DDL 期间拿表锁，并发查询排队，大表变更要规划窗口 `社区共识`。\n- 无 gh-ost 类生态，靠'建新表切换'手工操作 `社区共识`。"},
  "en": {"v": "Partial", "p": "Some ALTERs lock tables; costly on huge tables",
         "b": "- ADD COLUMN is light, but DISTKEY/SORTKEY changes need new-table + data copy `(official docs)`.\n- DDL takes table locks; concurrent queries queue — plan windows for huge-table changes `(community consensus)`.\n- No gh-ost-like ecosystem; manual new-table cutover is the norm `(community consensus)`."}}
CONTENT3_A.setdefault("bigquery", {})["online_ddl"] = {
  "zh": {"v": "有", "p": "加列/放宽模式在线",
         "b": "- 加列、放宽 required->nullable 等是在线元数据操作 `官方文档`。\n- 列改名/改类型支持有限，部分需重建表 `官方文档`。\n- 分区/聚簇变更代价高，建表时一次定好 `社区共识`。"},
  "en": {"v": "Supported", "p": "Online add-column / schema relaxation",
         "b": "- Add-column and relaxation (required→nullable) are online metadata ops `(official docs)`.\n- Renames / type changes are limited; some need table rebuilds `(official docs)`.\n- Partitioning/clustering changes are costly — get them right at creation `(community consensus)`."}}

# ---------------- 维度 multitenant：多租户与资源隔离 ----------------
# scope: 同一集群内多业务/租户的 CPU/内存/IO 限流与 QoS。不含认证隔离。
CONTENT3_A.setdefault("alloydb", {})["multitenant"] = {
  "zh": {"v": "部分支持", "p": "实例级隔离；无细粒度资源组",
         "b": "- 多租户靠多实例/多库逻辑隔离，无 CPU/内存/IO 细粒度限流 `社区共识`。\n- 读写实例分离可做业务隔离 `官方文档`。"},
  "en": {"v": "Partial", "p": "Instance-level isolation; no fine-grained resource groups",
         "b": "- Multi-tenancy via multiple instances/databases; no fine CPU/memory/IO throttling `(community consensus)`.\n- Read/write instance split can isolate workloads `(official docs)`."}}
CONTENT3_A.setdefault("aurora", {})["multitenant"] = {
  "zh": {"v": "部分支持", "p": "集群级隔离；Serverless v2 自动扩缩",
         "b": "- 租户隔离靠多集群/实例，单集群内无资源组限流 `社区共识`。\n- Serverless v2 按负载自动扩缩，部分缓解 noisy neighbor `官方文档`。"},
  "en": {"v": "Partial", "p": "Cluster-level isolation; Serverless v2 auto-scaling",
         "b": "- Tenant isolation via multiple clusters/instances; no in-cluster resource-group throttling `(community consensus)`.\n- Serverless v2 auto-scales with load, partly mitigating noisy neighbors `(official docs)`."}}
CONTENT3_A.setdefault("cassandra-scylladb", {})["multitenant"] = {
  "zh": {"v": "部分支持", "p": "keyspace 逻辑隔离；无资源限流",
         "b": "- keyspace 做逻辑隔离，但无 CPU/IO 限流，一个租户可拖慢全集群 `社区共识`。\n- ScyllaDB 有 workload 优先级调度，比开源 Cassandra 好一些 `官方文档`。"},
  "en": {"v": "Partial", "p": "Keyspace logical isolation; no resource throttling",
         "b": "- Keyspaces isolate logically, but with no CPU/IO throttling one tenant can slow the whole cluster `(community consensus)`.\n- ScyllaDB adds workload-priority scheduling, better than open-source Cassandra `(official docs)`."}}
CONTENT3_A.setdefault("clickhouse", {})["multitenant"] = {
  "zh": {"v": "部分支持", "p": "quota/用户级限流；隔离较粗",
         "b": "- 用户级 quota 可限查询数/执行时间/结果行数 `官方文档`。\n- 无 CPU/内存硬隔离，大查询仍可能挤占资源 `社区共识`。\n- 多租户生产上多用多集群，少用单集群混布 `社区共识`。"},
  "en": {"v": "Partial", "p": "Quota/user-level throttling; coarse isolation",
         "b": "- Per-user quotas cap query count, execution time, result rows `(official docs)`.\n- No hard CPU/memory isolation; huge queries can still hog resources `(community consensus)`.\n- Production multi-tenancy usually means multiple clusters, not mixed workloads `(community consensus)`."}}
CONTENT3_A.setdefault("cockroachdb", {})["multitenant"] = {
  "zh": {"v": "部分支持", "p": "admission control 有限；无租户资源组",
         "b": "- admission control 做过载保护，但不是租户级 QoS `官方文档`。\n- 多租户靠多集群/多 database 逻辑隔离 `社区共识`。"},
  "en": {"v": "Partial", "p": "Limited admission control; no tenant resource groups",
         "b": "- Admission control guards against overload, but it is not tenant-level QoS `(official docs)`.\n- Multi-tenancy via multiple clusters/databases for logical isolation `(community consensus)`."}}
CONTENT3_A.setdefault("databricks", {})["multitenant"] = {
  "zh": {"v": "有", "p": "工作区/集群隔离+Unity Catalog",
         "b": "- 工作区、集群/ SQL Warehouse 按团队隔离，Unity Catalog 做数据权限 `官方文档`。\n- 计算资源按集群/仓库隔离，noisy neighbor 天然规避 `官方文档`。\n- 成本归因到工作区/集群标签，FinOps 友好 `社区共识`。"},
  "en": {"v": "Supported", "p": "Workspace/cluster isolation + Unity Catalog",
         "b": "- Workspaces, clusters / SQL warehouses isolate teams; Unity Catalog governs data access `(official docs)`.\n- Compute is isolated per cluster/warehouse, sidestepping noisy neighbors `(official docs)`.\n- Cost attribution via workspace/cluster tags is FinOps-friendly `(community consensus)`."}}
CONTENT3_A.setdefault("doris", {})["multitenant"] = {
  "zh": {"v": "有", "p": "workload group 资源组限流",
         "b": "- workload group 可按用户/查询限 CPU/内存/IO，做租户 QoS `官方文档`。\n- 2.x 后资源组能力持续增强，是官方推荐的多租户方案 `官方文档`。\n- 配置不当仍可能互相影响，需压测调参 `社区共识`。"},
  "en": {"v": "Supported", "p": "Workload-group resource throttling",
         "b": "- Workload groups throttle CPU/memory/IO per user/query for tenant QoS `(official docs)`.\n- Steadily improved since 2.x; the officially recommended multi-tenancy approach `(official docs)`.\n- Misconfiguration can still cause interference; load-test the tuning `(community consensus)`."}}
CONTENT3_A.setdefault("duckdb", {})["multitenant"] = {
  "zh": {"v": "不适用", "p": "嵌入式单进程，无多租户场景",
         "b": "- 嵌入式单进程，资源隔离无意义 `官方文档`。\n- 单库单用户是典型用法，多租户请用服务端数据库 `社区共识`。"},
  "en": {"v": "N/A", "p": "Embedded single-process; no multi-tenancy scenario",
         "b": "- Embedded single process; resource isolation is meaningless `(official docs)`.\n- Single-database single-user is the typical use; use a server database for multi-tenancy `(community consensus)`."}}
CONTENT3_A.setdefault("dynamodb", {})["multitenant"] = {
  "zh": {"v": "部分支持", "p": "表级吞吐隔离；无集群内多租户",
         "b": "- 租户隔离靠多表/多账号，表级 WCU/按需计费天然隔离 `官方文档`。\n- 单表内多租户无资源限流，需应用层分区键设计 `社区共识`。"},
  "en": {"v": "Partial", "p": "Table-level throughput isolation; no in-cluster tenancy",
         "b": "- Tenant isolation via multiple tables/accounts; per-table WCU/on-demand billing isolates naturally `(official docs)`.\n- No resource throttling for multi-tenant single tables; design partition keys in the app `(community consensus)`."}}
CONTENT3_A.setdefault("edb", {})["multitenant"] = {
  "zh": {"v": "部分支持", "p": "PG 生态资源组能力有限",
         "b": "- 同 PG：无原生资源组，靠 cgroup/扩展有限管控 `社区共识`。\n- EDB 的 Kubernetes 部署可借 K8s 做资源限额 `厂商口径`。"},
  "en": {"v": "Partial", "p": "Limited resource-group capability in the PG ecosystem",
         "b": "- Same as PG: no native resource groups; limited control via cgroups/extensions `(community consensus)`.\n- EDB Kubernetes deployments can lean on K8s resource limits `(vendor claim)`."}}
CONTENT3_A.setdefault("etcd", {})["multitenant"] = {
  "zh": {"v": "不适用", "p": "元数据存储，无租户资源概念",
         "b": "- 定位是集群元数据/配置存储，无多租户资源隔离设计 `官方文档`。\n- quota 后端字节数是全局的，不是租户级 `官方文档`。"},
  "en": {"v": "N/A", "p": "Metadata store; no tenant-resource concept",
         "b": "- Built for cluster metadata/config; no multi-tenant resource isolation design `(official docs)`.\n- The backend-bytes quota is global, not per-tenant `(official docs)`."}}
CONTENT3_A.setdefault("mariadb", {})["multitenant"] = {
  "zh": {"v": "部分支持", "p": "无原生资源组；线程池有限缓解",
         "b": "- 无 CPU/内存/IO 租户限流 `社区共识`。\n- 线程池可缓解连接风暴，但不是 QoS `官方文档`。"},
  "en": {"v": "Partial", "p": "No native resource groups; thread pool helps only partly",
         "b": "- No per-tenant CPU/memory/IO throttling `(community consensus)`.\n- Thread pool mitigates connection storms but is not QoS `(official docs)`."}}
CONTENT3_A.setdefault("milvus", {})["multitenant"] = {
  "zh": {"v": "部分支持", "p": "RBAC+库级隔离；资源组有限",
         "b": "- RBAC + 多 database 逻辑隔离 `官方文档`。\n- 细粒度资源隔离能力弱，多租户多用多集合/多实例 `社区共识`。"},
  "en": {"v": "Partial", "p": "RBAC + database-level isolation; limited resource groups",
         "b": "- RBAC plus multi-database logical isolation `(official docs)`.\n- Weak fine-grained resource isolation; multi-tenancy usually means multiple collections/instances `(community consensus)`."}}
CONTENT3_A.setdefault("mongodb", {})["multitenant"] = {
  "zh": {"v": "部分支持", "p": "逻辑隔离为主；Atlas 有一定管控",
         "b": "- 自建靠多库/多集群逻辑隔离，无租户资源限流 `社区共识`。\n- Atlas 有慢查询终止等运维手段，但不是租户 QoS `官方文档`。"},
  "en": {"v": "Partial", "p": "Mostly logical isolation; Atlas adds some controls",
         "b": "- Self-hosted relies on multi-database/cluster logical isolation; no tenant throttling `(community consensus)`.\n- Atlas offers slow-query kill and ops tooling, but not tenant QoS `(official docs)`."}}
CONTENT3_A.setdefault("mysql", {})["multitenant"] = {
  "zh": {"v": "部分支持", "p": "resource group 有限，仅 CPU 亲和",
         "b": "- 8.0 resource group 可做线程 CPU 亲和/优先级，无内存/IO 限流 `官方文档`。\n- 生产多租户靠多实例，单实例混布 noisy neighbor 常见 `社区共识`。"},
  "en": {"v": "Partial", "p": "Limited resource groups; CPU affinity only",
         "b": "- 8.0 resource groups do thread CPU affinity/priority; no memory/IO throttling `(official docs)`.\n- Production multi-tenancy means multiple instances; noisy neighbors are common on shared ones `(community consensus)`."}}
CONTENT3_A.setdefault("oceanbase", {})["multitenant"] = {
  "zh": {"v": "有", "p": "资源单元/资源池，租户级隔离标杆",
         "b": "- Unit/资源池/租户三级体系，CPU/内存/IO/日志盘全可配额 `官方文档`。\n- 租户间资源硬隔离，是其多租户设计的核心 `官方文档`。\n- 规划 unit 规格需要容量评估，配小了扩、配大了浪费 `社区共识`。"},
  "en": {"v": "Supported", "p": "Resource units/pools; the tenant-isolation benchmark",
         "b": "- Unit/resource-pool/tenant hierarchy with quotas on CPU/memory/IO/log disk `(official docs)`.\n- Hard inter-tenant isolation is core to its multi-tenancy design `(official docs)`.\n- Sizing units needs capacity planning; too small forces scaling, too large wastes `(community consensus)`."}}
CONTENT3_A.setdefault("oracle", {})["multitenant"] = {
  "zh": {"v": "有", "p": "PDB+Resource Manager，多租户标杆",
         "b": "- Multitenant PDB + DB Resource Manager，CPU/IO/并行度租户级管控 `官方文档`。\n- 19c 起多租户是默认架构，隔离+资源管控最成熟 `官方文档`。\n- 授权按 PDB/选项收费，成本高 `社区共识`。"},
  "en": {"v": "Supported", "p": "PDB + Resource Manager; the multi-tenancy benchmark",
         "b": "- Multitenant PDBs + Database Resource Manager: tenant-level CPU/IO/parallelism control `(official docs)`.\n- Multitenant is the default architecture since 19c; the most mature isolation + control `(official docs)`.\n- Licensed per PDB/option; expensive `(community consensus)`."}}
CONTENT3_A.setdefault("polardb", {})["multitenant"] = {
  "zh": {"v": "部分支持", "p": "集群级隔离为主，无资源组",
         "b": "- 租户隔离靠多集群，单集群内无细粒度资源组 `社区共识`。\n- 读写分离+代理可做业务级分流 `官方文档`。"},
  "en": {"v": "Partial", "p": "Mostly cluster-level isolation",
         "b": "- Tenant isolation via multiple clusters; no fine-grained in-cluster resource groups `(community consensus)`.\n- Read/write splitting + proxy can separate workload classes `(official docs)`."}}
CONTENT3_A.setdefault("postgresql", {})["multitenant"] = {
  "zh": {"v": "部分支持", "p": "无原生资源组，靠外部手段",
         "b": "- 无原生 CPU/内存/IO 租户限流，statement_timeout 等是单查询保护 `社区共识`。\n- 靠 cgroup、连接池、多实例做隔离，方案散 `社区共识`。"},
  "en": {"v": "Partial", "p": "No native resource groups; external measures only",
         "b": "- No native per-tenant CPU/memory/IO throttling; statement_timeout only guards single queries `(community consensus)`.\n- Isolation via cgroups, pooling, multiple instances — fragmented approaches `(community consensus)`."}}
CONTENT3_A.setdefault("qdrant", {})["multitenant"] = {
  "zh": {"v": "部分支持", "p": "collection 逻辑隔离",
         "b": "- collection 级逻辑隔离，无资源限流 `社区共识`。\n- API key  crude 权限，不是 QoS `官方文档`。"},
  "en": {"v": "Partial", "p": "Collection-level logical isolation",
         "b": "- Logical isolation per collection; no resource throttling `(community consensus)`.\n- API keys are coarse auth, not QoS `(official docs)`."}}
CONTENT3_A.setdefault("redis-valkey", {})["multitenant"] = {
  "zh": {"v": "部分支持", "p": "db 编号逻辑隔离；无资源限流",
         "b": "- select db 编号做逻辑隔离，无 CPU/内存限流，一个租户可打满 `社区共识`。\n- 生产多租户靠多实例/分片，Redis Cluster 的 db 编号还受限 `社区共识`。"},
  "en": {"v": "Partial", "p": "DB-number logical isolation; no resource throttling",
         "b": "- SELECT db-number for logical isolation; no CPU/memory throttling — one tenant can saturate `(community consensus)`.\n- Production multi-tenancy means multiple instances/shards; db numbers are even restricted in Redis Cluster `(community consensus)`."}}
CONTENT3_A.setdefault("snowflake", {})["multitenant"] = {
  "zh": {"v": "有", "p": "warehouse 计算隔离，天然多租户",
         "b": "- 每个 warehouse 是独立计算集群，团队/业务按 warehouse 隔离，noisy neighbor 天然规避 `官方文档`。\n- warehouse 可设自动挂起/大小，成本与隔离兼得 `官方文档`。\n- 数据共享不复制，跨团队协作不破坏隔离 `官方文档`。"},
  "en": {"v": "Supported", "p": "Warehouse compute isolation; naturally multi-tenant",
         "b": "- Each warehouse is an isolated compute cluster; teams/workloads isolate by warehouse, sidestepping noisy neighbors `(official docs)`.\n- Warehouses auto-suspend/resize — isolation plus cost control `(official docs)`.\n- Data sharing without copies keeps collaboration from breaking isolation `(official docs)`."}}
CONTENT3_A.setdefault("spanner", {})["multitenant"] = {
  "zh": {"v": "部分支持", "p": "实例/库级隔离为主",
         "b": "- 租户隔离靠多实例/多库，单实例内无租户资源组 `社区共识`。\n- 托管自动扩缩部分缓解 noisy neighbor `官方文档`。"},
  "en": {"v": "Partial", "p": "Mostly instance/database-level isolation",
         "b": "- Tenant isolation via multiple instances/databases; no in-instance tenant resource groups `(community consensus)`.\n- Managed auto-scaling partly mitigates noisy neighbors `(official docs)`."}}
CONTENT3_A.setdefault("sqlserver", {})["multitenant"] = {
  "zh": {"v": "有", "p": "Resource Governor，租户级管控",
         "b": "- Resource Governor 按 workload group 限 CPU/内存/IO `官方文档`。\n- 配合 Resource Pool，租户 QoS 能力完整 `官方文档`。\n- 配置复杂，调优门槛高 `社区共识`。"},
  "en": {"v": "Supported", "p": "Resource Governor for tenant-level control",
         "b": "- Resource Governor throttles CPU/memory/IO per workload group `(official docs)`.\n- Combined with resource pools, tenant QoS is complete `(official docs)`.\n- Complex to configure; high tuning bar `(community consensus)`."}}
CONTENT3_A.setdefault("starrocks", {})["multitenant"] = {
  "zh": {"v": "有", "p": "workload group 资源组限流",
         "b": "- workload group 按用户/查询限 CPU/内存/IO `官方文档`。\n- 与 Doris 同源能力，是多租户推荐方案 `官方文档`。"},
  "en": {"v": "Supported", "p": "Workload-group resource throttling",
         "b": "- Workload groups throttle CPU/memory/IO per user/query `(official docs)`.\n- Same-lineage capability as Doris; the recommended multi-tenancy approach `(official docs)`."}}
CONTENT3_A.setdefault("tdsql", {})["multitenant"] = {
  "zh": {"v": "部分支持", "p": "实例/分片级隔离为主",
         "b": "- 租户隔离靠多实例/分片，细粒度资源组能力有限 `社区共识`。\n- 分布式版按分片打散天然有一定隔离 `社区共识`。"},
  "en": {"v": "Partial", "p": "Mostly instance/shard-level isolation",
         "b": "- Tenant isolation via multiple instances/shards; limited fine-grained resource groups `(community consensus)`.\n- The sharded edition's scattering gives some natural isolation `(community consensus)`."}}
CONTENT3_A.setdefault("tidb", {})["multitenant"] = {
  "zh": {"v": "有", "p": "Resource Control（RU）租户级限流",
         "b": "- Resource Control 按资源组分配 RU（Request Unit），CPU/IO 统一度量限流 `官方文档`。\n- 后台任务与前台业务可分组隔离，noisy neighbor 可控 `官方文档`。\n- RU 估算需要压测，配错会限错业务 `社区共识`。"},
  "en": {"v": "Supported", "p": "Resource Control (RU) tenant-level throttling",
         "b": "- Resource Control assigns RUs (Request Units) per resource group — unified CPU/IO metering `(official docs)`.\n- Background vs foreground workloads can be isolated by group; noisy neighbors contained `(official docs)`.\n- RU estimation needs load testing; misconfiguration throttles the wrong workload `(community consensus)`."}}
CONTENT3_A.setdefault("weaviate", {})["multitenant"] = {
  "zh": {"v": "部分支持", "p": "multi-tenancy 租户隔离；无资源限流",
         "b": "- 原生 multi-tenancy 按租户分数据，查询自动路由 `官方文档`。\n- 是数据隔离不是资源 QoS，无 CPU/内存限流 `社区共识`。"},
  "en": {"v": "Partial", "p": "Multi-tenancy data isolation; no resource throttling",
         "b": "- Native multi-tenancy shards data per tenant with automatic query routing `(official docs)`.\n- It's data isolation, not resource QoS — no CPU/memory throttling `(community consensus)`."}}
CONTENT3_A.setdefault("yugabytedb", {})["multitenant"] = {
  "zh": {"v": "部分支持", "p": "逻辑隔离为主；无租户资源组",
         "b": "- 靠多 keyspace/多库逻辑隔离，无租户级 CPU/IO 限流 `社区共识`。\n- admission control 类能力弱于 TiDB 的 RU `社区共识`。"},
  "en": {"v": "Partial", "p": "Mostly logical isolation; no tenant resource groups",
         "b": "- Logical isolation via multiple keyspaces/databases; no tenant CPU/IO throttling `(community consensus)`.\n- Admission-control weaker than TiDB's RU `(community consensus)`."}}
CONTENT3_A.setdefault("redshift", {})["multitenant"] = {
  "zh": {"v": "有", "p": "WLM 查询队列，查询级资源管理",
         "b": "- WLM 按队列分配内存/并发，业务按队列隔离 `官方文档`。\n- 自动 WLM 简化配置，手动 WLM 可精细调 `官方文档`。\n- 是查询级 QoS，不是租户级硬隔离，超大查询仍可挤占 `社区共识`。"},
  "en": {"v": "Supported", "p": "WLM query queues; query-level resource management",
         "b": "- WLM assigns memory/concurrency per queue; workloads isolate by queue `(official docs)`.\n- Auto WLM simplifies setup; manual WLM allows fine tuning `(official docs)`.\n- It's query-level QoS, not hard tenant isolation — huge queries can still crowd out `(community consensus)`."}}
CONTENT3_A.setdefault("bigquery", {})["multitenant"] = {
  "zh": {"v": "有", "p": "slot 预留/分配，计算资源隔离",
         "b": "- 预留 slot 按项目/团队分配，互不抢占 `官方文档`。\n- 按需模式靠配额限流，隔离弱于预留 `官方文档`。\n- 成本归因到项目标签，FinOps 友好 `社区共识`。"},
  "en": {"v": "Supported", "p": "Slot reservations/assignments; compute isolation",
         "b": "- Reserved slots assigned per project/team with no preemption `(official docs)`.\n- On-demand mode relies on quota throttling — weaker isolation than reservations `(official docs)`.\n- Cost attribution via project labels is FinOps-friendly `(community consensus)`."}}

# ---------------- 维度 multi_region：跨地域多活 ----------------
# scope: 多 region 写入、就近读、region 级容灾。与"支持跨云"区分：这里指地理多活。
CONTENT3_A.setdefault("alloydb", {})["multi_region"] = {
  "zh": {"v": "部分支持", "p": "跨区只读副本；无多活写入",
         "b": "- 支持跨区只读副本，就近读可以，写仍是单主 `官方文档`。\n- region 故障需手动/半自动提升，RTO 分钟级 `社区共识`。"},
  "en": {"v": "Partial", "p": "Cross-region read replicas; no multi-write",
         "b": "- Cross-region read replicas for local reads; writes stay single-primary `(official docs)`.\n- Region failure needs manual/semi-auto promotion, minutes of RTO `(community consensus)`."}}
CONTENT3_A.setdefault("aurora", {})["multi_region"] = {
  "zh": {"v": "部分支持", "p": "Global Database 跨区读；写单主",
         "b": "- Global Database：一写多读跨区，读延迟低，写仍单 region `官方文档`。\n- 跨区故障转移分钟级，有数据丢失窗口（RPO 非零）`官方文档`。\n- 写多活需应用层分片，无原生方案 `社区共识`。"},
  "en": {"v": "Partial", "p": "Global Database cross-region reads; single-writer",
         "b": "- Global Database: one writer, cross-region readers with low read latency `(official docs)`.\n- Cross-region failover takes minutes with a data-loss window (non-zero RPO) `(official docs)`.\n- Multi-writer needs app-layer sharding; no native option `(community consensus)`."}}
CONTENT3_A.setdefault("cassandra-scylladb", {})["multi_region"] = {
  "zh": {"v": "有", "p": "多 DC 原生，副本策略跨机房",
         "b": "- NetworkTopologyStrategy 按 DC 放副本，天然跨地域 `官方文档`。\n- LOCAL_QUORUM 就近读写，EACH_QUORUM 强一致但延迟高 `官方文档`。\n- 跨区延迟直接加到写路径，机房间网络质量决定体验 `社区共识`。"},
  "en": {"v": "Supported", "p": "Native multi-DC; replica strategy spans sites",
         "b": "- NetworkTopologyStrategy places replicas per DC — cross-region by design `(official docs)`.\n- LOCAL_QUORUM for local reads/writes; EACH_QUORUM for strong consistency at high latency `(official docs)`.\n- Cross-region latency lands directly on the write path; inter-DC network quality decides the experience `(community consensus)`."}}
CONTENT3_A.setdefault("clickhouse", {})["multi_region"] = {
  "zh": {"v": "部分支持", "p": "分片复制可跨区部署；无原生多活",
         "b": "- 分片+副本可手工跨区部署，无原生多 region 协调 `社区共识`。\n- 跨区写放大，ON CLUSTER DDL 跨区延迟高 `社区共识`。"},
  "en": {"v": "Partial", "p": "Sharded replication can span regions; no native active-active",
         "b": "- Shards + replicas can be hand-deployed across regions; no native multi-region coordination `(community consensus)`.\n- Cross-region write amplification; ON CLUSTER DDL is slow across regions `(community consensus)`."}}
CONTENT3_A.setdefault("cockroachdb", {})["multi_region"] = {
  "zh": {"v": "有", "p": "多 region 生存目标，原生多活",
         "b": "- REGIONAL BY ROW 等生存目标，数据放离用户近的 region `官方文档`。\n- 多 region 写原生支持，follower 读降低跨区读延迟 `官方文档`。\n- 跨区事务延迟是物理上限，设计表时要分区裁剪 `社区共识`。"},
  "en": {"v": "Supported", "p": "Multi-region survival goals; native active-active",
         "b": "- Survival goals like REGIONAL BY ROW pin data near users `(official docs)`.\n- Native multi-region writes; follower reads cut cross-region read latency `(official docs)`.\n- Cross-region transaction latency is a physics limit — design tables for partition pruning `(community consensus)`."}}
CONTENT3_A.setdefault("databricks", {})["multi_region"] = {
  "zh": {"v": "部分支持", "p": "Delta Sharing 跨区读；无跨区多活写",
         "b": "- Delta Sharing 可跨区/跨云共享数据读 `官方文档`。\n- 写仍是单工作区/单区，无多活写入语义 `社区共识`。\n- region 容灾靠工作区备份重建，RTO 看数据量 `社区共识`。"},
  "en": {"v": "Partial", "p": "Delta Sharing cross-region reads; no cross-region writes",
         "b": "- Delta Sharing shares data for reads across regions/clouds `(official docs)`.\n- Writes stay single-workspace/single-region; no active-active write semantics `(community consensus)`.\n- Region DR means rebuilding workspaces; RTO scales with data `(community consensus)`."}}
CONTENT3_A.setdefault("doris", {})["multi_region"] = {
  "zh": {"v": "部分支持", "p": "可手工跨区部署；无原生多活",
         "b": "- FE/BE 可跨区部署，但无原生多 region 写入协调 `社区共识`。\n- 跨区副本同步延迟影响写，生产多用单区+容灾 `社区共识`。"},
  "en": {"v": "Partial", "p": "Manual cross-region deployment; no native active-active",
         "b": "- FE/BE can span regions, but no native multi-region write coordination `(community consensus)`.\n- Cross-region replica lag affects writes; production usually single-region + DR `(community consensus)`."}}
CONTENT3_A.setdefault("duckdb", {})["multi_region"] = {
  "zh": {"v": "不适用", "p": "嵌入式单机，无地域概念",
         "b": "- 单进程嵌入式，多活无意义 `官方文档`。\n- 文件级复制可做异地备份，但不是多活语义 `社区共识`。"},
  "en": {"v": "N/A", "p": "Embedded single-node; no region concept",
         "b": "- Single-process embedded; active-active is meaningless `(official docs)`.\n- File-level copies work for offsite backup, not active-active semantics `(community consensus)`."}}
CONTENT3_A.setdefault("dynamodb", {})["multi_region"] = {
  "zh": {"v": "有", "p": "Global Tables 多活写",
         "b": "- Global Tables 多区多活写，最终一致，冲突 last-writer-wins `官方文档`。\n- 冲突解决粗糙，不适合强一致多写场景 `社区共识`。\n- 跨区复制延迟通常 1 秒内 `官方文档`。"},
  "en": {"v": "Supported", "p": "Global Tables active-active writes",
         "b": "- Global Tables: multi-region active writes, eventually consistent, last-writer-wins conflicts `(official docs)`.\n- Crude conflict resolution; unfit for strong-consistency multi-write needs `(community consensus)`.\n- Cross-region replication lag typically under a second `(official docs)`."}}
CONTENT3_A.setdefault("edb", {})["multi_region"] = {
  "zh": {"v": "部分支持", "p": "PG 流复制/逻辑复制跨区可配",
         "b": "- 流复制/逻辑复制可跨区，无原生多活写 `社区共识`。\n- 冲突解决靠应用层，双写是禁区 `社区共识`。"},
  "en": {"v": "Partial", "p": "PG streaming/logical replication across regions",
         "b": "- Streaming/logical replication can span regions; no native active-active writes `(community consensus)`.\n- Conflict resolution is app-layer; dual-write is off-limits `(community consensus)`."}}
CONTENT3_A.setdefault("etcd", {})["multi_region"] = {
  "zh": {"v": "不适用", "p": "Raft 单 region，不建议跨区",
         "b": "- Raft 强一致要求低延迟，跨区部署延迟爆炸 `官方文档`。\n- 定位是单 region 集群元数据存储 `社区共识`。"},
  "en": {"v": "N/A", "p": "Raft single-region; cross-region not advised",
         "b": "- Raft's strong consistency needs low latency; cross-region latency explodes `(official docs)`.\n- Built as single-region cluster metadata storage `(community consensus)`."}}
CONTENT3_A.setdefault("mariadb", {})["multi_region"] = {
  "zh": {"v": "部分支持", "p": "Galera/主从跨区可配；延迟敏感",
         "b": "- Galera 多写跨区对延迟极敏感，生产少用 `社区共识`。\n- 主从跨区是常规容灾，无多活写 `社区共识`。"},
  "en": {"v": "Partial", "p": "Galera/primary-replica across regions; latency-sensitive",
         "b": "- Galera multi-writer across regions is extremely latency-sensitive; rarely used in production `(community consensus)`.\n- Cross-region primary-replica is standard DR; no active-active writes `(community consensus)`."}}
CONTENT3_A.setdefault("milvus", {})["multi_region"] = {
  "zh": {"v": "无", "p": "集群单区，无跨区多活",
         "b": "- 集群按单区设计，无跨 region 多活写 `待验证`。\n- 跨区靠数据复制重建，无原生方案 `社区共识`。"},
  "en": {"v": "Not supported", "p": "Single-region clusters; no cross-region active-active",
         "b": "- Clusters are single-region by design; no cross-region active writes `(to be verified)`.\n- Cross-region means copy-and-rebuild; no native story `(community consensus)`."}}
CONTENT3_A.setdefault("mongodb", {})["multi_region"] = {
  "zh": {"v": "有", "p": "Atlas Global Cluster，多活写",
         "b": "- Global Cluster 按区放分片，就近写，zone 级故障自动转移 `官方文档`。\n- 自建分片集群也可跨区，但运维复杂度陡增 `社区共识`。\n- 跨区分片键设计决定延迟，错了难改 `社区共识`。"},
  "en": {"v": "Supported", "p": "Atlas Global Cluster; active-active writes",
         "b": "- Global Cluster pins shards per zone for local writes with automatic zone failover `(official docs)`.\n- Self-hosted sharded clusters can span regions but ops complexity jumps `(community consensus)`.\n- Cross-region shard-key design decides latency; hard to fix later `(community consensus)`."}}
CONTENT3_A.setdefault("mysql", {})["multi_region"] = {
  "zh": {"v": "部分支持", "p": "主从跨区可配；双写冲突无解",
         "b": "- 主从/组复制可跨区，延迟看网络 `社区共识`。\n- 双写多活无原生冲突解决，生产禁区 `社区共识`。\n- Group Replication 跨区对延迟敏感 `官方文档`。"},
  "en": {"v": "Partial", "p": "Cross-region replicas configurable; dual-write conflicts unsolved",
         "b": "- Primary-replica / Group Replication can span regions; latency follows the network `(community consensus)`.\n- No native conflict resolution for dual-write active-active; off-limits in production `(community consensus)`.\n- Group Replication is latency-sensitive across regions `(official docs)`."}}
CONTENT3_A.setdefault("oceanbase", {})["multi_region"] = {
  "zh": {"v": "有", "p": "三地五中心，多地多活",
         "b": "- Paxos 多副本天然跨机房/地域，'三地五中心'是标准架构 `官方文档`。\n- 多地写原生支持，时钟同步要求高 `官方文档`。\n- 跨城延迟进写路径，选型要实测 `社区共识`。"},
  "en": {"v": "Supported", "p": "Three-site/five-center; multi-site active-active",
         "b": "- Paxos multi-replica spans sites/regions natively; 'three-site five-center' is the standard architecture `(official docs)`.\n- Native multi-site writes; demanding clock-sync requirements `(official docs)`.\n- Cross-city latency lands on the write path — measure in selection `(community consensus)`."}}
CONTENT3_A.setdefault("oracle", {})["multi_region"] = {
  "zh": {"v": "部分支持", "p": "ADG/GG 可配；复杂且贵",
         "b": "- Active Data Guard 跨区备库、GoldenGate 双向复制可配多活 `官方文档`。\n- 方案成熟但架构复杂、授权贵，运维门槛高 `社区共识`。\n- 真多写冲突解决靠应用层 `社区共识`。"},
  "en": {"v": "Partial", "p": "ADG/GG configurable; complex and costly",
         "b": "- Active Data Guard cross-region standbys and GoldenGate bidirectional replication enable active-active `(official docs)`.\n- Mature but architecturally complex, costly licensing, high ops bar `(community consensus)`.\n- True multi-write conflict resolution stays app-layer `(community consensus)`."}}
CONTENT3_A.setdefault("polardb", {})["multi_region"] = {
  "zh": {"v": "有", "p": "全球多活网络（GDN）",
         "b": "- PolarDB GDN 支持跨地域集群，写单主、读就近 `官方文档`。\n- 跨区延迟 <100ms 场景可用，延迟高则体验下降 `官方文档`。\n- 多活写仍是单主语义 `社区共识`。"},
  "en": {"v": "Supported", "p": "Global active network (GDN)",
         "b": "- PolarDB GDN supports cross-region clusters: single writer, local reads `(official docs)`.\n- Works where cross-region latency is <100ms; degrades beyond `(official docs)`.\n- Multi-active is still single-writer semantics `(community consensus)`."}}
CONTENT3_A.setdefault("postgresql", {})["multi_region"] = {
  "zh": {"v": "部分支持", "p": "逻辑复制/流复制跨区可配",
         "b": "- 流复制/逻辑复制可跨区，无原生多活写 `社区共识`。\n- 双向逻辑复制冲突解决弱，生产慎用 `社区共识`。"},
  "en": {"v": "Partial", "p": "Logical/streaming replication across regions",
         "b": "- Streaming/logical replication can span regions; no native active-active writes `(community consensus)`.\n- Bidirectional logical replication has weak conflict handling; use cautiously `(community consensus)`."}}
CONTENT3_A.setdefault("qdrant", {})["multi_region"] = {
  "zh": {"v": "无", "p": "分布式集群单区；无跨区多活",
         "b": "- Raft 分布式按单区设计，无跨 region 多活 `待验证`。\n- 跨区靠重建集群同步数据 `社区共识`。"},
  "en": {"v": "Not supported", "p": "Single-region distributed clusters; no cross-region active-active",
         "b": "- Raft-based distribution is single-region by design; no cross-region active-active `(to be verified)`.\n- Cross-region means rebuilding and syncing data `(community consensus)`."}}
CONTENT3_A.setdefault("redis-valkey", {})["multi_region"] = {
  "zh": {"v": "部分支持", "p": "企业版 Active-Active（CRDT）；开源无",
         "b": "- Redis Enterprise Active-Active 用 CRDT 做多活写，开源版无 `厂商口径`。\n- 开源跨区靠主从复制，写单点 `社区共识`。"},
  "en": {"v": "Partial", "p": "Enterprise Active-Active (CRDT); not in open source",
         "b": "- Redis Enterprise Active-Active uses CRDTs for multi-writer; absent in open source `(vendor claim)`.\n- Open-source cross-region relies on primary-replica; single write point `(community consensus)`."}}
CONTENT3_A.setdefault("snowflake", {})["multi_region"] = {
  "zh": {"v": "有", "p": "跨区复制/故障转移；写仍单区",
         "b": "- 数据库复制到多区，故障时提升，RTO 分钟级 `官方文档`。\n- 是容灾不是多活写，写仍单区 `官方文档`。\n- 跨区复制产生计算+传输费用 `社区共识`。"},
  "en": {"v": "Supported", "p": "Cross-region replication/failover; single-region writes",
         "b": "- Databases replicate to multiple regions with promotion on failure; minutes of RTO `(official docs)`.\n- It's DR, not active-active writes — writes stay single-region `(official docs)`.\n- Cross-region replication incurs compute + transfer costs `(community consensus)`."}}
CONTENT3_A.setdefault("spanner", {})["multi_region"] = {
  "zh": {"v": "有", "p": "全球多活，原生强项",
         "b": "- TrueTime 下全球多活写，外部一致性，region 故障自动 `官方文档`。\n- 跨区延迟是物理下限， schema 设计（交错表）可优化 `官方文档`。\n- 多区实例成本显著高于单区 `社区共识`。"},
  "en": {"v": "Supported", "p": "Global active-active; native strength",
         "b": "- TrueTime-backed global active writes with external consistency and automatic region failover `(official docs)`.\n- Cross-region latency is a physics floor; schema design (interleaved tables) helps `(official docs)`.\n- Multi-region instances cost notably more than single-region `(community consensus)`."}}
CONTENT3_A.setdefault("sqlserver", {})["multi_region"] = {
  "zh": {"v": "部分支持", "p": "Always On AG 跨区可配",
         "b": "- AG 可跨子网/跨区，异步提交做容灾 `官方文档`。\n- 同步提交跨区延迟高，生产多用异步 `社区共识`。\n- 分布式 AG 可做多写，复杂 `官方文档`。"},
  "en": {"v": "Partial", "p": "Always On AG across regions",
         "b": "- AGs span subnets/regions; async commit for DR `(official docs)`.\n- Sync commit across regions is high-latency; production favors async `(community consensus)`.\n- Distributed AGs allow multi-write; complex `(official docs)`."}}
CONTENT3_A.setdefault("starrocks", {})["multi_region"] = {
  "zh": {"v": "部分支持", "p": "可手工跨区；无原生多活",
         "b": "- FE/BE 可跨区部署，无原生多 region 协调 `社区共识`。\n- 生产多用单区 + 容灾 `社区共识`。"},
  "en": {"v": "Partial", "p": "Manual cross-region; no native active-active",
         "b": "- FE/BE can span regions; no native multi-region coordination `(community consensus)`.\n- Production usually single-region + DR `(community consensus)`."}}
CONTENT3_A.setdefault("tdsql", {})["multi_region"] = {
  "zh": {"v": "有", "p": "多中心架构，跨区容灾/多活",
         "b": "- 分布式版支持跨中心部署，强同步多活可配 `官方文档`。\n- 跨中心延迟要求高，选型看网络 `社区共识`。"},
  "en": {"v": "Supported", "p": "Multi-center architecture; cross-region DR/active-active",
         "b": "- The distributed edition supports cross-center deployment with configurable strongly-sync active-active `(official docs)`.\n- Demands low cross-center latency; network decides `(community consensus)`."}}
CONTENT3_A.setdefault("tidb", {})["multi_region"] = {
  "zh": {"v": "有", "p": "多中心多活，放置规则跨区",
         "b": "- placement rules 按 DC/rack/zone 放副本，天然跨地域 `官方文档`。\n- follower 读 + stale read 降低跨区读延迟 `官方文档`。\n- 跨区写延迟是物理上限，业务分区键设计关键 `社区共识`。"},
  "en": {"v": "Supported", "p": "Multi-center active-active; placement rules span regions",
         "b": "- Placement rules place replicas by DC/rack/zone — cross-region by design `(official docs)`.\n- Follower reads + stale reads cut cross-region read latency `(official docs)`.\n- Cross-region write latency is a physics floor; business partition-key design is key `(community consensus)`."}}
CONTENT3_A.setdefault("weaviate", {})["multi_region"] = {
  "zh": {"v": "无", "p": "单区集群；无跨区多活",
         "b": "- 集群按单区设计，无跨 region 多活 `待验证`。\n- 跨区需求靠备份恢复重建 `社区共识`。"},
  "en": {"v": "Not supported", "p": "Single-region clusters; no cross-region active-active",
         "b": "- Clusters are single-region by design; no cross-region active-active `(to be verified)`.\n- Cross-region needs are met by backup-restore rebuilds `(community consensus)`."}}
CONTENT3_A.setdefault("yugabytedb", {})["multi_region"] = {
  "zh": {"v": "有", "p": "xCluster/多 region，原生多活",
         "b": "- xCluster 跨集群复制 + 多 region 部署，写多活原生 `官方文档`。\n- 按表/行级 geo-partition 就近读写 `官方文档`。\n- 跨区延迟同样进写路径，设计决定体验 `社区共识`。"},
  "en": {"v": "Supported", "p": "xCluster / multi-region; native active-active",
         "b": "- xCluster cross-cluster replication plus multi-region deployment; native active writes `(official docs)`.\n- Table-/row-level geo-partitioning for local reads/writes `(official docs)`.\n- Cross-region latency still hits the write path; design decides the experience `(community consensus)`."}}
CONTENT3_A.setdefault("redshift", {})["multi_region"] = {
  "zh": {"v": "部分支持", "p": "跨区快照复制；无多活写",
         "b": "- 跨区快照复制做容灾，RTO 看恢复时间 `官方文档`。\n- 写单区，无多活语义 `社区共识`。"},
  "en": {"v": "Partial", "p": "Cross-region snapshot copy; no active-active writes",
         "b": "- Cross-region snapshot copy for DR; RTO follows restore time `(official docs)`.\n- Single-region writes; no active-active semantics `(community consensus)`."}}
CONTENT3_A.setdefault("bigquery", {})["multi_region"] = {
  "zh": {"v": "部分支持", "p": "跨区数据集复制；写仍单区",
         "b": "- 数据集跨区复制（BigQuery 跨区域复制）做容灾/就近读 `官方文档`。\n- 写仍是单区语义，无多活写 `官方文档`。\n- 复制产生额外存储+作业费用 `社区共识`。"},
  "en": {"v": "Partial", "p": "Cross-region dataset copy; single-region writes",
         "b": "- Cross-region dataset copy for DR / local reads `(official docs)`.\n- Writes stay single-region; no active-active writes `(official docs)`.\n- Copies incur extra storage + job costs `(community consensus)`."}}

# ---------------- 维度 ha_rto：高可用架构与 RTO/RPO ----------------
# scope: 自动故障切换、脑裂防护、RTO/RPO 量级。偏可用性目标，不重复复制机制细节。
CONTENT3_A.setdefault("alloydb", {})["ha_rto"] = {
  "zh": {"v": "有", "p": "自动故障切换，RTO 分钟级",
         "b": "- 高可用实例自动故障切换，RTO 通常分钟级 `官方文档`。\n- 存储与计算分离，故障切换不丢已提交数据（RPO≈0）`官方文档`。\n- 跨区切换需手动，RTO 更长 `社区共识`。"},
  "en": {"v": "Supported", "p": "Automatic failover; minutes of RTO",
         "b": "- HA instances fail over automatically, typically minutes of RTO `(official docs)`.\n- Storage/compute separation means committed data survives failover (RPO≈0) `(official docs)`.\n- Cross-region failover is manual with longer RTO `(community consensus)`."}}
CONTENT3_A.setdefault("aurora", {})["ha_rto"] = {
  "zh": {"v": "有", "p": "存储 6 副本，故障切换 15 秒级",
         "b": "- 存储层 6 副本跨 3AZ，计算故障切换通常 15-30 秒 `官方文档`。\n- RPO≈0（存储层复制），是其 HA 核心优势 `官方文档`。\n- 切换期间连接闪断，应用需重试逻辑 `社区共识`。"},
  "en": {"v": "Supported", "p": "6-way storage replicas; ~15s failover",
         "b": "- Storage replicates 6 ways across 3 AZs; compute failover usually 15–30s `(official docs)`.\n- RPO≈0 via storage-layer replication — its core HA advantage `(official docs)`.\n- Connections flap during failover; apps need retry logic `(community consensus)`."}}
CONTENT3_A.setdefault("cassandra-scylladb", {})["ha_rto"] = {
  "zh": {"v": "有", "p": "无单点；节点故障自动绕过",
         "b": "- 对等架构无主节点，单节点故障客户端自动绕过，RTO≈0（读/写按一致性级别降级）`官方文档`。\n- RPO 取决于一致性级别，ONE 级别可能丢数 `官方文档`。\n- hinted handoff + 修复保障最终一致 `官方文档`。"},
  "en": {"v": "Supported", "p": "No single point; failed nodes bypassed automatically",
         "b": "- Peer architecture has no primary; clients bypass failed nodes automatically — RTO≈0 (reads/writes degrade per consistency level) `(official docs)`.\n- RPO follows the consistency level; ONE can lose data `(official docs)`.\n- Hinted handoff + repair ensure eventual consistency `(official docs)`."}}
CONTENT3_A.setdefault("clickhouse", {})["ha_rto"] = {
  "zh": {"v": "部分支持", "p": "副本+keeper；无自动主切换语义",
         "b": "- 分片副本 + ClickHouse Keeper 做协调，副本故障可切 `官方文档`。\n- 无传统主从自动切换语义，故障处理靠副本冗余+客户端重试 `社区共识`。\n- Keeper 本身要高可用部署，否则成单点 `社区共识`。"},
  "en": {"v": "Partial", "p": "Replicas + Keeper; no automatic primary failover semantics",
         "b": "- Shard replicas + ClickHouse Keeper for coordination; failed replicas can be cut over `(official docs)`.\n- No traditional primary-failover semantics; HA relies on replica redundancy + client retries `(community consensus)`.\n- Keeper itself needs an HA deployment or it becomes the single point `(community consensus)`."}}
CONTENT3_A.setdefault("cockroachdb", {})["ha_rto"] = {
  "zh": {"v": "有", "p": "Raft 自愈，RTO 秒级",
         "b": "- Raft 多副本，节点故障自动选主，RTO 秒级 `官方文档`。\n- RPO=0（多数派提交），脑裂靠 Raft 任期防护 `官方文档`。\n- 多活架构下单节点故障业务几乎无感 `社区共识`。"},
  "en": {"v": "Supported", "p": "Raft self-healing; seconds of RTO",
         "b": "- Raft multi-replica; failed nodes trigger automatic re-election in seconds `(official docs)`.\n- RPO=0 (majority commit); Raft terms guard against split-brain `(official docs)`.\n- In active-active setups single-node failure is nearly invisible to traffic `(community consensus)`."}}
CONTENT3_A.setdefault("databricks", {})["ha_rto"] = {
  "zh": {"v": "部分支持", "p": "托管控制平面；计算集群可重启恢复",
         "b": "- 控制平面托管高可用，计算集群故障可重建恢复 `官方文档`。\n- Delta Lake 的 ACID 让任务重跑不脏数据，RPO 靠检查点 `社区共识`。\n- SLA 是平台级，具体 RTO 看集群重建时间 `厂商口径`。"},
  "en": {"v": "Partial", "p": "Managed control plane; compute clusters rebuildable",
         "b": "- Managed control plane is HA; failed compute clusters rebuild `(official docs)`.\n- Delta Lake ACID keeps retries clean; RPO follows checkpoints `(community consensus)`.\n- SLA is platform-level; actual RTO follows cluster rebuild time `(vendor claim)`."}}
CONTENT3_A.setdefault("doris", {})["ha_rto"] = {
  "zh": {"v": "有", "p": "FE/BE 多副本，master 自动切换",
         "b": "- FE 多节点（master 自动选），BE 多副本，单点故障自动容错 `官方文档`。\n- RPO≈0（多数派写成功），RTO 分钟级内 `社区共识`。\n- FE 元数据依赖 bdbje 高可用，部署要注意 `社区共识`。"},
  "en": {"v": "Supported", "p": "Multi-replica FE/BE; automatic master election",
         "b": "- Multi-node FE (auto-elected master) and multi-replica BE tolerate single-point failures `(official docs)`.\n- RPO≈0 (majority writes); RTO within minutes `(community consensus)`.\n- FE metadata relies on bdbje HA — deploy it carefully `(community consensus)`."}}
CONTENT3_A.setdefault("duckdb", {})["ha_rto"] = {
  "zh": {"v": "不适用", "p": "嵌入式单机，无 HA 语义",
         "b": "- 单进程嵌入式，HA 靠宿主应用/文件备份 `官方文档`。\n- 进程崩溃靠宿主重启，单文件数据易备份 `社区共识`。"},
  "en": {"v": "N/A", "p": "Embedded single-node; no HA semantics",
         "b": "- Single-process embedded; HA is the host app's / file backups' job `(official docs)`.\n- Process crashes are the host's restart concern; the single-file data is easy to back up `(community consensus)`."}}
CONTENT3_A.setdefault("dynamodb", {})["ha_rto"] = {
  "zh": {"v": "有", "p": "托管多 AZ，SLA 99.99%",
         "b": "- 数据多 AZ 同步复制，AZ 故障自动容错 `官方文档`。\n- Global Tables 另有 99.999% SLA 档 `官方文档`。\n- RTO/RPO 由平台兜底，用户无感知 `社区共识`。"},
  "en": {"v": "Supported", "p": "Managed multi-AZ; 99.99% SLA",
         "b": "- Data replicates synchronously across AZs with automatic AZ-failure tolerance `(official docs)`.\n- Global Tables offer a 99.999% SLA tier `(official docs)`.\n- RTO/RPO are the platform's problem; users notice nothing `(community consensus)`."}}
CONTENT3_A.setdefault("edb", {})["ha_rto"] = {
  "zh": {"v": "部分支持", "p": "同 PG，需外部高可用组件",
         "b": "- 靠 Patroni/repmgr 等做自动切换，RTO 分钟级 `社区共识`。\n- 脑裂防护靠 fencing/多数派，需正确配置 `社区共识`。\n- EDB 托管/工具链可简化，但自建仍要 DBA 功力 `厂商口径`。"},
  "en": {"v": "Partial", "p": "Same as PG; external HA components needed",
         "b": "- Automatic failover via Patroni/repmgr; minutes of RTO `(community consensus)`.\n- Split-brain protection via fencing/quorum needs correct setup `(community consensus)`.\n- EDB managed/tooling simplifies, but self-hosted still demands DBA skill `(vendor claim)`."}}
CONTENT3_A.setdefault("etcd", {})["ha_rto"] = {
  "zh": {"v": "有", "p": "Raft 选主，秒级恢复",
         "b": "- Raft 多副本，leader 故障秒级重选，RPO=0 `官方文档`。\n- 推荐 3/5 节点，偶数节点无意义 `官方文档`。\n- 磁盘延迟是 leader 选举抖动常见根因 `社区共识`。"},
  "en": {"v": "Supported", "p": "Raft election; recovery in seconds",
         "b": "- Raft multi-replica; leader failure triggers re-election in seconds, RPO=0 `(official docs)`.\n- 3/5 nodes recommended; even counts are pointless `(official docs)`.\n- Disk latency is the classic cause of election flapping `(community consensus)`."}}
CONTENT3_A.setdefault("mariadb", {})["ha_rto"] = {
  "zh": {"v": "部分支持", "p": "主从/MHA/Galera，方案散",
         "b": "- MHA/MMM/主从手动切，RTO 分钟级，脑裂风险看方案 `社区共识`。\n- Galera 多主同步，节点故障自动，但写放大 `官方文档`。\n- 无一键托管 HA，自建拼装 `社区共识`。"},
  "en": {"v": "Partial", "p": "Primary-replica / MHA / Galera; fragmented options",
         "b": "- MHA/MMM/manual primary-replica cutover: minutes of RTO, split-brain risk varies `(community consensus)`.\n- Galera multi-primary syncs with automatic node handling but write amplification `(official docs)`.\n- No one-click managed HA; self-assembled `(community consensus)`."}}
CONTENT3_A.setdefault("milvus", {})["ha_rto"] = {
  "zh": {"v": "部分支持", "p": "K8s 多副本；恢复看编排",
         "b": "- K8s 部署多副本，Pod 故障重建，RTO 看调度速度 `官方文档`。\n- 元数据（etcd）与对象存储本身高可用 `社区共识`。"},
  "en": {"v": "Partial", "p": "K8s multi-replica; recovery follows orchestration",
         "b": "- K8s multi-replica; failed Pods rebuild — RTO follows scheduling speed `(official docs)`.\n- Metadata (etcd) and object storage are HA themselves `(community consensus)`."}}
CONTENT3_A.setdefault("mongodb", {})["ha_rto"] = {
  "zh": {"v": "有", "p": "副本集自动选举，约 10 秒",
         "b": "- 副本集主故障自动选举，通常 10 秒内 `官方文档`。\n- RPO 看 writeConcern，majority 则≈0 `官方文档`。\n- 选举期间写不可用，应用需重试 `社区共识`。"},
  "en": {"v": "Supported", "p": "Replica-set auto-election in ~10s",
         "b": "- Primary failure triggers automatic election, usually within 10s `(official docs)`.\n- RPO follows writeConcern; majority means ≈0 `(official docs)`.\n- Writes unavailable during election; apps must retry `(community consensus)`."}}
CONTENT3_A.setdefault("mysql", {})["ha_rto"] = {
  "zh": {"v": "部分支持", "p": "MHA/MGR/InnoDB Cluster，方案多但散",
         "b": "- MHA 手动/半自动切，RTO 分钟级，有脑裂风险 `社区共识`。\n- MGR/InnoDB Cluster 原生自动切，RTO 秒到分钟，但运维复杂 `官方文档`。\n- 半同步复制可保 RPO≈0，异步则可能丢数 `官方文档`。"},
  "en": {"v": "Partial", "p": "MHA / MGR / InnoDB Cluster; many but fragmented options",
         "b": "- MHA manual/semi-auto cutover: minutes of RTO with split-brain risk `(community consensus)`.\n- MGR/InnoDB Cluster fail over natively in seconds-to-minutes but are complex to run `(official docs)`.\n- Semi-sync keeps RPO≈0; async can lose data `(official docs)`."}}
CONTENT3_A.setdefault("oceanbase", {})["ha_rto"] = {
  "zh": {"v": "有", "p": "Paxos 多副本，RTO 30 秒内",
         "b": "- Paxos 多副本自动选主，RTO 通常 30 秒内 `官方文档`。\n- RPO=0（多数派提交），无脑裂 `官方文档`。\n- 城市级故障靠多地多中心架构 `官方文档`。"},
  "en": {"v": "Supported", "p": "Paxos multi-replica; RTO within 30s",
         "b": "- Paxos multi-replica with automatic leader election, usually within 30s `(official docs)`.\n- RPO=0 (majority commit); no split-brain `(official docs)`.\n- City-level failures handled by the multi-site architecture `(official docs)`."}}
CONTENT3_A.setdefault("oracle", {})["ha_rto"] = {
  "zh": {"v": "有", "p": "RAC/Data Guard，HA 标杆",
         "b": "- RAC 节点故障实例级接管，Data Guard 自动切换（FSFO）`官方文档`。\n- RTO 秒到分钟，RPO 可 0（同步备库）`官方文档`。\n- 方案成熟但贵且复杂 `社区共识`。"},
  "en": {"v": "Supported", "p": "RAC / Data Guard; the HA benchmark",
         "b": "- RAC takes over at instance level on node failure; Data Guard fast-start failover `(official docs)`.\n- RTO seconds-to-minutes; RPO can be 0 (sync standby) `(official docs)`.\n- Mature but expensive and complex `(community consensus)`."}}
CONTENT3_A.setdefault("polardb", {})["ha_rto"] = {
  "zh": {"v": "有", "p": "一写多读快速切换",
         "b": "- 共享存储一写多读，主故障只读节点快速提升，RTO 秒级 `官方文档`。\n- RPO≈0（Redo 日志共享）`官方文档`。\n- 切换对长连接有闪断，应用需重连 `社区共识`。"},
  "en": {"v": "Supported", "p": "Single-writer multi-reader fast failover",
         "b": "- Shared-storage single-writer multi-reader; readers promote in seconds on primary failure `(official docs)`.\n- RPO≈0 (shared redo log) `(official docs)`.\n- Long connections flap on failover; apps must reconnect `(community consensus)`."}}
CONTENT3_A.setdefault("postgresql", {})["ha_rto"] = {
  "zh": {"v": "部分支持", "p": "需 Patroni 等外部组件",
         "b": "- 原生无自动切换，靠 Patroni/Stolon，RTO 分钟级 `社区共识`。\n- 同步备库可保 RPO=0，异步有丢数窗口 `官方文档`。\n- 脑裂防护靠 fencing，配错会双主 `社区共识`。"},
  "en": {"v": "Partial", "p": "Needs external components like Patroni",
         "b": "- No native auto-failover; Patroni/Stolon give minutes of RTO `(community consensus)`.\n- Sync standbys keep RPO=0; async has a loss window `(official docs)`.\n- Split-brain protection via fencing; misconfiguration yields dual primaries `(community consensus)`."}}
CONTENT3_A.setdefault("qdrant", {})["ha_rto"] = {
  "zh": {"v": "有", "p": "Raft 分布式，节点故障自动容错",
         "b": "- Raft 共识，节点故障自动容错 `官方文档`。\n- 分布式模式成熟度不如传统数据库，生产案例少 `社区共识`。"},
  "en": {"v": "Supported", "p": "Raft-distributed; automatic node-failure tolerance",
         "b": "- Raft consensus tolerates node failures automatically `(official docs)`.\n- Distributed mode is less battle-tested than traditional databases; fewer production cases `(community consensus)`."}}
CONTENT3_A.setdefault("redis-valkey", {})["ha_rto"] = {
  "zh": {"v": "有", "p": "Sentinel/Cluster 秒级切换",
         "b": "- Sentinel 自动故障转移秒级，Cluster 分片主从自动切 `官方文档`。\n- 异步复制下切换可能丢数（RPO 非零），等 Valkey 的改进 `社区共识`。\n- 脑裂时旧主写入成幽灵数据，客户端要处理 `社区共识`。"},
  "en": {"v": "Supported", "p": "Sentinel/Cluster failover in seconds",
         "b": "- Sentinel auto-failover in seconds; Cluster shard primaries fail over automatically `(official docs)`.\n- Async replication can lose data on failover (non-zero RPO); await Valkey improvements `(community consensus)`.\n- Split-brain writes to the old primary become ghost data; clients must cope `(community consensus)`."}}
CONTENT3_A.setdefault("snowflake", {})["ha_rto"] = {
  "zh": {"v": "有", "p": "托管多 AZ，用户无感知",
         "b": "- 计算/存储/服务层全托管多 AZ，故障平台兜底 `官方文档`。\n- 用户侧无主从概念，RTO/RPO 不暴露 `社区共识`。\n- region 级故障靠跨区复制+提升 `官方文档`。"},
  "en": {"v": "Supported", "p": "Managed multi-AZ; invisible to users",
         "b": "- Compute/storage/services all managed multi-AZ; the platform absorbs failures `(official docs)`.\n- No primary/replica concept user-side; RTO/RPO not exposed `(community consensus)`.\n- Region failures handled via cross-region replication + promotion `(official docs)`."}}
CONTENT3_A.setdefault("spanner", {})["ha_rto"] = {
  "zh": {"v": "有", "p": "托管全球多活，用户无感知",
         "b": "- Paxos 多副本跨区，故障自动，RTO 秒级 `官方文档`。\n- RPO=0，外部一致性 `官方文档`。"},
  "en": {"v": "Supported", "p": "Managed global active-active; invisible to users",
         "b": "- Paxos multi-replica across regions with automatic failover in seconds `(official docs)`.\n- RPO=0 with external consistency `(official docs)`."}}
CONTENT3_A.setdefault("sqlserver", {})["ha_rto"] = {
  "zh": {"v": "有", "p": "Always On AG，自动切换成熟",
         "b": "- AG 自动故障转移，RTO 秒到分钟 `官方文档`。\n- 同步提交 RPO=0，异步有延迟 `官方文档`。\n- 见证/仲裁配错会脑裂或无法切换 `社区共识`。"},
  "en": {"v": "Supported", "p": "Always On AG; mature automatic failover",
         "b": "- AG automatic failover in seconds-to-minutes `(official docs)`.\n- Sync commit gives RPO=0; async lags `(official docs)`.\n- Misconfigured witness/quorum causes split-brain or failed failover `(community consensus)`."}}
CONTENT3_A.setdefault("starrocks", {})["ha_rto"] = {
  "zh": {"v": "有", "p": "FE/BE 多副本自动容错",
         "b": "- FE master 自动选，BE 多副本，单点故障自动容错 `官方文档`。\n- RTO 分钟级内 `社区共识`。"},
  "en": {"v": "Supported", "p": "Multi-replica FE/BE automatic tolerance",
         "b": "- FE master auto-elected; multi-replica BE tolerates single-point failures `(official docs)`.\n- RTO within minutes `(community consensus)`."}}
CONTENT3_A.setdefault("tdsql", {})["ha_rto"] = {
  "zh": {"v": "有", "p": "强同步多副本自动切换",
         "b": "- 强同步复制多副本，主故障自动切换 `官方文档`。\n- RPO=0，RTO 秒级 `官方文档`。"},
  "en": {"v": "Supported", "p": "Strong-sync multi-replica automatic failover",
         "b": "- Strongly-synchronous multi-replica with automatic primary failover `(official docs)`.\n- RPO=0; RTO in seconds `(official docs)`."}}
CONTENT3_A.setdefault("tidb", {})["ha_rto"] = {
  "zh": {"v": "有", "p": "Raft 自愈，RTO 秒级",
         "b": "- TiKV Raft 多副本，节点故障自动补副本+选主，RTO 秒级 `官方文档`。\n- RPO=0，脑裂靠 Raft 防护 `官方文档`。\n- PD 本身也要高可用部署 `社区共识`。"},
  "en": {"v": "Supported", "p": "Raft self-healing; seconds of RTO",
         "b": "- TiKV Raft multi-replica; failed nodes trigger re-replication + election in seconds `(official docs)`.\n- RPO=0; Raft guards against split-brain `(official docs)`.\n- PD itself needs an HA deployment `(community consensus)`."}}
CONTENT3_A.setdefault("weaviate", {})["ha_rto"] = {
  "zh": {"v": "部分支持", "p": "Raft（1.25+）；成熟度待验证",
         "b": "- 1.25+ 引入 Raft 做高可用 `官方文档`。\n- 相对年轻，生产故障案例少，RTO 数据少 `待验证`。"},
  "en": {"v": "Partial", "p": "Raft (1.25+); maturity to be verified",
         "b": "- Raft-based HA since 1.25 `(official docs)`.\n- Relatively young with few production failure stories; little RTO data `(to be verified)`."}}
CONTENT3_A.setdefault("yugabytedb", {})["ha_rto"] = {
  "zh": {"v": "有", "p": "Raft 自愈，RTO 秒级",
         "b": "- Raft 多副本自动选主，RTO 秒级，RPO=0 `官方文档`。\n- 跨区部署下故障域隔离天然 `官方文档`。"},
  "en": {"v": "Supported", "p": "Raft self-healing; seconds of RTO",
         "b": "- Raft multi-replica auto-election in seconds; RPO=0 `(official docs)`.\n- Cross-region deployments isolate failure domains naturally `(official docs)`."}}
CONTENT3_A.setdefault("redshift", {})["ha_rto"] = {
  "zh": {"v": "有", "p": "托管多 AZ，故障自动恢复",
         "b": "- 托管多 AZ，节点故障自动替换恢复 `官方文档`。\n- 快照可恢复到任意时间点，RPO 看快照频率 `官方文档`。\n- 恢复期间集群只读或不可用，大集群恢复慢 `社区共识`。"},
  "en": {"v": "Supported", "p": "Managed multi-AZ; automatic recovery",
         "b": "- Managed multi-AZ with automatic node replacement `(official docs)`.\n- Snapshots restore to any point; RPO follows snapshot frequency `(official docs)`.\n- Clusters go read-only/unavailable during restore; big clusters restore slowly `(community consensus)`."}}
CONTENT3_A.setdefault("bigquery", {})["ha_rto"] = {
  "zh": {"v": "有", "p": "托管多区，用户无感知",
         "b": "- 计算存储全托管多区复制，故障平台兜底 `官方文档`。\n- 时间旅行 7 天可恢复误删，用户侧 RPO≈0 `官方文档`。"},
  "en": {"v": "Supported", "p": "Managed multi-zone; invisible to users",
         "b": "- Fully managed multi-zone compute/storage replication; the platform absorbs failures `(official docs)`.\n- 7-day time travel recovers accidental deletes; user-side RPO≈0 `(official docs)`."}}

# ---------------- 维度 multi_cloud：支持跨云 ----------------
# scope: 同一产品横跨 AWS/Azure/GCP/阿里云/腾讯云的可部署性、跨云复制。与跨地域多活区分：这里指多云厂商。
CONTENT3_A.setdefault("alloydb", {})["multi_cloud"] = {
  "zh": {"v": "无", "p": "GCP 绑定，无跨云",
         "b": "- 仅 GCP 提供，无 AWS/Azure 版本 `官方文档`。\n- 迁出需逻辑迁移（pg_dump），无跨云复制 `社区共识`。"},
  "en": {"v": "Not supported", "p": "GCP-bound; no cross-cloud",
         "b": "- GCP-only; no AWS/Azure offering `(official docs)`.\n- Moving out needs logical migration (pg_dump); no cross-cloud replication `(community consensus)`."}}
CONTENT3_A.setdefault("aurora", {})["multi_cloud"] = {
  "zh": {"v": "无", "p": "AWS 绑定，无跨云",
         "b": "- 仅 AWS，无其他云版本 `官方文档`。\n- 迁出靠 DMS/逻辑导出，无跨云原生复制 `官方文档`。"},
  "en": {"v": "Not supported", "p": "AWS-bound; no cross-cloud",
         "b": "- AWS-only; no other-cloud offering `(official docs)`.\n- Moving out via DMS/logical export; no native cross-cloud replication `(official docs)`."}}
CONTENT3_A.setdefault("cassandra-scylladb", {})["multi_cloud"] = {
  "zh": {"v": "有", "p": "开源任意云；ScyllaDB Cloud 多云",
         "b": "- 开源版任意云/自建可部署，无厂商绑定 `官方文档`。\n- ScyllaDB Cloud 支持 AWS/GCP，跨云靠自建集群 `官方文档`。\n- 跨云延迟进 gossip/复制路径，网络质量关键 `社区共识`。"},
  "en": {"v": "Supported", "p": "Open source on any cloud; ScyllaDB Cloud multi-cloud",
         "b": "- Open source deploys on any cloud/self-hosted; no vendor lock `(official docs)`.\n- ScyllaDB Cloud covers AWS/GCP; cross-cloud via self-hosted clusters `(official docs)`.\n- Cross-cloud latency hits gossip/replication; network quality is key `(community consensus)`."}}
CONTENT3_A.setdefault("clickhouse", {})["multi_cloud"] = {
  "zh": {"v": "有", "p": "开源任意云；ClickHouse Cloud 多云",
         "b": "- 开源版任意云可部署 `官方文档`。\n- ClickHouse Cloud 支持 AWS/GCP/Azure `官方文档`。\n- 跨云用 remote 表函数/复制表可配，无一键方案 `社区共识`。"},
  "en": {"v": "Supported", "p": "Open source on any cloud; ClickHouse Cloud multi-cloud",
         "b": "- Open source deploys on any cloud `(official docs)`.\n- ClickHouse Cloud supports AWS/GCP/Azure `(official docs)`.\n- Cross-cloud via remote table functions / replicated tables; no one-click story `(community consensus)`."}}
CONTENT3_A.setdefault("cockroachdb", {})["multi_cloud"] = {
  "zh": {"v": "有", "p": "自建任意云；CockroachDB Cloud 多云",
         "b": "- 开源/企业自建版任意云可部署 `官方文档`。\n- CockroachDB Cloud 支持 AWS/GCP `官方文档`。\n- 跨云多活理论可行，延迟与成本是现实门槛 `社区共识`。"},
  "en": {"v": "Supported", "p": "Self-hosted on any cloud; CockroachDB Cloud multi-cloud",
         "b": "- Open-source/enterprise self-hosted deploys on any cloud `(official docs)`.\n- CockroachDB Cloud supports AWS/GCP `(official docs)`.\n- Cross-cloud active-active is theoretically possible; latency and cost are the real gates `(community consensus)`."}}
CONTENT3_A.setdefault("databricks", {})["multi_cloud"] = {
  "zh": {"v": "有", "p": "AWS/Azure/GCP 三云原生",
         "b": "- 同一平台横跨 AWS/Azure/GCP，是其核心卖点 `官方文档`。\n- Delta Sharing 可跨云共享数据 `官方文档`。\n- 跨云有数据传输费，大表要算账 `社区共识`。"},
  "en": {"v": "Supported", "p": "Native on AWS/Azure/GCP",
         "b": "- One platform spanning AWS/Azure/GCP — a core selling point `(official docs)`.\n- Delta Sharing shares data across clouds `(official docs)`.\n- Cross-cloud transfer fees apply; do the math on huge tables `(community consensus)`."}}
CONTENT3_A.setdefault("doris", {})["multi_cloud"] = {
  "zh": {"v": "有", "p": "开源任意云；SelectDB Cloud 多云",
         "b": "- 开源版任意云/自建可部署 `官方文档`。\n- SelectDB Cloud 支持多雲 `厂商口径`。\n- 存算分离架构下对象存储跨云是主要 friction `社区共识`。"},
  "en": {"v": "Supported", "p": "Open source on any cloud; SelectDB Cloud multi-cloud",
         "b": "- Open source deploys on any cloud/self-hosted `(official docs)`.\n- SelectDB Cloud supports multiple clouds `(vendor claim)`.\n- With decoupled storage/compute, cross-cloud object storage is the main friction `(community consensus)`."}}
CONTENT3_A.setdefault("duckdb", {})["multi_cloud"] = {
  "zh": {"v": "不适用", "p": "嵌入式，无云绑定",
         "b": "- 嵌入式库，跑在哪里由宿主决定，无云厂商绑定 `官方文档`。\n- 跨云概念不适用，文件拷到哪里算哪里 `社区共识`。"},
  "en": {"v": "N/A", "p": "Embedded; no cloud binding",
         "b": "- Embedded library; the host decides where it runs — no cloud binding `(official docs)`.\n- Cross-cloud is N/A; the file runs wherever you copy it `(community consensus)`."}}
CONTENT3_A.setdefault("dynamodb", {})["multi_cloud"] = {
  "zh": {"v": "无", "p": "AWS 绑定，无跨云",
         "b": "- 仅 AWS，无其他云版本 `官方文档`。\n- 迁出靠导出到 S3 + 导入目标库，无跨云复制 `社区共识`。"},
  "en": {"v": "Not supported", "p": "AWS-bound; no cross-cloud",
         "b": "- AWS-only; no other-cloud offering `(official docs)`.\n- Moving out via S3 export + import; no cross-cloud replication `(community consensus)`."}}
CONTENT3_A.setdefault("edb", {})["multi_cloud"] = {
  "zh": {"v": "有", "p": "任意云/自建可部署",
         "b": "- 软件形态，AWS/Azure/GCP/自建均可部署 `官方文档`。\n- 无云厂商绑定，迁移自由度高于云原生绑定产品 `社区共识`。"},
  "en": {"v": "Supported", "p": "Deployable on any cloud / self-hosted",
         "b": "- Software form; deploys on AWS/Azure/GCP/self-hosted `(official docs)`.\n- No cloud-vendor binding; freer to move than cloud-tied products `(community consensus)`."}}
CONTENT3_A.setdefault("etcd", {})["multi_cloud"] = {
  "zh": {"v": "有", "p": "开源任意云；无云绑定",
         "b": "- 开源 CNCF 项目，任意环境可部署 `官方文档`。\n- 跨云部署无意义（Raft 延迟敏感），单云/单区是常态 `社区共识`。"},
  "en": {"v": "Supported", "p": "Open source on any cloud; no cloud binding",
         "b": "- Open-source CNCF project; deploys anywhere `(official docs)`.\n- Cross-cloud deployment is pointless (Raft is latency-sensitive); single-cloud/region is the norm `(community consensus)`."}}
CONTENT3_A.setdefault("mariadb", {})["multi_cloud"] = {
  "zh": {"v": "有", "p": "开源任意云；SkySQL 多云",
         "b": "- 开源版任意云可部署 `官方文档`。\n- SkySQL 支持多云 `厂商口径`。"},
  "en": {"v": "Supported", "p": "Open source on any cloud; SkySQL multi-cloud",
         "b": "- Open source deploys on any cloud `(official docs)`.\n- SkySQL supports multiple clouds `(vendor claim)`."}}
CONTENT3_A.setdefault("milvus", {})["multi_cloud"] = {
  "zh": {"v": "有", "p": "开源任意云；Zilliz Cloud 多云",
         "b": "- 开源版任意云 K8s 可部署 `官方文档`。\n- Zilliz Cloud 支持 AWS/GCP/Azure `官方文档`。"},
  "en": {"v": "Supported", "p": "Open source on any cloud; Zilliz Cloud multi-cloud",
         "b": "- Open source deploys on any cloud's K8s `(official docs)`.\n- Zilliz Cloud supports AWS/GCP/Azure `(official docs)`."}}
CONTENT3_A.setdefault("mongodb", {})["multi_cloud"] = {
  "zh": {"v": "有", "p": "Atlas AWS/GCP/Azure，多云标杆",
         "b": "- Atlas 横跨 AWS/GCP/Azure，可跨云部署集群 `官方文档`。\n- 开源/企业版任意云自建 `官方文档`。\n- 跨云分片集群延迟与费用都要评估 `社区共识`。"},
  "en": {"v": "Supported", "p": "Atlas on AWS/GCP/Azure; the multi-cloud benchmark",
         "b": "- Atlas spans AWS/GCP/Azure with cross-cloud cluster deployment `(official docs)`.\n- Open-source/enterprise self-hosted on any cloud `(official docs)`.\n- Evaluate latency and cost for cross-cloud sharded clusters `(community consensus)`."}}
CONTENT3_A.setdefault("mysql", {})["multi_cloud"] = {
  "zh": {"v": "有", "p": "开源任意云，无绑定",
         "b": "- 开源版任意云/自建可部署，无厂商绑定 `官方文档`。\n- 各云 RDS 大同小异，迁云主要是逻辑迁移 `社区共识`。"},
  "en": {"v": "Supported", "p": "Open source on any cloud; no binding",
         "b": "- Open source deploys on any cloud/self-hosted; no vendor binding `(official docs)`.\n- Cloud RDS offerings are similar; moving clouds is mostly logical migration `(community consensus)`."}}
CONTENT3_A.setdefault("oceanbase", {})["multi_cloud"] = {
  "zh": {"v": "有", "p": "任意云/自建；OceanBase Cloud 多区",
         "b": "- 软件形态，阿里云/腾讯云/华为云/自建均可部署 `官方文档`。\n- OceanBase Cloud 覆盖多区 `官方文档`。\n- 跨云多活理论可行，延迟门槛高 `社区共识`。"},
  "en": {"v": "Supported", "p": "Any cloud / self-hosted; OceanBase Cloud multi-zone",
         "b": "- Software form; deploys on Alibaba/Tencent/Huawei clouds and self-hosted `(official docs)`.\n- OceanBase Cloud covers multiple zones `(official docs)`.\n- Cross-cloud active-active theoretically possible; latency bar is high `(community consensus)`."}}
CONTENT3_A.setdefault("oracle", {})["multi_cloud"] = {
  "zh": {"v": "部分支持", "p": "OCI 为主；与 Azure/AWS/GCP 有合作",
         "b": "- Oracle Database@Azure / @AWS / @Google Cloud 把 OCI 数据库放到对方云机房 `官方文档`。\n- 本质仍是 OCI 技术栈，不是真正多云原生 `社区共识`。\n- 授权跨云复杂，谈判桌见 `社区共识`。"},
  "en": {"v": "Partial", "p": "OCI-first; partnerships with Azure/AWS/GCP",
         "b": "- Oracle Database@Azure / @AWS / @Google Cloud place OCI databases in partner datacenters `(official docs)`.\n- Still fundamentally the OCI stack, not truly multi-cloud native `(community consensus)`.\n- Cross-cloud licensing is complex; negotiated case by case `(community consensus)`."}}
CONTENT3_A.setdefault("polardb", {})["multi_cloud"] = {
  "zh": {"v": "无", "p": "阿里云绑定，无跨云",
         "b": "- 仅阿里云提供 `官方文档`。\n- 迁出靠逻辑迁移，无跨云复制 `社区共识`。"},
  "en": {"v": "Not supported", "p": "Alibaba Cloud-bound; no cross-cloud",
         "b": "- Alibaba Cloud only `(official docs)`.\n- Moving out via logical migration; no cross-cloud replication `(community consensus)`."}}
CONTENT3_A.setdefault("postgresql", {})["multi_cloud"] = {
  "zh": {"v": "有", "p": "开源任意云，无绑定",
         "b": "- 开源版任意云/自建可部署，是跨云自由度最高的数据库之一 `官方文档`。\n- 各云托管 PG 差异小，迁云成本低 `社区共识`。"},
  "en": {"v": "Supported", "p": "Open source on any cloud; no binding",
         "b": "- Open source deploys on any cloud/self-hosted — among the freest databases for cross-cloud `(official docs)`.\n- Managed PG offerings differ little; moving clouds is cheap `(community consensus)`."}}
CONTENT3_A.setdefault("qdrant", {})["multi_cloud"] = {
  "zh": {"v": "有", "p": "开源任意云；Qdrant Cloud 多云",
         "b": "- 开源版任意云可部署 `官方文档`。\n- Qdrant Cloud 支持多云 `官方文档`。"},
  "en": {"v": "Supported", "p": "Open source on any cloud; Qdrant Cloud multi-cloud",
         "b": "- Open source deploys on any cloud `(official docs)`.\n- Qdrant Cloud supports multiple clouds `(official docs)`."}}
CONTENT3_A.setdefault("redis-valkey", {})["multi_cloud"] = {
  "zh": {"v": "有", "p": "开源任意云，无绑定",
         "b": "- 开源版任意云可部署 `官方文档`。\n- Redis Enterprise Cloud 支持多云，但那是商业版 `厂商口径`。"},
  "en": {"v": "Supported", "p": "Open source on any cloud; no binding",
         "b": "- Open source deploys on any cloud `(official docs)`.\n- Redis Enterprise Cloud is multi-cloud, but that's the commercial edition `(vendor claim)`."}}
CONTENT3_A.setdefault("snowflake", {})["multi_cloud"] = {
  "zh": {"v": "有", "p": "AWS/Azure/GCP 三云，多云标杆",
         "b": "- 横跨 AWS/Azure/GCP，账号可跨云，数据共享跨云 `官方文档`。\n- 跨云复制/共享有传输费 `官方文档`。\n- 商业绑定仍在 Snowflake 自身，不在云厂商 `社区共识`。"},
  "en": {"v": "Supported", "p": "AWS/Azure/GCP; the multi-cloud benchmark",
         "b": "- Spans AWS/Azure/GCP with cross-cloud accounts and data sharing `(official docs)`.\n- Cross-cloud replication/sharing incurs transfer fees `(official docs)`.\n- Commercial lock-in sits with Snowflake itself, not the cloud vendor `(community consensus)`."}}
CONTENT3_A.setdefault("spanner", {})["multi_cloud"] = {
  "zh": {"v": "无", "p": "GCP 绑定，无跨云",
         "b": "- 仅 GCP，无其他云版本 `官方文档`。\n- 迁出需导出重建，无跨云复制 `社区共识`。"},
  "en": {"v": "Not supported", "p": "GCP-bound; no cross-cloud",
         "b": "- GCP-only; no other-cloud offering `(official docs)`.\n- Moving out needs export-and-rebuild; no cross-cloud replication `(community consensus)`."}}
CONTENT3_A.setdefault("sqlserver", {})["multi_cloud"] = {
  "zh": {"v": "部分支持", "p": "自建版任意云；Azure SQL 绑定 Azure",
         "b": "- 自建 SQL Server 任意云/本地可部署 `官方文档`。\n- Azure SQL Database/Managed Instance 绑定 Azure `官方文档`。\n- 授权跨云（License Mobility）规则复杂 `社区共识`。"},
  "en": {"v": "Partial", "p": "Self-hosted on any cloud; Azure SQL binds to Azure",
         "b": "- Self-hosted SQL Server deploys on any cloud/on-prem `(official docs)`.\n- Azure SQL Database / Managed Instance bind to Azure `(official docs)`.\n- Cross-cloud licensing (License Mobility) rules are complex `(community consensus)`."}}
CONTENT3_A.setdefault("starrocks", {})["multi_cloud"] = {
  "zh": {"v": "有", "p": "开源任意云；CelerData 多云",
         "b": "- 开源版任意云可部署 `官方文档`。\n- CelerData Cloud 支持多云 `厂商口径`。"},
  "en": {"v": "Supported", "p": "Open source on any cloud; CelerData multi-cloud",
         "b": "- Open source deploys on any cloud `(official docs)`.\n- CelerData Cloud supports multiple clouds `(vendor claim)`."}}
CONTENT3_A.setdefault("tdsql", {})["multi_cloud"] = {
  "zh": {"v": "部分支持", "p": "腾讯云为主；私有化可出云",
         "b": "- 主力是腾讯云 `官方文档`。\n- 有私有化/本地部署版本，可出云但非多云原生 `厂商口径`。"},
  "en": {"v": "Partial", "p": "Tencent Cloud-first; on-prem edition can leave the cloud",
         "b": "- Primarily Tencent Cloud `(official docs)`.\n- An on-prem edition exists — can leave the cloud but not multi-cloud native `(vendor claim)`."}}
CONTENT3_A.setdefault("tidb", {})["multi_cloud"] = {
  "zh": {"v": "有", "p": "开源任意云；TiDB Cloud AWS/GCP",
         "b": "- 开源版任意云/自建可部署 `官方文档`。\n- TiDB Cloud 支持 AWS/GCP `官方文档`。\n- 跨云部署延迟门槛同多活维度 `社区共识`。"},
  "en": {"v": "Supported", "p": "Open source on any cloud; TiDB Cloud on AWS/GCP",
         "b": "- Open source deploys on any cloud/self-hosted `(official docs)`.\n- TiDB Cloud supports AWS/GCP `(official docs)`.\n- Cross-cloud latency bar same as the active-active dimension `(community consensus)`."}}
CONTENT3_A.setdefault("weaviate", {})["multi_cloud"] = {
  "zh": {"v": "有", "p": "开源任意云；Weaviate Cloud 多云",
         "b": "- 开源版任意云 K8s 可部署 `官方文档`。\n- Weaviate Cloud 支持多云 `官方文档`。"},
  "en": {"v": "Supported", "p": "Open source on any cloud; Weaviate Cloud multi-cloud",
         "b": "- Open source deploys on any cloud's K8s `(official docs)`.\n- Weaviate Cloud supports multiple clouds `(official docs)`."}}
CONTENT3_A.setdefault("yugabytedb", {})["multi_cloud"] = {
  "zh": {"v": "有", "p": "开源任意云；YB Cloud 多云",
         "b": "- 开源版任意云可部署 `官方文档`。\n- YugabyteDB Managed 支持 AWS/GCP/Azure `官方文档`。"},
  "en": {"v": "Supported", "p": "Open source on any cloud; YB Cloud multi-cloud",
         "b": "- Open source deploys on any cloud `(official docs)`.\n- YugabyteDB Managed supports AWS/GCP/Azure `(official docs)`."}}
CONTENT3_A.setdefault("redshift", {})["multi_cloud"] = {
  "zh": {"v": "无", "p": "AWS 绑定，无跨云",
         "b": "- 仅 AWS，无其他云版本 `官方文档`。\n- 迁出靠 unload 到 S3 + 重建，无跨云复制 `社区共识`。"},
  "en": {"v": "Not supported", "p": "AWS-bound; no cross-cloud",
         "b": "- AWS-only; no other-cloud offering `(official docs)`.\n- Moving out via UNLOAD to S3 + rebuild; no cross-cloud replication `(community consensus)`."}}
CONTENT3_A.setdefault("bigquery", {})["multi_cloud"] = {
  "zh": {"v": "无", "p": "GCP 绑定，无跨云",
         "b": "- 仅 GCP，无其他云版本 `官方文档`。\n- 跨云用 BigQuery Omni 读其他云数据，但计算仍在 GCP 侧 `官方文档`。\n- 迁出靠导出到 GCS，无跨云复制 `社区共识`。"},
  "en": {"v": "Not supported", "p": "GCP-bound; no cross-cloud",
         "b": "- GCP-only; no other-cloud offering `(official docs)`.\n- BigQuery Omni reads other clouds' data, but compute stays GCP-side `(official docs)`.\n- Moving out via GCS export; no cross-cloud replication `(community consensus)`."}}
