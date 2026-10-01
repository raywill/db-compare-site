# -*- coding: utf-8 -*-
"""3 个新增数据集成维度的数据：ingest / extdata / cdc.
CONTENT2[slug][dimkey] = {"zh": {"v","p","b"}, "en": {"v","p","b"}}
v = verdict（有/部分支持/无/不适用/未找到证据；Supported/...），p = 短语，b = markdown 正文。
正文沿用档案体例：`- ` 条目 + 反引号证据徽章（`官方文档`/`厂商口径`/`社区实测`/`社区共识`/`待验证`）。
"""

NEW_DIMS2 = [
    {"key": "ingest", "zh": "数据接入与摄入", "en": "Data ingestion",
     "keys": ["数据接入", "数据摄入", "Ingestion", "ingestion", "接入"]},
    {"key": "extdata", "zh": "外部数据访问", "en": "External data access",
     "keys": ["外部数据", "External data", "联邦查询", "外部表"]},
    {"key": "cdc", "zh": "CDC 与下游同步", "en": "CDC & downstream",
     "keys": ["CDC", "cdc", "下游同步", "Downstream", "downstream"]},
]

CONTENT2 = {}
# ---------------- 维度1：数据接入与摄入 ----------------
CONTENT2["alloydb"] = {"ingest": {
  "zh": {"v": "有", "p": "COPY/pg_dump/DMS；与 PG 工具链兼容",
         "b": "- 批量：COPY、pg_dump/pg_restore、pgloader 等 PG 原生工具直接可用 `官方文档`。\n- 迁移：Database Migration Service（DMS）支持从自建/云 PG 在线迁移 `官方文档`。\n- 超大库迁移建议分片并行，DMS 吞吐取决于实例规格 `社区共识`。"},
  "en": {"v": "Supported", "p": "COPY/pg_dump/DMS; PG toolchain compatible",
         "b": "- Bulk: COPY, pg_dump/pg_restore, pgloader and other native PG tools work directly `(official docs)`.\n- Migration: Database Migration Service (DMS) supports online migration from self-hosted/cloud PG `(official docs)`.\n- Very large databases should be migrated in sharded/parallel fashion; DMS throughput depends on instance size `(community consensus)`."}}}
CONTENT2["aurora"] = {"ingest": {
  "zh": {"v": "有", "p": "S3 直导（LOAD DATA FROM S3/aws_s3）；DMS",
         "b": "- Aurora MySQL：LOAD DATA FROM S3 并行导入；Aurora PG：aws_s3 扩展从 S3 导入/导出 `官方文档`。\n- DMS 支持同构/异构迁移与持续复制 `官方文档`。\n- 跨区/跨账号 S3 导入注意 IAM 权限与网络 `社区共识`。"},
  "en": {"v": "Supported", "p": "Direct S3 load (LOAD DATA FROM S3/aws_s3); DMS",
         "b": "- Aurora MySQL: parallel LOAD DATA FROM S3; Aurora PG: aws_s3 extension for S3 import/export `(official docs)`.\n- DMS supports homogeneous/heterogeneous migration and ongoing replication `(official docs)`.\n- Cross-region/cross-account S3 loads need IAM and network care `(community consensus)`."}}}
CONTENT2["cassandra-scylladb"] = {"ingest": {
  "zh": {"v": "有", "p": "DSBulk/sstableloader；cqlsh COPY 只适合小数据",
         "b": "- DSBulk（DataStax Bulk Loader）是生产级批量导入/导出工具 `官方文档`。\n- sstableloader 可直接加载 SSTable（ScyllaDB 同理）`官方文档`。\n- cqlsh COPY 单线程慢只适合小表；大宽行注意超时 `社区共识`。"},
  "en": {"v": "Supported", "p": "DSBulk/sstableloader; cqlsh COPY for small data only",
         "b": "- DSBulk (DataStax Bulk Loader) is the production-grade bulk import/export tool `(official docs)`.\n- sstableloader can load SSTables directly (same for ScyllaDB) `(official docs)`.\n- cqlsh COPY is single-threaded and slow, small tables only; watch timeouts on wide rows `(community consensus)`."}}}
CONTENT2["clickhouse"] = {"ingest": {
  "zh": {"v": "有", "p": "批量 INSERT/Kafka 引擎/S3 表函数，摄入是强项",
         "b": "- 批量：clickhouse-client/HTTP 批量 INSERT；支持 CSV/Parquet/JSONEachRow 等格式 `官方文档`。\n- 流式：Kafka 表引擎直连消费；S3/s3Cluster 表函数直接读对象存储 `官方文档`。\n- 大批量写入注意 parts 合并压力，分批与异步插入调优是常规操作 `社区共识`。"},
  "en": {"v": "Supported", "p": "Batch INSERT/Kafka engine/S3 table function; ingestion is a strength",
         "b": "- Batch: clickhouse-client/HTTP batch INSERT; formats include CSV/Parquet/JSONEachRow `(official docs)`.\n- Streaming: Kafka table engine consumes directly; S3/s3Cluster table functions read object storage `(official docs)`.\n- Heavy writes stress part merges — batching and async-insert tuning are routine `(community consensus)`."}}}
CONTENT2["cockroachdb"] = {"ingest": {
  "zh": {"v": "有", "p": "IMPORT（CSV/Parquet/Avro）；PG COPY 兼容",
         "b": "- IMPORT FROM 可从 S3/GCS/HTTP 批量导入 CSV/Parquet/Avro `官方文档`。\n- PG 协议兼容，COPY、pg_dump/pg_restore 可用 `官方文档`。\n- 大表 IMPORT 注意拆分与超时，并行度需实测 `社区共识`。"},
  "en": {"v": "Supported", "p": "IMPORT (CSV/Parquet/Avro); PG COPY compatible",
         "b": "- IMPORT FROM bulk-loads CSV/Parquet/Avro from S3/GCS/HTTP `(official docs)`.\n- PG-protocol compatible: COPY, pg_dump/pg_restore work `(official docs)`.\n- Split large IMPORTs and watch timeouts; parallelism needs real testing `(community consensus)`."}}}
CONTENT2["doris"] = {"ingest": {
  "zh": {"v": "有", "p": "Stream/Broker/Routine/Spark Load 四件套",
         "b": "- Stream Load（HTTP 推）、Broker Load（HDFS/S3 拉）、Routine Load（Kafka 常驻）、Spark Load（大批量）`官方文档`。\n- Flink Doris Connector / Doris Stream Loader 生态成熟 `社区共识`。\n- 选型看数据量与实时性：Routine Load 适合常驻流，Broker 适合离线大文件 `社区共识`。"},
  "en": {"v": "Supported", "p": "Stream/Broker/Routine/Spark Load quartet",
         "b": "- Stream Load (HTTP push), Broker Load (HDFS/S3 pull), Routine Load (persistent Kafka), Spark Load (huge batches) `(official docs)`.\n- Flink Doris Connector / Doris Stream Loader ecosystem is mature `(community consensus)`.\n- Pick by volume and latency: Routine Load for persistent streams, Broker Load for offline large files `(community consensus)`."}}}
CONTENT2["duckdb"] = {"ingest": {
  "zh": {"v": "有", "p": "COPY FROM/Parquet 直读，单机摄入极简",
         "b": "- COPY FROM 支持 CSV/Parquet/JSON；read_parquet/read_csv 可直接查文件不导入 `官方文档`。\n- 批量 INSERT 也快，单机分析场景摄入几乎零运维 `社区共识`。\n- 大文件注意内存与临时目录，可用流式读 `社区共识`。"},
  "en": {"v": "Supported", "p": "COPY FROM/direct Parquet reads; trivial single-node ingest",
         "b": "- COPY FROM supports CSV/Parquet/JSON; read_parquet/read_csv query files without importing `(official docs)`.\n- Batch INSERT is fast too; near-zero-ops ingestion for single-node analytics `(community consensus)`.\n- Large files need memory/temp-dir care; streaming reads available `(community consensus)`."}}}
