# 多人地下城架构：部署平面与尚未确定的模拟平面

> 2026-10-22 更新：已补齐 v0.6 对象所有权任务；保留既有 v0.7。新结论以 [E47–E56](evidence.md#e47) 和 [对象布局补充](game-owner-static.md#instance-ownership-v06) 为准，以下旧版本段落保留研究历史。

**研究状态：静态 v0.1**。进程/端口是配置事实；进程内部副本实例与游戏循环仍未知。

## 可识别的服务

| 服务/程序 | 已检查材料支持的职责 | 已知端口或配置 | 证据级别 |
|---|---|---|---|
| `df_game_r` | 文档称处理“地下城等级和地下城内游戏进行”、角色、装备等；每频道有独立启动命令 | `tcp_port=__SERVER_GROUP__00__CHANNEL_NO__`、`udp_port=__SERVER_GROUP__10__CHANNEL_NO__`；示例频道 11 为 30011/TCP + 31011/UDP | 已证实（文档/配置） [E01][E04][E05][E09] |
| `df_stun_r` | 文档将其定位为 UDP 打洞辅助服务 | `2__SERVER_GROUP__11/12/13`；示例 2311-2313/UDP | 已证实（文档/配置） [E02][E06][E09] |
| `df_relay_r` | 文档称不能直连时中继客户端通信；连接 Monitor 配置信息 | 当前示例 7300/TCP+UDP；历史文档 7200 | 已证实（文档/配置），转发内容未知 [E02][E07][E09] |
| `df_channel_r` | 频道信息下发（文档描述），向 Bridge 取信息 | 示例 7001/TCP+UDP | 已证实（文档/配置） [E01][E08][E09] |
| `df_bridge_r` | 收集/维护频道信息，配置 `d_channel_...` 数据库 | `__BRIDGE_TCP_PORT__`；历史文档 7000 | 已证实（文档/配置） [E01][E08] |
| `df_monitor_r` | 文档称跨服务器组防重复登录、聊天/邮件通知等；Monitor 显式配置 DBMW、Manager、Relay | `__MONITOR_TCP_PORT__`；历史文档 30303 | 已证实（文档/配置） [E03][E07][E21] |
| `df_dbmw_r`（多实例） | DB 中间件：`dbmw_mnt`/`dbmw_guild`/`dbmw_stat` | 监控实例连接 `d_taiwan` 与本地 MySQL 代理 | 已证实（文档/配置），调用细节未知 [E21] |
| `df_gate-server` | 登录/认证配套网关，读取数据库和 `GAME_SERVER_IP` | 示例 5505/TCP（HTTP） | 已证实（脚本/Compose） [E09] |

注：表内的“职责”若来自 `doc/ArchitectureDiagram.md`，证实的是**该文档作出了此陈述**。尚不是独立动态验证。具体端口随 `SERVER_GROUP`、频道、脚本环境而变化。

## 已知部署与连接配置图

以下实线表示仓库**显式配置或文档描述的关系**，**不是抓包验证后的实际应用消息流**。

```mermaid
flowchart LR
  Client["DNF 客户端"]
  Gate["Gateway / dnf-gate-server"]
  Chan["df_channel_r"]
  Bridge["df_bridge_r"]
  Game["df_game_r / 每个频道"]
  Stun["df_stun_r"]
  Relay["df_relay_r"]
  Mon["df_monitor_r"]
  DBMW["df_dbmw_r / 多实例"]
  Mysql[("MySQL / 本地代理")]
  Client ---|"频道发现：文档陈述"| Chan
  Client ---|"频道游戏 TCP/UDP 入口：配置"| Game
  Client ---|"UDP 打洞服务：文档陈述"| Stun
  Client ---|"候选回退路径"| Relay
  Client --- Gate
  Chan -->|"bridge_ip / bridge_port"| Bridge
  Game -->|"monitor 地址"| Mon
  Game -->|"relay 地址"| Relay
  Game -->|"channel 参数实际指向 Bridge"| Bridge
  Mon -->|"DBMW 端口"| DBMW
  Mon -->|"Relay 登记配置"| Relay
  DBMW --> Mysql
  Game -->|"master_db 配置"| Mysql
  Gate --> Mysql
```

**注意：** `game/cfg/server.template:23-25` 的 `udp_ip_of_channel`、`tcp_port_of_channel` 取的是 `__MAIN_BRIDGE_IP__` 与 `__BRIDGE_TCP_PORT__`。所以其变量名 `channel` 不应直接解读为与 `df_channel_r:7001` 对接。参见 [E04](evidence.md#e04) 和 [E08](evidence.md#e08)。

## 生命周期与多进程边界

`start_game.sh` 以 `channel_no` 和 `process_sequence` 生成频道配置，启动 `./df_game_r "$channel_name" nofork`；`s6` 的 `game_template` 声明依赖 Bridge、数据库初始化、数据库代理、Monitor IP 解析、安全代理等。**部署上是频道级进程隔离**，并没有证据表明“每队一进程”或“每队一线程”。[E05][E22]

`frida.js` 将 `G_GameWorld()` 和 `CParty::...`、`CDungeon::...`、`MapInfo::...` 作为当前游戏进程中可调用的对象/函数，这使“游戏进程参与副本状态管理”成为有力的研究方向。然而脚本只证明自己**引用了这些函数地址和接口**，并没有给出每个副本的 Actor、线程、tick 或内存结构布局。[E10][E12][E14][E16][E17]

## 需要区分的三层状态

| 层 | 可见线索 | 最关键未知 |
|---|---|---|
| 会话与频道层 | `G_GameWorld`、`CUser`、`CParty`；频道进程/端口 | 哪些状态跨频道迁移，掉线时缓存多久 |
| 副本战斗层 | `CDungeon_get_index`、`CParty::OnFightVillageMonster`、`MapInfo::Add_Mob` | 普通副本实例标识、怪物 AI/HP 所有者、P2P Host 职责 |
| 经济/持久化层 | `CInventory`、`CUser_gain_exp_sp`、`ReqDBSend...Mail`、MySQL/DBMW | 普通掉落、结算与数据库事务、幂等操作标识 |

**小结：** 现在可以画出可启动的频道服务拓扑，但不可以给出确定的“每队副本运行时”框架。验证路径见 [副本生命周期](dungeon-lifecycle.md)。


## v0.5：Game ELF 里的对象所有权（替代上文「内部未知」的历史表述）

> 该节是 2026-10-12 对完整 `df_game_r` 的新证据；上文 v0.1 仅描述此前已知部署信息。完整反汇编与地址：[game-owner-static.md](game-owner-static.md)，[E32–E39](evidence.md#v05完整-game-elf-只读反汇编2026-10-12)。

**已确认（H）**：`CGameManager::GetParty() 0x08294E10` 在 `0x08294E21` 调 `StaticPool<CParty,600>::Acquire`，`GetParty(int) 0x08294F32` 在 `0x08294F52` 查 `hash_map<int,CParty*>`。`CUser::GetParty() 0x0865514C` 在 `0x08655156` 读用户队伍索引、`0x0865517B` 调 `GetParty(int)`。`CParty::CParty` 在 `0x082A565A` 调 `CBattle_Field::SetParty 0x082A43BE`，后者在 `0x082A43C7` 写反向的 `CParty*` 指针。`CBattle_Field::GetDungeon 0x080FDCFC` 从 `+0x188` 读取 `CDungeon*`（`0x080FDD02`），`GetMapInfo 0x0822D03E` 通过 `0x0822D04A` 调 `GetCurrentMapInfo 0x0822CBCC`。

**高可信静态架构推断（M）**：频道 Game 进程持有队伍对象注册表，队伍对象联结战场及地图状态。**未知（U）**：战场对象是否队伍结构体直接内嵌、多人入本时共享的是哪个确切战场指针、Host/P2P 是否执行普通实时物理/HP 模拟。

```mermaid
flowchart LR
  USER["CUser::GetParty 0x0865514C"] -->|"0x0865517B call"| LOOK["CGameManager::GetParty(int) 0x08294F32"]
  LOOK -->|"0x08294F52 find"| REG["GameManager hash_map<int,CParty*> +0x270"]
  REG --> PARTY["CParty*"]
  NEW["CGameManager::GetParty() 0x08294E10"] -->|"0x08294E21 Acquire"| POOL["StaticPool<CParty,600>"]
  POOL --> PARTY
  PARTY -->|"constructor 0x082A565A call SetParty"| FIELD["CBattle_Field / backref to CParty*"]
  FIELD -->|"0x080FDD02 load"| DUNG["CDungeon*"]
  FIELD -->|"0x0822D04A call"| MAP["GetCurrentMapInfo"]
  PARTY -. "仍未证明普通帧战斗权威" .-> HOST["Host / P2P / Client"]
```

## v0.6 对象所有权补充（2026-10-22）

本节更新上文 v0.5 的布局未知项；[E47–E50](evidence.md#e47) 与
[完整对象图/字段表](game-owner-static.md#instance-ownership-v06) 是依据。
频道进程 `df_game_r` 内，CGameManager 管理活跃 CParty，
每个 CParty **内嵌** `CBattle_Field at +0xB24`；
战场 **内嵌 map 容器 at +0x78**，节点按值保存 MapInfo，
MapInfo+0x0C 又持有怪物 map。由不同活跃队伍对象地址实现运行数据隔离，
没有“每队新进程”证据。相同队伍索引的成员在 Game 侧取得同一战场上下文。

CDungeon* 从 CDataManager/CDungeonList 查到并存 B+0x188；
CMap* 按 MapInfo 地图索引查询后存 B+0x108。
这些配置引用与按队伍维护的怪物/房间/难度状态不同，不是唯一运行实例 ID。
普通 reset 清地图容器/配置引用；destroy → init → PutParty 归还池，
不能把 Pool::Free 说成 delete 战场。[E48](evidence.md#e48)

静态结论只覆盖 Game 内状态持有；客户端资源、Peer 帧同步、Host AI/伤害计算
仍是未知。STUN/Relay 部署关系不构成它们持有普通副本运行数据的证据。
同队共享和不同队伍隔离的实际会话地址、复用世代与异常回收尚待动态验证。
