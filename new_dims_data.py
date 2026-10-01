# -*- coding: utf-8 -*-
"""6 个新增硬维度的数据：perf / cert / maturity / adopters / tooling / managed。

CONTENT[slug][dimkey] = {"zh": {"v","p","b"}, "en": {"v","p","b"}}
v = verdict（有/部分支持/无/不适用/未找到证据；Supported/...），p = 短语，b = markdown 正文。
正文沿用档案体例：`- ` 条目 + 反引号证据徽章（`官方文档`/`厂商口径`/`社区实测`/`社区共识`/`待验证`）。
"""

NEW_DIMS = [
    {"key": "perf", "zh": "性能与延迟特征", "en": "Performance & latency",
     "keys": ["性能", "延迟", "Performance", "performance", "Latency", "latency"]},
    {"key": "cert", "zh": "合规与认证", "en": "Compliance & certifications",
     "keys": ["合规", "信创", "国测", "等保", "资质", "Compliance", "compliance",
              "Certification", "certification"]},
    {"key": "maturity", "zh": "成熟度与社区生态", "en": "Maturity & community",
     "keys": ["成熟度", "社区生态", "Maturity", "maturity"]},
    {"key": "adopters", "zh": "标杆用户", "en": "Notable adopters",
     "keys": ["标杆", "Notable adopters", "notable adopters"]},
    {"key": "tooling", "zh": "生态工具链", "en": "Ecosystem tooling",
     "keys": ["工具链", "Tooling", "tooling"]},
    {"key": "managed", "zh": "云托管与 Serverless", "en": "Managed & serverless",
     "keys": ["云托管", "Serverless", "serverless", "Managed", "managed"]},
]

CONTENT = {}
# ---------------- 维度1：性能与延迟特征 ----------------
CONTENT["mysql"] = {"perf": {
  "zh": {"v": "有", "p": "单机 OLTP 标杆；写扩展靠分片",
         "b": "- 点查/短事务：单机 sysbench 点查可达数万 QPS 量级，P99 毫秒级（视硬件与调优）`社区实测`。\n- 读扩展靠主从复制加从库；写是单机上限，靠分片中间件（ShardingSphere/DBLE）或业务分片 `社区共识`。\n- 瓶颈：大事务、长 DDL（8.0 Instant DDL 缓解部分场景）、单表过大 `社区共识`。"},
  "en": {"v": "Supported", "p": "single-node OLTP benchmark; write scaling via sharding",
         "b": "- Point lookups/short transactions: tens of thousands of QPS per node in sysbench point-select, P99 in milliseconds (hardware/tuning dependent) `(community-tested)`.\n- Read scaling via async replicas; single-node write ceiling — scale writes with sharding middleware (ShardingSphere/DBLE) or application sharding `(community consensus)`.\n- Bottlenecks: large transactions, long DDL (8.0 Instant DDL helps some cases), oversized single tables `(community consensus)`."}}}
CONTENT["postgresql"] = {"perf": {
  "zh": {"v": "有", "p": "单机综合性能强；复杂查询优化器是长板",
         "b": "- OLTP 与 MySQL 同量级；复杂 SQL（窗口函数/CTE/多表关联）优化器更强 `社区共识`。\n- 并行查询、BRIN/GIN 索引对分析型负载友好；写扩展同样靠分片（Citus 等）`社区共识`。\n- 深水点：长事务导致表膨胀（bloat），VACUUM/自动清理策略直接影响性能稳定性 `社区共识`。"},
  "en": {"v": "Supported", "p": "strong single-node all-rounder; optimizer shines on complex queries",
         "b": "- OLTP on par with MySQL; stronger optimizer for complex SQL (window functions, CTEs, multi-table joins) `(community consensus)`.\n- Parallel queries and BRIN/GIN indexes help analytical workloads; write scaling still needs sharding (e.g. Citus) `(community consensus)`.\n- Deep-water point: long transactions cause table bloat; VACUUM/autovacuum strategy directly affects performance stability `(community consensus)`."}}}
CONTENT["oracle"] = {"perf": {
  "zh": {"v": "有", "p": "高端硬件上的极限性能标杆；公开可复现实测少",
         "b": "- Exadata/RAC 组合是传统高性能 OLTP 的参考实现；RAC 提供写扩展，但 Cache Fusion 私有互联有开销 `厂商口径`。\n- 优化器成熟，复杂负载表现稳定；深度调优依赖 AWR/ASH 等商业诊断包 `社区共识`。\n- 闭源商业产品，公开可复现的第三方 benchmark 少，性能数据多为厂商口径 `待验证`。"},
  "en": {"v": "Supported", "p": "top-end hardware performance benchmark; few reproducible public tests",
         "b": "- Exadata/RAC is the reference implementation for high-end OLTP; RAC scales writes but Cache Fusion interconnect has overhead `(vendor claim)`.\n- Mature optimizer, stable on complex workloads; deep tuning relies on commercial diagnostics (AWR/ASH) `(community consensus)`.\n- Closed-source commercial product: few reproducible third-party benchmarks; most performance figures are vendor claims `(to-be-verified)`."}}}
CONTENT["oceanbase"] = {"perf": {
  "zh": {"v": "有", "p": "原生分布式；公开 TPC-C 纪录保持者",
         "b": "- 公开 TPC-C/TPC-H 纪录（厂商口径，特定版本与硬件配置）`厂商口径`。\n- LSM-Tree + 多副本 Paxos：分布式写延迟高于单机 MySQL，读可就近副本 `社区共识`。\n- 多租户资源隔离，混合负载间互相影响小；单机极限性能不如 MySQL 极致调优 `社区共识`。"},
  "en": {"v": "Supported", "p": "cloud-native distributed; public TPC-C record holder",
         "b": "- Public TPC-C/TPC-H records (vendor claim, specific versions and hardware) `(vendor claim)`.\n- LSM-Tree + multi-replica Paxos: distributed write latency above single-node MySQL; reads can go to nearby replicas `(community consensus)`.\n- Multi-tenant resource isolation keeps mixed workloads from interfering; single-node peak throughput below a fully tuned MySQL `(community consensus)`."}}}
CONTENT["tidb"] = {"perf": {
  "zh": {"v": "有", "p": "分布式 HTAP；OLTP 延迟高于单机",
         "b": "- TPC-C 分布式纪录（厂商口径）；加 TiKV 节点即扩展 `厂商口径`。\n- 分布式事务 2PC：跨分片写入延迟明显高于单机 MySQL，单分片小事务接近单机水平 `社区共识`。\n- TiFlash 列存副本加速分析查询，一套集群跑 HTAP `官方文档`。"},
  "en": {"v": "Supported", "p": "distributed HTAP; OLTP latency above single-node",
         "b": "- Distributed TPC-C record (vendor claim); add TiKV nodes to scale `(vendor claim)`.\n- Distributed 2PC transactions: cross-shard write latency clearly above single-node MySQL; single-shard small transactions close to single-node `(community consensus)`.\n- TiFlash columnar replicas accelerate analytical queries — HTAP on one cluster `(official docs)`."}}}
CONTENT["polardb"] = {"perf": {
  "zh": {"v": "有", "p": "云原生一写多读；读扩展秒级",
         "b": "- 共享存储架构：加只读节点不搬数据，扩展读能力快（分钟级/秒级）`官方文档`。\n- 单机性能接近社区 MySQL/PG；写上限为单主规格 `社区共识`。\n- PolarDB-X（分布式版）提供水平写扩展 `官方文档`。"},
  "en": {"v": "Supported", "p": "cloud-native single-writer/multiple-readers; read scaling in seconds",
         "b": "- Shared-storage architecture: adding read replicas moves no data, read scaling in minutes/seconds `(official docs)`.\n- Single-node performance close to community MySQL/PG; writes capped by the single primary's size `(community consensus)`.\n- PolarDB-X (distributed edition) provides horizontal write scaling `(official docs)`."}}}
CONTENT["alloydb"] = {"perf": {
  "zh": {"v": "有", "p": "Google 托管 PG；分析加速是卖点",
         "b": "- 官方称 OLTP 约 2 倍 vanilla PG、分析查询快一个数量级（厂商口径）`厂商口径`。\n- 列存引擎自动加速 HTAP 查询；写扩展靠纵向升级规格 `官方文档`。\n- 实际表现依赖 Google Cloud 网络与实例规格，跨区延迟需实测 `社区共识`。"},
  "en": {"v": "Supported", "p": "Google-managed PG; analytical acceleration is the selling point",
         "b": "- Officially ~2x vanilla PostgreSQL on OLTP and an order of magnitude on analytical queries (vendor claim) `(vendor claim)`.\n- Columnar engine auto-accelerates HTAP queries; write scaling via vertical upgrades `(official docs)`.\n- Real-world results depend on Google Cloud networking and instance sizing; cross-region latency needs your own tests `(community consensus)`."}}}
CONTENT["aurora"] = {"perf": {
  "zh": {"v": "有", "p": "存算分离；读扩展与故障恢复快",
         "b": "- 读副本共享存储卷，加节点不复制数据；故障恢复通常秒级（存储层仲裁）`官方文档`。\n- 写仍是单 writer 上限；延迟与 vanilla MySQL/PG 相近 `社区共识`。\n- Serverless v2 支持自动纵向伸缩，应对波峰 `官方文档`。"},
  "en": {"v": "Supported", "p": "storage-compute separation; fast read scaling and recovery",
         "b": "- Read replicas share the storage volume — no data copy when scaling; failover typically in seconds (storage-layer quorum) `(official docs)`.\n- Writes still capped by the single writer; latency close to vanilla MySQL/PG `(community consensus)`.\n- Serverless v2 auto-scales vertically for spiky workloads `(official docs)`."}}}
CONTENT["tdsql"] = {"perf": {
  "zh": {"v": "有", "p": "金融级分布式；强一致优先",
         "b": "- 分片/集群版水平扩展读写；强一致复制带来写延迟代价 `官方文档`。\n- 公开性能数据以厂商口径为主，第三方可复现实测少 `待验证`。\n- 金融场景优化：高并发短事务是强项，复杂分析靠列存/HTAP 引擎 `厂商口径`。"},
  "en": {"v": "Supported", "p": "finance-grade distributed; strong consistency first",
         "b": "- Sharded/cluster editions scale reads and writes horizontally; strongly consistent replication adds write-latency cost `(official docs)`.\n- Public performance figures are mostly vendor claims; few reproducible third-party tests `(to-be-verified)`.\n- Tuned for finance: high-concurrency short transactions are the strength; complex analytics go to columnar/HTAP engines `(vendor claim)`."}}}
CONTENT["edb"] = {"perf": {
  "zh": {"v": "有", "p": "基线即 PG；Oracle 兼容模式有转义开销",
         "b": "- EPAS 性能基线与社区 PG 一致：并行查询、分区表、分片扩展能力相同 `社区共识`。\n- Oracle 兼容模式（存储过程/包/语法转义）有额外开销，性能关键路径建议实测 `社区共识`。\n- 大对象/分区等企业特性不改变单机性能上限 `官方文档`。"},
  "en": {"v": "Supported", "p": "baseline is PostgreSQL; Oracle-compat mode adds translation overhead",
         "b": "- EPAS performance baseline matches community PostgreSQL: parallel queries, partitioning, sharding behave the same `(community consensus)`.\n- Oracle compatibility mode (procedures/packages/syntax translation) adds overhead — benchmark performance-critical paths `(community consensus)`.\n- Enterprise features (large objects, partitioning) don't raise the single-node ceiling `(official docs)`."}}}
CONTENT["mariadb"] = {"perf": {
  "zh": {"v": "有", "p": "单机性能与 MySQL 相近；Galera 多写有代价",
         "b": "- 单机 OLTP 与 MySQL 同量级；线程池开源、优化器有差异化特性 `社区共识`。\n- Galera 多主写：认证复制有开销，写冲突导致回滚，高冲突负载下不如单主 `社区共识`。\n- ColumnStore 做分析，行列混合不如原生 HTAP 一体 `社区共识`。"},
  "en": {"v": "Supported", "p": "single-node close to MySQL; Galera multi-writer has a cost",
         "b": "- Single-node OLTP on par with MySQL; open-source thread pool and differentiated optimizer features `(community consensus)`.\n- Galera multi-primary writes: certification replication adds overhead and write conflicts cause rollbacks — worse than single-primary under high-conflict load `(community consensus)`.\n- ColumnStore handles analytics; hybrid row/column less integrated than native HTAP `(community consensus)`."}}}
CONTENT["cockroachdb"] = {"perf": {
  "zh": {"v": "有", "p": "用延迟换全球可用性；吞吐随节点线性扩展",
         "b": "- 单行读写延迟毫秒级（跨地域更高），高于单机 DB；吞吐随节点数线性扩展 `官方文档`。\n- follower reads / 就近 leaseholder 降低读尾延迟 `官方文档`。\n- 热点行/高冲突事务是性能杀手，schema 设计需避免全局序列热点 `社区共识`。"},
  "en": {"v": "Supported", "p": "trades latency for global availability; throughput scales linearly",
         "b": "- Single-row read/write latency in milliseconds (higher across regions), above single-node DBs; throughput scales linearly with node count `(official docs)`.\n- Follower reads and nearby leaseholders cut read tail latency `(official docs)`.\n- Hot rows/high-contention transactions are the performance killer — schema design must avoid global-sequence hotspots `(community consensus)`."}}}
CONTENT["yugabytedb"] = {"perf": {
  "zh": {"v": "有", "p": "延迟特征与 CRDB 同类；双 API 路径",
         "b": "- YSQL（PG 兼容）分布式事务延迟高于单机 PG；YCQL（Cassandra 协议）路径延迟更低 `社区共识`。\n- 读可调 follower reads / 表级 follower 读取降延迟 `官方文档`。\n- 跨区部署的延迟主要由 Raft 复制距离决定，选型前按拓扑实测 `社区共识`。"},
  "en": {"v": "Supported", "p": "latency profile similar to CRDB; dual-API paths",
         "b": "- YSQL (PG-compatible) distributed-transaction latency above single-node PG; the YCQL (Cassandra-protocol) path is lower-latency `(community consensus)`.\n- Tunable follower reads (including per-table) cut read latency `(official docs)`.\n- Cross-region latency is dominated by Raft replication distance — benchmark against your planned topology `(community consensus)`."}}}
CONTENT["spanner"] = {"perf": {
  "zh": {"v": "有", "p": "TrueTime 外部一致性的代价是提交延迟",
         "b": "- 读写吞吐随节点线性扩展（官方称数十万 QPS 量级，厂商口径）`厂商口径`。\n- 提交需 Paxos + TrueTime 等待，单事务延迟高于单机 DB；只读事务可用快照读降延迟 `官方文档`。\n- 热点 key 的读写仍受单分片限制，分片键设计是性能关键 `社区共识`。"},
  "en": {"v": "Supported", "p": "TrueTime external consistency costs commit latency",
         "b": "- Read/write throughput scales linearly with nodes (officially hundreds of thousands of QPS, vendor claim) `(vendor claim)`.\n- Commits need Paxos + TrueTime waits, so single-transaction latency exceeds single-node DBs; snapshot reads cut read-only latency `(official docs)`.\n- Hot keys are still bound by a single split — split-key design is the performance key `(community consensus)`."}}}
CONTENT["mongodb"] = {"perf": {
  "zh": {"v": "有", "p": "文档 OLTP 性能好；分析靠聚合管道",
         "b": "- WiredTiger：点查/写入吞吐高；分片集群水平扩展写 `社区共识`。\n- 复杂聚合/多表关联（$lookup）性能一般，大文档/大数组是性能坑 `社区共识`。\n- 读关注点/写关注点可调一致性-延迟权衡 `官方文档`。"},
  "en": {"v": "Supported", "p": "good document OLTP; analytics via aggregation pipeline",
         "b": "- WiredTiger: high point-lookup/write throughput; sharded clusters scale writes horizontally `(community consensus)`.\n- Complex aggregations/multi-collection joins ($lookup) are mediocre; huge documents/arrays are the performance pitfall `(community consensus)`.\n- Tunable read/write concerns trade consistency against latency `(official docs)`."}}}
CONTENT["redis-valkey"] = {"perf": {
  "zh": {"v": "有", "p": "内存级亚毫秒 P99；大 key/热 key 是瓶颈",
         "b": "- 单 key 操作亚毫秒 P99；Redis 单线程命令执行（7.0+ IO 多线程），Valkey 持续多线程化 `社区共识`。\n- Cluster 分片扩展吞吐；大 key（慢操作阻塞）、热 key（单分片）是瓶颈 `社区共识`。\n- 持久化（AOF/RDB）与复制对尾延迟有影响，fork 时的延迟毛刺是经典问题 `社区共识`。"},
  "en": {"v": "Supported", "p": "in-memory sub-millisecond P99; big keys/hot keys are the bottleneck",
         "b": "- Sub-millisecond P99 on single-key ops; Redis single-threaded command execution (7.0+ multi-threaded I/O), Valkey pushing multi-threading further `(community consensus)`.\n- Cluster sharding scales throughput; big keys (blocking slow ops) and hot keys (single shard) are the bottlenecks `(community consensus)`.\n- Persistence (AOF/RDB) and replication affect tail latency; fork-time latency spikes are the classic issue `(community consensus)`."}}}