CONTENT2["dynamodb"] = {"ingest": {
  "zh": {"v": "有", "p": "S3 导入、BatchWriteItem、zero-ETL",
         "b": "- Import from S3（CSV/DynamoDB JSON/ION）是官方批量导入通道 `官方文档`。\n- BatchWriteItem + 并行是 SDK 侧常规做法，注意 WCU 与限流 `社区共识`。\n- DynamoDB zero-ETL 集成到 Redshift 是新通道 `官方文档`。"},
  "en": {"v": "Supported", "p": "S3 import, BatchWriteItem, zero-ETL",
         "b": "- Import from S3 (CSV/DynamoDB JSON/ION) is the official bulk channel `(official docs)`.\n- BatchWriteItem with parallelism is the standard SDK approach; watch WCU and throttling `(community consensus)`.\n- DynamoDB zero-ETL integration to Redshift is a newer channel `(official docs)`."}}}
CONTENT2["edb"] = {"ingest": {
  "zh": {"v": "有", "p": "PG 工具链全兼容；Migration Toolkit",
         "b": "- COPY、pg_dump/pg_restore、pgloader 等 PG 工具直接可用 `官方文档`。\n- EDB Migration Toolkit 支持 Oracle→EDB 迁移 `官方文档`。\n- 大对象/分区表迁移注意并行度 `社区共识`。"},
  "en": {"v": "Supported", "p": "Full PG toolchain; Migration Toolkit",
         "b": "- COPY, pg_dump/pg_restore, pgloader and other PG tools work directly `(official docs)`.\n- EDB Migration Toolkit supports Oracle-to-EDB migration `(official docs)`.\n- Watch parallelism for large objects/partitioned tables `(community consensus)`."}}}
CONTENT2["etcd"] = {"ingest": {
  "zh": {"v": "不适用", "p": "KV 元数据存储，无批量数据摄入语义",
         "b": "- etcd 存配置/元数据 KV，不是数据平台，无批量导入工具 `官方文档`。\n- 数据恢复靠 snapshot restore，不是摄入通道 `官方文档`。"},
  "en": {"v": "N/A", "p": "KV metadata store; no bulk ingest semantics",
         "b": "- etcd stores config/metadata KVs, not a data platform; no bulk import tooling `(official docs)`.\n- Recovery is via snapshot restore, not an ingest channel `(official docs)`."}}}
CONTENT2["mariadb"] = {"ingest": {
  "zh": {"v": "有", "p": "LOAD DATA/mariadb-import；mydumper",
         "b": "- LOAD DATA INFILE、mariadb-import（mysqlimport 对应）`官方文档`。\n- mydumper/myloader 并行逻辑导入导出，社区主流 `社区共识`。\n- ColumnStore 有 cpimport 专用批量导入 `官方文档`。"},
  "en": {"v": "Supported", "p": "LOAD DATA/mariadb-import; mydumper",
         "b": "- LOAD DATA INFILE, mariadb-import (mysqlimport equivalent) `(official docs)`.\n- mydumper/myloader for parallel logical import/export, community mainstream `(community consensus)`.\n- ColumnStore has dedicated cpimport bulk loading `(official docs)`."}}}
CONTENT2["milvus"] = {"ingest": {
  "zh": {"v": "有", "p": "BulkInsert（对象存储上 Parquet/JSON）；SDK 批量",
         "b": "- BulkInsert：把 Parquet/JSON 文件放对象存储后触发导入，适合大批量 `官方文档`。\n- SDK 批量 insert 适合中小规模；向量维度与索引类型先定好 `官方文档`。\n- 大规模导入建议先建集合、导完再建索引 `社区共识`。"},
  "en": {"v": "Supported", "p": "BulkInsert (Parquet/JSON on object storage); SDK batch",
         "b": "- BulkInsert: stage Parquet/JSON files on object storage then trigger import, best for large batches `(official docs)`.\n- SDK batch insert for small/medium scale; fix vector dimension and index type first `(official docs)`.\n- For large imports, create the collection first and build the index after loading `(community consensus)`."}}}
CONTENT2["mongodb"] = {"ingest": {
  "zh": {"v": "有", "p": "mongoimport/mongorestore；Bulk Write API",
         "b": "- mongoimport（JSON/CSV）、mongorestore（BSON dump）是标准工具 `官方文档`。\n- Bulk Write API 适合程序化大批量写入 `官方文档`。\n- Atlas Live Migration 做在线迁移 `官方文档`。"},
  "en": {"v": "Supported", "p": "mongoimport/mongorestore; Bulk Write API",
         "b": "- mongoimport (JSON/CSV) and mongorestore (BSON dump) are the standard tools `(official docs)`.\n- Bulk Write API for programmatic high-volume writes `(official docs)`.\n- Atlas Live Migration for online migration `(official docs)`."}}}
CONTENT2["mysql"] = {"ingest": {
  "zh": {"v": "有", "p": "LOAD DATA/mysqlimport；mydumper；mysqlsh",
         "b": "- LOAD DATA INFILE、mysqlimport 是最快单机导入通道 `官方文档`。\n- mydumper/myloader 并行逻辑导入导出，社区主流 `社区共识`。\n- mysqlsh util.loadDump 支持 MySQL Shell dump 的并行加载 `官方文档`。"},
  "en": {"v": "Supported", "p": "LOAD DATA/mysqlimport; mydumper; mysqlsh",
         "b": "- LOAD DATA INFILE and mysqlimport are the fastest single-node load paths `(official docs)`.\n- mydumper/myloader for parallel logical import/export, community mainstream `(community consensus)`.\n- mysqlsh util.loadDump parallel-loads MySQL Shell dumps `(official docs)`."}}}
CONTENT2["oceanbase"] = {"ingest": {
  "zh": {"v": "有", "p": "obloader/obdumper；LOAD DATA；OMS 迁移",
         "b": "- obloader/obdumper 是官方并行导入导出工具 `官方文档`。\n- LOAD DATA 语法兼容 MySQL `官方文档`。\n- OMS（OceanBase 迁移服务）支持异构迁移与持续同步 `官方文档`。"},
  "en": {"v": "Supported", "p": "obloader/obdumper; LOAD DATA; OMS migration",
         "b": "- obloader/obdumper are the official parallel import/export tools `(official docs)`.\n- LOAD DATA syntax is MySQL-compatible `(official docs)`.\n- OMS (OceanBase Migration Service) supports heterogeneous migration and ongoing sync `(official docs)`."}}}
CONTENT2["oracle"] = {"ingest": {
  "zh": {"v": "有", "p": "SQL*Loader/Data Pump/外部表，传统强项",
         "b": "- SQL*Loader、Data Pump（impdp/expdp 并行）是标准批量通道 `官方文档`。\n- 外部表可直接读平面文件不落地 `官方文档`。\n- 大数据量导入注意 direct path 与索引维护 `社区共识`。"},
  "en": {"v": "Supported", "p": "SQL*Loader/Data Pump/external tables; traditional strength",
         "b": "- SQL*Loader and Data Pump (parallel impdp/expdp) are the standard bulk channels `(official docs)`.\n- External tables read flat files without staging `(official docs)`.\n- For huge loads, mind direct path and index maintenance `(community consensus)`."}}}
CONTENT2["polardb"] = {"ingest": {
  "zh": {"v": "有", "p": "兼容 MySQL/PG 工具链；DTS 数据传输服务",
         "b": "- MySQL 版：LOAD DATA、mydumper 等 MySQL 工具直接可用 `官方文档`。\n- PG 版：COPY、pg_dump/pg_restore 可用 `官方文档`。\n- 阿里云 DTS/数据传输服务做迁移与持续同步 `官方文档`。"},
  "en": {"v": "Supported", "p": "MySQL/PG toolchain compatible; DTS transfer service",
         "b": "- MySQL edition: LOAD DATA, mydumper and other MySQL tools work directly `(official docs)`.\n- PG edition: COPY, pg_dump/pg_restore available `(official docs)`.\n- Alibaba Cloud DTS/data-transmission service for migration and ongoing sync `(official docs)`."}}}
