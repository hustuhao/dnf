# 证据记录（Game ELF 静态 v0.7）

- **固定基线：** `main` commit `1d59eeafeaa105a3c109091c3d5fc061a30bbf19`
- **方法：** GitHub 连接器读取仓库文本、目录与 Git tree；人工交叉检查配置和 Frida 入口。已解析 Relay/STUN ELF 和 Game ELF 的符号及机器码；已在 GitHub Actions 环境中反汇编 Game 相关函数，未运行服务端、未抓包。
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

### E26

**已证实·Relay 真实机器码及直接调用（UDP→TCP）。** 来源 [`df_relay_r` ELF](https://github.com/hustuhao/dnf/blob/1d59eeafeaa105a3c109091c3d5fc061a30bbf19/build/dnf_data/home/template/neople/relay/df_relay_r)，Git blob `c39c47eeb19127a105a0c3309e9b663de81e239a`，`.text` 文件偏移 `0x1B80`，虚拟地址 `0x08049B80`。从 ELF `.text` 提取函数机器码，再用 GNU `objdump -D -b binary -m i386 -M intel --adjust-vma` 验证：`UDPHandlerRelay::dispatch +0x31`（`0x0805E4F1`）直接 `call 0x8051B76`；该函数首字段需等于 0 才到达分支。`RelayService::relayToTCP 0x08051B7F` 写 `word ptr [eax]=3`、`0x08051B87` 读 `[eax+8]`、`0x08051B97` 调 `Users::getTCPUser`、`0x08051BB2` 调 `TCPUser::send`。这**已证实一条具体的内部转发逻辑**，不是推定全部地下城 UDP 都走 TCP。详见 [relay-control-flow.md](relay-control-flow.md)。

### E27

**已证实·TCP Relay 账号映射和有条件转发。** 实际机器码 `TCPHandlerRelay::dispatch(0x0805B958)` 首 16 位字段分支为 0、1；类型 0 通过 `getACCID`、`setACCID(0x0805B9F7)`、`setTCPUser(0x0805BA1E)`、`setAuthenticated(0x0805BA3B)` 关联用户；类型 1 在已有账号关联条件下经 `0x0805BA86` 调用 `relayToTCP`。`TCPUser::onPacketParse` 的已检查入口机器码在 `0x0805D049` 调 `isPopStraight(12)`，`0x0805D070` 读 `[ptr+2]` 16 位长度，`0x0805D07D` 读首 16 位类型，异常类型走 `postDisconnected`。**仅检查了 parser 的前约 220 字节，不能声称已经还原完整 TCP 封包协议。**

### E28

**已证实·UDP S2S 控制分支和授权链路。** `UDPHandlerS2S::dispatch(0x0805E406)` 首 16 位值为 0 时调用 `RelayService::setAuthenticated(0x0805E44D)`；值为 `0x09C4`（2500）且偏移 `+14` 字节为 0 时经 `0x0805E488` 调 `postDisconnectEvent2TCPUser`；值为 1 时不在此函数执行其他实质处理。`setAuthenticated` 在特定模式下的 `0x08051B69` 调用真实符号 `UDPSocket::pushMonitorAuthPacket`。**这些是内部机器码的比较数值与路径，未经抓包验证，不宜称网络协议消息 ID。**

### E29

**已证实·STUN main 绑定端口与线程创建的真实机器码。** [`df_stun_r` ELF](https://github.com/hustuhao/dnf/blob/1d59eeafeaa105a3c109091c3d5fc061a30bbf19/build/dnf_data/home/template/neople/stun/df_stun_r) (`9e8e459f5bc1144617213d3141e2c5a740e2bc2c`)。`main(0x401F64)` 在 `0x402027–0x402036`、`0x402067–0x402076`、`0x4020A7–0x4020B6` 三次直接调用 `openPort(0x401C92)`，端口立即数分别 `0x907=2311`、`0x908=2312`、`0x909=2313`，把 Socket 存入 `0x603FA4`、`0x603FA8`、`0x603FAC`。`pthread_create` 处 `0x40210D/0x402128/0x402143` 传入 `stunProcess1/2/3`。三线程分别使用 RealIP、NAT、MTU_CHECKER 的二进制内字符串。不同于 v0.2，当下**已由反汇编确认线程及端口对应关系**。不能由此认定整个项目其他版本的 STUN 配置必然无效。

### E30

**已证实·STUN 请求类型与 7 字节响应内存布局。** `msgProcess(0x401584, 239B)` 反汇编 `0x4015A4–0x4015BA` 对输入第一个字节比较 `1`、`5`、`0`；`1`/`5` 分支 `0x4015BF/0x40160D` 写第一个响应字节为 `2`，从来源地址对象 `+4` 拷贝 4 字节 IP 字段、`+0` 拷贝 2 字节端口，`0x4015F3/0x401644` 发送长度参数 `7`。类型 `1` 用传入的 Socket；类型 `5` 在 `0x40163B` 从全局 `0x603FAC` 读取第三 Socket 发送。类型 `0` 在本函数中不发送并返回成功。**字段为静态内存写操作，还未用 pcap 验证实际字节序或客户端含义。** [stun-protocol.md](stun-protocol.md)。

### E31

**已证实·STUN MTU thread 的长度回包。** `stunProcess3(0x401674)` 在 `0x40169D` 使用缓冲容量 `0x5DC=1500`，`0x4016EB` 调 `getMessage(0x401AC0)`，`0x4016F4–0x4016F7` 将收到的实际字节数截成 16 位写入两个字节，`0x401712–0x401717` 以 `sendMessage(0x40189A)` 发回长度为 `2` 的消息。**未验证路径 MTU 发现算法或返回值字节序。**


## v0.5：完整 Game ELF 只读反汇编（2026-10-12）

基线：`df_game_r` Git blob `f7a65ba7bc723e96fadeae07e87b72e05560d989`、SHA256 `8859c99d8290dc5fb58151444138cf2697b2bfff12d47d6159596a03f20b5261`；ELF32/x86 `ET_EXEC`，带符号与调试信息。机器码和直接交叉引用见 [Actions 成功扫描](https://github.com/hustuhao/dnf/actions/runs/38208943902)、[独立扫描报告](game-owner-static.md)。下述 H 指函数与指令直接吻合，M 指可信结构推断，U 指未知。不提交原始机器码 dump。

### E32：Game ELF / Frida 地址确实匹配此版本（H）

`cloud/verify-env.sh` 与 `cloud/scan-static.sh` 在云端扫描完成：`file` 报 ELF32 Intel 80386、not stripped、with debug_info；`readelf` 提供 `PT_LOAD(R E)` 起始 `0x08048000`，大小 `0x1320E61`。Frida `ptr(...)` 共 162 次，其中 156 次落在可执行段，6 次落在非执行段。注意脚本仅按段地址分类；但 `nm/objdump` 已进一步独立核验 `CDungeon::get_index(0x080FDCF0)`、`CParty::get_user(0x08145764)`、`CParty::UseAncientDungeonItems(0x0859EAC2)`、`MapInfo::Add_Mob(0x08151612)`、`CUser::GetParty(0x0865514C)`、`CUser::Send(0x086485BA)`、`PacketBuf::get_int(0x0858D27E)` 函数身份。**161/162 或 156/162 都不能据此定义为 Hook 正确率。**

### E33：Game 进程内 `CGameManager` 管理共享队伍对象（H）

`CGameManager::GetParty()` 在 `0x08294E21: call 0x082B0E5A` 获取 `StaticPool<CParty,600>` 对象，在 `0x08294EE2: call 0x082B112A` 使用 `hash_map<int,CParty*>::operator[]`。按 ID 查队伍的 `CGameManager::GetParty(int)` (`0x08294F32`) 在 `0x08294F3B: lea ecx,[eax+0x270]` 取管理器容器字段，`0x08294F52: call 0x082B10C4` 调用 `hash_map::find`，`0x08294F9D: mov eax,[eax+0x4]` 读取 `CParty*`。释放 `CGameManager::PutParty(CParty*)` (`0x08294FC8`) 在 `0x0829505A` 调 `hash_map::erase`，`0x08295072` 调 `StaticPool<CParty,600>::Free`。这是**实际对象注册、查找、回收代码**；`600` 仅为池模板容量。

### E34：玩家通过队伍索引回查同一注册表（H）

`CUser::GetParty` (`0x0865514C`) 的 `0x08655156: movzx eax,WORD PTR [eax+0x8d004]` 读取用户保存的队伍索引；`0x0865516F: call 0x080CC18E` 获取 `G_CGameManager`；`0x0865517B: call 0x08294F32` 根据索引得到 `CParty*`。`CParty::join_user` (`0x0859B2B6`) 的 `0x0859B3AF: call 0x085BFD96` 调用 `CUser::SetPartyIndex`。`CParty::get_user` (`0x08145764`) 在 `0x08145773` 将 slot*3 再左移 3 位，在 `0x08145779` 加 `0x78`，`0x0814577C` 取指针，即 `CParty+0x78+slot*24` 的队员记录起始字段。**“同一频道两个已入队玩家的查找目标是同一 `CParty`”为 M 静态结构推断**，还未核实双客户端对象地址。

### E35：队伍与战场 MapInfo 的真实对象边（H / M）

`CParty::CParty` 的 `0x082A565A: call 0x082A43BE` 调用 `CBattle_Field::SetParty(CParty*)`；`0x082A43C7: mov DWORD PTR [eax],edx` 把队伍指针写入 `CBattle_Field` 首字段（H）。`CBattle_Field::GetDungeon` (`0x080FDCFC`) 的 `0x080FDD02: mov eax,[eax+0x188]` 读取 `CDungeon*`（H）；`CBattle_Field::GetCurrentMapInfo` 的 `0x0822CBF4: call 0x08300DA6` 读取当前坐标、`0x0822CC15: call 0x0822CC48` 获取地图信息（H）。`CBattle_Field` 由谁分配及是否内嵌在 `CParty` 尚为 U；关联为 H，完整所有权模型为 M。

### E36：入本/换图的实际 Dispatcher 调用边（H）

`DisPatcher_SelectDungeon::process` 的 `0x081C8E0F: call 0x085A0954` 进入 `CParty::dungeon_start`。`DisPatcher_MoveMap::process` 的 `0x081C54D4: call 0x085A8F4E` 进入 `CParty::move_map`；其中 `0x085A9143: call 0x08308AE6` 调 `CBattle_Field::MoveMap`、`0x085A910B: call 0x0827A96E` 调路径异常计数检查。`CParty::checkInoutConditionDungeon` 的 `0x085ABF3B: call 0x0859EAC2` 调 `UseAncientDungeonItems`。Dispatcher 名称与业务结构是 ELF 真实符号，**尚未确认上游网络 command/opcode**。

### E37：怪物死亡、道具和结算在 Game 上具有处理路径（H）

`DisPatcher_DieMob::dispatch_sig` 的 `0x081EBB73: call 0x085A27E8` → `CParty::kill_monster`，该函数的 `0x085A2B44: call 0x0830BC78` → `CBattle_Field::kill_monster`。`DisPatcher_GetItem::process` 的 `0x081C3905: call 0x085A3B98` → `CParty::get_item`，其 `0x085A3D19: call 0x0830D9C0` → `CBattle_Field::get_field_item`。`Dispatcher_Select_Card::dispatch_sig` 的 `0x081FFA45: call 0x085AB736` → `CParty::dungeon_clear`，同目标亦被定时器在 `0x08633160` 调用；清算内部 `0x085AB74C: call 0x085B3520`（`SaveCoin`）和 `0x085AB7E0: call 0x085AAB84`（`_putItemIntoUser`）存在。**只证实服务器处理死亡报告/掉落拾取/奖励；不能推出怪物每次受击/HP、AI、技能或客户端移动帧的权威。**

### E38：明确的 Game→队伍成员发送调用（H）

`CParty::send_host_info` 的 `0x0859CE5C: call 0x0859D14E` → `CParty::send_to_party(PacketGuard&)`；群发函数先在 `0x0859D16A: call 0x085B4D12` 检查用户有效性，在 `0x0859D194: call 0x086485BA` 发送 `CUser::Send(PacketGuard&)`。这证明 Game 可逐用户发送队伍报文，不说明普通战斗 UDP/P2P 是否也使用该接口。

### E39：Host/P2P 状态存在，但战斗权威仍未确定（H / U）

`CParty::set_host` (`0x0859CDBC`) 中 `0x0859CDC2: mov edx,[eax+0x74]`、`0x0859CDC8: mov [eax+0x70],edx`，保存 Host 相关字段；同一二进制另含 `CParty::ConnectP2P` (`0x0859A48C`)、`CParty::send_party_ipinfo` (`0x0859CEA2`) 和 `DisPatcher_ResPeer::dispatch_sig` 对队伍创建/加入的直接调用。**存在 Host/P2P 管理代码（H），Host 负责哪些位置、伤害、AI、死亡事件（U）。** 文件级进一步证据见 [v0.5 调用图](game-owner-static.md)。

### E40：普通技能入站字段和合法性检查（H）

来自原始 `df_game_r`（Git blob `f7a65ba7bc723e96fadeae07e87b72e05560d989`）机器码。`DisPatcher_UseSkill::read(0x081CAC5E)` 在 `0x081CAC7A/0x081CACBF` 调 `PacketBuf::get_byte`，在 `0x081CAD04/0x081CAD46` 调 `get_short`；`DisPatcher_UseSkill::process(0x081CADAA)` 的 `0x081CAE7E` 构造 `SKILL_USING_VALIDATE_INFO`，`0x081CAE89` 调 `CHackLog_InvalidUsingSkill::IsValidUsingSkill`，`0x081CAF15` 调 `CParty::use_skill(0x085A77D8)`，其 `0x085A77F9` 调 `CParty::OnUsedSkill(0x085B5F8E)`。本证据只证明技能消息处理和合法性检查**存在于代码**，不证明实时视觉技能全由 Game 同步。[run 38506766447](https://github.com/hustuhao/dnf/actions/runs/38506766447)。

### E41：SDC 伤害检查读取数据并定位服务端怪物记录（H）

`Dispatcher_SDC_Damage_Check::dispatch_sig(0x081E9E84)` 的 `0x081E9EA7/0x081E9F4A/0x081E9FC9` 分别调 `PacketBuf::get_byte/get_int/get_binary`；`0x081EA085` 调 `computeHpDamageSDC(0x08095C32)`；`0x081EA0D8` 调 `CHackAnalyzer::addServerHackCnt`；`0x081EA11E/0x081EA143` 调 `CBattle_Field::SetDamagedPacketCnt(0x08308F4E)` / `SetDamageValue(0x08308FF8)`。两个 Setter 都经 `GetCurrentMapInfo` / `std::map<int,map_monster>::find` 找到当前战场的怪物数据。主动状态伤害检查处理器 `0x081EA16E` 同样调这两个 Setter。**有伤害相关服务端计算/计数，不代表最终怪物 HP 的权威由 Game 决定。** [run 38506766447](https://github.com/hustuhao/dnf/actions/runs/38506766447)。

### E42：怪物死亡报告处理与额外反作弊检查（H）

`DisPatcher_DieMob::dispatch_sig(0x081EB0C4)` 多次读取 byte/int/short 并进行队伍检查，`0x081EB686` 调 `CParty::setMonsterMoveHack`，`0x081EBB73` 调 `CParty::kill_monster`，`0x081EBC6D` 调 `Secu_HackLogCheck::DieMob`；`CParty::kill_monster` 的 `0x085A2D11` 调 `OnKilledMonster`，后者在 `0x085B5AC4` 调 `CTraceMobDieHack::addMonsterDamage`，另有 `CHackAnalyzer::addServerHackCnt` 与 `CBattle_Field::onClearMap` 调用。 `CParty::CheckHackAverageHitCount` 在 `dungeon_clear` / `giveup_game` / `party_dungeon_fail` 等调用。**报告验证/处罚细节仍需全函数逆向。** [run 38506571907](https://github.com/hustuhao/dnf/actions/runs/38506571907)、[run 38506766447](https://github.com/hustuhao/dnf/actions/runs/38506766447)。

### E43：限定 Host/PvP 等相邻机制的结论（H/U）

`Dispatcher_ChangeHost::dispatch_sig(0x08204C1E)` 的 `0x08204D5C` 调 `CParty::change_manager`；`CParty::send_host_info` 可向队员群发 Host 信息；**Host 是否负责 PvE 实时 AI/伤害仍未知**。`Dispatcher_ChangeHp::dispatch_sig(0x0820748A)` 的 `0x0820752B` 调 `pvp_assault::CAssaultMgr::OnChangeHp(0x082EF570)`，**不能将其用作普通 PvE 血量同步机制的证据**。反汇编来源 [run 38506766447](https://github.com/hustuhao/dnf/actions/runs/38506766447)。


### E44：SDC 校验值的服务器重算与 ±1 比较（H）

在原版 Game ELF `f7a65ba7bc723e96fadeae07e87b72e05560d989` 上运行的 [Actions 静态分析](https://github.com/hustuhao/dnf/actions/runs/38507418346)：`Dispatcher_SDC_Damage_Check(0x081E9E84)` 在 `0x081EA025` 调 `uncompress`；`0x081EA066` 从解压结构 +`0x1E6` 读取报告值，`0x081EA085` 调 `computeHpDamageSDC(0x08095C32)`，`0x081EA090–0x081EA0A1` 以 **±1** 容差比较报告值与计算值；偏差过大时 `0x081EA0D8` 调 `CHackAnalyzer::addServerHackCnt`。**这证明代码中确实存在重算及校验，未证明怪物 HP 在此被扣减。**

### E45：MapInfo 怪物记录偏移 +0x20 / +0x24 的确切写操作（H）

[同一 ELF 机器码证据](https://github.com/hustuhao/dnf/actions/runs/38507418346)：`CBattle_Field::SetDamagedPacketCnt(0x08308F4E)` 通过 `GetCurrentMapInfo`、`std::map<int,map_monster>::find` 定位怪物，`0x08308FE4` 读 `[monster+0x20]`，`0x08308FE7` 令其 +1，`0x08308FED` 写回。`CBattle_Field::SetDamageValue(0x08308FF8)` 也查怪物，`0x0830908E` 读取 `[monster+0x24]`，`0x08309093` 与函数第三参数相加，`0x08309099` 写回。**这些字段是累计值，并非这两个函数里的 HP 扣减。**

### E46：校验后传入累计函数的是收到的报告值（H）

[同一反汇编](https://github.com/hustuhao/dnf/actions/runs/38507418346)：`Dispatcher_SDC_Damage_Check` 在 `0x081EA0E3–0x081EA0F7` 从 `CUser::GetPartyIndex` 经 `CGameManager::GetParty` 找到队伍，使用队伍内 `+0xB24` 指向的战场、报文结构 `+0x1CA` 对应的怪物键调用 `SetDamagedPacketCnt`，并在 `0x081EA123–0x081EA143` 以报告结构 `+0x1E6` 的**报告伤害值**调用 `SetDamageValue`，而不是以 `computeHpDamageSDC` 刚计算的校验值进行记录。`computeHpDamageSDC` ELF 符号长度 `0xAC8`，含 `getDamageInflict`、`isValidAttackInfoElement`、`SDC_Rand` 和浮点运算。**该路径不等于最终 HP 权威计算。**

## v0.6 对象所有权补充：2026-10-22（E47–E56）

远端基线实际为 v0.7 @ `3bc715164c1d9a56c36fd0555db18932270b699b`。
E40–E46 已有记录，本轮从 E47 续号；不覆盖既有证据。
统一来源：`build/dnf_data/home/template/init/df_game_r`，
Git blob `f7a65ba7bc723e96fadeae07e87b72e05560d989`，
SHA256 `8859c99d8290dc5fb58151444138cf2697b2bfff12d47d6159596a03f20b5261`，
ELF32 little-endian Intel x86 ET_EXEC；PT_LOAD 基址及入口沿用已重新核验的 E32。
工具：GNU binutils 2.44，完整符号边界 objdump；未执行游戏程序。
H=直接机器码/表数据；M=由已确认布局推导；U=未知。
复核：`python3 research/dungeon-sync/cloud/probe-instance-layout.py`；
完整函数及直接调用者留在 gitignored `artifacts-local/instance-layout-v06/`。

### E47

**H：战场为内嵌子对象，B=P+0xB24。**
CParty 构造入口 0x082A5516：
`0x082A55B1: 05 24 0b 00 00 / add eax,0xb24`，
`0x082A55B9: e8 40 ef ff ff / call 0x082A44FE`。
0x082A564A 的 lea 同一偏移给 SetParty，
0x082A5653 保存 P 到第二参数，0x082A565A 调 0x082A43BE，
后者 0x082A43C7 写 [B]=P。
正常析构 `0x082A58E5 add eax,0xb24`，
`0x082A58ED: e8 aa f0 ff ff / call 0x082A499C`。
不存在这里“从 P+0xB24 读取战场指针”的操作。
**M：** 活跃 P 不同则 B 不同；同队索引解析同一 P 则同一 B。
未做双客户端地址观测，不外推全部客户端状态相同。

### E48

**H：池复用、业务重置与 C++ 析构分离。**
SetIDX(0x082A59CA) 在 0x082A59D6 写 P+0x64，
0x082A59DF 调 init(0x0859A974)；
init 的 `0x0859ABE2: e8 0f f6 d6 ff / call 0x0830A1F6` 为 reset_field，
this 取 P+0xB24。
reset_field 的 `0x0830A33A: c7 80 88 01 00 00 00 00 00 00` 清 CDungeon*，
0x0830A40E 调 std::map<int,MapInfo>::clear(0x08311CEE)，实参 B+0x78。
destroy(0x0859AD4C) 的 0x0859AE48 调 init，0x0859AE5C 调 PutParty。
Pool::Free(0x082B11AA) 的 0x082B1214 调空闲 queue::push，
0x082B12F5 写节点 +0x1B04 的递减标志，完整函数没有 CParty 析构调用。
真正 B 析构的正常尾 0x082A4C3D 调 map 析构(0x082A43DE)。
**U：** 所有异常/断线/重连路径的最终清理条件未穷尽。

### E49

**H：MapInfo 按值存在每战场的 std::map<int,MapInfo> B+0x78。**
B 构造：`0x082A4557: 83 c0 78`，
`0x082A455D: e8 6e 66 00 00 / call 0x082AABD0`（map 构造）。
GetMapInfoFromPos(0x0822CC48) 的 0x0822CC7E 取 B+0x78，
0x0822CC98 调 find(0x08235C88)；
存在节点时 0x0822CCED 调 operator->，0x0822CCF2 取 pair+4；
缺失时 0x0822CD92 构造 MapInfo，0x0822CE10 调 insert(0x08235FEC)。
GetMapInfoKeyValue(0x0822CBBE)：
`0x0822CBC4: 6b c0 64 / imul eax,eax,0x64`，
0x0822CBC7 加 y，故键=100*x+y。
**H：** 另有 P+0x1AF4 vector<MapInfo>，0x082A5609 构造；用途 U。
GetMapInfoFromPos 的 layered 分支 0x0822CD51/0x0822CD67 与
getCurPosXY 的 seat 分支说明不能推广为所有副本全员永远同一 MapInfo。

### E50

**H：配置引用、难度与房间运行数据区分。**
dungeon_start 0x085A09D4 调 G_CDataManager，
0x085A09E0 调 find_dungeon(0x0835F9F8)，后者 0x0835FA0D 调 CDungeonList::find_dungeon。
SelectDungeon 的 `0x082FF6D7: 89 90 88 01 00 00` 把配置入参写到 B+0x188；
0x082FF4B6 调 set_dungeon_diff(0x0830ED1E)，
该 setter 在 `0x0830ED31: 89 90 a0 01 00 00` 保存 B+0x1A0，
之前将 unsigned byte 输入上限限制为 4。
getCurPosXY(0x08300DA6) 默认 0x08300E2E/0x08300E39 读 B+0x60/+0x64；
IsEnterEachMap 分支按 B+0x114 的 seat 索引取其他坐标。
ConsistMap 的 0x083031FB 读 MapInfo+4 配置索引，
0x08303208 调 getMap(0x08300ED4)，0x08303210 写 B+0x108。
**U：** 独立唯一副本运行 ID 未找到；队伍索引、CDungeon ID、地图键均不能直接充当它。

### E51

**H：真实注册索引与 SelectDungeon 虚调用解析。**
PacketDispatcher 构造(0x08590A2E)：
0x08590F2D 构造 SelectDungeon 后 0x08590F39 写 [this+0x40]；
0x085912BF 构造 DieMob 后 0x085912CB 写 +0xA8；
0x08591353 构造 GetItem 后 0x0859135F 写 +0xB8；
0x0859139D 构造 MoveMap 后 0x085913A9 写 +0xC0；
0x0859173A 构造 Select_Card 后 0x08591746 写 +0x128。
get_dispatcher(0x085948E2) 在
`0x08594908: 8b 04 90 / mov eax,[eax+edx*4]` 取项，无表头偏置；
因此 command 索引依次为 **16、42、46、48、74**。
doDispatch 的 0x0859492D/0x08594933 将 unsigned short 命令入参保存，
0x08594A20 调 get_dispatcher，0x08594D39 经 vtable 首项 call edx。
SelectDungeon 构造的 0x0859527C 写 vptr=0x08BDBDC8。
真实 .rodata vtable：+0=0x08258956（dispatch_template），
+0x14=0x081C7E10（read），+0x18=0x081C8102（process），+0x1C=0x081C8E9C（send）。
模板 0x082589B6、0x082589FE、0x08258A3E 分别调用这些槽；
process 内 0x081C8131 直接调用 check_error(0x081C7F32)。
**限制：** 这是 Game command 分派值；上游解密/完整包头、TCP/UDP 入口与线上时序未复原。

### E52

**H：进入副本的连续业务调用链与队员通知。**
process:0x081C8E0F → dungeon_start(0x085A0954)；
0x085A0D71 计算 P+0xB24，0x085A0DAE → SelectDungeon(0x082FF486)；
0x082FF70C → GetAppropriateMaze(0x082FF128)；
0x082FF764 → SetGridPath(0x082FFB30)；
0x082FF84F → MapInfo 构造(0x08151394)，
0x082FF8E7 → 本战场 map::insert(0x08235FEC)；
`0x082FF943: e8 8a 38 00 00` → ConsistMap(0x083031D2)。
普通发送分支 0x085A1697/0x085A16B0 为 put_header(0,28)，
0x085A16C5/0x085A16DE 追加 dungeon short / difficulty byte；
0x085A1701 → MakePacket(28)，0x085A1716 → send_to_party；
0x085A1747 → MakePacket(29)，0x085A175C → send_to_party。
MakePacket 的 0x08309107/0x0830911A 构造 (0,29) 头。
send_to_party:0x0859D194 → CUser::Send(0x086485BA)。
0x085A2046 → send_loadingcheck_msg(0x085B1FE0)，其 0x085B205B
实际是 InsertTimer，不是直接发包。
**U：** 客户端资源加载/ACK 完整链路、对象是否在实际双人会话被共享尚无动态观测。

### E53

**H：普通死亡处理是从入站 PacketBuf 解包进入的路径。**
DieMob::dispatch_sig 入口 0x081EB0C4；
0x081EB0E9/0x081EB131 为两个 get_short(unsigned short&)，
0x081EB179/0x081EB1C1 为两个 get_int(int&)，
0x081EB20B/0x081EB255 为两个 get_int(unsigned int&)，
0x081EB29D 为 get_byte(unsigned char&)。
这些是顺序固定前缀，后续有计数与重复字段，不能展开成固定全长。
0x081EB9B7/0x081EB9BC 比较 CUser::get_state()==5，
0x081EB9E4 按队伍索引查询非空 CParty，
0x081EBB73 调 CParty::kill_monster。
**已证实：** Game 接收用户连接上的报告；**U：** 发包客户端是否先接受 Host 计算、
是否限制为 Host、坐标/伤害/归属全部接受条件。本轮没有把存在反作弊函数写成已完成全面校验。

### E54

**H：死亡消费怪物记录，产生掉落/任务/经验/广播。**
CBattle_Field::kill_monster(0x0830BC78) 在 0x0830BCE9 取当前 MapInfo，
0x0830BCFA 取 MapInfo+0x0C；
`0x0830BD14: e8 41 67 e4 ff` 调 map<int,map_monster>::find；
0x0830BD4D/0x0830BD54 比较 end 并分支，未找到时
0x0830BE4D 令返回值=0 后跳尾。
成功路径 0x0830CD58 调 _MakeDropItems(0x0830ADF6)，
`0x0830D1C4: e8 7d 47 00 00` 对该怪物容器 erase，
0x0830D221 / 0x0830D336 调 IsClearDungeon。
CParty 层 0x085A2D11 调 OnKilledMonster，
0x085A3037 调 CheckQuestMonster，
0x085A3832 调 gain_exp_sp，0x085A39D6 调 send_to_party。
**限定：** 普通成功删除后同一活跃记录不可再次查到；特殊副本/复活/重新插入、
并发与奖励事务幂等性没有全面证明。E45 的累计量不等于当前 HP。
**U：** 对报告位置/伤害的完整判据、最终怪物 HP 扣减字段。

### E55

**H：存在服务端定时器触发的死亡处理，不能说所有死亡都仅来自客户端报告。**
TimerBossDieTimeout::dispatch_sig(0x0863647E) 的
`0x086364BC: e8 13 41 f7 ff` 调 OnTimeoutBossDie(0x085AA5D4)。
后者检查 P+0xC48 与入参 timer key（0x085AA5E2–0x085AA5EB），
0x085AA68B 取 GetMonsterMap，
将 map_monster+0x2C 非零的记录索引收集到 vector（0x085AA6D5–0x085AA6F2）。
0x085AA833 调 ActiveStaticInfo::getHpMax 填本地数据，
0x085AA85D 设置第三实参=0xFFFF，
`0x085AA876: e8 6d 7f ff ff` 调 kill_monster。
**M：** 这是受 timer/记录标志约束的超时补偿死亡路径。
**U：** 触发计时器的业务条件与 +0x2C 准确类型，是否针对哪些 Boss/模式；
不能据此推断普通逐次 HP 模拟，更不能把 getHpMax 当成读取当前 HP。

### E56

**H：Host 指针、manager 关系、通知及成员退出后的重选。**
getManager:0x08145786 返回 [P+0x74]；
set_host:0x0859CDC2 读 +0x74，
`0x0859CDC8: 89 50 70` 写 +0x70。
send_host_info(0x0859CDD2)：
0x0859CDE5 设置命令=26，0x0859CDFB 调 put_header(0,26)；
0x0859CE23/0x0859CE26 将 +0x70 与成员 CUser* 比较，
0x0859CE37 写槽号 byte，0x0859CE5C 广播。
leave_user(0x0859C114) 在 0x0859C664/0x0859C667 比较 manager 与离开用户，
0x0859C672 调 change_manager(0x0859C832)；
0x0859C8F2 检查有效成员，0x0859C915 保存首个有效成员到 +0x74，
0x0859C91E 调 set_host、0x0859C929 调 send_host_info。
**H：** 两字段分开保存，已检查 set_host 路径令两者相同；
不是两种角色概念永远等价的证明。
send_party_ipinfo(0x0859CEA2) 在 0x0859CEB5/0x0859CECB 组 (0,11)，
逐成员写 UID、内网 IP、外网 IP、port、acc id、NAT、MTU 及末 byte，
0x0859D119 调 send_to_party。
ConnectP2P(0x0859A48C) 检查 party state==1（0x0859A49D），
0x0859A57D 写 P+0x84+24*i 完成标志，
0x0859A5C1 将最多 4 字节复制到 P+0x86+24*i，
全部有效成员完成后 0x0859A609 调 ClearBadP2PUser。
ResPeer 的 0x081F13E6/0x081F141E 调 create_party/join_user，
0x081F14DD 调 send_party_ipinfo。
**U：** Host 单独断线而 manager 保留的迁移、断线到 leave_user 的完整入口、
具体 peer 战斗报文及 Host AI/命中计算范围。