CONTENT["cassandra-scylladb"] = {"perf": {
  "zh": {"v": "有", "p": "写吞吐线性扩展的标杆；读看调优",
         "b": "- Cassandra：加节点即加写吞吐，调优得当单集群百万写入/秒量级（视硬件，社区实测）`社区实测`。\n- ScyllaDB（C++ 重写）官方称单节点数倍于 Cassandra（厂商口径）；seastar 分片-per-core 架构 `厂商口径`。\n- 读 P99 取决于 compaction 策略与布隆过滤器调优；跨数据中心复制延迟可配 `社区共识`。"},
  "en": {"v": "Supported", "p": "the benchmark for linearly scaling write throughput; reads depend on tuning",
         "b": "- Cassandra: add nodes to add write throughput; well-tuned single clusters reach millions of writes/sec (hardware-dependent, community-tested) `(community-tested)`.\n- ScyllaDB (C++ rewrite) claims multiple-x per-node vs Cassandra (vendor claim); seastar shard-per-core architecture `(vendor claim)`.\n- Read P99 depends on compaction strategy and Bloom-filter tuning; cross-DC replication latency is tunable `(community consensus)`."}}}
CONTENT["dynamodb"] = {"perf": {
  "zh": {"v": "有", "p": "Serverless 下个位数毫秒 P99；热分区是坑",
         "b": "- 官方口径：任意规模个位数毫秒 P99；DAX 提供微秒级缓存 `厂商口径`。\n- 按需/预置容量模式；热分区限流是主要性能坑，分区键设计是关键 `社区共识`。\n- 大 scan/跨分区查询贵且慢，建模时就要避免 `社区共识`。"},
  "en": {"v": "Supported", "p": "single-digit ms P99 serverless; hot partitions are the pitfall",
         "b": "- Officially single-digit-millisecond P99 at any scale; DAX adds microsecond caching `(vendor claim)`.\n- On-demand/provisioned capacity modes; hot-partition throttling is the main performance pitfall — partition-key design is key `(community consensus)`.\n- Large scans/cross-partition queries are expensive and slow; avoid them at modeling time `(community consensus)`."}}}
CONTENT["etcd"] = {"perf": {
  "zh": {"v": "有", "p": "一致性优先；吞吐天花板低",
         "b": "- 写经 Raft 走主节点，单集群写入通常万级 QPS 以下；读可走 follower/learner 扩展 `官方文档`。\n- 不是数据面数据库：value 建议 KB 级，不要当通用 KV 用 `社区共识`。\n- 磁盘 fsync 延迟直接决定写延迟，盘是第一性能件 `社区共识`。"},
  "en": {"v": "Supported", "p": "consistency first; low throughput ceiling",
         "b": "- Writes go through the Raft leader; single-cluster writes typically below tens of thousands of QPS; reads can scale via followers/learners `(official docs)`.\n- Not a data-plane database: keep values at KB scale, don't use it as a general KV store `(community consensus)`.\n- Disk fsync latency directly determines write latency — the disk is the #1 performance component `(community consensus)`."}}}
CONTENT["clickhouse"] = {"perf": {
  "zh": {"v": "有", "p": "OLAP 扫描性能标杆；点查弱",
         "b": "- 单机列存扫描 GB/s 量级（视硬件与压缩率，社区实测）；分布式表线性扩展 `社区实测`。\n- 点查/高频小写入弱；MergeTree 后台合并是主要调优点 `社区共识`。\n- 排序键/分区键设计决定查询性能，建表即定生死 `社区共识`。"},
  "en": {"v": "Supported", "p": "the OLAP scan benchmark; weak point lookups",
         "b": "- Single-node columnar scans at GB/s scale (hardware/compression dependent, community-tested); distributed tables scale linearly `(community-tested)`.\n- Weak point lookups and high-frequency small writes; MergeTree background merges are the main tuning knob `(community consensus)`.\n- Sort-key/partition-key design determines query performance — the table definition decides everything `(community consensus)`."}}}
CONTENT["doris"] = {"perf": {
  "zh": {"v": "有", "p": "MPP 向量化；与 StarRocks 同代竞争",
         "b": "- 向量化执行引擎；官方 TPC-H/TPC-DS 数据（厂商口径）`厂商口径`。\n- 主键模型支持实时更新，并发点查好于传统 OLAP `官方文档`。\n- 存算分离、物化视图是查询加速主要手段 `社区共识`。"},
  "en": {"v": "Supported", "p": "vectorized MPP; same generation as StarRocks",
         "b": "- Vectorized execution engine; official TPC-H/TPC-DS figures (vendor claim) `(vendor claim)`.\n- Primary-key model supports real-time updates with better concurrent point lookups than classic OLAP `(official docs)`.\n- Disaggregated storage-compute and materialized views are the main query accelerators `(community consensus)`."}}}
CONTENT["starrocks"] = {"perf": {
  "zh": {"v": "有", "p": "向量化 MPP；公开 TPC-DS 纪录",
         "b": "- 公开 TPC-DS 纪录（厂商口径，特定版本）`厂商口径`。\n- 主键模型/物化视图是实时数仓卖点；查询并发能力在 OLAP 中偏强 `社区共识`。\n- 3.x 存算分离降低扩展成本，性能与存算一体接近 `官方文档`。"},
  "en": {"v": "Supported", "p": "vectorized MPP; public TPC-DS record",
         "b": "- Public TPC-DS record (vendor claim, specific version) `(vendor claim)`.\n- Primary-key model/materialized views are the real-time-warehouse selling point; strong concurrent-query capability for OLAP `(community consensus)`.\n- 3.x disaggregated storage-compute lowers scaling cost with near-identical performance `(official docs)`."}}}
CONTENT["duckdb"] = {"perf": {
  "zh": {"v": "有", "p": "嵌入式 OLAP 单机极快；无分布式",
         "b": "- 进程内列存向量化执行，笔记本上 TB 级以下分析查询秒级（社区共识）`社区共识`。\n- 无分布式，并行上限为单机核数；超大内存需求靠溢出到磁盘 `官方文档`。\n- 读 Parquet/CSV 极快，是“单机数仓”的事实标准 `社区共识`。"},
  "en": {"v": "Supported", "p": "blazing embedded OLAP; no distribution",
         "b": "- In-process columnar vectorized execution: sub-TB analytical queries in seconds on a laptop (community consensus) `(community consensus)`.\n- No distribution; parallelism capped by single-machine cores; spills to disk when memory is exceeded `(official docs)`.\n- Extremely fast Parquet/CSV reads — the de-facto “single-machine warehouse” `(community consensus)`."}}}
CONTENT["milvus"] = {"perf": {
  "zh": {"v": "有", "p": "召回率/QPS/成本三角权衡",
         "b": "- HNSW 高召回高 QPS 但内存大；DiskANN/IVF 降成本也降性能 `官方文档`。\n- 官方 benchmark（厂商口径）；真实选型要在自己的数据集上实测 recall@k `社区共识`。\n- 标量过滤+向量混合查询的性能取决于索引与分区裁剪 `社区共识`。"},
  "en": {"v": "Supported", "p": "recall/QPS/cost trilemma",
         "b": "- HNSW: high recall and QPS but memory-heavy; DiskANN/IVF cut cost and performance `(official docs)`.\n- Official benchmarks (vendor claim); real selection needs recall@k measured on your own dataset `(community consensus)`.\n- Scalar-filter + vector hybrid query performance depends on indexing and partition pruning `(community consensus)`."}}}
CONTENT["weaviate"] = {"perf": {
  "zh": {"v": "有", "p": "与 Milvus 同级讨论；混合检索是特色",
         "b": "- HNSW 为主；BM25+向量混合检索是特色，性能调优看分片与缓存 `官方文档`。\n- 公开 benchmark 以厂商口径为主，第三方横向对比少 `待验证`。\n- 多租户/多向量场景的内存规划是主要性能工作 `社区共识`。"},
  "en": {"v": "Supported", "p": "discussed in the same tier as Milvus; hybrid search is the specialty",
         "b": "- HNSW-based; BM25+vector hybrid search is the specialty; tuning centers on sharding and caching `(official docs)`.\n- Public benchmarks are mostly vendor claims; few third-party head-to-heads `(to-be-verified)`.\n- Memory planning for multi-tenant/multi-vector workloads is the main performance work `(community consensus)`."}}}
CONTENT["qdrant"] = {"perf": {
  "zh": {"v": "有", "p": "Rust 实现；单机口碑好",
         "b": "- 内存 HNSW 模式 QPS 高；量化（scalar/binary）降内存换召回 `官方文档`。\n- 单机性能口碑好（社区共识）；分布式分片 Raft，社区版功能完整 `社区共识`。\n- 磁盘模式（memmap）可在大向量集上降成本，QPS 相应下降 `官方文档`。"},
  "en": {"v": "Supported", "p": "Rust implementation; good single-node reputation",
         "b": "- In-memory HNSW mode with high QPS; quantization (scalar/binary) trades recall for memory `(official docs)`.\n- Good single-node reputation (community consensus); distributed sharding via Raft with a complete community edition `(community consensus)`.\n- On-disk (memmap) mode cuts cost on large vector sets with proportionally lower QPS `(official docs)`."}}}
CONTENT["sqlserver"] = {"perf": {
  "zh": {"v": "有", "p": "企业级 OLTP 标杆；许可按核计费",
         "b": "- 单机 OLTP 与 Oracle 同级讨论；Always On 读扩展；列存索引加速分析 `社区共识`。\n- 内存优化表（In-Memory OLTP）适合特定高并发场景，但有诸多限制 `官方文档`。\n- 许可按核计费，性能/成本比常被吐槽；Linux 版性能与 Windows 版接近 `社区共识`。"},
  "en": {"v": "Supported", "p": "enterprise OLTP benchmark; per-core licensing",
         "b": "- Single-node OLTP discussed alongside Oracle; Always On read scaling; columnstore indexes accelerate analytics `(community consensus)`.\n- In-Memory OLTP suits specific high-concurrency scenarios but has many restrictions `(official docs)`.\n- Per-core licensing makes the performance/cost ratio a common complaint; Linux build performs close to Windows `(community consensus)`."}}}
# ---------------- 维度2：合规与认证 ----------------
CONTENT["mysql"]["cert"] = {
  "zh": {"v": "部分支持", "p": "开源版无官方认证；合规靠部署方或云厂商",
         "b": "- 社区版/企业版（Oracle）：无公开的国测/信创认证信息；等保合规由部署方测评 `待验证`。\n- 各云厂商的托管 MySQL（RDS 等）继承云厂商的等保三级/可信云资质 `厂商口径`。\n- 国际：Oracle 云体系的 SOC2/ISO 等适用于 Oracle 运营的 MySQL HeatWave 云服务 `厂商口径`。"},
  "en": {"v": "Partially supported", "p": "no official certs for open source; compliance via deployer or cloud",
         "b": "- Community/Enterprise editions (Oracle): no public information on Chinese national testing/trusted-innovation certification; MLPS (等保) compliance is the deployer's responsibility `(to-be-verified)`.\n- Managed MySQL offerings inherit their cloud provider's MLPS Level 3 / Trusted Cloud qualifications `(vendor claim)`.\n- International: Oracle Cloud's SOC2/ISO family covers Oracle-operated MySQL HeatWave cloud service `(vendor claim)`."}}
CONTENT["postgresql"]["cert"] = {
  "zh": {"v": "部分支持", "p": "开源版无官方认证；合规靠部署方或发行版",
         "b": "- 社区版：无官方合规认证，等保/密评由部署方负责 `社区共识`。\n- 商业发行版（EDB/各云 RDS）：各自持有云厂商或厂商的合规资质 `厂商口径`。\n- 国际：各托管 PG 服务通常具备 SOC2/ISO27001（以云厂商公开页为准）`厂商口径`。"},
  "en": {"v": "Partially supported", "p": "no official certs for open source; via deployer or distribution",
         "b": "- Community edition: no official compliance certifications; MLPS/crypto reviews are the deployer's job `(community consensus)`.\n- Commercial distributions (EDB, cloud RDS offerings) carry their vendor's or cloud's qualifications `(vendor claim)`.\n- International: managed PostgreSQL services typically hold SOC2/ISO 27001 (per providers' public pages) `(vendor claim)`."}}
CONTENT["oracle"]["cert"] = {
  "zh": {"v": "有", "p": "国际认证齐全；中国区以上云/部署方测评为准",
         "b": "- 国际：SOC2、ISO27001/27017/27018、PCI DSS 等（厂商口径，以 Oracle 合规页为准）`厂商口径`。\n- 中国：公有云（OCI 中国区）参与等保测评；本地部署的合规责任在用户方 `厂商口径`。\n- 未见 Oracle Database 进入中国信创名录的公开信息 `待验证`。"},
  "en": {"v": "Supported", "p": "full international set; China compliance via cloud/deployer assessment",
         "b": "- International: SOC2, ISO 27001/27017/27018, PCI DSS, etc. (vendor claim, per Oracle's compliance page) `(vendor claim)`.\n- China: OCI China regions undergo MLPS assessment; on-premises compliance is the customer's responsibility `(vendor claim)`.\n- No public information found on Oracle Database entering China's trusted-innovation catalog `(to-be-verified)`."}}
CONTENT["oceanbase"]["cert"] = {
  "zh": {"v": "有", "p": "信创名录常客；信通院分布式事务库测评",
         "b": "- 通过中国信通院分布式事务型数据库能力测评（厂商口径）`厂商口径`。\n- 进入信创名录/党政集采目录版本以官方公告为准；金融行业案例多，满足监管报备要求 `厂商口径`。\n- 国际认证（SOC2/ISO）以上云版本公开页为准 `待验证`。"},
  "en": {"v": "Supported", "p": "regular in trusted-innovation catalogs; CAICT distributed-transaction DB test",
         "b": "- Passed CAICT distributed-transactional-database capability testing (vendor claim) `(vendor claim)`.\n- Listed in trusted-innovation / government procurement catalogs per official announcements; widely adopted in finance with regulatory filing support `(vendor claim)`.\n- International certs (SOC2/ISO) per the cloud edition's public pages `(to-be-verified)`."}}
CONTENT["tidb"]["cert"] = {
  "zh": {"v": "有", "p": "信通院可信云；分布式事务库测评",
         "b": "- 通过中国信通院可信云、分布式事务型数据库能力测评（厂商口径）`厂商口径`。\n- 信创名录/集采目录版本以 PingCAP 官方公告为准 `厂商口径`。\n- TiDB Cloud（海外）走国际合规体系，以公开页为准 `待验证`。"},
  "en": {"v": "Supported", "p": "CAICT Trusted Cloud; distributed-transaction DB testing",
         "b": "- Passed CAICT Trusted Cloud and distributed-transactional-database capability tests (vendor claim) `(vendor claim)`.\n- Trusted-innovation catalog / procurement listing status per PingCAP's official announcements `(vendor claim)`.\n- TiDB Cloud (overseas) follows international compliance per its public pages `(to-be-verified)`."}}
CONTENT["polardb"]["cert"] = {
  "zh": {"v": "有", "p": "继承阿里云合规体系",
         "b": "- 阿里云：等保三级、可信云、ISO27001/SOC2 等（厂商口径）`厂商口径`。\n- PolarDB 进入信创名录/集采目录的版本以阿里云官方公告为准 `厂商口径`。\n- 本地部署版（PolarDB-X 企业版）的合规测评由部署项目单独做 `待验证`。"},
  "en": {"v": "Supported", "p": "inherits Alibaba Cloud's compliance system",
         "b": "- Alibaba Cloud: MLPS Level 3, Trusted Cloud, ISO 27001/SOC2, etc. (vendor claim) `(vendor claim)`.\n- PolarDB's trusted-innovation catalog / procurement listing per Alibaba Cloud announcements `(vendor claim)`.\n- On-premises editions (PolarDB-X enterprise) are assessed per deployment project `(to-be-verified)`."}}
CONTENT["alloydb"]["cert"] = {
  "zh": {"v": "有", "p": "继承 Google Cloud 合规体系",
         "b": "- Google Cloud：SOC2、ISO27001/27017/27018、PCI DSS 等（厂商口径）`厂商口径`。\n- 无中国区服务，中国用户合规需自行评估跨境与数据出境要求 `社区共识`。\n- Omni（本地版）的合规责任在部署方 `官方文档`。"},
  "en": {"v": "Supported", "p": "inherits Google Cloud's compliance system",
         "b": "- Google Cloud: SOC2, ISO 27001/27017/27018, PCI DSS, etc. (vendor claim) `(vendor claim)`.\n- No China regions; Chinese users must self-assess cross-border and data-export requirements `(community consensus)`.\n- Omni (on-premises edition): compliance is the deployer's responsibility `(official docs)`."}}