CONTENT2["postgresql"] = {"ingest": {
  "zh": {"v": "有", "p": "COPY 最快；pg_bulkload/pgloader",
         "b": "- COPY 是单机最快导入通道；\\copy、file_fdw 读 CSV `官方文档`。\n- pg_bulkload 并行 direct path 加载 `社区共识`。\n- pg_dump/pg_restore 逻辑迁移标准 `官方文档`。"},
  "en": {"v": "Supported", "p": "COPY is fastest; pg_bulkload/pgloader",
         "b": "- COPY is the fastest single-node load path; \\copy and file_fdw read CSV `(official docs)`.\n- pg_bulkload for parallel direct-path loading `(community consensus)`.\n- pg_dump/pg_restore is the logical-migration standard `(official docs)`."}}}
CONTENT2["qdrant"] = {"ingest": {
  "zh": {"v": "有", "p": "批量上传 API；快照恢复",
         "b": "- REST/gRPC 批量 upsert，支持 batch 接口 `官方文档`。\n- 快照（snapshot）可做备份恢复与迁移 `官方文档`。\n- 大批量注意 payload 索引先关后建 `社区共识`。"},
  "en": {"v": "Supported", "p": "Batch upload API; snapshot restore",
         "b": "- REST/gRPC batch upsert with a batch interface `(official docs)`.\n- Snapshots for backup/restore and migration `(official docs)`.\n- For large batches, disable payload indexes during load and build after `(community consensus)`."}}}
CONTENT2["redis-valkey"] = {"ingest": {
  "zh": {"v": "部分支持", "p": "无专用批量工具；靠 --pipe/RESTORE/脚本",
         "b": "- 无官方 bulk load 工具；redis-cli --pipe 协议导入是常用土法 `社区共识`。\n- RESTORE/DUMP 做单 key 迁移；RDB 可做冷导入 `官方文档`。\n- 大批量写入注意单线程阻塞，用 pipeline 拆批 `社区共识`。"},
  "en": {"v": "Partially supported", "p": "No dedicated bulk tool; --pipe/RESTORE/scripts",
         "b": "- No official bulk-load tool; redis-cli --pipe protocol import is the common workaround `(community consensus)`.\n- RESTORE/DUMP for single-key moves; RDB for cold imports `(official docs)`.\n- Large writes can block the single thread — split into pipelined batches `(community consensus)`."}}}
CONTENT2["spanner"] = {"ingest": {
  "zh": {"v": "有", "p": "Dataflow 模板；GCS Avro/CSV 导入",
         "b": "- Dataflow 模板（Avro/CSV 从 GCS）是官方批量导入通道 `官方文档`。\n- gcloud CLI 也支持导入导出 `官方文档`。\n- 大批量导入建议先升节点数再降，省时间 `社区共识`。"},
  "en": {"v": "Supported", "p": "Dataflow templates; GCS Avro/CSV import",
         "b": "- Dataflow templates (Avro/CSV from GCS) are the official bulk channel `(official docs)`.\n- gcloud CLI also supports import/export `(official docs)`.\n- Scale nodes up before a huge import and back down after to save time `(community consensus)`."}}}
CONTENT2["sqlserver"] = {"ingest": {
  "zh": {"v": "有", "p": "bcp/BULK INSERT/SSIS，传统强项",
         "b": "- bcp、BULK INSERT、SSIS 是标准批量通道 `官方文档`。\n- Azure Data Factory 做云上 ETL `官方文档`。\n- 大批量注意锁升级与日志增长 `社区共识`。"},
  "en": {"v": "Supported", "p": "bcp/BULK INSERT/SSIS; traditional strength",
         "b": "- bcp, BULK INSERT and SSIS are the standard bulk channels `(official docs)`.\n- Azure Data Factory for cloud ETL `(official docs)`.\n- Watch lock escalation and log growth on huge loads `(community consensus)`."}}}
CONTENT2["starrocks"] = {"ingest": {
  "zh": {"v": "有", "p": "Stream/Broker/Routine/Spark Load；Flink 连接器",
         "b": "- Stream Load（HTTP）、Broker Load（HDFS/S3）、Routine Load（Kafka）、Spark Load `官方文档`。\n- Flink Connector / Kafka Routine Load 是流式标准链路 `社区共识`。\n- 主键模型流式 upsert 注意内存与 compaction `社区共识`。"},
  "en": {"v": "Supported", "p": "Stream/Broker/Routine/Spark Load; Flink connector",
         "b": "- Stream Load (HTTP), Broker Load (HDFS/S3), Routine Load (Kafka), Spark Load `(official docs)`.\n- Flink Connector / Kafka Routine Load is the standard streaming path `(community consensus)`.\n- Streaming upserts on the primary-key model need memory and compaction care `(community consensus)`."}}}
CONTENT2["tdsql"] = {"ingest": {
  "zh": {"v": "有", "p": "兼容 MySQL 工具链；DTS 迁移",
         "b": "- LOAD DATA、mydumper 等 MySQL 工具可用 `官方文档`。\n- 腾讯云 DTS 做迁移与同步 `官方文档`。\n- 分片集群导入注意按 shard key 打散，避免热点 `社区共识`。"},
  "en": {"v": "Supported", "p": "MySQL toolchain compatible; DTS migration",
         "b": "- LOAD DATA, mydumper and other MySQL tools work `(official docs)`.\n- Tencent Cloud DTS for migration and sync `(official docs)`.\n- On sharded clusters, spread loads by shard key to avoid hotspots `(community consensus)`."}}}
CONTENT2["tidb"] = {"ingest": {
  "zh": {"v": "有", "p": "TiDB Lightning（物理/逻辑）；Dumpling；BR",
         "b": "- Lightning 物理导入模式（SST 直写）TB 级最快 `官方文档`。\n- Dumpling 逻辑导出；BR 做备份恢复 `官方文档`。\n- Lightning 逻辑模式兼容 mydumper 文件 `官方文档`。"},
  "en": {"v": "Supported", "p": "TiDB Lightning (physical/logical); Dumpling; BR",
         "b": "- Lightning physical-import mode (direct SST writes) is fastest at TB scale `(official docs)`.\n- Dumpling for logical export; BR for backup/restore `(official docs)`.\n- Lightning logical mode accepts mydumper-format files `(official docs)`."}}}
CONTENT2["weaviate"] = {"ingest": {
  "zh": {"v": "有", "p": "Batch 导入 API；向量化可内置",
         "b": "- batch API 批量导入对象；可配 vectorizer 自动向量化 `官方文档`。\n- 大批量注意 batch size 与超时 `社区共识`。\n- 已有向量可直接导入跳过向量化 `官方文档`。"},
  "en": {"v": "Supported", "p": "Batch import API; built-in vectorization optional",
         "b": "- batch API for bulk object import; configurable vectorizer for automatic vectorization `(official docs)`.\n- Tune batch size and timeouts for large loads `(community consensus)`.\n- Pre-computed vectors can be imported directly, skipping vectorization `(official docs)`."}}}
CONTENT2["yugabytedb"] = {"ingest": {
  "zh": {"v": "有", "p": "YSQL 用 COPY/PG 工具；yb-voyager 迁移",
         "b": "- YSQL（PG 兼容）：COPY、pg_dump/pg_restore 可用 `官方文档`。\n- 大批量用多连接并行 COPY；yb-voyager 是官方迁移工具 `官方文档`。\n- YCQL（Cassandra 兼容）：可用 cassandra-loader 类工具 `待验证`。"},
  "en": {"v": "Supported", "p": "COPY/PG tools on YSQL; yb-voyager for migration",
         "b": "- YSQL (PG-compatible): COPY, pg_dump/pg_restore work `(official docs)`.\n- Large loads via multi-connection parallel COPY; yb-voyager is the official migration tool `(official docs)`.\n- YCQL (Cassandra-compatible): cassandra-loader style tools `(to-be-verified)`."}}}
