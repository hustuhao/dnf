# 证据记录（静态 v0.2）

- **固定基线：** `main` commit `1d59eeafeaa105a3c109091c3d5fc061a30bbf19`
- **方法：** GitHub 连接器读取仓库文本、目录与 Git tree；人工交叉检查配置和 Frida 入口。已解析 Relay/STUN 的 ELF 头、实际符号和字符串；仍未获得 Game ELF 字节、未反汇编、未运行程序或抓包。
- **分级纪律：** “已证实”可指**确实存在某行配置/代码/文档陈述**，而不自动代表运行时行为已验证。Frida 的地址归于**脚本给出的标注**，非独立核验结果。
- 链接固定到上述 commit，避免随主分支漂移。

## 可复核证据

### E01
**已证实·架构文档陈述。** [`doc/ArchitectureDiagram.md#L180-L203`](https://github.com/hustuhao/dnf/blob/1d59eeafeaa105a3c109091c3d5fc061a30bbf19/doc/ArchitectureDiagram.md#L180-L203) 描述 `game` 处理地下城内游戏、角色等业务，以及 Game 指向 Monitor、Relay 等服务的历史路径。不是抓包证据。

### E02
**已证实·架构文档陈述。** [`doc/ArchitectureDiagram.md#L11-L39`](https://github.com/hustuhao/dnf/blob/1d59eeafeaa105a3c109091c3d5fc061a30bbf19/doc/ArchitectureDiagram.md#L11-L39) 指出 Relay 在 P2P 无法连接时作中继、STUN 用 UDP 打洞；该页把 Relay 写成 7200。

### E03
**已证实·架构文档陈述。** [`doc/ArchitectureDiagram.md#L139-L160`](https://github.com/hustuhao/dnf/blob/1d59eeafeaa105a3c109091c3d5fc061a30bbf19/doc/ArchitectureDiagram.md#L139-L160) 描述 Monitor 的跨服务登录、聊天、邮件、状态职责，并列出与 DBMW、Manager、Relay 的关系。

### E04
**已证实·配置文本。** [`build/dnf_data/home/template/neople/game/cfg/server.template#L1-L25`](https://github.com/hustuhao/dnf/blob/1d59eeafeaa105a3c109091c3d5fc061a30bbf19/build/dnf_data/home/template/neople/game/cfg/server.template#L1-L25) 频道 TCP/UDP 公式和相关服务地址；[`#L44-L54`](https://github.com/hustuhao/dnf/blob/1d59eeafeaa105a3c109091c3d5fc061a30bbf19/build/dnf_data/home/template/neople/game/cfg/server.template#L44-L54) Relay / STUN；[`#L69-L90`](https://github.com/hustuhao/dnf/blob/1d59eeafeaa105a3c109091c3d5fc061a30bbf19/build/dnf_data/home/template/neople/game/cfg/server.template#L69-L90) DB 连接参数与消息头字段名称。**不存在消息字段运行时偏移的独立验证。**

### E05
**已证实·启动脚本。** [`build/dnf_data/home/template/init/run/start_game.sh#L5-L29`](https://github.com/hustuhao/dnf/blob/1d59eeafeaa105a3c109091c3d5fc061a30bbf19/build/dnf_data/home/template/init/run/start_game.sh#L5-L29) 生成频道配置；[`#L33-L46`](https://github.com/hustuhao/dnf/blob/1d59eeafeaa105a3c109091c3d5fc061a30bbf19/build/dnf_data/home/template/init/run/start_game.sh#L33-L46) 启动 `df_game_r "$channel_name" nofork`、预加载 Frida 等动态库。

### E06
**已证实·脚本与配置。** [`start_stun.sh#L3-L9`](https://github.com/hustuhao/dnf/blob/1d59eeafeaa105a3c109091c3d5fc061a30bbf19/build/dnf_data/home/template/init/run/start_stun.sh#L3-L9)、[`stun/cfg/udp_server.cfg#L1-L3`](https://github.com/hustuhao/dnf/blob/1d59eeafeaa105a3c109091c3d5fc061a30bbf19/build/dnf_data/home/template/neople/stun/cfg/udp_server.cfg#L1-L3)、[`start_relay.sh#L3-L9`](https://github.com/hustuhao/dnf/blob/1d59eeafeaa105a3c109091c3d5fc061a30bbf19/build/dnf_data/home/template/init/run/start_relay.sh#L3-L9) 分别启动独立程序。

### E07
**已证实·配置。** [`relay/cfg/relay_200.cfg#L1-L12`](https://github.com/hustuhao/dnf/blob/1d59eeafeaa105a3c109091c3d5fc061a30bbf19/build/dnf_data/home/template/neople/relay/cfg/relay_200.cfg#L1-L12) TCP/UDP 同端口、Monitor 目标、`relay_index`/`this_pvp_channel`；[`monitor/cfg/server.cfg#L1-L14`](https://github.com/hustuhao/dnf/blob/1d59eeafeaa105a3c109091c3d5fc061a30bbf19/build/dnf_data/home/template/neople/monitor/cfg/server.cfg#L1-L14) DBMW、Manager、Relay 目标参数。

### E08
**已证实·配置与脚本。** [`channel/cfg/server.cfg#L1-L9`](https://github.com/hustuhao/dnf/blob/1d59eeafeaa105a3c109091c3d5fc061a30bbf19/build/dnf_data/home/template/neople/channel/cfg/server.cfg#L1-L9) Channel 对外和 Bridge 对内配置；[`bridge/cfg/server.cfg#L1-L11`](https://github.com/hustuhao/dnf/blob/1d59eeafeaa105a3c109091c3d5fc061a30bbf19/build/dnf_data/home/template/neople/bridge/cfg/server.cfg#L1-L11) Bridge 监听和数据库；[`start_channel.sh#L12-L29`](https://github.com/hustuhao/dnf/blob/1d59eeafeaa105a3c109091c3d5fc061a30bbf19/build/dnf_data/home/template/init/run/start_channel.sh#L12-L29) 实际替换规则。

### E09
**已证实·部署样例。** [`deploy/dnf/docker-compose/basic/docker-compose.yaml#L47-L59`](https://github.com/hustuhao/dnf/blob/1d59eeafeaa105a3c109091c3d5fc061a30bbf19/deploy/dnf/docker-compose/basic/docker-compose.yaml#L47-L59) 包含 7001、7300、频道 11/52、2311-2313 的网络映射。此端口是**样例**而不是所有部署实例的事实。

### E10
**已证实·Hook 脚本中的声明。** [`frida.js#L88-L105`](https://github.com/hustuhao/dnf/blob/1d59eeafeaa105a3c109091c3d5fc061a30bbf19/build/dnf_data/home/template/init/frida.js#L88-L105) 包含 `CUserCharacInfo_enableSaveCharacStat=0x819A870` 和 `CDungeon_get_index=0x080FDCF0`；[`#L124-L131`](https://github.com/hustuhao/dnf/blob/1d59eeafeaa105a3c109091c3d5fc061a30bbf19/build/dnf_data/home/template/init/frida.js#L124-L131) 包含 `G_GameWorld=0x80DA3A7`、`G_CDataManager=0x80CC19B`。

### E11
**已证实·Hook 脚本中的声明。** [`frida.js#L164-L221`](https://github.com/hustuhao/dnf/blob/1d59eeafeaa105a3c109091c3d5fc061a30bbf19/build/dnf_data/home/template/init/frida.js#L164-L221) 金币、背包、发经验、`CUser_Send=0x86485BA`、`PacketBuf_get_int=0x858D27E` 与组包接口。`CParty::send_to_party` 仅出现在注释中，不作为已验证的函数地址。

### E12
**已证实·Hook 脚本中的声明。** [`frida.js#L305-L314`](https://github.com/hustuhao/dnf/blob/1d59eeafeaa105a3c109091c3d5fc061a30bbf19/build/dnf_data/home/template/init/frida.js#L305-L314) `CUser_GetParty=0x0865514C`、`CParty_get_user=0x08145764`。

### E13
**已证实·特定怪物攻城脚本逻辑。** [`frida.js#L1157-L1212`](https://github.com/hustuhao/dnf/blob/1d59eeafeaa105a3c109091c3d5fc061a30bbf19/build/dnf_data/home/template/init/frida.js#L1157-L1212) 挂接 `0x086B34A0` 和 `SendVillageMonsterFightResult=0x086B330A`，检查 `result`，枚举最多四名队员。**这不是普通 dungeon 怪物伤害判定证据。**

### E14
**已证实·特定活动 Hook 逻辑。** [`frida.js#L1388-L1427`](https://github.com/hustuhao/dnf/blob/1d59eeafeaa105a3c109091c3d5fc061a30bbf19/build/dnf_data/home/template/init/frida.js#L1388-L1427) Hook `CParty::OnFightVillageMonster=0x085B9596`、`OnFightVillageMonster=0x086B3240`，替换 `MapInfo::Add_Mob=0x08151612`；[`#L1479-L1536`](https://github.com/hustuhao/dnf/blob/1d59eeafeaa105a3c109091c3d5fc061a30bbf19/build/dnf_data/home/template/init/frida.js#L1479-L1536) 通过怪物参数复制修改数量/UID。**所有名称与地址是该脚本标注，未独立逆向验证。**

### E15
**已证实·特定活动 Hook 逻辑。** [`frida.js#L1537-L1567`](https://github.com/hustuhao/dnf/blob/1d59eeafeaa105a3c109091c3d5fc061a30bbf19/build/dnf_data/home/template/init/frida.js#L1537-L1567) 怪物攻城奖励 Hook 可遍历队伍、随机计算额外经验并调用 `CUser_gain_exp_sp`。不是普通掉落 RNG 证据。

### E16
**已证实·副本处理 Hook 逻辑。** [`frida.js#L1799-L1815`](https://github.com/hustuhao/dnf/blob/1d59eeafeaa105a3c109091c3d5fc061a30bbf19/build/dnf_data/home/template/init/frida.js#L1799-L1815) `CParty::UseAncientDungeonItems=0x859EAC2` 替换回调，带 `party, dungeon` 参数；使用 `CDungeon_get_index` 测定特定副本 ID 免扣除消耗。**副本配置索引不等于运行时实例 ID。**

### E17
**已证实·Frida 自定义任务队列。** [`frida.js#L895-L953`](https://github.com/hustuhao/dnf/blob/1d59eeafeaa105a3c109091c3d5fc061a30bbf19/build/dnf_data/home/template/init/frida.js#L895-L953) 任务队列借助 `TimerDispatcher::dispatch=0x8632A18` Hook 执行，申请锁同步；**不能推出副本线程模型**。

### E18
**已证实·角色进出世界 Hook。** [`frida.js#L2172-L2213`](https://github.com/hustuhao/dnf/blob/1d59eeafeaa105a3c109091c3d5fc061a30bbf19/build/dnf_data/home/template/init/frida.js#L2172-L2213) `GameWorld::reach_game_world=0x86C4E50`、`leave_game_world=0x86C5288` Hook。不能等价为副本上下线/重连状态机。

### E19
**已证实·脚本邮件 API。** [`frida.js#L380-L402`](https://github.com/hustuhao/dnf/blob/1d59eeafeaa105a3c109091c3d5fc061a30bbf19/build/dnf_data/home/template/init/frida.js#L380-L402)、[`#L564-L594`](https://github.com/hustuhao/dnf/blob/1d59eeafeaa105a3c109091c3d5fc061a30bbf19/build/dnf_data/home/template/init/frida.js#L564-L594) 构造道具邮件并触发 `ReqDBSendNewSystemMail` 系列。**实际写库事务与失败重试未知**。

### E20
**已证实·脚本 DB 调用线索。** [`frida.js#L228-L255`](https://github.com/hustuhao/dnf/blob/1d59eeafeaa105a3c109091c3d5fc061a30bbf19/build/dnf_data/home/template/init/frida.js#L228-L255)、[`#L815-L825`](https://github.com/hustuhao/dnf/blob/1d59eeafeaa105a3c109091c3d5fc061a30bbf19/build/dnf_data/home/template/init/frida.js#L815-L825) MySQL 本地句柄与直接操作。**不证明普通副本全部直接访问数据库**。

### E21
**已证实·监控/DBMW 配置。** [`dbmw_mnt/cfg/server_01.cfg#L1-L10`](https://github.com/hustuhao/dnf/blob/1d59eeafeaa105a3c109091c3d5fc061a30bbf19/build/dnf_data/home/template/neople/dbmw_mnt/cfg/server_01.cfg#L1-L10)、[`monitor/cfg/server.cfg#L1-L14`](https://github.com/hustuhao/dnf/blob/1d59eeafeaa105a3c109091c3d5fc061a30bbf19/build/dnf_data/home/template/neople/monitor/cfg/server.cfg#L1-L14)、[`game/cfg/server.template#L69-L74`](https://github.com/hustuhao/dnf/blob/1d59eeafeaa105a3c109091c3d5fc061a30bbf19/build/dnf_data/home/template/neople/game/cfg/server.template#L69-L74) 数据库与服务关联。

### E22
**已证实·部署依赖配置。** `build/dnf_data/etc/s6-overlay/s6-rc.d/game_template/dependencies.d/` 包含 `bridge`、`init-data`、`init-db`、`main_mysql_proxy`、`monitor_ip`、`sg_mysql_proxy`、`zergsvr_secagent`；[`game_template/run#L1-L8`](https://github.com/hustuhao/dnf/blob/1d59eeafeaa105a3c109091c3d5fc061a30bbf19/build/dnf_data/etc/s6-overlay/s6-rc.d/game_template/run#L1-L8) 调用频道启动脚本。依赖是 **s6 服务级依赖**，不是请求调用边。

## 可复核二进制对象（尚未静态分析）

| 文件 | Git tree 元数据大小 | 下一步 |
|---|---:|---|
| `build/dnf_data/home/template/init/df_game_r` | 36,360,954 bytes | ELF 架构/Build ID/符号/函数调用链 |
| `build/dnf_data/home/template/neople/stun/df_stun_r` | 见仓库 | 协议/会话逻辑 |
| `build/dnf_data/home/template/neople/relay/df_relay_r` | 418,098 bytes | 报文转发与接入 |
| `build/dnf_data/home/template/neople/channel/df_channel_r` | 1,305,013 bytes | 频道列表 |
| `build/dnf_data/home/template/neople/monitor/df_monitor_r` | 2,461,318 bytes | Session 协调 |
| `build/dnf_data/home/template/init/df_dbmw_r` | 4,041,084 bytes | 写库入口 |

### 尚未获得的证据

`doc/台服dnf服务架构.docx`（目录可见，连接器不能读取二进制正文）；`df_game_r` 实际 `readelf/objdump/Ghidra` 结果；运行日志；pcap；客户端协议解析。**不存在已执行的动态实验记录**，不可填写伪造的 PID、时间戳、哈希和包号。

### E23

**已证实·Relay 实际 ELF 符号表。** [df_relay_r](https://github.com/hustuhao/dnf/blob/1d59eeafeaa105a3c109091c3d5fc061a30bbf19/build/dnf_data/home/template/neople/relay/df_relay_r)，Git blob SHA `c39c47eeb19127a105a0c3309e9b663de81e239a`，418,098 字节、ELF32/x86，含 `.symtab`。真实符号：`TCPUser::onPacketParse(0x0805D02E)`、`TCPHandlerRelay::dispatch(0x0805B958)`、`UDPHandlerRelay::dispatch(0x0805E4C0)`、`UDPHandlerS2S::dispatch(0x0805E406)`、`RelayService::relayToTCP(0x08051B76)`、`RelayService::setAuthenticated(0x08051B2C)`，其共同的 C++ 命名空间为 `RelayServiceApp`。从 Base64 原始二进制字节解析 `.symtab`；**只证明代码入口存在，不证明实际调用链或战斗消息含义**。地址和大小见 [binary-static.md](binary-static.md)。

### E24

**已证实·Relay 实际字符串。** 同一 ELF 含有 `Relay Server v2.5.6.9`、`Monitor Auth: Fail.. Disconnect User!!`、`Auth Packet Queue`、`Error UDPS2SSocket!! Not Auth mode`、`Set Relay Server for PVP Channel`。其存在可与 `relay_200.cfg` 的 `[aradauth]` 和 `this_pvp_channel=1` 交叉核对，但运行时业务流尚未确认。

### E25

**已证实·STUN 实际 ELF 头、符号、字符串。** [df_stun_r](https://github.com/hustuhao/dnf/blob/1d59eeafeaa105a3c109091c3d5fc061a30bbf19/build/dnf_data/home/template/neople/stun/df_stun_r)，Git blob SHA `9e8e459f5bc1144617213d3141e2c5a740e2bc2c`，131,126 字节，ELF64/x86-64，含 `.symtab` 和 `.debug_info`。`stunProcess1/2/3(void*)` 在 `0x4017A4`、`0x401722`、`0x401674`，包含日志 `Create Thread1 RealIP Socket`、`Create Thread2 NAT Socket`、`Create Thread3 MTU_CHECKER Socket`、`STUN Server v1.4.0.0`。精确的线程调用链和端口映射仍待反汇编。