CONTENT["aurora"]["cert"] = {
  "zh": {"v": "有", "p": "继承 AWS 合规体系；中国区走光环/西云",
         "b": "- AWS：SOC2、ISO27001、PCI DSS 等（厂商口径）`厂商口径`。\n- 中国区（北京/宁夏，由光环新网/西云数据运营）参与等保测评 `厂商口径`。\n- 无信创名录信息；政企选型以上云版本资质为准 `待验证`。"},
  "en": {"v": "Supported", "p": "inherits AWS compliance; China regions via local operators",
         "b": "- AWS: SOC2, ISO 27001, PCI DSS, etc. (vendor claim) `(vendor claim)`.\n- China regions (Beijing/Ningxia, operated by local partners) undergo MLPS assessment `(vendor claim)`.\n- No trusted-innovation catalog information; government/enterprise selection per the cloud edition's qualifications `(to-be-verified)`."}}
CONTENT["tdsql"]["cert"] = {
  "zh": {"v": "有", "p": "继承腾讯云合规体系；金融监管友好",
         "b": "- 腾讯云：等保三级、可信云、ISO27001 等（厂商口径）`厂商口径`。\n- 信创名录/金融集采版本以腾讯云官方公告为准；服务大量金融机构，监管报备链条成熟 `厂商口径`。\n- 私有化部署项目的合规测评单独做 `待验证`。"},
  "en": {"v": "Supported", "p": "inherits Tencent Cloud compliance; finance-regulator friendly",
         "b": "- Tencent Cloud: MLPS Level 3, Trusted Cloud, ISO 27001, etc. (vendor claim) `(vendor claim)`.\n- Trusted-innovation catalog / finance procurement status per Tencent Cloud announcements; deep finance footprint with mature regulatory filing `(vendor claim)`.\n- Private-deployment projects are assessed individually `(to-be-verified)`."}}
CONTENT["edb"]["cert"] = {
  "zh": {"v": "部分支持", "p": "国际认证走 EDB 厂商体系；国内靠项目测评",
         "b": "- EDB 公开 SOC2 等企业合规信息（厂商口径，以官方合规页为准）`厂商口径`。\n- 中国区：无信创名录公开信息；政企项目合规以上云/本地部署测评为准 `待验证`。\n- 开源 PG 部分无官方认证，见 postgresql 条目 `社区共识`。"},
  "en": {"v": "Partially supported", "p": "international certs via EDB; China via project assessment",
         "b": "- EDB publishes SOC2 and other enterprise compliance (vendor claim, per its compliance page) `(vendor claim)`.\n- China: no public trusted-innovation catalog information; government/enterprise compliance via cloud or on-premises assessment `(to-be-verified)`.\n- Open-source PostgreSQL parts carry no official certs — see the PostgreSQL entry `(community consensus)`."}}
CONTENT["mariadb"]["cert"] = {
  "zh": {"v": "部分支持", "p": "开源无官方认证；企业版走厂商体系",
         "b": "- 社区版：无官方合规认证，合规责任在部署方 `社区共识`。\n- MariaDB 企业版/SkySQL 的合规资质以厂商公开页为准 `厂商口径`。\n- 无信创名录公开信息 `待验证`。"},
  "en": {"v": "Partially supported", "p": "no official certs for open source; enterprise via vendor",
         "b": "- Community edition: no official compliance certifications; deployer responsible `(community consensus)`.\n- MariaDB Enterprise/SkySQL qualifications per the vendor's public pages `(vendor claim)`.\n- No public trusted-innovation catalog information `(to-be-verified)`."}}
CONTENT["cockroachdb"]["cert"] = {
  "zh": {"v": "有", "p": "SOC2 Type II；国际合规为主",
         "b": "- CockroachDB 公开 SOC2 Type II（厂商口径）`厂商口径`。\n- 无中国区服务/信创名录信息；中国用户需评估跨境合规 `待验证`。\n- 自托管版的合规责任在部署方 `社区共识`。"},
  "en": {"v": "Supported", "p": "SOC2 Type II; international compliance focus",
         "b": "- CockroachDB publishes SOC2 Type II (vendor claim) `(vendor claim)`.\n- No China regions or trusted-innovation catalog information; Chinese users must assess cross-border compliance `(to-be-verified)`.\n- Self-hosted compliance is the deployer's responsibility `(community consensus)`."}}
CONTENT["yugabytedb"]["cert"] = {
  "zh": {"v": "有", "p": "SOC2 Type II；国际合规为主",
         "b": "- Yugabyte 公开 SOC2 Type II（厂商口径）`厂商口径`。\n- 无中国区服务/信创名录信息 `待验证`。\n- 自托管版合规责任在部署方 `社区共识`。"},
  "en": {"v": "Supported", "p": "SOC2 Type II; international compliance focus",
         "b": "- Yugabyte publishes SOC2 Type II (vendor claim) `(vendor claim)`.\n- No China regions or trusted-innovation catalog information `(to-be-verified)`.\n- Self-hosted compliance is the deployer's responsibility `(community consensus)`."}}
CONTENT["spanner"]["cert"] = {
  "zh": {"v": "有", "p": "继承 Google Cloud 合规体系",
         "b": "- Google Cloud：SOC2、ISO27001/27017/27018、PCI DSS 等（厂商口径）`厂商口径`。\n- 无中国区服务；中国用户需评估跨境与数据出境要求 `社区共识`。"},
  "en": {"v": "Supported", "p": "inherits Google Cloud's compliance system",
         "b": "- Google Cloud: SOC2, ISO 27001/27017/27018, PCI DSS, etc. (vendor claim) `(vendor claim)`.\n- No China regions; Chinese users must assess cross-border and data-export requirements `(community consensus)`."}}
CONTENT["mongodb"]["cert"] = {
  "zh": {"v": "有", "p": "Atlas 国际认证齐全；社区版无",
         "b": "- Atlas：SOC2、ISO27001、PCI DSS、HIPAA 等（厂商口径）`厂商口径`。\n- 社区版：无官方认证，合规责任在部署方 `社区共识`。\n- 无信创名录公开信息；国内政企多用云厂商托管版资质 `待验证`。"},
  "en": {"v": "Supported", "p": "Atlas fully certified internationally; community edition has none",
         "b": "- Atlas: SOC2, ISO 27001, PCI DSS, HIPAA, etc. (vendor claim) `(vendor claim)`.\n- Community edition: no official certs; deployer responsible `(community consensus)`.\n- No public trusted-innovation catalog information; Chinese government/enterprise users typically rely on cloud-provider managed editions `(to-be-verified)`."}}
CONTENT["redis-valkey"]["cert"] = {
  "zh": {"v": "部分支持", "p": "开源无官方认证；Redis 企业版有",
         "b": "- Redis 开源版/Valkey：无官方合规认证，合规责任在部署方 `社区共识`。\n- Redis Enterprise（Redis Inc）：SOC2 等企业合规（厂商口径）`厂商口径`。\n- 各云厂商托管 Redis 继承云厂商资质 `厂商口径`。"},
  "en": {"v": "Partially supported", "p": "no official certs for open source; Redis Enterprise certified",
         "b": "- Open-source Redis / Valkey: no official compliance certs; deployer responsible `(community consensus)`.\n- Redis Enterprise (Redis Inc.): SOC2 and enterprise compliance (vendor claim) `(vendor claim)`.\n- Cloud-managed Redis offerings inherit provider qualifications `(vendor claim)`."}}
CONTENT["cassandra-scylladb"]["cert"] = {
  "zh": {"v": "部分支持", "p": "开源无官方认证；企业版各走各",
         "b": "- Apache Cassandra 开源版：无官方合规认证 `社区共识`。\n- DataStax Enterprise / ScyllaDB 企业版各自持有企业合规资质（厂商口径）`厂商口径`。\n- 云厂商托管版继承云厂商资质 `厂商口径`。"},
  "en": {"v": "Partially supported", "p": "no official certs for open source; enterprise editions differ",
         "b": "- Apache Cassandra open source: no official compliance certs `(community consensus)`.\n- DataStax Enterprise / ScyllaDB enterprise editions hold their own enterprise qualifications (vendor claim) `(vendor claim)`.\n- Cloud-managed editions inherit provider qualifications `(vendor claim)`."}}
CONTENT["dynamodb"]["cert"] = {
  "zh": {"v": "有", "p": "继承 AWS 合规体系",
         "b": "- AWS：SOC2、ISO27001、PCI DSS、HIPAA 等（厂商口径）`厂商口径`。\n- 中国区（北京/宁夏）参与等保测评 `厂商口径`。"},
  "en": {"v": "Supported", "p": "inherits AWS compliance system",
         "b": "- AWS: SOC2, ISO 27001, PCI DSS, HIPAA, etc. (vendor claim) `(vendor claim)`.\n- China regions (Beijing/Ningxia) undergo MLPS assessment `(vendor claim)`."}}
CONTENT["etcd"]["cert"] = {
  "zh": {"v": "无", "p": "CNCF 项目；无官方合规认证",
         "b": "- etcd 是 CNCF 毕业项目，无官方合规认证 `社区共识`。\n- 合规责任在使用 etcd 的平台/产品方（如各云厂商托管 k8s）`社区共识`。"},
  "en": {"v": "Not supported", "p": "CNCF project; no official compliance certs",
         "b": "- etcd is a CNCF graduated project with no official compliance certifications `(community consensus)`.\n- Compliance responsibility sits with the platform/product embedding etcd (e.g. managed Kubernetes offerings) `(community consensus)`."}}
CONTENT["clickhouse"]["cert"] = {
  "zh": {"v": "部分支持", "p": "ClickHouse Cloud 有 SOC2；开源无",
         "b": "- ClickHouse Cloud：SOC2（厂商口径）`厂商口径`。\n- 开源版：无官方合规认证，合规责任在部署方 `社区共识`。\n- 无信创名录公开信息 `待验证`。"},
  "en": {"v": "Partially supported", "p": "ClickHouse Cloud has SOC2; open source has none",
         "b": "- ClickHouse Cloud: SOC2 (vendor claim) `(vendor claim)`.\n- Open source: no official compliance certs; deployer responsible `(community consensus)`.\n- No public trusted-innovation catalog information `(to-be-verified)`."}}
CONTENT["doris"]["cert"] = {
  "zh": {"v": "部分支持", "p": "国产 OLAP；信创与云资质走厂商",
         "b": "- Apache Doris 开源版：无官方合规认证 `社区共识`。\n- 信创名录/信通院测评、SelectDB Cloud 合规资质以厂商官方公告为准（厂商口径）`厂商口径`。"},
  "en": {"v": "Partially supported", "p": "Chinese OLAP; trusted-innovation and cloud quals via vendor",
         "b": "- Apache Doris open source: no official compliance certs `(community consensus)`.\n- Trusted-innovation catalog / CAICT testing and SelectDB Cloud qualifications per vendor announcements (vendor claim) `(vendor claim)`."}}
CONTENT["starrocks"]["cert"] = {
  "zh": {"v": "部分支持", "p": "开源无官方认证；云版本走厂商",
         "b": "- StarRocks 开源版：无官方合规认证 `社区共识`。\n- 信创名录/测评、CelerData Cloud 合规资质以厂商官方公告为准（厂商口径）`厂商口径`。"},
  "en": {"v": "Partially supported", "p": "no official certs for open source; cloud via vendor",
         "b": "- StarRocks open source: no official compliance certs `(community consensus)`.\n- Trusted-innovation catalog / testing and CelerData Cloud qualifications per vendor announcements (vendor claim) `(vendor claim)`."}}
CONTENT["duckdb"]["cert"] = {
  "zh": {"v": "部分支持", "p": "嵌入式无；MotherDuck 云服务有 SOC2",
         "b": "- DuckDB 嵌入式库：无合规认证概念，合规责任在宿主应用 `社区共识`。\n- MotherDuck（云服务）：SOC2（厂商口径）`厂商口径`。"},
  "en": {"v": "Partially supported", "p": "embedded has none; MotherDuck cloud has SOC2",
         "b": "- DuckDB embedded library: compliance doesn't apply; the host application is responsible `(community consensus)`.\n- MotherDuck (cloud service): SOC2 (vendor claim) `(vendor claim)`."}}
CONTENT["milvus"]["cert"] = {
  "zh": {"v": "部分支持", "p": "Zilliz Cloud 有 SOC2；开源无",
         "b": "- Zilliz Cloud：SOC2（厂商口径）`厂商口径`。\n- Milvus 开源版：无官方合规认证 `社区共识`。\n- 信创名录信息以厂商官方公告为准 `待验证`。"},
  "en": {"v": "Partially supported", "p": "Zilliz Cloud has SOC2; open source has none",
         "b": "- Zilliz Cloud: SOC2 (vendor claim) `(vendor claim)`.\n- Milvus open source: no official compliance certs `(community consensus)`.\n- Trusted-innovation catalog status per vendor announcements `(to-be-verified)`."}}
CONTENT["weaviate"]["cert"] = {
  "zh": {"v": "部分支持", "p": "Weaviate Cloud 有 SOC2；开源无",
         "b": "- Weaviate Cloud：SOC2（厂商口径）`厂商口径`。\n- 开源版：无官方合规认证，合规责任在部署方 `社区共识`。"},
  "en": {"v": "Partially supported", "p": "Weaviate Cloud has SOC2; open source has none",
         "b": "- Weaviate Cloud: SOC2 (vendor claim) `(vendor claim)`.\n- Open source: no official compliance certs; deployer responsible `(community consensus)`."}}
CONTENT["qdrant"]["cert"] = {
  "zh": {"v": "部分支持", "p": "Qdrant Cloud 有 SOC2；开源无",
         "b": "- Qdrant Cloud：SOC2（厂商口径）`厂商口径`。\n- 开源版：无官方合规认证 `社区共识`。"},
  "en": {"v": "Partially supported", "p": "Qdrant Cloud has SOC2; open source has none",
         "b": "- Qdrant Cloud: SOC2 (vendor claim) `(vendor claim)`.\n- Open source: no official compliance certs `(community consensus)`."}}
CONTENT["sqlserver"]["cert"] = {
  "zh": {"v": "有", "p": "继承微软合规体系；中国区由世纪互联运营",
         "b": "- 微软：SOC2、ISO27001、PCI DSS、HIPAA 等（厂商口径）`厂商口径`。\n- Azure 中国区（世纪互联运营）：等保测评 `厂商口径`。\n- 本地部署版合规责任在用户方 `社区共识`。"},
  "en": {"v": "Supported", "p": "inherits Microsoft compliance; China via 21Vianet",
         "b": "- Microsoft: SOC2, ISO 27001, PCI DSS, HIPAA, etc. (vendor claim) `(vendor claim)`.\n- Azure China (operated by 21Vianet): MLPS assessment `(vendor claim)`.\n- On-premises compliance is the customer's responsibility `(community consensus)`."}}
# ---------------- 维度3：成熟度与社区生态 ----------------
CONTENT["mysql"]["maturity"] = {
  "zh": {"v": "有", "p": "1995 年发布；最成熟的开源关系型之一",
         "b": "- 1995 年发布，2010 年随 Sun 并入 Oracle；8.0/8.4 LTS、9.x 创新版并行 `社区共识`。\n- GitHub stars 万级，生态（驱动/工具/教程）最厚 `社区共识`。\n- 风险点：Oracle 主导下社区版与企业版功能分界时有争议 `社区共识`。"},
  "en": {"v": "Supported", "p": "released 1995; among the most mature open-source RDBMS",
         "b": "- Released 1995; joined Oracle via Sun in 2010; 8.0/8.4 LTS plus 9.x innovation releases `(community consensus)`.\n- Tens of thousands of GitHub stars; the thickest ecosystem (drivers, tools, tutorials) `(community consensus)`.\n- Risk: Oracle's stewardship periodically sparks community-vs-enterprise feature-split controversies `(community consensus)`."}}
CONTENT["postgresql"]["maturity"] = {
  "zh": {"v": "有", "p": "1996 年发布；全球开发者社区驱动",
         "b": "- 源自 Berkeley Postgres，1996 年发布；无单一商业主导，全球开发者社区驱动 `社区共识`。\n- 每年一个大版本（现 17/18 代），扩展生态（PostGIS/Citus/向量插件）最活跃 `社区共识`。\n- GitHub stars 万级；长期主义代表，版本兼容性口碑好 `社区共识`。"},
  "en": {"v": "Supported", "p": "released 1996; global developer community driven",
         "b": "- Descended from Berkeley Postgres, released 1996; no single commercial owner, driven by a global developer community `(community consensus)`.\n- Yearly major releases (now generations 17/18); the most active extension ecosystem (PostGIS, Citus, vector plugins) `(community consensus)`.\n- Tens of thousands of GitHub stars; the long-termist's choice with a strong compatibility reputation `(community consensus)`."}}