# ---------------- 维度2：外部数据访问 ----------------
CONTENT2["alloydb"]["extdata"] = {
  "zh": {"v": "部分支持", "p": "postgres_fdw 可用；BigQuery 侧可联邦查 AlloyDB",
         "b": "- AlloyDB 内：postgres_fdw 等扩展可用，受托管扩展白名单限制 `官方文档`。\n- 反向：BigQuery 可通过外部连接联邦查询 AlloyDB `官方文档`。\n- 无 S3/对象存储直查这类湖仓外部表语义 `待验证`。"},
  "en": {"v": "Partially supported", "p": "postgres_fdw available; BigQuery can federate into AlloyDB",
         "b": "- Inside AlloyDB: postgres_fdw and similar extensions available, limited by the managed extension allowlist `(official docs)`.\n- Reverse direction: BigQuery can federate queries into AlloyDB via external connections `(official docs)`.\n- No lakehouse-style external tables over S3/object storage `(to-be-verified)`."}}
CONTENT2["aurora"]["extdata"] = {
  "zh": {"v": "部分支持", "p": "PG 版有 postgres_fdw/aws_s3；无湖仓外部表",
         "b": "- Aurora PG：postgres_fdw、dblink 可用；aws_s3 可读写 S3 对象 `官方文档`。\n- Aurora MySQL：无外部表语义 `社区共识`。\n- 湖仓格式（Iceberg/Delta）直查不支持 `待验证`。"},
  "en": {"v": "Partially supported", "p": "PG edition has postgres_fdw/aws_s3; no lakehouse tables",
         "b": "- Aurora PG: postgres_fdw and dblink available; aws_s3 reads/writes S3 objects `(official docs)`.\n- Aurora MySQL: no external-table semantics `(community consensus)`.\n- Direct queries over lakehouse formats (Iceberg/Delta) not supported `(to-be-verified)`."}}
CONTENT2["cassandra-scylladb"]["extdata"] = {
  "zh": {"v": "部分支持", "p": "无外部表；靠 Spark Connector 做分析侧联邦",
         "b": "- CQL 无外部表/联邦查询语义 `社区共识`。\n- Spark Cassandra Connector 可把 C* 当数据源做离线分析 `官方文档`。\n- ScyllaDB 兼容同一套连接器 `厂商口径`。"},
  "en": {"v": "Partially supported", "p": "No external tables; Spark Connector for analytics-side federation",
         "b": "- CQL has no external-table/federated-query semantics `(community consensus)`.\n- Spark Cassandra Connector exposes C* as a data source for offline analytics `(official docs)`.\n- ScyllaDB is compatible with the same connectors `(vendor claim)`."}}
CONTENT2["clickhouse"]["extdata"] = {
  "zh": {"v": "有", "p": "S3/URL/MySQL/PG 表引擎；JDBC/ODBC 桥",
         "b": "- S3、URL、File 表函数可直接查询外部数据不落地 `官方文档`。\n- MySQL/PostgreSQL 表引擎可联邦查询外部库表 `官方文档`。\n- jdbcBridge/odbcBridge 扩展到任意 JDBC/ODBC 源 `官方文档`。"},
  "en": {"v": "Supported", "p": "S3/URL/MySQL/PG table engines; JDBC/ODBC bridge",
         "b": "- S3, URL and File table functions query external data without staging `(official docs)`.\n- MySQL/PostgreSQL table engines federate queries into external tables `(official docs)`.\n- jdbcBridge/odbcBridge extend to any JDBC/ODBC source `(official docs)`."}}
CONTENT2["cockroachdb"]["extdata"] = {
  "zh": {"v": "部分支持", "p": "IMPORT 读外部存储；无 FDW/外部表",
         "b": "- 可从外部存储 IMPORT，但那是导入不是联邦查询 `官方文档`。\n- 无 postgres_fdw 等外部表机制 `社区共识`。\n- 跨库查询需求一般在应用层或用 CDC 同步后解决 `社区共识`。"},
  "en": {"v": "Partially supported", "p": "IMPORT reads external storage; no FDW/external tables",
         "b": "- Can IMPORT from external storage, but that is ingestion, not federated querying `(official docs)`.\n- No postgres_fdw-style external table mechanism `(community consensus)`.\n- Cross-database queries are typically solved in the app layer or via CDC sync `(community consensus)`."}}
CONTENT2["doris"]["extdata"] = {
  "zh": {"v": "有", "p": "Multi-Catalog：Hive/Iceberg/Hudi/JDBC/ES",
         "b": "- Multi-Catalog 可直查 Hive/Iceberg/Hudi/Delta Lake、Elasticsearch、JDBC 源 `官方文档`。\n- 外表查询可下推谓词，湖仓一体是主打场景 `厂商口径`。\n- 外表性能弱于内表，大查询建议先导入 `社区共识`。"},
  "en": {"v": "Supported", "p": "Multi-Catalog: Hive/Iceberg/Hudi/JDBC/ES",
         "b": "- Multi-Catalog queries Hive/Iceberg/Hudi/Delta Lake, Elasticsearch and JDBC sources directly `(official docs)`.\n- Predicate pushdown on external tables; lakehouse is the flagship scenario `(vendor claim)`.\n- External tables are slower than internal ones — import first for heavy queries `(community consensus)`."}}
CONTENT2["duckdb"]["extdata"] = {
  "zh": {"v": "有", "p": "httpfs 直查对象存储；PG/MySQL scanner 扩展",
         "b": "- httpfs 扩展可直接查询 S3/HTTP 上的 Parquet/CSV `官方文档`。\n- postgres/mysql 扩展可把外部库表当本地表扫描 `官方文档`。\n- 嵌入式场景下这是它最被低估的能力之一 `社区共识`。"},
  "en": {"v": "Supported", "p": "httpfs over object storage; PG/MySQL scanner extensions",
         "b": "- httpfs extension queries Parquet/CSV on S3/HTTP directly `(official docs)`.\n- postgres/mysql extensions scan external tables as local ones `(official docs)`.\n- One of its most underrated capabilities in embedded scenarios `(community consensus)`."}}
CONTENT2["dynamodb"]["extdata"] = {
  "zh": {"v": "部分支持", "p": "自身无外部表；Athena 可联邦查 DynamoDB",
         "b": "- DynamoDB 无外部表语义 `官方文档`。\n- Athena DynamoDB 连接器可做联邦查询 `官方文档`。\n- PartiQL 只能查本表，跨源要在上层做 `社区共识`。"},
  "en": {"v": "Partially supported", "p": "No external tables natively; Athena can federate into DynamoDB",
         "b": "- DynamoDB has no external-table semantics `(official docs)`.\n- The Athena DynamoDB connector enables federated queries `(official docs)`.\n- PartiQL only queries local tables; cross-source joins happen upstream `(community consensus)`."}}
CONTENT2["edb"]["extdata"] = {
  "zh": {"v": "有", "p": "postgres_fdw/mongo_fdw；EDB 扩展的 FDW 生态",
         "b": "- PG 原生 FDW（postgres_fdw/file_fdw/dblink）全可用 `官方文档`。\n- EDB 提供/维护 mongo_fdw 等扩展，可联邦查询 MongoDB `官方文档`。\n- 异构 FDW 下推能力看具体扩展实现 `社区共识`。"},
  "en": {"v": "Supported", "p": "postgres_fdw/mongo_fdw; EDB-extended FDW ecosystem",
         "b": "- Native PG FDWs (postgres_fdw/file_fdw/dblink) all available `(official docs)`.\n- EDB ships/maintains mongo_fdw and others for federating into MongoDB `(official docs)`.\n- Pushdown capability on heterogeneous FDWs depends on the extension `(community consensus)`."}}
CONTENT2["etcd"]["extdata"] = {
  "zh": {"v": "不适用", "p": "无查询引擎，无外部数据访问概念",
         "b": "- KV API 只读写自身数据，无联邦查询/外部表 `官方文档`。"},
  "en": {"v": "N/A", "p": "No query engine; no external-data concept",
         "b": "- The KV API only reads/writes its own data; no federated queries or external tables `(official docs)`."}}