CONTENT["oracle"]["maturity"] = {
  "zh": {"v": "有", "p": "1979 年发布；商业数据库的定义者",
         "b": "- 1979 年发布首个商用 SQL 数据库；现 19c/23ai/26ai 代 `社区共识`。\n- 生态：DBA 人才、第三方工具、教材最完整，但与 Oracle 绑定深 `社区共识`。\n- 趋势：云与去 O 运动下新增市场收缩，存量基本盘极大 `社区共识`。"},
  "en": {"v": "Supported", "p": "released 1979; defined the commercial database",
         "b": "- First commercial SQL database, 1979; current generations 19c/23ai/26ai `(community consensus)`.\n- Ecosystem: deepest DBA talent pool, third-party tools and training materials — but deeply Oracle-tied `(community consensus)`.\n- Trend: new-market share shrinking under cloud and off-Oracle moves; installed base remains enormous `(community consensus)`."}}
CONTENT["oceanbase"]["maturity"] = {
  "zh": {"v": "有", "p": "2010 年支付宝内部诞生；2021 年开源",
         "b": "- 2010 年为支付宝诞生，2021 年开源；现 4.x 代 `官方文档`。\n- GitHub stars 接近万级；蚂蚁集团持续投入，研发团队规模大 `社区共识`。\n- 金融/政企基本盘扎实；海外与互联网行业声量弱于国内金融 `社区共识`。"},
  "en": {"v": "Supported", "p": "born inside Alipay 2010; open-sourced 2021",
         "b": "- Born for Alipay in 2010, open-sourced 2021; now generation 4.x `(official docs)`.\n- Approaching ten thousand GitHub stars; sustained Ant Group investment with a large R&D team `(community consensus)`.\n- Solid finance/government base; weaker mindshare overseas and in internet companies than in domestic finance `(community consensus)`."}}
CONTENT["tidb"]["maturity"] = {
  "zh": {"v": "有", "p": "2015 年开源；分布式开源标杆",
         "b": "- 2015 年开源（PingCAP）；现 7.x/8.x 代 `官方文档`。\n- GitHub stars 数万级，CNCF 毕业项目，社区活跃 `社区共识`。\n- 商业公司 PingCAP 持续融资与投入；HTAP 与云是增长方向 `社区共识`。"},
  "en": {"v": "Supported", "p": "open-sourced 2015; the distributed open-source benchmark",
         "b": "- Open-sourced 2015 (PingCAP); now generations 7.x/8.x `(official docs)`.\n- Tens of thousands of GitHub stars; CNCF graduated project with an active community `(community consensus)`.\n- PingCAP keeps raising and investing; HTAP and cloud are the growth bets `(community consensus)`."}}
CONTENT["polardb"]["maturity"] = {
  "zh": {"v": "有", "p": "2017 年发布；阿里云主推云原生数据库",
         "b": "- 2017 年发布；PolarDB-X、PolarDB for PostgreSQL 等陆续开源 `官方文档`。\n- 背靠阿里云，研发投入稳定；开源社区声量弱于 TiDB/OceanBase `社区共识`。\n- 版本线较多（MySQL/PG/X），选型时注意对准版本 `社区共识`。"},
  "en": {"v": "Supported", "p": "launched 2017; Alibaba Cloud's flagship cloud-native DB",
         "b": "- Launched 2017; PolarDB-X and PolarDB for PostgreSQL open-sourced later `(official docs)`.\n- Backed by Alibaba Cloud with steady R&D; quieter open-source community than TiDB/OceanBase `(community consensus)`.\n- Several product lines (MySQL/PG/X) — align on the right edition when selecting `(community consensus)`."}}
CONTENT["alloydb"]["maturity"] = {
  "zh": {"v": "有", "p": "2022 年 GA；Google 全资投入",
         "b": "- 2022 年 GA；Google Cloud 全资自研，Omni 本地版 2024 年后发力 `官方文档`。\n- 年轻产品：功能迭代快，但长期行为变更记录短，生产案例少于 Aurora `社区共识`。\n- 依赖 Google Cloud 生态，中立性弱于开源 PG `社区共识`。"},
  "en": {"v": "Supported", "p": "GA 2022; fully Google-funded",
         "b": "- GA 2022; fully Google-built, with the Omni on-premises edition pushed after 2024 `(official docs)`.\n- Young product: fast iteration but short behavioral track record and fewer production cases than Aurora `(community consensus)`.\n- Tied to the Google Cloud ecosystem; less neutral than open-source PostgreSQL `(community consensus)`."}}
CONTENT["aurora"]["maturity"] = {
  "zh": {"v": "有", "p": "2014 年发布；云原生数据库的开创者",
         "b": "- 2014 年 re:Invent 发布，MySQL/PG 兼容双引擎；AWS 增长最快的服务之一 `社区共识`。\n- 生产案例极多，调优/排障资料丰富 `社区共识`。\n- 闭源云服务：行为由 AWS 定义，大版本跟进上游有延迟 `社区共识`。"},
  "en": {"v": "Supported", "p": "launched 2014; pioneered the cloud-native database",
         "b": "- Launched at re:Invent 2014 with MySQL- and PostgreSQL-compatible engines; among AWS's fastest-growing services `(community consensus)`.\n- Enormous production footprint with rich tuning/troubleshooting material `(community consensus)`.\n- Closed cloud service: behavior defined by AWS; major-version tracking of upstream lags `(community consensus)`."}}
CONTENT["tdsql"]["maturity"] = {
  "zh": {"v": "有", "p": "2007 年腾讯内部诞生；金融场景久经考验",
         "b": "- 2007 年为腾讯计费系统诞生，后开放；TDSQL-C（Serverless）是新一代 `官方文档`。\n- 金融/政企案例多，腾讯云持续投入 `厂商口径`。\n- 开源与社区声量弱于 OceanBase/TiDB，公开技术细节少 `社区共识`。"},
  "en": {"v": "Supported", "p": "born inside Tencent 2007; battle-tested in finance",
         "b": "- Born 2007 for Tencent's billing system, later opened up; TDSQL-C (serverless) is the new generation `(official docs)`.\n- Strong finance/government footprint with continued Tencent Cloud investment `(vendor claim)`.\n- Quieter open-source/community presence than OceanBase/TiDB; fewer public technical details `(community consensus)`."}}
CONTENT["edb"]["maturity"] = {
  "zh": {"v": "有", "p": "2004 年成立；PG 商业化的老玩家",
         "b": "- EnterpriseDB 2004 年成立，EPAS 主打 Oracle 兼容迁移 `社区共识`。\n- 2024 年被 Bain Capital 收购私有化，战略延续性待观察 `社区共识`。\n- 社区声量小于云厂商 PG，强项是传统企业迁移项目 `社区共识`。"},
  "en": {"v": "Supported", "p": "founded 2004; veteran of PostgreSQL commercialization",
         "b": "- EnterpriseDB founded 2004; EPAS targets Oracle-compatible migrations `(community consensus)`.\n- Taken private by Bain Capital in 2024 — strategic continuity worth watching `(community consensus)`.\n- Quieter community than cloud PG offerings; strength is traditional enterprise migrations `(community consensus)`."}}
CONTENT["mariadb"]["maturity"] = {
  "zh": {"v": "有", "p": "2009 年从 MySQL fork；上市公司",
         "b": "- 2009 年由 MySQL 创始人 Monty fork；MariaDB plc 上市 `社区共识`。\n- 曾财务动荡、2024 年被 K1 私有化，治理稳定性有问号 `社区共识`。\n- 社区版持续迭代，但生态声量弱于 MySQL/PG `社区共识`。"},
  "en": {"v": "Supported", "p": "forked from MySQL 2009; publicly traded",
         "b": "- Forked 2009 by MySQL founder Monty; MariaDB plc went public `(community consensus)`.\n- Financial turbulence and a 2024 take-private by K1 raise governance questions `(community consensus)`.\n- Community edition keeps iterating, but mindshare trails MySQL/PG `(community consensus)`."}}
CONTENT["cockroachdb"]["maturity"] = {
  "zh": {"v": "有", "p": "2015 年开源；2023 年转 BSL 许可",
         "b": "- 2015 年开源；2023 年核心改 BSL 引发社区 fork 讨论 `社区共识`。\n- GitHub stars 数万级；Cockroach Labs 持续融资 `社区共识`。\n- Serverless/Standard/Dedicated 多形态，版本线需对准 `官方文档`。"},
  "en": {"v": "Supported", "p": "open-sourced 2015; moved to BSL in 2023",
         "b": "- Open-sourced 2015; the 2023 core move to BSL sparked fork debates `(community consensus)`.\n- Tens of thousands of GitHub stars; Cockroach Labs keeps raising `(community consensus)`.\n- Serverless/Standard/Dedicated editions — align on the right one `(official docs)`."}}
CONTENT["yugabytedb"]["maturity"] = {
  "zh": {"v": "有", "p": "2016 年成立；2024 年转 Apache 2.0",
         "b": "- 2016 年成立，2017 年开源；2024 年将核心转回 Apache 2.0 许可证 `官方文档`。\n- GitHub stars 万级；Yugabyte Inc 持续投入 `社区共识`。\n- 许可证回摆是加分项，但社区规模仍小于 CRDB/TiDB `社区共识`。"},
  "en": {"v": "Supported", "p": "founded 2016; returned to Apache 2.0 in 2024",
         "b": "- Founded 2016, open-sourced 2017; core moved back to Apache 2.0 in 2024 `(official docs)`.\n- Tens of thousands of GitHub stars; Yugabyte Inc keeps investing `(community consensus)`.\n- The license reversal is a plus, but community scale still trails CRDB/TiDB `(community consensus)`."}}
CONTENT["spanner"]["maturity"] = {
  "zh": {"v": "有", "p": "2012 年论文；2017 年 GA",
         "b": "- 2012 年 Spanner 论文定义全球分布式数据库；2017 年 Cloud Spanner GA `社区共识`。\n- Google 内部（Ads 等）大规模使用，外部标杆案例多为大型企业 `社区共识`。\n- 定价高，长期是“贵但省心”的代表 `社区共识`。"},
  "en": {"v": "Supported", "p": "2012 paper; GA 2017",
         "b": "- The 2012 Spanner paper defined the global distributed database; Cloud Spanner GA 2017 `(community consensus)`.\n- Massive internal Google use (Ads etc.); external flagships are mostly large enterprises `(community consensus)`.\n- Premium pricing — long the poster child of “expensive but worry-free” `(community consensus)`."}}
CONTENT["mongodb"]["maturity"] = {
  "zh": {"v": "有", "p": "2009 年发布；文档数据库代名词",
         "b": "- 2009 年发布；2018 年改 SSPL 许可，引发社区版分歧 `社区共识`。\n- GitHub stars 数万级；Atlas 是增长引擎，上市公司 MongoDB Inc `社区共识`。\n- 生态（Mongoose/Compass/驱动）极厚，招聘容易 `社区共识`。"},
  "en": {"v": "Supported", "p": "released 2009; synonymous with document databases",
         "b": "- Released 2009; the 2018 SSPL switch split the community edition's future `(community consensus)`.\n- Tens of thousands of GitHub stars; Atlas is the growth engine of public MongoDB Inc. `(community consensus)`.\n- Extremely thick ecosystem (Mongoose, Compass, drivers); easy hiring `(community consensus)`."}}
CONTENT["redis-valkey"]["maturity"] = {
  "zh": {"v": "有", "p": "2009 年诞生；2024 年许可风波后分叉",
         "b": "- Redis 2009 年由 Salvatore Sanfilippo 发布；2024 年改 RSALv2/SSPL，Valkey fork 并入 Linux 基金会 `社区共识`。\n- redis/redis GitHub stars 数万级（历史积累），Valkey 从零快速追赶 `社区共识`。\n- 选型需做许可尽调：Redis 7.4+ 不再是 OSI 开源 `社区共识`。"},
  "en": {"v": "Supported", "p": "born 2009; forked after the 2024 license storm",
         "b": "- Redis released 2009 by Salvatore Sanfilippo; the 2024 RSALv2/SSPL switch led to the Valkey fork under the Linux Foundation `(community consensus)`.\n- redis/redis holds tens of thousands of stars (historical); Valkey catching up fast from zero `(community consensus)`.\n- Selection needs license due diligence: Redis 7.4+ is no longer OSI open source `(community consensus)`."}}
CONTENT["cassandra-scylladb"]["maturity"] = {
  "zh": {"v": "有", "p": "Cassandra 2008 开源；ScyllaDB 2016 开源",
         "b": "- Cassandra：2008 年 Facebook 开源，2010 年 Apache 毕业；老牌分布式宽列 `社区共识`。\n- ScyllaDB：2015 年成立，C++ 重写，DynamoDB 兼容是差异化 `社区共识`。\n- 两者社区都活跃，但新增项目热度不如向量/Serverless 新贵 `社区共识`。"},
  "en": {"v": "Supported", "p": "Cassandra open-sourced 2008; ScyllaDB 2016",
         "b": "- Cassandra: open-sourced by Facebook 2008, Apache graduated 2010; the veteran distributed wide-column store `(community consensus)`.\n- ScyllaDB: founded 2015, C++ rewrite; DynamoDB compatibility is the differentiator `(community consensus)`.\n- Both communities active, but new-project buzz trails vector/serverless upstarts `(community consensus)`."}}
CONTENT["dynamodb"]["maturity"] = {
  "zh": {"v": "有", "p": "2012 年 GA；Serverless KV 的定义者",
         "b": "- 2012 年 GA（源自 2007 Dynamo 论文）；AWS 核心服务之一 `社区共识`。\n- 行为稳定，API 十余年基本不动；向后兼容口碑好 `社区共识`。\n- 闭源云服务，能力演进由 AWS 排期 `社区共识`。"},
  "en": {"v": "Supported", "p": "GA 2012; defined serverless KV",
         "b": "- GA 2012 (from the 2007 Dynamo paper); a core AWS service `(community consensus)`.\n- Stable behavior with a mostly unchanged API for over a decade; strong backward-compatibility reputation `(community consensus)`.\n- Closed cloud service; feature evolution follows AWS's roadmap `(community consensus)`."}}
CONTENT["etcd"]["maturity"] = {
  "zh": {"v": "有", "p": "2013 年诞生；CNCF 毕业项目",
         "b": "- 2013 年由 CoreOS 发布；2020 年 CNCF 毕业 `社区共识`。\n- Kubernetes 的默认元数据存储，间接装机量极大 `社区共识`。\n- 治理中立，长期维护有保障；但功能演进保守 `社区共识`。"},
  "en": {"v": "Supported", "p": "born 2013; CNCF graduated project",
         "b": "- Released 2013 by CoreOS; CNCF graduated 2020 `(community consensus)`.\n- Kubernetes' default metadata store — enormous indirect install base `(community consensus)`.\n- Neutral governance with assured long-term maintenance; conservative feature evolution `(community consensus)`."}}
CONTENT["clickhouse"]["maturity"] = {
  "zh": {"v": "有", "p": "2016 年开源；OLAP 开源标杆",
         "b": "- 2016 年由 Yandex 开源；2021 年 ClickHouse Inc 独立融资 `社区共识`。\n- GitHub stars 数万级，社区极活跃；云（Cloud）是商业化主线 `社区共识`。\n- 版本迭代快，企业用需跟紧 LTS 线 `社区共识`。"},
  "en": {"v": "Supported", "p": "open-sourced 2016; the open-source OLAP benchmark",
         "b": "- Open-sourced by Yandex 2016; ClickHouse Inc. spun out and funded 2021 `(community consensus)`.\n- Tens of thousands of GitHub stars and a hyperactive community; Cloud is the commercial mainline `(community consensus)`.\n- Fast release cadence — enterprises should track the LTS line `(community consensus)`."}}
CONTENT["doris"]["maturity"] = {
  "zh": {"v": "有", "p": "2017 年开源；2022 年 Apache 毕业",
         "b": "- 前身百度 Palo，2017 年开源，2022 年 Apache 毕业 `社区共识`。\n- GitHub stars 万级；SelectDB 提供商业支持 `社区共识`。\n- 国内社区活跃，海外声量弱于 ClickHouse/StarRocks `社区共识`。"},
  "en": {"v": "Supported", "p": "open-sourced 2017; Apache graduated 2022",
         "b": "- Formerly Baidu Palo, open-sourced 2017, Apache graduated 2022 `(community consensus)`.\n- Tens of thousands of GitHub stars; SelectDB provides commercial support `(community consensus)`.\n- Active domestic community; weaker overseas mindshare than ClickHouse/StarRocks `(community consensus)`."}}