CONTENT2["mariadb"]["extdata"] = {
  "zh": {"v": "有", "p": "CONNECT 引擎查 CSV/ODBC；Spider 做分片联邦",
         "b": "- CONNECT 存储引擎可把 CSV/XML/ODBC/JSON 等当表查询，是特色能力 `官方文档`。\n- Spider 引擎可做分片与跨节点联邦查询 `官方文档`。\n- FEDERATED 引擎也可用但功能较弱 `社区共识`。"},
  "en": {"v": "Supported", "p": "CONNECT engine over CSV/ODBC; Spider for sharded federation",
         "b": "- The CONNECT storage engine queries CSV/XML/ODBC/JSON as tables — a signature feature `(official docs)`.\n- The Spider engine handles sharding and cross-node federated queries `(official docs)`.\n- The FEDERATED engine exists but is weak `(community consensus)`."}}
CONTENT2["milvus"]["extdata"] = {
  "zh": {"v": "不适用", "p": "向量库无外部表/联邦查询语义",
         "b": "- 无外部数据访问概念，数据必须先入 Milvus `官方文档`。\n- 多模态/结构化过滤靠标量字段，不是联邦查询 `社区共识`。"},
  "en": {"v": "N/A", "p": "Vector DB; no external-table/federation semantics",
         "b": "- No external-data-access concept; data must live in Milvus first `(official docs)`.\n- Multimodal/structured filtering uses scalar fields, not federated queries `(community consensus)`."}}
CONTENT2["mongodb"]["extdata"] = {
  "zh": {"v": "部分支持", "p": "Atlas Data Federation 查 S3；无通用外部表",
         "b": "- Atlas Data Federation 可查询 S3 上的数据（与 Atlas 集群联邦）`官方文档`。\n- 自建版无外部表语义；$lookup 只支持本库集合 `官方文档`。\n- BI Connector 把 MongoDB 暴露成 SQL 源是反向能力 `社区共识`。"},
  "en": {"v": "Partially supported", "p": "Atlas Data Federation over S3; no generic external tables",
         "b": "- Atlas Data Federation queries data on S3 (federated with Atlas clusters) `(official docs)`.\n- Self-hosted has no external-table semantics; $lookup only joins collections in the same DB `(official docs)`.\n- The BI Connector exposing MongoDB as a SQL source is the reverse direction `(community consensus)`."}}
CONTENT2["mysql"]["extdata"] = {
  "zh": {"v": "部分支持", "p": "FEDERATED 引擎功能弱；无现代外部表",
         "b": "- FEDERATED 引擎可映射远端 MySQL 表，但功能/性能弱，生产少用 `社区共识`。\n- 无 S3/对象存储直查、湖仓格式支持 `官方文档`。\n- MySQL HeatWave 侧有对象存储查询，是商业版能力 `厂商口径`。"},
  "en": {"v": "Partially supported", "p": "FEDERATED engine is weak; no modern external tables",
         "b": "- The FEDERATED engine maps remote MySQL tables but is weak in features/performance, rarely used in prod `(community consensus)`.\n- No direct S3/object-storage or lakehouse-format querying `(official docs)`.\n- MySQL HeatWave offers object-storage queries as a commercial capability `(vendor claim)`."}}
CONTENT2["oceanbase"]["extdata"] = {
  "zh": {"v": "部分支持", "p": "DBLink 查 Oracle/MySQL；外部表能力有限",
         "b": "- DBLink 可联邦查询 Oracle/MySQL（Oracle 租户）`官方文档`。\n- 外部表/对象存储直查能力弱于 ClickHouse/Doris 系 `待验证`。\n- 跨租户查询受限 `社区共识`。"},
  "en": {"v": "Partially supported", "p": "DBLink into Oracle/MySQL; limited external tables",
         "b": "- DBLink federates into Oracle/MySQL (Oracle tenant) `(official docs)`.\n- External-table/object-storage querying is weaker than the ClickHouse/Doris family `(to-be-verified)`.\n- Cross-tenant queries are restricted `(community consensus)`."}}
CONTENT2["oracle"]["extdata"] = {
  "zh": {"v": "有", "p": "外部表+DB Link+异构服务，联邦查询老牌",
         "b": "- DB Link 做 Oracle 间联邦查询；Heterogeneous Services 连非 Oracle 源 `官方文档`。\n- 外部表支持平面文件直查 `官方文档`。\n- Big Data SQL 曾主打 Hadoop 联邦，现为 Oracle Big Data Service 能力 `厂商口径`。"},
  "en": {"v": "Supported", "p": "External tables + DB links + heterogeneous services; federation veteran",
         "b": "- DB links federate across Oracle instances; Heterogeneous Services reach non-Oracle sources `(official docs)`.\n- External tables query flat files directly `(official docs)`.\n- Big Data SQL once targeted Hadoop federation, now an Oracle Big Data Service capability `(vendor claim)`."}}
CONTENT2["polardb"]["extdata"] = {
  "zh": {"v": "部分支持", "p": "PG 版有 postgres_fdw；MySQL 版无外部表",
         "b": "- PolarDB-PG：postgres_fdw、dblink 可用（受扩展白名单限制）`官方文档`。\n- PolarDB-MySQL：无外部表语义 `社区共识`。\n- 跨库查询多在应用层或 DTS 同步后解决 `社区共识`。"},
  "en": {"v": "Partially supported", "p": "PG edition has postgres_fdw; MySQL edition has none",
         "b": "- PolarDB-PG: postgres_fdw and dblink available (extension allowlist applies) `(official docs)`.\n- PolarDB-MySQL: no external-table semantics `(community consensus)`.\n- Cross-database queries are usually solved in the app layer or after DTS sync `(community consensus)`."}}
CONTENT2["postgresql"]["extdata"] = {
  "zh": {"v": "有", "p": "FDW 生态最强：postgres_fdw/file_fdw/dblink",
         "b": "- postgres_fdw 可联邦查询远端 PG，下推谓词 `官方文档`。\n- file_fdw 读 CSV；dblink 做临时的跨库查询 `官方文档`。\n- 社区 FDW（mysql_fdw、odbc_fdw 等）覆盖主流源 `社区共识`。"},
  "en": {"v": "Supported", "p": "Strongest FDW ecosystem: postgres_fdw/file_fdw/dblink",
         "b": "- postgres_fdw federates into remote PG with predicate pushdown `(official docs)`.\n- file_fdw reads CSV; dblink for ad-hoc cross-database queries `(official docs)`.\n- Community FDWs (mysql_fdw, odbc_fdw, etc.) cover mainstream sources `(community consensus)`."}}
CONTENT2["qdrant"]["extdata"] = {
  "zh": {"v": "不适用", "p": "向量库无外部表/联邦查询语义",
         "b": "- 无外部数据访问概念 `官方文档`。"},
  "en": {"v": "N/A", "p": "Vector DB; no external-table/federation semantics",
         "b": "- No external-data-access concept `(official docs)`."}}
CONTENT2["redis-valkey"]["extdata"] = {
  "zh": {"v": "无", "p": "无外部表/联邦查询",
         "b": "- OSS 无外部数据访问语义 `官方文档`。\n- RedisGears 可写脚本调外部，但那是计算不是查询联邦 `待验证`。"},
  "en": {"v": "Not supported", "p": "No external tables/federated queries",
         "b": "- OSS has no external-data-access semantics `(official docs)`.\n- RedisGears scripts can call out, but that is compute, not query federation `(to-be-verified)`."}}
CONTENT2["spanner"]["extdata"] = {
  "zh": {"v": "部分支持", "p": "自身无外部表；BigQuery 可联邦查 Spanner",
         "b": "- Spanner 无外部表语义 `官方文档`。\n- BigQuery 外部连接可联邦查询 Spanner（反向）`官方文档`。\n- 跨源分析一般走 BigQuery 联邦或导出到 GCS `社区共识`。"},
  "en": {"v": "Partially supported", "p": "No external tables natively; BigQuery can federate into Spanner",
         "b": "- Spanner has no external-table semantics `(official docs)`.\n- BigQuery external connections can federate into Spanner (reverse direction) `(official docs)`.\n- Cross-source analytics typically goes through BigQuery federation or GCS export `(community consensus)`."}}
CONTENT2["sqlserver"]["extdata"] = {
  "zh": {"v": "有", "p": "PolyBase 外部表；Linked Server",
         "b": "- PolyBase 可建外部表查 Hadoop/S3/Oracle/MongoDB 等 `官方文档`。\n- Linked Server 做实例间联邦查询（老但好用）`社区共识`。\n- OPENROWSET 做临时的外部文件查询 `官方文档`。"},
  "en": {"v": "Supported", "p": "PolyBase external tables; Linked Servers",
         "b": "- PolyBase external tables query Hadoop/S3/Oracle/MongoDB and more `(official docs)`.\n- Linked Servers for inter-instance federation (old but effective) `(community consensus)`.\n- OPENROWSET for ad-hoc external file queries `(official docs)`."}}
CONTENT2["starrocks"]["extdata"] = {
  "zh": {"v": "有", "p": "External Catalog：Hive/Iceberg/Hudi/Delta/JDBC/ES",
         "b": "- External Catalog 直查 Hive/Iceberg/Hudi/Delta Lake/JDBC/ES `官方文档`。\n- 物化视图可基于外表加速，湖仓一体主打 `厂商口径`。\n- 外表查询性能弱于内表，谓词下推是关键 `社区共识`。"},
  "en": {"v": "Supported", "p": "External Catalog: Hive/Iceberg/Hudi/Delta/JDBC/ES",
         "b": "- External Catalog queries Hive/Iceberg/Hudi/Delta Lake/JDBC/ES directly `(official docs)`.\n- Materialized views can accelerate external tables; lakehouse is the flagship pitch `(vendor claim)`.\n- External tables are slower than internal ones — predicate pushdown is key `(community consensus)`."}}
CONTENT2["tdsql"]["extdata"] = {
  "zh": {"v": "部分支持", "p": "MySQL 版无外部表；PG 版有 FDW",
         "b": "- TDSQL-MySQL 无外部表语义 `社区共识`。\n- TDSQL-PG（基于 PG）可用 postgres_fdw `待验证`。"},
  "en": {"v": "Partially supported", "p": "MySQL edition: none; PG edition has FDW",
         "b": "- TDSQL-MySQL: no external-table semantics `(community consensus)`.\n- TDSQL-PG (PG-based) can use postgres_fdw `(to-be-verified)`."}}
CONTENT2["tidb"]["extdata"] = {
  "zh": {"v": "部分支持", "p": "Lightning 可从 S3/Parquet 导入；无联邦查询",
         "b": "- Lightning 支持从 S3/GCS 读 Parquet/CSV 导入 `官方文档`。\n- 无外部表/FDW 语义，跨源查询要先入 TiDB `社区共识`。\n- 实时联邦场景一般用 Doris/StarRocks 外表代替 `社区共识`。"},
  "en": {"v": "Partially supported", "p": "Lightning imports from S3/Parquet; no federated queries",
         "b": "- Lightning imports Parquet/CSV from S3/GCS `(official docs)`.\n- No external-table/FDW semantics; cross-source queries must land in TiDB first `(community consensus)`.\n- Real-time federation scenarios usually use Doris/StarRocks external tables instead `(community consensus)`."}}
CONTENT2["weaviate"]["extdata"] = {
  "zh": {"v": "不适用", "p": "无外部表/联邦查询语义",
         "b": "- 无外部数据访问概念 `官方文档`。"},
  "en": {"v": "N/A", "p": "No external-table/federation semantics",
         "b": "- No external-data-access concept `(official docs)`."}}
CONTENT2["yugabytedb"]["extdata"] = {
  "zh": {"v": "部分支持", "p": "YSQL 有 postgres_fdw；YCQL 无",
         "b": "- YSQL（PG 兼容）可用 postgres_fdw `官方文档`。\n- YCQL（Cassandra 兼容）无外部表 `社区共识`。"},
  "en": {"v": "Partially supported", "p": "postgres_fdw on YSQL; none on YCQL",
         "b": "- YSQL (PG-compatible) supports postgres_fdw `(official docs)`.\n- YCQL (Cassandra-compatible) has no external tables `(community consensus)`."}}
# ---------------- 维度3：CDC 与下游同步 ----------------
CONTENT2["alloydb"]["cdc"] = {
  "zh": {"v": "有", "p": "逻辑复制（pgoutput）；Datastream/Debezium",
         "b": "- 支持 PG 逻辑复制，可建 publication + replication slot `官方文档`。\n- 下游：Datastream for BigQuery、Debezium 均可消费 `官方文档`。\n- 大事务/高频更新下 slot 堆积会涨存储，需监控 `社区共识`。"},
  "en": {"v": "Supported", "p": "Logical replication (pgoutput); Datastream/Debezium",
         "b": "- Supports PG logical replication with publications and replication slots `(official docs)`.\n- Downstream: Datastream for BigQuery and Debezium both work `(official docs)`.\n- Heavy transactions/frequent updates can bloat slot storage — monitor it `(community consensus)`."}}
CONTENT2["aurora"]["cdc"] = {
  "zh": {"v": "有", "p": "binlog/逻辑复制；DMS、Debezium",
         "b": "- Aurora MySQL 开 binlog；Aurora PG 开逻辑复制，均可对接 Debezium `官方文档`。\n- DMS 做持续复制到下游 `官方文档`。\n- 只读副本延迟与主库 binlog 保留期是常见坑 `社区共识`。"},
  "en": {"v": "Supported", "p": "binlog/logical replication; DMS, Debezium",
         "b": "- Aurora MySQL with binlog, Aurora PG with logical replication — both feed Debezium `(official docs)`.\n- DMS for ongoing replication downstream `(official docs)`.\n- Replica lag and primary binlog retention are the usual pitfalls `(community consensus)`."}}
CONTENT2["cassandra-scylladb"]["cdc"] = {
  "zh": {"v": "有", "p": "Scylla CDC 日志表；C* 4.0+ CDC；Debezium",
         "b": "- ScyllaDB：按表开启 CDC，变更写入专用日志表供消费 `官方文档`。\n- Cassandra 4.0+：cdc_enabled 提交日志式 CDC，需自行消费 `官方文档`。\n- Debezium 有 Cassandra/Scylla 连接器（社区成熟度不一）`社区共识`。"},
  "en": {"v": "Supported", "p": "Scylla CDC log tables; C* 4.0+ CDC; Debezium",
         "b": "- ScyllaDB: per-table CDC writes changes to dedicated log tables for consumption `(official docs)`.\n- Cassandra 4.0+: commitlog-based CDC via cdc_enabled, self-consumed `(official docs)`.\n- Debezium has Cassandra/Scylla connectors (community maturity varies) `(community consensus)`."}}
CONTENT2["clickhouse"]["cdc"] = {
  "zh": {"v": "部分支持", "p": "无原生 CDC 输出；靠物化视图+Kafka 引擎外发",
         "b": "- ClickHouse 不记录行级变更日志，无官方 CDC 输出 `社区共识`。\n- 常见做法：物化视图 + Kafka 表引擎把结果推下游 `社区实测`。\n- 上游变更一般靠 Debezium→Kafka→Kafka 引擎链路解决 `社区共识`。"},
  "en": {"v": "Partially supported", "p": "No native CDC output; materialized views + Kafka engine",
         "b": "- ClickHouse keeps no row-level change log; no official CDC output `(community consensus)`.\n- Common pattern: materialized views + Kafka table engine push results downstream `(community-tested)`.\n- Upstream changes usually arrive via Debezium → Kafka → Kafka engine `(community consensus)`."}}
CONTENT2["cockroachdb"]["cdc"] = {
  "zh": {"v": "有", "p": "CHANGEFEED 一等公民：Kafka/云存储/webhook",
         "b": "- CHANGEFEED 可把行级变更推到 Kafka、云存储（Parquet/CSV）、webhook `官方文档`。\n- 支持 Avro/JSON 信封，可做下游流处理 `官方文档`。\n- 大事务变更 feed 延迟与内存是已知调优点 `社区共识`。"},
  "en": {"v": "Supported", "p": "First-class CHANGEFEED: Kafka/cloud storage/webhook",
         "b": "- CHANGEFEED streams row changes to Kafka, cloud storage (Parquet/CSV) and webhooks `(official docs)`.\n- Avro/JSON envelopes for downstream stream processing `(official docs)`.\n- Changefeed lag and memory on huge transactions are known tuning points `(community consensus)`."}}