CONTENT["starrocks"]["maturity"] = {
  "zh": {"v": "有", "p": "2021 年开源；发展最快的 OLAP 新贵之一",
         "b": "- 2021 年开源；CelerData 商业化，融资顺利 `社区共识`。\n- GitHub stars 接近万级，社区增长快 `社区共识`。\n- 年轻：长期生产案例少于 ClickHouse/Doris，版本行为变更需跟进 `社区共识`。"},
  "en": {"v": "Supported", "p": "open-sourced 2021; among the fastest-growing OLAP upstarts",
         "b": "- Open-sourced 2021; commercialized by CelerData with smooth fundraising `(community consensus)`.\n- Approaching ten thousand GitHub stars with fast community growth `(community consensus)`.\n- Young: fewer long-term production cases than ClickHouse/Doris; track behavioral changes across versions `(community consensus)`."}}
CONTENT["duckdb"]["maturity"] = {
  "zh": {"v": "有", "p": "2018 年诞生；嵌入式 OLAP 的现象级项目",
         "b": "- 2018 年由 CWI（荷兰数学与计算机中心）发布；DuckDB Labs/MotherDuck 商业化 `社区共识`。\n- GitHub stars 数万级，增长极快；基金会治理，中立性好 `社区共识`。\n- 年轻但口碑极佳，“SQLite for Analytics”定位深入人心 `社区共识`。"},
  "en": {"v": "Supported", "p": "born 2018; the phenomenal embedded-OLAP project",
         "b": "- Released 2018 by CWI (Dutch national research institute); commercialized via DuckDB Labs/MotherDuck `(community consensus)`.\n- Tens of thousands of GitHub stars and explosive growth; foundation-governed with good neutrality `(community consensus)`.\n- Young but superb reputation; the “SQLite for Analytics” positioning resonates widely `(community consensus)`."}}
CONTENT["milvus"]["maturity"] = {
  "zh": {"v": "有", "p": "2019 年开源；向量数据库的先行者",
         "b": "- 2019 年开源（Zilliz）；2021 年进入 LF AI 基金会 `官方文档`。\n- GitHub stars 数万级，向量领域最高之一 `社区共识`。\n- 2.x 重构后稳定性提升；大模型浪潮的最大受益者之一 `社区共识`。"},
  "en": {"v": "Supported", "p": "open-sourced 2019; the vector-database pioneer",
         "b": "- Open-sourced 2019 (Zilliz); joined the LF AI Foundation 2021 `(official docs)`.\n- Tens of thousands of GitHub stars, among the highest in vector DBs `(community consensus)`.\n- Stability improved after the 2.x rewrite; a prime beneficiary of the LLM wave `(community consensus)`."}}
CONTENT["weaviate"]["maturity"] = {
  "zh": {"v": "有", "p": "2019 年前后开源；混合检索见长",
         "b": "- 2019 年前后开源；Weaviate 公司持续融资 `社区共识`。\n- GitHub stars 万级；模块化（向量化模块可选）是特色 `社区共识`。\n- 社区规模小于 Milvus，文档与教程持续补齐中 `社区共识`。"},
  "en": {"v": "Supported", "p": "open-sourced around 2019; excels at hybrid search",
         "b": "- Open-sourced around 2019; the Weaviate company keeps raising `(community consensus)`.\n- Tens of thousands of GitHub stars; modular design (pluggable vectorizer modules) is the specialty `(community consensus)`.\n- Smaller community than Milvus; docs and tutorials still catching up `(community consensus)`."}}
CONTENT["qdrant"]["maturity"] = {
  "zh": {"v": "有", "p": "2021 年开源；Rust 实现的新贵",
         "b": "- 2021 年开源；Qdrant 公司持续融资 `社区共识`。\n- GitHub stars 数万级，增长快；Rust 实现是性能口碑来源 `社区共识`。\n- 年轻：超大规模生产案例少于 Milvus `社区共识`。"},
  "en": {"v": "Supported", "p": "open-sourced 2021; the Rust upstart",
         "b": "- Open-sourced 2021; the Qdrant company keeps raising `(community consensus)`.\n- Tens of thousands of GitHub stars and fast growth; the Rust implementation underpins its performance reputation `(community consensus)`.\n- Young: fewer hyperscale production cases than Milvus `(community consensus)`."}}
CONTENT["sqlserver"]["maturity"] = {
  "zh": {"v": "有", "p": "1989 年诞生；微软生态的基本盘",
         "b": "- 1989 年与 Sybase 合作诞生；2016 年推出 Linux 版 `社区共识`。\n- .NET/Windows 生态基本盘极大，企业存量多 `社区共识`。\n- 云趋势下新增份额被云原生分流，但存量迁移需求稳定 `社区共识`。"},
  "en": {"v": "Supported", "p": "born 1989; the bedrock of the Microsoft ecosystem",
         "b": "- Born 1989 with Sybase; Linux edition launched 2016 `(community consensus)`.\n- Enormous .NET/Windows installed base with heavy enterprise presence `(community consensus)`.\n- New share diverted to cloud-native, but steady migration demand from the installed base `(community consensus)`."}}
# ---------------- 维度4：标杆用户 ----------------
CONTENT["mysql"]["adopters"] = {
  "zh": {"v": "有", "p": "互联网大厂的基本盘",
         "b": "- Meta（Facebook）、Wikipedia 等公开重度用户 `社区共识`。\n- 曾支撑 YouTube/Twitter/Uber 早期架构，后部分迁移 `社区共识`。\n- 国内：各大厂自建 MySQL 分支（阿里/腾讯）是事实标准 `社区共识`。"},
  "en": {"v": "Supported", "p": "the bedrock of big internet companies",
         "b": "- Public heavy users include Meta (Facebook) and Wikipedia `(community consensus)`.\n- Once powered early YouTube/Twitter/Uber architectures; some later migrated `(community consensus)`.\n- China: in-house MySQL forks at major internet companies (Alibaba/Tencent) are the de-facto standard `(community consensus)`."}}
CONTENT["postgresql"]["adopters"] = {
  "zh": {"v": "有", "p": "Instagram/Reddit 等公开案例",
         "b": "- Instagram、Reddit 等公开大规模 PG 用户 `社区共识`。\n- 金融/政企去 O 迁移的首选目标之一 `社区共识`。\n- 各云厂商 RDS PG 用户极多，间接证明 `厂商口径`。"},
  "en": {"v": "Supported", "p": "public cases like Instagram/Reddit",
         "b": "- Public large-scale users include Instagram and Reddit `(community consensus)`.\n- A top target for off-Oracle migrations in finance/government `(community consensus)`.\n- Huge managed-RDS PostgreSQL user counts across clouds, indirectly confirming adoption `(vendor claim)`."}}
CONTENT["oracle"]["adopters"] = {
  "zh": {"v": "有", "p": "银行/电信/政府的核心系统",
         "b": "- 全球大型银行、电信运营商、政府机构核心系统（厂商口径）`厂商口径`。\n- 中国：国有大行、运营商 BOSS 系统存量大 `社区共识`。\n- 去 O 运动下新增减少，但存量迁移周期以十年计 `社区共识`。"},
  "en": {"v": "Supported", "p": "core systems of banks/telecoms/governments",
         "b": "- Core systems of global banks, telecom operators and government agencies (vendor claim) `(vendor claim)`.\n- China: large installed base in state-owned banks and carrier BSS/OSS systems `(community consensus)`.\n- New adoption shrinking under off-Oracle moves, but migration cycles from the installed base span decades `(community consensus)`."}}
CONTENT["oceanbase"]["adopters"] = {
  "zh": {"v": "有", "p": "蚂蚁/支付宝全系；国有大行",
         "b": "- 蚂蚁集团全系（支付宝）核心交易系统 `厂商口径`。\n- 中国工商银行等国有大行核心系统（厂商口径）`厂商口径`。\n- 政企/运营商集采案例多，金融基本盘最扎实 `社区共识`。"},
  "en": {"v": "Supported", "p": "full Ant/Alipay stack; state-owned banks",
         "b": "- Ant Group's full stack (Alipay) core transaction systems `(vendor claim)`.\n- Core systems of state-owned banks such as ICBC (vendor claim) `(vendor claim)`.\n- Many government/enterprise and carrier procurement wins; the most solid finance base `(community consensus)`."}}
CONTENT["tidb"]["adopters"] = {
  "zh": {"v": "有", "p": "美团/知乎/小米等互联网与金融",
         "b": "- 美团、知乎、小米等互联网公司公开案例（厂商口径）`厂商口径`。\n- 金融：部分银行核心/外围系统 `厂商口径`。\n- 海外：日本 PayPay 等（厂商口径）`厂商口径`。"},
  "en": {"v": "Supported", "p": "Meituan/Zhihu/Xiaomi; internet and finance",
         "b": "- Public internet-company cases: Meituan, Zhihu, Xiaomi, etc. (vendor claim) `(vendor claim)`.\n- Finance: core/peripheral systems at some banks `(vendor claim)`.\n- Overseas: PayPay (Japan) and others (vendor claim) `(vendor claim)`."}}
CONTENT["polardb"]["adopters"] = {
  "zh": {"v": "有", "p": "阿里系（淘宝/天猫/钉钉）",
         "b": "- 淘宝/天猫/钉钉等阿里系核心业务（厂商口径）`厂商口径`。\n- 阿里云公共云客户广泛，政企案例多 `厂商口径`。\n- 双 11 大促是年度极限考验 `社区共识`。"},
  "en": {"v": "Supported", "p": "Alibaba stack (Taobao/Tmall/DingTalk)",
         "b": "- Core Alibaba businesses: Taobao, Tmall, DingTalk, etc. (vendor claim) `(vendor claim)`.\n- Broad Alibaba Cloud public-cloud customer base with many government/enterprise cases `(vendor claim)`.\n- The Double-11 shopping festival is the annual extreme test `(community consensus)`."}}
CONTENT["alloydb"]["adopters"] = {
  "zh": {"v": "有", "p": "Google Cloud 客户；案例少于 Aurora",
         "b": "- Google Cloud 官方客户案例（厂商口径）`厂商口径`。\n- 年轻产品，公开大规模生产案例少于 Aurora/RDS `社区共识`。\n- 从 PG 迁移来的用户是主要来源 `社区共识`。"},
  "en": {"v": "Supported", "p": "Google Cloud customers; fewer cases than Aurora",
         "b": "- Official Google Cloud customer stories (vendor claim) `(vendor claim)`.\n- Young product with fewer public hyperscale production cases than Aurora/RDS `(community consensus)`.\n- Mainly adopted by users migrating from PostgreSQL `(community consensus)`."}}
CONTENT["aurora"]["adopters"] = {
  "zh": {"v": "有", "p": "AWS 上最流行的关系型之一",
         "b": "- Airbnb、Capital One 等公开案例（厂商口径）`厂商口径`。\n- 大量从自建 MySQL/PG 迁移上云的用户 `社区共识`。\n- 中国区（宁夏/北京）亦有规模化用户 `厂商口径`。"},
  "en": {"v": "Supported", "p": "among the most popular relationals on AWS",
         "b": "- Public cases: Airbnb, Capital One, etc. (vendor claim) `(vendor claim)`.\n- Huge numbers migrating from self-hosted MySQL/PG `(community consensus)`.\n- Scaled adoption in China regions (Ningxia/Beijing) too `(vendor claim)`."}}
CONTENT["tdsql"]["adopters"] = {
  "zh": {"v": "有", "p": "腾讯系（微信支付/王者荣耀）",
         "b": "- 微信支付、王者荣耀等腾讯核心业务（厂商口径）`厂商口径`。\n- 金融机构（银行/证券）案例多 `厂商口径`。\n- 春节红包等极端峰值场景验证 `社区共识`。"},
  "en": {"v": "Supported", "p": "Tencent stack (WeChat Pay/Honor of Kings)",
         "b": "- Core Tencent businesses: WeChat Pay, Honor of Kings, etc. (vendor claim) `(vendor claim)`.\n- Many financial-institution (bank/securities) cases `(vendor claim)`.\n- Proven in extreme peaks like Lunar New Year red packets `(community consensus)`."}}
CONTENT["edb"]["adopters"] = {
  "zh": {"v": "有", "p": "传统企业去 O 迁移项目",
         "b": "- 全球传统企业（金融/政府/制造）的 Oracle 迁移项目（厂商口径）`厂商口径`。\n- 公开点名的互联网大厂案例少 `社区共识`。\n- 国内政企去 O 项目是主要阵地 `社区共识`。"},
  "en": {"v": "Supported", "p": "traditional-enterprise off-Oracle projects",
         "b": "- Oracle-migration projects at traditional enterprises worldwide — finance, government, manufacturing (vendor claim) `(vendor claim)`.\n- Few named public internet-scale cases `(community consensus)`.\n- Domestic government/enterprise off-Oracle projects are the main battleground `(community consensus)`."}}
CONTENT["mariadb"]["adopters"] = {
  "zh": {"v": "有", "p": "Wikipedia 是最著名的公开案例",
         "b": "- Wikipedia 从 MySQL 迁移到 MariaDB（公开）`社区共识`。\n- Google 内部曾用 MariaDB（公开报道）`社区共识`。\n- Linux 发行版默认 MySQL 替代，装机量大但多为中小场景 `社区共识`。"},
  "en": {"v": "Supported", "p": "Wikipedia is the most famous public case",
         "b": "- Wikipedia migrated from MySQL to MariaDB (public) `(community consensus)`.\n- Google used MariaDB internally (public reporting) `(community consensus)`.\n- Default MySQL replacement in Linux distros — huge install base, mostly smaller workloads `(community consensus)`."}}
CONTENT["cockroachdb"]["adopters"] = {
  "zh": {"v": "有", "p": "新兴市场金融科技；案例少于 TiDB",
         "b": "- 公开案例以新兴市场金融科技、SaaS 为主（厂商口径）`厂商口径`。\n- 顶级互联网大厂公开案例少于 TiDB/Cassandra `社区共识`。\n- 选型参考：多活/全球部署是主要采用动因 `社区共识`。"},
  "en": {"v": "Supported", "p": "emerging-market fintech; fewer cases than TiDB",
         "b": "- Public cases skew to emerging-market fintech and SaaS (vendor claim) `(vendor claim)`.\n- Fewer named hyperscaler cases than TiDB/Cassandra `(community consensus)`.\n- Selection signal: multi-active/global deployment is the main adoption driver `(community consensus)`."}}
CONTENT["yugabytedb"]["adopters"] = {
  "zh": {"v": "有", "p": "以厂商口径案例为主",
         "b": "- Kroger 等零售/企业案例（厂商口径）`厂商口径`。\n- 公开互联网大厂案例少于 Cassandra/CRDB `社区共识`。\n- YCQL 兼容 Cassandra 的迁移案例是特色 `社区共识`。"},
  "en": {"v": "Supported", "p": "mainly vendor-claimed cases",
         "b": "- Retail/enterprise cases such as Kroger (vendor claim) `(vendor claim)`.\n- Fewer named hyperscaler cases than Cassandra/CRDB `(community consensus)`.\n- YCQL's Cassandra compatibility makes migration stories the specialty `(community consensus)`."}}
CONTENT["spanner"]["adopters"] = {
  "zh": {"v": "有", "p": "Google Ads；Pokémon Go",
         "b": "- Google Ads 等内部核心业务 `社区共识`。\n- Pokémon Go（Niantic）上线初期的标杆案例（公开）`社区共识`。\n- 外部多为付得起溢价的大型企业 `社区共识`。"},
  "en": {"v": "Supported", "p": "Google Ads; Pokémon Go",
         "b": "- Internal cores like Google Ads `(community consensus)`.\n- Pokémon Go (Niantic) — the flagship launch story (public) `(community consensus)`.\n- External adopters are mostly large enterprises that can afford the premium `(community consensus)`."}}
CONTENT["mongodb"]["adopters"] = {
  "zh": {"v": "有", "p": "互联网/企业应用极广",
         "b": "- eBay、Bosch 等公开案例（厂商口径）`厂商口径`。\n- 国内：大量互联网与游戏公司 `社区共识`。\n- Atlas 用户数是 MongoDB Inc 财报核心指标 `厂商口径`。"},
  "en": {"v": "Supported", "p": "extremely broad internet/enterprise use",
         "b": "- Public cases: eBay, Bosch, etc. (vendor claim) `(vendor claim)`.\n- China: huge internet and gaming adoption `(community consensus)`.\n- Atlas customer count is the core metric in MongoDB Inc. earnings `(vendor claim)`."}}