CONTENT2["doris"]["cdc"] = {
  "zh": {"v": "部分支持", "p": "Flink CDC 入 Doris 成熟；对外无原生 CDC",
         "b": "- 入：Flink CDC → Doris 是标准链路 `社区共识`。\n- 出：Doris 无行级变更日志，对外靠 Binlog（版本覆盖有限）或定期导出 `待验证`。\n- 常见替代：用 Routine Load 消费上游 Kafka 而不是从 Doris 抽变更 `社区共识`。"},
  "en": {"v": "Partially supported", "p": "Flink CDC into Doris is mature; no native CDC out",
         "b": "- In: Flink CDC → Doris is the standard path `(community consensus)`.\n- Out: Doris has no row-level change log; export relies on binlog (limited version coverage) or periodic dumps `(to-be-verified)`.\n- Common alternative: Routine Load consumes upstream Kafka instead of extracting changes from Doris `(community consensus)`."}}
CONTENT2["duckdb"]["cdc"] = {
  "zh": {"v": "不适用", "p": "嵌入式无服务进程，无 CDC 语义",
         "b": "- 单进程嵌入式引擎，无变更日志/复制槽概念 `官方文档`。\n- 数据同步靠重新导入文件或上层应用处理 `社区共识`。"},
  "en": {"v": "N/A", "p": "Embedded, no server process; no CDC semantics",
         "b": "- Single-process embedded engine; no change log or replication slots `(official docs)`.\n- Sync by re-importing files or handling it in the application layer `(community consensus)`."}}
CONTENT2["dynamodb"]["cdc"] = {
  "zh": {"v": "有", "p": "DynamoDB Streams：Lambda/Kinesis",
         "b": "- DynamoDB Streams 提供 24 小时变更日志，可接 Lambda/Kinesis Data Streams `官方文档`。\n- Kinesis Data Streams for DynamoDB 支持更长保留与多消费者 `官方文档`。\n- 大写入量下 Stream 分片热点与 Lambda 并发是调优点 `社区共识`。"},
  "en": {"v": "Supported", "p": "DynamoDB Streams: Lambda/Kinesis",
         "b": "- DynamoDB Streams provide a 24-hour change log feeding Lambda/Kinesis Data Streams `(official docs)`.\n- Kinesis Data Streams for DynamoDB adds longer retention and multiple consumers `(official docs)`.\n- Stream shard hotspots and Lambda concurrency matter at high write rates `(community consensus)`."}}
CONTENT2["edb"]["cdc"] = {
  "zh": {"v": "有", "p": "逻辑复制；PGD 多主靠逻辑复制；Debezium",
         "b": "- 逻辑解码 + publication/subscription 与社区 PG 一致 `官方文档`。\n- EDB Postgres Distributed（PGD）内部用逻辑复制做多主 `官方文档`。\n- Debezium 可直接消费 `社区共识`。"},
  "en": {"v": "Supported", "p": "Logical replication; PGD multi-master on it; Debezium",
         "b": "- Logical decoding + publication/subscription, same as community PG `(official docs)`.\n- EDB Postgres Distributed (PGD) uses logical replication internally for multi-master `(official docs)`.\n- Debezium consumes directly `(community consensus)`."}}
CONTENT2["etcd"]["cdc"] = {
  "zh": {"v": "部分支持", "p": "Watch API 可当变更订阅用，非标准 CDC",
         "b": "- Watch API 提供 key 前缀/范围的变更通知，可做轻量订阅 `官方文档`。\n- 无变更日志持久化、无 exactly-once 语义，不等于 CDC `社区共识`。\n- 历史版本可通过 revision 回看，但保留期有限 `官方文档`。"},
  "en": {"v": "Partially supported", "p": "Watch API as change subscription; not standard CDC",
         "b": "- The Watch API notifies on key prefix/range changes; usable as a lightweight subscription `(official docs)`.\n- No durable change log, no exactly-once semantics — not CDC `(community consensus)`.\n- Past revisions are readable via revision, with limited retention `(official docs)`."}}
CONTENT2["mariadb"]["cdc"] = {
  "zh": {"v": "有", "p": "binlog；Debezium/Maxwell/Canal",
         "b": "- binlog（row 格式）+ GTID，与 MySQL 生态工具兼容 `官方文档`。\n- Debezium、Maxwell 均可消费 `社区共识`。\n- Galera 集群下 CDC 建议从单节点取 binlog `社区共识`。"},
  "en": {"v": "Supported", "p": "binlog; Debezium/Maxwell/Canal",
         "b": "- Row-format binlog + GTID, compatible with MySQL ecosystem tools `(official docs)`.\n- Debezium and Maxwell both consume it `(community consensus)`.\n- On Galera clusters, take binlog from a single node `(community consensus)`."}}
CONTENT2["milvus"]["cdc"] = {
  "zh": {"v": "无", "p": "无变更数据捕获；同步靠客户端重导",
         "b": "- 无行级变更日志与 CDC 接口 `官方文档`。\n- 增量同步靠业务层记录后重导，或定时全量 `社区共识`。"},
  "en": {"v": "Not supported", "p": "No change data capture; sync via client re-import",
         "b": "- No row-level change log or CDC interface `(official docs)`.\n- Incremental sync means tracking changes in the app layer and re-importing, or periodic full reloads `(community consensus)`."}}
CONTENT2["mongodb"]["cdc"] = {
  "zh": {"v": "有", "p": "Change Streams 一等公民",
         "b": "- Change Streams 提供集合/库/集群级变更订阅（基于 oplog）`官方文档`。\n- 可接 Kafka（MongoDB Kafka Connector sink/source）`官方文档`。\n- 大 oplog 压力、分片集群 resume token 管理是已知坑 `社区共识`。"},
  "en": {"v": "Supported", "p": "First-class Change Streams",
         "b": "- Change Streams subscribe to collection/database/cluster changes (oplog-based) `(official docs)`.\n- Kafka via the MongoDB Kafka Connector (sink/source) `(official docs)`.\n- Oplog pressure and resume-token management on sharded clusters are known pitfalls `(community consensus)`."}}
CONTENT2["mysql"]["cdc"] = {
  "zh": {"v": "有", "p": "binlog（row）生态最成熟：Debezium/Canal/Maxwell",
         "b": "- row 格式 binlog 是事实标准 CDC 源 `官方文档`。\n- Debezium、Canal、Maxwell、Flink CDC 均成熟 `社区共识`。\n- GTID + 半同步下位点管理简单；大事务 binlog 膨胀是常见坑 `社区共识`。"},
  "en": {"v": "Supported", "p": "Row binlog has the most mature ecosystem: Debezium/Canal/Maxwell",
         "b": "- Row-format binlog is the de-facto CDC source `(official docs)`.\n- Debezium, Canal, Maxwell and Flink CDC are all mature `(community consensus)`.\n- GTID + semisync make position management easy; huge transactions bloat binlog `(community consensus)`."}}
CONTENT2["oceanbase"]["cdc"] = {
  "zh": {"v": "有", "p": "oblogproxy（binlog 兼容）；Flink CDC 连接器",
         "b": "- oblogproxy 把 clog 转成 MySQL 兼容 binlog，下游工具无感 `官方文档`。\n- Flink CDC 有 OceanBase 连接器 `官方文档`。\n- OMS 也可做持续增量同步到下游 `官方文档`。"},
  "en": {"v": "Supported", "p": "oblogproxy (binlog-compatible); Flink CDC connector",
         "b": "- oblogproxy converts clog into MySQL-compatible binlog; downstream tools work unchanged `(official docs)`.\n- Flink CDC ships an OceanBase connector `(official docs)`.\n- OMS also does ongoing incremental sync downstream `(official docs)`."}}