CONTENT["redis-valkey"]["adopters"] = {
  "zh": {"v": "有", "p": "Twitter/X、GitHub、Stack Overflow",
         "b": "- Twitter/X、GitHub、Stack Overflow 等公开重度用户 `社区共识`。\n- 几乎所有互联网公司的缓存/队列标配 `社区共识`。\n- Valkey：AWS/Google 等云厂商与 Linux 基金会背书，迁移案例增长中 `社区共识`。"},
  "en": {"v": "Supported", "p": "Twitter/X, GitHub, Stack Overflow",
         "b": "- Public heavy users: Twitter/X, GitHub, Stack Overflow `(community consensus)`.\n- The default cache/queue at virtually every internet company `(community consensus)`.\n- Valkey: backed by AWS/Google and the Linux Foundation; migration stories growing `(community consensus)`."}}
CONTENT["cassandra-scylladb"]["adopters"] = {
  "zh": {"v": "有", "p": "Netflix、Apple、Discord",
         "b": "- Netflix、Apple、Discord 等公开大规模用户 `社区共识`。\n- Discord 从 Cassandra 迁到 ScyllaDB 是著名案例（公开博客）`社区共识`。\n- 国内大厂（字节/快手等）有规模化使用 `社区共识`。"},
  "en": {"v": "Supported", "p": "Netflix, Apple, Discord",
         "b": "- Public hyperscale users: Netflix, Apple, Discord `(community consensus)`.\n- Discord's Cassandra-to-ScyllaDB migration is a famous public case `(community consensus)`.\n- Scaled use at Chinese hyperscalers (ByteDance/Kuaishou etc.) `(community consensus)`."}}
CONTENT["dynamodb"]["adopters"] = {
  "zh": {"v": "有", "p": "AWS 内部+海量外部用户",
         "b": "- Snap 等公开大规模案例（厂商口径）`厂商口径`。\n- AWS 内部大量服务依赖 DynamoDB `社区共识`。\n- Serverless 架构的首选 KV，初创公司采用极广 `社区共识`。"},
  "en": {"v": "Supported", "p": "inside AWS plus massive external use",
         "b": "- Public hyperscale cases: Snap, etc. (vendor claim) `(vendor claim)`.\n- Many internal AWS services depend on DynamoDB `(community consensus)`.\n- The default KV for serverless architectures; extremely broad startup adoption `(community consensus)`."}}
CONTENT["etcd"]["adopters"] = {
  "zh": {"v": "有", "p": "Kubernetes 间接装机量极大",
         "b": "- 所有 Kubernetes 集群默认用 etcd 存元数据（公开）`社区共识`。\n- 直接把 etcd 当业务 KV 用的公开案例少 `社区共识`。\n- 云厂商托管 k8s  behind the scenes 大规模使用 `社区共识`。"},
  "en": {"v": "Supported", "p": "enormous indirect install via Kubernetes",
         "b": "- Every Kubernetes cluster uses etcd for metadata by default (public) `(community consensus)`.\n- Few public cases use etcd directly as a business KV store `(community consensus)`.\n- Cloud managed-Kubernetes offerings run it at scale behind the scenes `(community consensus)`."}}
CONTENT["clickhouse"]["adopters"] = {
  "zh": {"v": "有", "p": "Cloudflare、字节等公开案例",
         "b": "- Cloudflare（公开博客）、字节跳动等大规模用户 `社区共识`。\n- 可观测性（日志分析）是最大采用场景之一 `社区共识`。\n- 国内互联网大厂自建 ClickHouse 集群普遍 `社区共识`。"},
  "en": {"v": "Supported", "p": "public cases: Cloudflare, ByteDance, etc.",
         "b": "- Large-scale public users: Cloudflare (public blog), ByteDance, etc. `(community consensus)`.\n- Observability (log analytics) is one of the biggest adoption scenarios `(community consensus)`.\n- Self-built ClickHouse clusters are common at Chinese hyperscalers `(community consensus)`."}}
CONTENT["doris"]["adopters"] = {
  "zh": {"v": "有", "p": "百度系起源；互联网与金融",
         "b": "- 起源百度，百度内部大规模使用 `社区共识`。\n- 小米、美团等互联网公司公开案例（厂商口径）`厂商口径`。\n- 金融/运营商实时数仓案例增长中 `厂商口径`。"},
  "en": {"v": "Supported", "p": "Baidu origins; internet and finance",
         "b": "- Originated at Baidu with large-scale internal use `(community consensus)`.\n- Public internet cases: Xiaomi, Meituan, etc. (vendor claim) `(vendor claim)`.\n- Growing finance/carrier real-time-warehouse cases `(vendor claim)`."}}
CONTENT["starrocks"]["adopters"] = {
  "zh": {"v": "有", "p": "小红书/爱奇艺等；增长快",
         "b": "- 小红书、爱奇艺等公开案例（厂商口径）`厂商口径`。\n- 从 ClickHouse/ES 迁移来的实时分析案例多 `社区共识`。\n- 年轻产品，超大规模案例少于 ClickHouse `社区共识`。"},
  "en": {"v": "Supported", "p": "Xiaohongshu/iQIYI etc.; fast growing",
         "b": "- Public cases: Xiaohongshu, iQIYI, etc. (vendor claim) `(vendor claim)`.\n- Many real-time-analytics migrations from ClickHouse/Elasticsearch `(community consensus)`.\n- Young product with fewer hyperscale cases than ClickHouse `(community consensus)`."}}
CONTENT["duckdb"]["adopters"] = {
  "zh": {"v": "有", "p": "数据团队/个人开发者极广；企业级案例在积累",
         "b": "- 个人开发者、数据团队几乎人手一个（社区共识）`社区共识`。\n- 被大量数据工具内嵌（dbt 等）`社区共识`。\n- 大型企业核心数仓案例少于 ClickHouse，MotherDuck 在积累 `社区共识`。"},
  "en": {"v": "Supported", "p": "ubiquitous with data teams/individuals; enterprise cases accumulating",
         "b": "- Nearly every data practitioner has one (community consensus) `(community consensus)`.\n- Embedded in many data tools (dbt etc.) `(community consensus)`.\n- Fewer large-enterprise core-warehouse cases than ClickHouse; MotherDuck accumulating `(community consensus)`."}}
CONTENT["milvus"]["adopters"] = {
  "zh": {"v": "有", "p": "大模型/AI 公司广泛采用",
         "b": "- 大模型与 AI 初创广泛采用（厂商口径）`厂商口径`。\n- 小米等互联网公司公开案例（厂商口径）`厂商口径`。\n- 向量领域案例数最多，但多为 RAG/推荐场景 `社区共识`。"},
  "en": {"v": "Supported", "p": "broadly adopted by LLM/AI companies",
         "b": "- Broadly adopted by LLM and AI startups (vendor claim) `(vendor claim)`.\n- Public internet cases: Xiaomi, etc. (vendor claim) `(vendor claim)`.\n- Most cases in the vector space, concentrated in RAG/recommendation `(community consensus)`."}}
CONTENT["weaviate"]["adopters"] = {
  "zh": {"v": "有", "p": "以厂商口径案例为主",
         "b": "- 官方客户案例（厂商口径）`厂商口径`。\n- 公开大规模案例少于 Milvus `社区共识`。\n- 混合检索场景（知识库/搜索）是主要采用动因 `社区共识`。"},
  "en": {"v": "Supported", "p": "mainly vendor-claimed cases",
         "b": "- Official customer stories (vendor claim) `(vendor claim)`.\n- Fewer public hyperscale cases than Milvus `(community consensus)`.\n- Hybrid-search scenarios (knowledge bases/search) are the main adoption driver `(community consensus)`."}}
CONTENT["qdrant"]["adopters"] = {
  "zh": {"v": "有", "p": "AI 初创采用多；案例少于 Milvus",
         "b": "- AI 初创与个人开发者采用多（社区共识）`社区共识`。\n- 公开大规模企业案例少于 Milvus `社区共识`。\n- 开源口碑好，社区版即完整功能是采用动因 `社区共识`。"},
  "en": {"v": "Supported", "p": "popular with AI startups; fewer cases than Milvus",
         "b": "- Popular with AI startups and individual developers (community consensus) `(community consensus)`.\n- Fewer public large-enterprise cases than Milvus `(community consensus)`.\n- Good open-source reputation; the complete community edition drives adoption `(community consensus)`."}}
CONTENT["sqlserver"]["adopters"] = {
  "zh": {"v": "有", "p": "微软系企业/政府的基本盘",
         "b": "- .NET/Windows 系企业、政府机构存量极大 `社区共识`。\n- ERP/OA 等传统应用软件的默认搭配 `社区共识`。\n- 新增互联网项目少，多为存量与迁移 `社区共识`。"},
  "en": {"v": "Supported", "p": "the bedrock of Microsoft-stack enterprises/governments",
         "b": "- Enormous installed base in .NET/Windows enterprises and government agencies `(community consensus)`.\n- The default pairing for traditional ERP/OA applications `(community consensus)`.\n- Few new internet projects; mostly installed base and migrations `(community consensus)`."}}
# ---------------- 维度5：生态工具链 ----------------
CONTENT["mysql"]["tooling"] = {
  "zh": {"v": "有", "p": "工具链最完整：备份/迁移/CDC/监控",
         "b": "- 备份：mysqldump/MySQL Shell/XtraBackup/Clone 插件 `社区共识`。\n- 在线 DDL/迁移：gh-ost、pt-online-schema-change `社区共识`。\n- CDC：Debezium、Canal；监控：PMM、mysqld_exporter + Prometheus `社区共识`。"},
  "en": {"v": "Supported", "p": "most complete: backup/migration/CDC/monitoring",
         "b": "- Backup: mysqldump, MySQL Shell, XtraBackup, Clone plugin `(community consensus)`.\n- Online DDL/migration: gh-ost, pt-online-schema-change `(community consensus)`.\n- CDC: Debezium, Canal; monitoring: PMM, mysqld_exporter + Prometheus `(community consensus)`."}}
CONTENT["postgresql"]["tooling"] = {
  "zh": {"v": "有", "p": "备份/CDC/监控完整；迁移有 ora2pg",
         "b": "- 备份：pg_dump/pg_basebackup/pgBackRest/Barman `社区共识`。\n- CDC：Debezium（逻辑复制）；迁移：ora2pg（Oracle→PG）`社区共识`。\n- 监控：pg_exporter/PMM；连接池：PgBouncer/Pgpool `社区共识`。"},
  "en": {"v": "Supported", "p": "complete backup/CDC/monitoring; ora2pg for migration",
         "b": "- Backup: pg_dump, pg_basebackup, pgBackRest, Barman `(community consensus)`.\n- CDC: Debezium (logical replication); migration: ora2pg (Oracle→PG) `(community consensus)`.\n- Monitoring: pg_exporter, PMM; pooling: PgBouncer, Pgpool `(community consensus)`."}}
CONTENT["oracle"]["tooling"] = {
  "zh": {"v": "有", "p": "RMAN/Data Pump/OGG；商业工具链",
         "b": "- 备份：RMAN；逻辑：Data Pump；CDC/同步：Oracle GoldenGate `社区共识`。\n- 迁移/升级：AutoUpgrade、DBUA；诊断：AWR/ASH（需 Diagnostic Pack 许可）`社区共识`。\n- 第三方开源工具少，生态围绕 Oracle 商业体系 `社区共识`。"},
  "en": {"v": "Supported", "p": "RMAN/Data Pump/OGG; commercial toolchain",
         "b": "- Backup: RMAN; logical: Data Pump; CDC/sync: Oracle GoldenGate `(community consensus)`.\n- Migration/upgrade: AutoUpgrade, DBUA; diagnostics: AWR/ASH (needs Diagnostic Pack license) `(community consensus)`.\n- Few third-party open-source tools; ecosystem revolves around Oracle's commercial stack `(community consensus)`."}}
CONTENT["oceanbase"]["tooling"] = {
  "zh": {"v": "有", "p": "OBD/OCP/OMS 全家桶；Flink CDC",
         "b": "- 部署运维：OBD/OCP；迁移：OMS（支持 Oracle/MySQL 迁入）`官方文档`。\n- CDC：Flink CDC、Debezium（OceanBase 连接器）`社区共识`。\n- 备份：物理备份/日志归档，PITR 完整 `官方文档`。"},
  "en": {"v": "Supported", "p": "OBD/OCP/OMS suite; Flink CDC",
         "b": "- Deploy/ops: OBD/OCP; migration: OMS (Oracle/MySQL inbound) `(official docs)`.\n- CDC: Flink CDC, Debezium (OceanBase connector) `(community consensus)`.\n- Backup: physical backup + log archiving with full PITR `(official docs)`."}}
CONTENT["tidb"]["tooling"] = {
  "zh": {"v": "有", "p": "BR/Dumpling/Lightning/DM/TiCDC；监控内置",
         "b": "- 备份恢复：BR；逻辑：Dumpling/Lightning；迁移：DM（MySQL→TiDB）`官方文档`。\n- CDC：TiCDC（到 Kafka/下游 TiDB）`官方文档`。\n- 监控：Prometheus + Grafana 内置 Dashboard，开箱即用 `官方文档`。"},
  "en": {"v": "Supported", "p": "BR/Dumpling/Lightning/DM/TiCDC; monitoring built in",
         "b": "- Backup/restore: BR; logical: Dumpling/Lightning; migration: DM (MySQL→TiDB) `(official docs)`.\n- CDC: TiCDC (to Kafka/downstream TiDB) `(official docs)`.\n- Monitoring: built-in Prometheus + Grafana dashboards, ready out of the box `(official docs)`."}}
CONTENT["polardb"]["tooling"] = {
  "zh": {"v": "有", "p": "阿里云 DTS/备份全托管",
         "b": "- 迁移/同步：阿里云 DTS（RDS/自建→PolarDB）`官方文档`。\n- 备份恢复：自动备份+PITR，控制台一键 `官方文档`。\n- 监控：云监控集成，慢 SQL 诊断（DAS）`官方文档`。"},
  "en": {"v": "Supported", "p": "Alibaba Cloud DTS and fully managed backup",
         "b": "- Migration/sync: Alibaba Cloud DTS (RDS/self-hosted→PolarDB) `(official docs)`.\n- Backup/restore: automated backup + PITR, one-click in console `(official docs)`.\n- Monitoring: CloudMonitor integration with slow-SQL diagnostics (DAS) `(official docs)`."}}
CONTENT["alloydb"]["tooling"] = {
  "zh": {"v": "有", "p": "Google 迁移服务+内置备份",
         "b": "- 迁移：Database Migration Service（PG→AlloyDB）`官方文档`。\n- 备份：自动备份+PITR；CDC：AlloyDB 与 Pub/Sub/Datastream 集成 `官方文档`。\n- 监控：Cloud Monitoring/Logging 原生集成 `官方文档`。"},
  "en": {"v": "Supported", "p": "Google migration service + built-in backup",
         "b": "- Migration: Database Migration Service (PG→AlloyDB) `(official docs)`.\n- Backup: automated backup + PITR; CDC via Pub/Sub/Datastream integration `(official docs)`.\n- Monitoring: native Cloud Monitoring/Logging integration `(official docs)`."}}
CONTENT["aurora"]["tooling"] = {
  "zh": {"v": "有", "p": "AWS DMS+快照/PITR 全托管",
         "b": "- 迁移：AWS DMS（异构/同构）；快照共享跨账号/跨区 `官方文档`。\n- 备份：连续备份到 S3，PITR 到秒级 `官方文档`。\n- 监控：CloudWatch/Performance Insights；CDC：DMS/Kinesis 集成 `官方文档`。"},
  "en": {"v": "Supported", "p": "AWS DMS + fully managed snapshots/PITR",
         "b": "- Migration: AWS DMS (heterogeneous/homogeneous); snapshot sharing across accounts/regions `(official docs)`.\n- Backup: continuous backup to S3 with second-granularity PITR `(official docs)`.\n- Monitoring: CloudWatch/Performance Insights; CDC via DMS/Kinesis integration `(official docs)`."}}
CONTENT["tdsql"]["tooling"] = {
  "zh": {"v": "有", "p": "腾讯云 DTS/备份全托管",
         "b": "- 迁移/同步：腾讯云 DTS `官方文档`。\n- 备份：自动备份+PITR `官方文档`。\n- 监控：云监控+DBbrain 诊断 `官方文档`。"},
  "en": {"v": "Supported", "p": "Tencent Cloud DTS and fully managed backup",
         "b": "- Migration/sync: Tencent Cloud DTS `(official docs)`.\n- Backup: automated backup + PITR `(official docs)`.\n- Monitoring: CloudMonitor + DBbrain diagnostics `(official docs)`."}}
CONTENT["edb"]["tooling"] = {
  "zh": {"v": "有", "p": "PG 工具链+EDB 迁移工具",
         "b": "- 继承 PG 工具链（pgBackRest/Barman/Debezium）`社区共识`。\n- 迁移：EDB Migration Toolkit（Oracle→EPAS）`官方文档`。\n- 监控：EDB Postgres Enterprise Manager `官方文档`。"},
  "en": {"v": "Supported", "p": "PG toolchain plus EDB migration tools",
         "b": "- Inherits the PG toolchain (pgBackRest, Barman, Debezium) `(community consensus)`.\n- Migration: EDB Migration Toolkit (Oracle→EPAS) `(official docs)`.\n- Monitoring: EDB Postgres Enterprise Manager `(official docs)`."}}
CONTENT["mariadb"]["tooling"] = {
  "zh": {"v": "有", "p": "基本继承 MySQL 工具链",
         "b": "- mysqldump/MariaDB 备份工具；gh-ost/pt-osc 多数可用 `社区共识`。\n- CDC：Debezium/Canal（协议兼容 MySQL）`社区共识`。\n- 专属工具少于 MySQL，SkySQL 托管版补齐 `社区共识`。"},
  "en": {"v": "Supported", "p": "largely inherits the MySQL toolchain",
         "b": "- mysqldump/MariaDB backup tools; gh-ost/pt-osc mostly work `(community consensus)`.\n- CDC: Debezium, Canal (protocol-compatible with MySQL) `(community consensus)`.\n- Fewer dedicated tools than MySQL; SkySQL managed edition fills gaps `(community consensus)`."}}
CONTENT["cockroachdb"]["tooling"] = {
  "zh": {"v": "有", "p": "CHANGEFEED 做 CDC；备份内置",
         "b": "- CDC：CHANGEFEED（到 Kafka/云存储）`官方文档`。\n- 备份：全量/增量内置，支持 PITR `官方文档`。\n- 迁移：MOLT（MySQL/Postgres→CRDB）等官方工具 `官方文档`。"},
  "en": {"v": "Supported", "p": "CHANGEFEED for CDC; built-in backup",
         "b": "- CDC: CHANGEFEED (to Kafka/cloud storage) `(official docs)`.\n- Backup: built-in full/incremental with PITR `(official docs)`.\n- Migration: official tools like MOLT (MySQL/Postgres→CRDB) `(official docs)`."}}
CONTENT["yugabytedb"]["tooling"] = {
  "zh": {"v": "有", "p": "yb-voyager 迁移；CDC streams",
         "b": "- 迁移：yb-voyager（Oracle/MySQL/PG/Cassandra→YB）`官方文档`。\n- CDC：CDC streams（gRPC/Kafka）`官方文档`。\n- 备份：分布式快照内置 `官方文档`。"},
  "en": {"v": "Supported", "p": "yb-voyager migration; CDC streams",
         "b": "- Migration: yb-voyager (Oracle/MySQL/PG/Cassandra→YB) `(official docs)`.\n- CDC: CDC streams (gRPC/Kafka) `(official docs)`.\n- Backup: built-in distributed snapshots `(official docs)`."}}
CONTENT["spanner"]["tooling"] = {
  "zh": {"v": "有", "p": "Google 生态集成；备份导入导出内置",
         "b": "- 备份/导出/导入内置（到 GCS）；PITR `官方文档`。\n- 数据处理：Dataflow/Beam 连接器；CDC：Change Streams `官方文档`。\n- 迁移：HarbourBridge（PG/MySQL→Spanner）`官方文档`。"},
  "en": {"v": "Supported", "p": "Google ecosystem integration; built-in backup/export/import",
         "b": "- Built-in backup/export/import (to GCS); PITR `(official docs)`.\n- Data processing: Dataflow/Beam connectors; CDC via Change Streams `(official docs)`.\n- Migration: HarbourBridge (PG/MySQL→Spanner) `(official docs)`."}}
CONTENT["mongodb"]["tooling"] = {
  "zh": {"v": "有", "p": "mongodump/Atlas 备份；Change Streams 做 CDC",
         "b": "- 备份：mongodump/mongorestore；Atlas 连续备份+PITR `官方文档`。\n- CDC：Change Streams；Debezium MongoDB 连接器 `社区共识`。\n- 迁移：Atlas Live Migration、mongomirror `官方文档`；Compass 图形工具 `社区共识`。"},
  "en": {"v": "Supported", "p": "mongodump/Atlas backup; Change Streams for CDC",
         "b": "- Backup: mongodump/mongorestore; Atlas continuous backup + PITR `(official docs)`.\n- CDC: Change Streams; Debezium MongoDB connector `(community consensus)`.\n- Migration: Atlas Live Migration, mongomirror `(official docs)`; Compass GUI `(community consensus)`."}}
CONTENT["redis-valkey"]["tooling"] = {
  "zh": {"v": "有", "p": "redis-shake 迁移；备份靠 RDB/AOF",
         "b": "- 备份：RDB 快照/AOF；云托管版自动备份 `社区共识`。\n- 迁移/同步：redis-shake（异构/跨云，社区共识）`社区共识`。\n- CDC：Debezium Redis 连接器；监控：redis_exporter `社区共识`。"},
  "en": {"v": "Supported", "p": "redis-shake migration; backup via RDB/AOF",
         "b": "- Backup: RDB snapshots/AOF; managed editions automate it `(community consensus)`.\n- Migration/sync: redis-shake (heterogeneous/cross-cloud, community standard) `(community consensus)`.\n- CDC: Debezium Redis connector; monitoring: redis_exporter `(community consensus)`."}}
CONTENT["cassandra-scylladb"]["tooling"] = {
  "zh": {"v": "有", "p": "Medusa 备份；sstableloader 迁移",
         "b": "- 备份：nodetool snapshot；Medusa（Spotify 开源，S3 备份编排）`社区共识`。\n- 迁移：sstableloader；ScyllaDB 有 DynamoDB/Cassandra 迁移工具 `社区共识`。\n- CDC：Debezium Cassandra 连接器；监控：JMX exporter `社区共识`。"},
  "en": {"v": "Supported", "p": "Medusa backup; sstableloader migration",
         "b": "- Backup: nodetool snapshot; Medusa (Spotify-open-sourced S3 backup orchestration) `(community consensus)`.\n- Migration: sstableloader; ScyllaDB ships DynamoDB/Cassandra migration tools `(community consensus)`.\n- CDC: Debezium Cassandra connector; monitoring: JMX exporter `(community consensus)`."}}
CONTENT["dynamodb"]["tooling"] = {
  "zh": {"v": "有", "p": "Streams 做 CDC；备份按需/PITR",
         "b": "- 备份：按需备份+PITR（35 天）`官方文档`。\n- CDC：DynamoDB Streams（+Lambda 触发器）`官方文档`。\n- 迁移：AWS DMS；导出到 S3（Parquet）做分析 `官方文档`。"},
  "en": {"v": "Supported", "p": "Streams for CDC; on-demand/PITR backup",
         "b": "- Backup: on-demand + PITR (35 days) `(official docs)`.\n- CDC: DynamoDB Streams (+ Lambda triggers) `(official docs)`.\n- Migration: AWS DMS; export to S3 (Parquet) for analytics `(official docs)`."}}
CONTENT["etcd"]["tooling"] = {
  "zh": {"v": "部分支持", "p": "工具链薄；etcdctl 快照够用",
         "b": "- 备份：etcdctl snapshot save/restore，简单可靠 `官方文档`。\n- 无 CDC/迁移工具概念（KV 语义简单）；监控：Prometheus metrics 内置 `官方文档`。\n- 工具链薄是定位决定的，不是缺点 `社区共识`。"},
  "en": {"v": "Partially supported", "p": "thin toolchain; etcdctl snapshots suffice",
         "b": "- Backup: etcdctl snapshot save/restore — simple and reliable `(official docs)`.\n- No CDC/migration-tooling concept (simple KV semantics); monitoring via built-in Prometheus metrics `(official docs)`.\n- The thin toolchain follows from its scope, not a weakness `(community consensus)`."}}
CONTENT["clickhouse"]["tooling"] = {
  "zh": {"v": "有", "p": "clickhouse-backup；Flink/Kafka 生态",
         "b": "- 备份：clickhouse-backup（社区事实标准）/官方备份恢复 `社区共识`。\n- 入数：Kafka 表引擎、Flink CDC、clickhouse-copier（分片间）`社区共识`。\n- 监控：Prometheus 集成；可视化：Tabix/官方 Play UI `社区共识`。"},
  "en": {"v": "Supported", "p": "clickhouse-backup; Flink/Kafka ecosystem",
         "b": "- Backup: clickhouse-backup (community standard) / official BACKUP/RESTORE `(community consensus)`.\n- Ingestion: Kafka table engine, Flink CDC, clickhouse-copier (inter-shard) `(community consensus)`.\n- Monitoring: Prometheus integration; UIs: Tabix / official Play UI `(community consensus)`."}}
CONTENT["doris"]["tooling"] = {
  "zh": {"v": "有", "p": "Broker 备份；Flink CDC；Stream Load",
         "b": "- 备份：Broker 备份到 HDFS/S3 `官方文档`。\n- 入数/CDC：Flink CDC、Stream Load、Routine Load（Kafka）`官方文档`。\n- 迁移：Doris-Spark/Flink 连接器；监控：Prometheus `社区共识`。"},
  "en": {"v": "Supported", "p": "Broker backup; Flink CDC; Stream Load",
         "b": "- Backup: Broker backup to HDFS/S3 `(official docs)`.\n- Ingestion/CDC: Flink CDC, Stream Load, Routine Load (Kafka) `(official docs)`.\n- Migration: Doris-Spark/Flink connectors; monitoring: Prometheus `(community consensus)`."}}
CONTENT["starrocks"]["tooling"] = {
  "zh": {"v": "有", "p": "Broker 备份；Flink CDC；Stream Load",
         "b": "- 备份：Broker 备份到 HDFS/S3 `官方文档`。\n- 入数/CDC：Flink CDC、Stream Load、Routine Load `官方文档`。\n- 迁移：Spark/Flink 连接器；监控：Prometheus `社区共识`。"},
  "en": {"v": "Supported", "p": "Broker backup; Flink CDC; Stream Load",
         "b": "- Backup: Broker backup to HDFS/S3 `(official docs)`.\n- Ingestion/CDC: Flink CDC, Stream Load, Routine Load `(official docs)`.\n- Migration: Spark/Flink connectors; monitoring: Prometheus `(community consensus)`."}}
CONTENT["duckdb"]["tooling"] = {
  "zh": {"v": "部分支持", "p": "文件即备份；无 CDC 概念",
         "b": "- 备份：文件拷贝即备份；MotherDuck 云同步/分享 `官方文档`。\n- 无 CDC/复制工具链（嵌入式定位）；与 pandas/Arrow/dbt 集成极好 `社区共识`。\n- 工具链薄是形态决定的 `社区共识`。"},
  "en": {"v": "Partially supported", "p": "the file is the backup; no CDC concept",
         "b": "- Backup: copy the file; MotherDuck cloud sync/sharing `(official docs)`.\n- No CDC/replication toolchain (embedded by design); excellent pandas/Arrow/dbt integration `(community consensus)`.\n- Thin toolchain follows from the form factor `(community consensus)`."}}
CONTENT["milvus"]["tooling"] = {
  "zh": {"v": "部分支持", "p": "Attu 管理；backup 工具；生态在补",
         "b": "- 管理：Attu（官方可视化）；备份：milvus-backup `官方文档`。\n- 迁移：milvus-migration（Elasticsearch/FAISS→Milvus）`官方文档`。\n- 对比 OLTP 生态，CDC/监控第三方工具少，生态在补齐中 `社区共识`。"},
  "en": {"v": "Partially supported", "p": "Attu admin; backup tool; ecosystem catching up",
         "b": "- Admin: Attu (official UI); backup: milvus-backup `(official docs)`.\n- Migration: milvus-migration (Elasticsearch/FAISS→Milvus) `(official docs)`.\n- Versus OLTP ecosystems, fewer third-party CDC/monitoring tools; ecosystem catching up `(community consensus)`."}}
CONTENT["weaviate"]["tooling"] = {
  "zh": {"v": "部分支持", "p": "备份 API；第三方工具少",
         "b": "- 备份：备份 API（到 S3/GCS）`官方文档`。\n- 迁移：各语言客户端+批导入；向量化模块生态（OpenAI/Cohere 等）`官方文档`。\n- 第三方 CDC/监控工具少于 Milvus `社区共识`。"},
  "en": {"v": "Partially supported", "p": "backup API; few third-party tools",
         "b": "- Backup: backup API (to S3/GCS) `(official docs)`.\n- Migration: per-language clients + batch import; vectorizer module ecosystem (OpenAI, Cohere, etc.) `(official docs)`.\n- Fewer third-party CDC/monitoring tools than Milvus `(community consensus)`."}}
CONTENT["qdrant"]["tooling"] = {
  "zh": {"v": "部分支持", "p": "快照 API；Web UI 内置",
         "b": "- 备份：集合/存储快照 API `官方文档`。\n- 管理：内置 Web UI；迁移：各语言客户端+批量 API `官方文档`。\n- 第三方生态小于 Milvus，但官方工具完整度好 `社区共识`。"},
  "en": {"v": "Partially supported", "p": "snapshot API; built-in Web UI",
         "b": "- Backup: collection/storage snapshot APIs `(official docs)`.\n- Admin: built-in Web UI; migration via per-language clients + batch APIs `(official docs)`.\n- Smaller third-party ecosystem than Milvus, but official tooling is complete `(community consensus)`."}}
CONTENT["sqlserver"]["tooling"] = {
  "zh": {"v": "有", "p": "SSMS/SSIS；微软全家桶",
         "b": "- 管理：SSMS；ETL：SSIS；备份：完整/差异/日志内置 `社区共识`。\n- CDC：内置 CDC/Change Tracking `官方文档`。\n- 迁移：DMA（Data Migration Assistant，SQL Server→Azure）`官方文档`。"},
  "en": {"v": "Supported", "p": "SSMS/SSIS; the full Microsoft suite",
         "b": "- Admin: SSMS; ETL: SSIS; backup: built-in full/differential/log `(community consensus)`.\n- CDC: built-in CDC / Change Tracking `(official docs)`.\n- Migration: DMA (Data Migration Assistant, SQL Server→Azure) `(official docs)`."}}
# ---------------- 维度6：云托管与 Serverless ----------------
CONTENT["mysql"]["managed"] = {
  "zh": {"v": "有", "p": "各云 RDS；PlanetScale 做 Serverless",
         "b": "- 各云厂商 RDS（阿里/腾讯/AWS/华为）全覆盖 `社区共识`。\n- Oracle MySQL HeatWave（云原生+分析加速）`厂商口径`。\n- Serverless：PlanetScale（基于 Vitess 的 Serverless MySQL）`社区共识`。"},
  "en": {"v": "Supported", "p": "RDS on every cloud; PlanetScale does serverless",
         "b": "- RDS on every cloud vendor (Alibaba/Tencent/AWS/Huawei) `(community consensus)`.\n- Oracle MySQL HeatWave (cloud-native + analytics acceleration) `(vendor claim)`.\n- Serverless: PlanetScale (serverless MySQL on Vitess) `(community consensus)`."}}
CONTENT["postgresql"]["managed"] = {
  "zh": {"v": "有", "p": "各云 RDS；Neon/Supabase 做 Serverless",
         "b": "- 各云厂商 RDS PG 全覆盖 `社区共识`。\n- Serverless：Neon（存算分离 Serverless PG）、Supabase `社区共识`。\n- 选择多，云中立性好，不易被单一厂商锁定 `社区共识`。"},
  "en": {"v": "Supported", "p": "RDS on every cloud; Neon/Supabase do serverless",
         "b": "- RDS PostgreSQL on every cloud vendor `(community consensus)`.\n- Serverless: Neon (disaggregated serverless PG), Supabase `(community consensus)`.\n- Plenty of choice with good cloud neutrality — hard to get locked to one vendor `(community consensus)`."}}
CONTENT["oracle"]["managed"] = {
  "zh": {"v": "有", "p": "OCI Autonomous Database；AWS RDS for Oracle",
         "b": "- OCI Autonomous Database（自治+Serverless 按量）`厂商口径`。\n- AWS RDS for Oracle（BYOL/托管）`厂商口径`。\n- 云上 Oracle 许可复杂，选型前做许可尽调 `社区共识`。"},
  "en": {"v": "Supported", "p": "OCI Autonomous Database; AWS RDS for Oracle",
         "b": "- OCI Autonomous Database (self-driving + serverless pay-per-use) `(vendor claim)`.\n- AWS RDS for Oracle (BYOL/managed) `(vendor claim)`.\n- Oracle licensing on cloud is complex — do license due diligence before selecting `(community consensus)`."}}