CONTENT2["oracle"]["cdc"] = {
  "zh": {"v": "有", "p": "GoldenGate（商业）；LogMiner/XStream",
         "b": "- GoldenGate 是官方 CDC/复制方案（单独许可）`官方文档`。\n- LogMiner 可解析 redo 做轻量 CDC；XStream 面向 OCI `官方文档`。\n- 原生 Streams 已废弃，不要再用 `官方文档`。"},
  "en": {"v": "Supported", "p": "GoldenGate (commercial); LogMiner/XStream",
         "b": "- GoldenGate is the official CDC/replication offering (separate license) `(official docs)`.\n- LogMiner parses redo for lightweight CDC; XStream targets OCI `(official docs)`.\n- Native Streams is deprecated — do not use `(official docs)`."}}
CONTENT2["polardb"]["cdc"] = {
  "zh": {"v": "有", "p": "binlog/逻辑复制兼容；DTS、Debezium",
         "b": "- MySQL 版 binlog 与社区兼容，可接 Canal/Debezium `官方文档`。\n- PG 版逻辑复制可用 `官方文档`。\n- DTS 持续同步是云上标准链路 `官方文档`。"},
  "en": {"v": "Supported", "p": "binlog/logical-replication compatible; DTS, Debezium",
         "b": "- MySQL edition binlog is community-compatible; works with Canal/Debezium `(official docs)`.\n- PG edition logical replication available `(official docs)`.\n- DTS ongoing sync is the standard cloud path `(official docs)`."}}
CONTENT2["postgresql"]["cdc"] = {
  "zh": {"v": "有", "p": "逻辑解码（pgoutput）生态最成熟",
         "b": "- 逻辑复制槽 + pgoutput，wal2json/test_decoding 可选 `官方文档`。\n- Debezium PG 连接器是事实标准 `社区共识`。\n- 大事务解码延迟、slot 堆积涨 WAL 是已知运维点 `社区共识`。"},
  "en": {"v": "Supported", "p": "Most mature logical-decoding (pgoutput) ecosystem",
         "b": "- Logical replication slots + pgoutput; wal2json/test_decoding as options `(official docs)`.\n- The Debezium PG connector is the de-facto standard `(community consensus)`.\n- Decode lag on huge transactions and WAL growth from lagging slots are known ops concerns `(community consensus)`."}}
CONTENT2["qdrant"]["cdc"] = {
  "zh": {"v": "无", "p": "无 CDC；增量靠客户端",
         "b": "- 无变更日志与 CDC 接口 `官方文档`。\n- 增量同步靠业务层维护后调用 API `社区共识`。"},
  "en": {"v": "Not supported", "p": "No CDC; incrementals via client",
         "b": "- No change log or CDC interface `(official docs)`.\n- Incremental sync means the app layer tracks changes and calls the API `(community consensus)`."}}
CONTENT2["redis-valkey"]["cdc"] = {
  "zh": {"v": "部分支持", "p": "Keyspace 通知+Stream，非标准 CDC",
         "b": "- Keyspace notifications 可订阅变更事件，但不可靠（fire-and-forget）`官方文档`。\n- Redis Streams 可当 append-only 日志自己实现变更流 `社区共识`。\n- Debezium Redis 连接器多为 sink（写入）方向，source 侧弱 `待验证`。"},
  "en": {"v": "Partially supported", "p": "Keyspace notifications + Streams; not standard CDC",
         "b": "- Keyspace notifications subscribe to change events but are unreliable (fire-and-forget) `(official docs)`.\n- Redis Streams can serve as an append-only log for a hand-rolled change feed `(community consensus)`.\n- The Debezium Redis connector is mostly a sink (write) direction; source side is weak `(to-be-verified)`."}}
CONTENT2["spanner"]["cdc"] = {
  "zh": {"v": "有", "p": "Change streams：Dataflow/Kafka",
         "b": "- Change streams 按表/库捕获变更，可接 Dataflow 再到 Kafka/BigQuery `官方文档`。\n- 支持精确一次语义的数据流处理 `官方文档`。\n- 保留期与分区拆分是设计要点 `社区共识`。"},
  "en": {"v": "Supported", "p": "Change streams: Dataflow/Kafka",
         "b": "- Change streams capture per-table/database changes, feeding Dataflow then Kafka/BigQuery `(official docs)`.\n- Exactly-once stream processing supported `(official docs)`.\n- Retention period and partition splits are key design points `(community consensus)`."}}
CONTENT2["sqlserver"]["cdc"] = {
  "zh": {"v": "有", "p": "内置 CDC 功能；Change Tracking；Debezium",
         "b": "- 内置 CDC（基于日志读取作业）+ Change Tracking 两种机制 `官方文档`。\n- Debezium SQL Server 连接器成熟 `社区共识`。\n- CDC 作业延迟与清理策略是运维点 `社区共识`。"},
  "en": {"v": "Supported", "p": "Built-in CDC; Change Tracking; Debezium",
         "b": "- Built-in CDC (log-reader jobs) plus Change Tracking `(official docs)`.\n- The Debezium SQL Server connector is mature `(community consensus)`.\n- CDC job latency and cleanup policy are ops concerns `(community consensus)`."}}
CONTENT2["starrocks"]["cdc"] = {
  "zh": {"v": "部分支持", "p": "Flink CDC 入 StarRocks 成熟；对外无原生 CDC",
         "b": "- 入：Flink CDC → StarRocks 标准 `社区共识`。\n- 出：无行级变更日志，对外靠导出或 Binlog（版本覆盖有限）`待验证`。"},
  "en": {"v": "Partially supported", "p": "Flink CDC into StarRocks is mature; no native CDC out",
         "b": "- In: Flink CDC → StarRocks is standard `(community consensus)`.\n- Out: no row-level change log; extraction relies on export or binlog (limited version coverage) `(to-be-verified)`."}}
CONTENT2["tdsql"]["cdc"] = {
  "zh": {"v": "有", "p": "binlog 兼容；DTS、Debezium/Canal",
         "b": "- binlog 与 MySQL 兼容，可接 Canal/Debezium `官方文档`。\n- DTS 持续同步是云上标准链路 `官方文档`。"},
  "en": {"v": "Supported", "p": "binlog-compatible; DTS, Debezium/Canal",
         "b": "- MySQL-compatible binlog works with Canal/Debezium `(official docs)`.\n- DTS ongoing sync is the standard cloud path `(official docs)`."}}
CONTENT2["tidb"]["cdc"] = {
  "zh": {"v": "有", "p": "TiCDC：Kafka/MySQL 下游一等公民",
         "b": "- TiCDC 捕获 TiKV 变更推到 Kafka/MySQL/Pulsar/对象存储 `官方文档`。\n- 支持 Avro/Canal-JSON 等协议 `官方文档`。\n- 大事务与 changefeed 延迟监控是运维重点 `社区共识`。"},
  "en": {"v": "Supported", "p": "First-class TiCDC to Kafka/MySQL",
         "b": "- TiCDC captures TiKV changes into Kafka/MySQL/Pulsar/object storage `(official docs)`.\n- Avro/Canal-JSON and other protocols supported `(official docs)`.\n- Monitoring changefeed lag on huge transactions is an ops priority `(community consensus)`."}}
CONTENT2["weaviate"]["cdc"] = {
  "zh": {"v": "无", "p": "无 CDC；增量靠客户端",
         "b": "- 无变更日志与 CDC 接口 `官方文档`。"},
  "en": {"v": "Not supported", "p": "No CDC; incrementals via client",
         "b": "- No change log or CDC interface `(official docs)`."}}
CONTENT2["yugabytedb"]["cdc"] = {
  "zh": {"v": "有", "p": "CDC Streams；Debezium YugabyteDB 连接器",
         "b": "- YugabyteDB CDC（WAL 式）+ gRPC 流 `官方文档`。\n- Debezium 有官方 YugabyteDB 连接器 `官方文档`。\n- YCQL 侧 CDC 覆盖弱于 YSQL `社区共识`。"},
  "en": {"v": "Supported", "p": "CDC Streams; Debezium YugabyteDB connector",
         "b": "- YugabyteDB CDC (WAL-based) with gRPC streaming `(official docs)`.\n- Debezium ships an official YugabyteDB connector `(official docs)`.\n- CDC coverage on the YCQL side is weaker than YSQL `(community consensus)`."}}