CONTENT["oceanbase"]["managed"] = {
  "zh": {"v": "有", "p": "OB Cloud（公有云/专属云）",
         "b": "- OB Cloud：阿里云/腾讯云/华为云等上线（厂商口径）`厂商口径`。\n- 支持公有云与专属云（VPC 内）形态 `官方文档`。\n- 海外云覆盖弱于 AWS 系 `社区共识`。"},
  "en": {"v": "Supported", "p": "OB Cloud (public/dedicated cloud)",
         "b": "- OB Cloud on Alibaba/Tencent/Huawei clouds (vendor claim) `(vendor claim)`.\n- Public-cloud and dedicated-cloud (in-VPC) forms `(official docs)`.\n- Weaker overseas cloud coverage than the AWS family `(community consensus)`."}}
CONTENT["tidb"]["managed"] = {
  "zh": {"v": "有", "p": "TiDB Cloud（Serverless/Dedicated）",
         "b": "- TiDB Cloud Serverless（按量）/ Dedicated（独享）`官方文档`。\n- 覆盖 AWS/GCP，国内走腾讯云/阿里云 `官方文档`。\n- 自建与云 API 一致，迁移顺滑 `社区共识`。"},
  "en": {"v": "Supported", "p": "TiDB Cloud (Serverless/Dedicated)",
         "b": "- TiDB Cloud Serverless (pay-per-use) / Dedicated `(official docs)`.\n- On AWS/GCP; in China via Tencent/Alibaba Cloud `(official docs)`.\n- Self-hosted and cloud share APIs for smooth migration `(community consensus)`."}}
CONTENT["polardb"]["managed"] = {
  "zh": {"v": "有", "p": "本身就是云服务；Serverless 形态",
         "b": "- PolarDB 本身就是阿里云托管服务，Serverless 按量计费 `官方文档`。\n- 无中立第三方托管，阿里云绑定 `社区共识`。\n- 开源版可自建，但与云版本能力有差异 `社区共识`。"},
  "en": {"v": "Supported", "p": "is itself a cloud service; serverless form",
         "b": "- PolarDB is itself an Alibaba Cloud managed service with serverless pay-per-use `(official docs)`.\n- No neutral third-party hosting; Alibaba Cloud-bound `(community consensus)`.\n- Open-source edition is self-hostable but differs from the cloud edition `(community consensus)`."}}
CONTENT["alloydb"]["managed"] = {
  "zh": {"v": "有", "p": "本身就是云服务；Omni 可本地",
         "b": "- AlloyDB 本身就是 Google Cloud 托管服务 `官方文档`。\n- Omni 版可在本地/GKE 运行，混合部署 `官方文档`。\n- 无第三方托管，Google Cloud 绑定 `社区共识`。"},
  "en": {"v": "Supported", "p": "is itself a cloud service; Omni runs on-premises",
         "b": "- AlloyDB is itself a Google Cloud managed service `(official docs)`.\n- Omni edition runs on-premises/GKE for hybrid deployment `(official docs)`.\n- No third-party hosting; Google Cloud-bound `(community consensus)`."}}
CONTENT["aurora"]["managed"] = {
  "zh": {"v": "有", "p": "本身就是云服务；Serverless v2",
         "b": "- Aurora 本身就是 AWS 托管服务；Serverless v2 自动伸缩 `官方文档`。\n- Global Database 跨区，Backtrack 回拨 `官方文档`。\n- AWS 绑定，无本地版（Outposts 除外）`社区共识`。"},
  "en": {"v": "Supported", "p": "is itself a cloud service; Serverless v2",
         "b": "- Aurora is itself an AWS managed service; Serverless v2 auto-scales `(official docs)`.\n- Global Database across regions; Backtrack rewind `(official docs)`.\n- AWS-bound; no on-premises edition (except Outposts) `(community consensus)`."}}
CONTENT["tdsql"]["managed"] = {
  "zh": {"v": "有", "p": "本身就是云服务；TDSQL-C Serverless",
         "b": "- TDSQL 本身就是腾讯云托管服务；TDSQL-C Serverless 按量 `官方文档`。\n- 私有化/专有云版本面向政企 `官方文档`。\n- 腾讯云绑定 `社区共识`。"},
  "en": {"v": "Supported", "p": "is itself a cloud service; TDSQL-C serverless",
         "b": "- TDSQL is itself a Tencent Cloud managed service; TDSQL-C serverless pay-per-use `(official docs)`.\n- Private/dedicated-cloud editions for government/enterprise `(official docs)`.\n- Tencent Cloud-bound `(community consensus)`."}}
CONTENT["edb"]["managed"] = {
  "zh": {"v": "有", "p": "EDB 托管云服务；各云也有 PG 托管",
         "b": "- EDB 提供托管云服务（厂商口径）`厂商口径`。\n- 各云厂商 RDS PG 可跑 EDB 兼容工作负载（需验证兼容层）`社区共识`。\n- 声量小于云厂商原生 PG 托管 `社区共识`。"},
  "en": {"v": "Supported", "p": "EDB managed cloud; PG hosting on every cloud too",
         "b": "- EDB offers a managed cloud service (vendor claim) `(vendor claim)`.\n- Cloud RDS PostgreSQL can run EDB-compatible workloads (verify the compatibility layer) `(community consensus)`.\n- Quieter than cloud-native PG hosting `(community consensus)`."}}
CONTENT["mariadb"]["managed"] = {
  "zh": {"v": "有", "p": "SkySQL；各云 MySQL 托管多兼容",
         "b": "- SkySQL（MariaDB 官方云，Serverless 形态）`厂商口径`。\n- 各云 MySQL 托管与 MariaDB 协议兼容，迁移成本低 `社区共识`。\n- 第三方托管选择少于 MySQL `社区共识`。"},
  "en": {"v": "Supported", "p": "SkySQL; cloud MySQL hosting mostly compatible",
         "b": "- SkySQL (official MariaDB cloud, serverless form) `(vendor claim)`.\n- Cloud MySQL hosting is protocol-compatible with MariaDB; low migration cost `(community consensus)`.\n- Fewer third-party hosting options than MySQL `(community consensus)`."}}
CONTENT["cockroachdb"]["managed"] = {
  "zh": {"v": "有", "p": "CockroachDB Cloud（Serverless/Standard/Dedicated）",
         "b": "- Cloud Serverless（按量）/ Standard / Dedicated 三档 `官方文档`。\n- 跨云部署（AWS/GCP）是特色 `官方文档`。\n- 自建版与云版功能对齐，BSL 许可注意 `社区共识`。"},
  "en": {"v": "Supported", "p": "CockroachDB Cloud (Serverless/Standard/Dedicated)",
         "b": "- Cloud Serverless (pay-per-use) / Standard / Dedicated tiers `(official docs)`.\n- Cross-cloud deployment (AWS/GCP) is the specialty `(official docs)`.\n- Self-hosted and cloud editions aligned; note the BSL license `(community consensus)`."}}
CONTENT["yugabytedb"]["managed"] = {
  "zh": {"v": "有", "p": "YugabyteDB Managed",
         "b": "- YugabyteDB Managed（云托管，AWS/GCP/Azure）`官方文档`。\n- 2024 年转 Apache 2.0 后，自建与云无许可顾虑 `官方文档`。\n- 托管规模声量小于 CRDB Cloud `社区共识`。"},
  "en": {"v": "Supported", "p": "YugabyteDB Managed",
         "b": "- YugabyteDB Managed (AWS/GCP/Azure) `(official docs)`.\n- After the 2024 return to Apache 2.0, no licensing worries for self-hosted or cloud `(official docs)`.\n- Quieter managed footprint than CRDB Cloud `(community consensus)`."}}
CONTENT["spanner"]["managed"] = {
  "zh": {"v": "有", "p": "纯云服务，无自建版",
         "b": "- Spanner 只有 Google Cloud 托管形态，无自建版 `官方文档`。\n- 按节点/按量计费，成本高是主要门槛 `社区共识`。\n- 选即绑定 Google Cloud `社区共识`。"},
  "en": {"v": "Supported", "p": "pure cloud service; no self-hosted edition",
         "b": "- Spanner exists only as a Google Cloud managed service; no self-hosted edition `(official docs)`.\n- Per-node/pay-per-use pricing; cost is the main barrier `(community consensus)`.\n- Choosing it means committing to Google Cloud `(community consensus)`."}}
CONTENT["mongodb"]["managed"] = {
  "zh": {"v": "有", "p": "Atlas（Serverless 实例）；各云也有托管",
         "b": "- Atlas：Serverless 实例按量，全球多区 `官方文档`。\n- 各云厂商也有 MongoDB 兼容/托管版 `社区共识`。\n- Atlas 是 MongoDB Inc 收入核心，功能优先上 Atlas `社区共识`。"},
  "en": {"v": "Supported", "p": "Atlas (serverless instances); hosted on every cloud too",
         "b": "- Atlas: serverless pay-per-use instances, global multi-region `(official docs)`.\n- MongoDB-compatible/hosted editions on every cloud `(community consensus)`.\n- Atlas is MongoDB Inc.'s revenue core; features land there first `(community consensus)`."}}
CONTENT["redis-valkey"]["managed"] = {
  "zh": {"v": "有", "p": "Upstash 做 Serverless；各云托管全",
         "b": "- Serverless：Upstash（按请求计费）`社区共识`。\n- 各云托管（ElastiCache/MemoryDB/阿里云等）支持 Redis 与 Valkey `社区共识`。\n- Redis Cloud（Redis Inc）企业级托管 `厂商口径`。"},
  "en": {"v": "Supported", "p": "Upstash does serverless; hosted on every cloud",
         "b": "- Serverless: Upstash (per-request billing) `(community consensus)`.\n- Managed on every cloud (ElastiCache/MemoryDB/Alibaba Cloud) for Redis and Valkey `(community consensus)`.\n- Redis Cloud (Redis Inc.) enterprise hosting `(vendor claim)`."}}
CONTENT["cassandra-scylladb"]["managed"] = {
  "zh": {"v": "有", "p": "Astra Serverless；ScyllaDB Cloud",
         "b": "- DataStax Astra：Serverless 按量 `厂商口径`。\n- ScyllaDB Cloud：托管 ScyllaDB `厂商口径`。\n- 各云也有 Keyspaces 等兼容托管 `社区共识`。"},
  "en": {"v": "Supported", "p": "Astra serverless; ScyllaDB Cloud",
         "b": "- DataStax Astra: serverless pay-per-use `(vendor claim)`.\n- ScyllaDB Cloud: managed ScyllaDB `(vendor claim)`.\n- Compatible managed options on clouds (e.g. Keyspaces) `(community consensus)`."}}
CONTENT["dynamodb"]["managed"] = {
  "zh": {"v": "有", "p": "纯 Serverless，无自建版",
         "b": "- DynamoDB 本身就是 Serverless：无服务器概念，按需/预置 `官方文档`。\n- 无自建版；本地开发用 DynamoDB Local（功能子集）`官方文档`。\n- AWS 绑定 `社区共识`。"},
  "en": {"v": "Supported", "p": "pure serverless; no self-hosted edition",
         "b": "- DynamoDB is itself serverless: no servers, on-demand/provisioned `(official docs)`.\n- No self-hosted edition; DynamoDB Local (feature subset) for development `(official docs)`.\n- AWS-bound `(community consensus)`."}}
CONTENT["etcd"]["managed"] = {
  "zh": {"v": "部分支持", "p": "无官方托管；第三方/Aiven 等",
         "b": "- 无官方托管服务 `社区共识`。\n- Aiven 等第三方提供托管 etcd `社区共识`。\n- 实践中多随 Kubernetes 托管版间接使用 `社区共识`。"},
  "en": {"v": "Partially supported", "p": "no official hosting; third parties like Aiven",
         "b": "- No official managed service `(community consensus)`.\n- Third parties (e.g. Aiven) offer managed etcd `(community consensus)`.\n- In practice mostly consumed indirectly via managed Kubernetes `(community consensus)`."}}
CONTENT["clickhouse"]["managed"] = {
  "zh": {"v": "有", "p": "ClickHouse Cloud；各云也有托管",
         "b": "- ClickHouse Cloud（官方，Serverless/按量）`官方文档`。\n- 各云厂商/第三方托管版多 `社区共识`。\n- 云版与开源版能力对齐好 `社区共识`。"},
  "en": {"v": "Supported", "p": "ClickHouse Cloud; hosted on clouds too",
         "b": "- ClickHouse Cloud (official, serverless/pay-per-use) `(official docs)`.\n- Many cloud/third-party managed editions `(community consensus)`.\n- Cloud and open-source editions well aligned `(community consensus)`."}}
CONTENT["doris"]["managed"] = {
  "zh": {"v": "有", "p": "SelectDB Cloud",
         "b": "- SelectDB Cloud（官方云服务）`厂商口径`。\n- 阿里云/腾讯云等也有 Doris 托管/Serverless 形态 `厂商口径`。\n- 开源自建仍是主流形态之一 `社区共识`。"},
  "en": {"v": "Supported", "p": "SelectDB Cloud",
         "b": "- SelectDB Cloud (official cloud service) `(vendor claim)`.\n- Alibaba/Tencent clouds also offer managed/serverless Doris `(vendor claim)`.\n- Self-hosted open source remains a mainstream form `(community consensus)`."}}
CONTENT["starrocks"]["managed"] = {
  "zh": {"v": "有", "p": "CelerData Cloud（Serverless）",
         "b": "- CelerData Cloud：Serverless 按量 `厂商口径`。\n- 阿里云 EMR-StarRocks 等云集成 `厂商口径`。\n- 开源自建仍是主流 `社区共识`。"},
  "en": {"v": "Supported", "p": "CelerData Cloud (serverless)",
         "b": "- CelerData Cloud: serverless pay-per-use `(vendor claim)`.\n- Cloud integrations like Alibaba EMR-StarRocks `(vendor claim)`.\n- Self-hosted open source remains mainstream `(community consensus)`."}}
CONTENT["duckdb"]["managed"] = {
  "zh": {"v": "有", "p": "MotherDuck（Serverless 云）",
         "b": "- MotherDuck：DuckDB 的 Serverless 云服务，共享/协作 `官方文档`。\n- 嵌入式本质不变：云是可选增强，不是必需 `社区共识`。"},
  "en": {"v": "Supported", "p": "MotherDuck (serverless cloud)",
         "b": "- MotherDuck: serverless cloud for DuckDB with sharing/collaboration `(official docs)`.\n- Embedded nature unchanged: cloud is an optional enhancement, not a requirement `(community consensus)`."}}
CONTENT["milvus"]["managed"] = {
  "zh": {"v": "有", "p": "Zilliz Cloud（Serverless）",
         "b": "- Zilliz Cloud：Serverless/专属集群 `官方文档`。\n- 按量计费，免运维是主要卖点 `厂商口径`。\n- 开源自建（k8s operator）仍是主流之一 `社区共识`。"},
  "en": {"v": "Supported", "p": "Zilliz Cloud (serverless)",
         "b": "- Zilliz Cloud: serverless / dedicated clusters `(official docs)`.\n- Pay-per-use with no-ops as the selling point `(vendor claim)`.\n- Self-hosted open source (k8s operator) remains mainstream `(community consensus)`."}}
CONTENT["weaviate"]["managed"] = {
  "zh": {"v": "有", "p": "Weaviate Cloud（Serverless）",
         "b": "- Weaviate Cloud：Serverless 按量 `官方文档`。\n- 开源自建（Docker/k8s）文档完整 `官方文档`。"},
  "en": {"v": "Supported", "p": "Weaviate Cloud (serverless)",
         "b": "- Weaviate Cloud: serverless pay-per-use `(official docs)`.\n- Self-hosted open source (Docker/k8s) well documented `(official docs)`."}}
CONTENT["qdrant"]["managed"] = {
  "zh": {"v": "有", "p": "Qdrant Cloud",
         "b": "- Qdrant Cloud：官方托管（Cloud/Edge/私有云）`官方文档`。\n- 开源版单二进制自建极简 `社区共识`。"},
  "en": {"v": "Supported", "p": "Qdrant Cloud",
         "b": "- Qdrant Cloud: official hosting (Cloud/Edge/private cloud) `(official docs)`.\n- Open-source single-binary self-hosting is minimal-effort `(community consensus)`."}}
CONTENT["sqlserver"]["managed"] = {
  "zh": {"v": "有", "p": "Azure SQL（Managed Instance/Serverless）；RDS",
         "b": "- Azure SQL Database（Serverless 按量）/ Managed Instance `官方文档`。\n- AWS RDS for SQL Server `厂商口径`。\n- 本地版许可模式与云差异大，注意对准 `社区共识`。"},
  "en": {"v": "Supported", "p": "Azure SQL (Managed Instance/serverless); RDS",
         "b": "- Azure SQL Database (serverless pay-per-use) / Managed Instance `(official docs)`.\n- AWS RDS for SQL Server `(vendor claim)`.\n- On-premises licensing differs greatly from cloud — align carefully `(community consensus)`."}}
