# DNF 多人地下城实时同步机制研究（Game ELF 静态研究 v0.7）

> 基线：hustuhao/dnf，`main` @ `1d59eeafeaa105a3c109091c3d5fc061a30bbf19`；分析日期：2026-10-11。  
> 状态：**研究 v0.7（2026-10-14）**。已在 GitHub Actions 对完整 `df_game_r` ELF 进行静态 `readelf/nm/objdump` 检查，补全队伍注册表、用户查找、战场关系及副本业务分发直接调用；仍未运行游戏服务或抓包。本文仅适用于本仓库 ELF 基线。下方 v0.4 条目保留作历史阶段记录。

## v0.6：多人战斗核心处理器已反汇编（2026-10-14）

**新证据：** 两轮 [Game ELF 战斗静态探针](https://github.com/hustuhao/dnf/actions/runs/38506571907)、[技能/伤害详细探针](https://github.com/hustuhao/dnf/actions/runs/38506766447) 已成功完成。发现：`DisPatcher_UseSkill::read/process` → `CHackLog_InvalidUsingSkill::IsValidUsingSkill` → `CParty::use_skill` → `CParty::OnUsedSkill`；另一条 `Dispatcher_SDC_Damage_Check` → `computeHpDamageSDC` → `CBattle_Field::SetDamagedPacketCnt / SetDamageValue`。死亡报告处理器 `DieMob` → `CParty::kill_monster`，再经怪物记录、命中统计和反作弊检查，确认服务端不仅负责发奖，还处理**部分技能与伤害检查业务**。

**依然未知：** 伤害是客户端/Host 算出还是 Game 最终裁决、P2P 中具体哪些是命中/动画、怪物 AI 执行地。注意 `Dispatcher_ChangeHp` 的直接调用目标属于 `pvp_assault`，不能作为普通 PvE HP 权威的证据。阅读 [v0.6 战斗专报](combat-authority-v0.6.md)、[E40–E43](evidence.md#e40)。

## v0.5 关键结论（优先阅读）

**已证实（完整 Game ELF 机器码）**：`df_game_r` 的 `CGameManager` 通过 `StaticPool<CParty,600>` 分配队伍并通过 `hash_map<int,CParty*>` 注册，`CUser::GetParty` 从用户对象读队伍索引后在管理器中查询 `CParty*`；`CParty` 构造阶段给 `CBattle_Field` 设置反向 `CParty*`，战场对象提供 `GetDungeon` / `GetCurrentMapInfo`。 `DisPatcher_SelectDungeon` / `MoveMap` / `DieMob` / `GetItem` / `Select_Card` 有直连 `CParty` 与战场方法的机器码调用。

**最可信的静态模型（中置信）**：每频道 `df_game_r` 通过 `CParty` 关联组队成员及副本级业务状态，`CBattle_Field` 承载相关地图/战场数据。但双客户端对象地址、每队唯一副本 ID 与 `CBattle_Field` 的分配方式仍未动态/完整数据流确认；**普通移动帧、逐次伤害计算、怪物 AI 权威属于未知**，不能据 Game 有死亡处理函数就断言服务端帧模拟。

完整函数地址、指令、置信度、两张 Mermaid 图及后续验证见 **[Game ELF v0.5 静态调用链](game-owner-static.md)**、[E32–E39](evidence.md#v05完整-game-elf-只读反汇编2026-10-12)，[Actions 验证记录](https://github.com/hustuhao/dnf/actions/runs/38208943902)。

## 先说结论（以下 v0.4 历史基线）

| 命题 | 证据级别 | 证据 |
|---|---|---|
| `df_game_r` 所在游戏服务负责地下城内游戏相关处理 | **已证实（架构文档对职责的明确陈述）**；实际内部实现待二进制核对 | [E01](evidence.md#e01) |
| 一个配置的频道对应一次 `df_game_r CHANNEL nofork` 启动，具备独立 TCP/UDP 端口 | **已证实（启动与配置）** | [E04](evidence.md#e04)、[E05](evidence.md#e05) |
| 游戏环境配置了 STUN、Relay 和 Game Server 三类端点；文档声称打洞失败时 Relay 中继 | **已证实（存在与文档宣称的用途）**；实际回退协议未知 | [E02](evidence.md#e02)、[E06](evidence.md#e06)、[E07](evidence.md#e07) |
| 游戏进程的 Hook 脚本可读队伍、地下城标识，并干预特定怪物攻城副本的刷怪/奖励逻辑 | **已证实（脚本实现与声明）**；所列地址是否与仓库二进制完全匹配未验证 | [E10](evidence.md#e10)、[E12](evidence.md#e12)、[E13](evidence.md#e13)、[E14](evidence.md#e14)、[E16](evidence.md#e16) |
| 每队独立副本实例及其运行时状态由 `df_game_r` 独占 | **待验证假设** | [Q01](open-questions.md#q01) |
| 位置/技能/怪物 AI/伤害分别由 P2P、Host 或服务器何者负责 | **未知** | [Q02](open-questions.md#q02)–[Q05](open-questions.md#q05) |
| 普通地下城掉落生成、拾取原子性与通关结算幂等机制 | **未知** | [Q06](open-questions.md#q06) |

**最有价值的新线索：** `frida.js` 的 `CParty::UseAncientDungeonItems` 替换 Hook 接收 `party, dungeon` 并调用 `CDungeon_get_index`；`CParty::OnFightVillageMonster` 与 `MapInfo::Add_Mob` Hook 改变特定副本怪物参数。它们为深入核验游戏进程的副本逻辑提供了具体的交叉引用锚点，**不等于**证明位置/伤害/AI 都由服务端权威模拟。

## 阅读顺序

1. [总体架构](architecture.md)：部署服务、职责、依赖和状态所有权候选图
2. [网络协议](network-protocol.md)：实际端口、STUN/Relay 两种候选路径、消息头配置和抓包方案
3. [副本生命周期](dungeon-lifecycle.md)：进入、房间切换、退出和断线重连
4. [移动同步](movement-sync.md)：消息链路竞争假设与双客户端测量
5. [战斗同步](combat-sync.md)：技能与伤害权威边界、怪物 AI、可用 Hook 点
6. [掉落与结算](loot-settlement.md)：活动特例与普通副本的证据隔离
7. [证据索引](evidence.md)：可追溯行号、代码地址、置信度说明
8. [待解决问题](open-questions.md)：分优先级的可证伪实验

## 证据分级

- **已证实**：被检查的源码、配置、启动脚本中的明确事实；如只是作者的架构说明，会限定成“**文档明确陈述**”，而不越界认定实际运行行为。
- **高可信推断**：两项或更多独立静态/运行证据支持，但尚未直接证实。
- **待验证假设**：合理候选解释；在图中用虚线或文字显式标注。
- **未知**：没有足够资料作出判断。

## 研究边界和缺口

- 核心 `df_game_r` 是约 36 MB 预编译程序。**v0.4 时**尚未读取 Game ELF；**v0.5 已获取真实 ELF 符号和局部反汇编**，但未完成全程序 CFG、全量间接跳转与动态协议确认。
- `doc/台服dnf服务架构.docx` 确实位于仓库，但本轮连接未能获取其二进制正文，未将其内容作为证据。
- 未验证客户端版本、PVF 内容、客户端发包代码、协议 ID、实测 UDP/TCP 流量。
- 请勿把 `frida.js` 中“怪物攻城”活动奖励逻辑扩展成普通地下城掉落、结算机制。
- 2026 年部署模板和历史架构文档有端口差异；优先保留具体配置上下文，不混用实例配置和历史默认值。

## 后续研究的成功判据

能使用**至少一条真实的两客户端实验捕获与对应的服务端处理证据**，明确：（1）副本实例状态在哪个进程；（2）移动消息的真实路由；（3）怪物/伤害权威；（4）掉落拾取及数据库持久化边界。实验前所有通关全链路图均属于候选模型。

本目录仅保存研究笔记、脱敏字段和测试设计；不提交真实账号、密钥、原始敏感封包或游戏客户端专有资源。

## 第二阶段结果：Relay/STUN 二进制静态解析

在 [binary-static.md](binary-static.md) 中已记录 Relay/STUN 的真实 ELF 格式、Blob SHA 与符号表地址。Relay 的 `TCPUser::onPacketParse`、`PacketHeaderS2S`、TCP/UDP/S2S `dispatch`、`setAuthenticated` 符号确实存在，STUN 也存在三个 `stunProcess` 入口及 RealIP/NAT/MTU 线程日志。这说明 Relay 有包解析和鉴权相关代码，而不能再仅根据服务名称概括为“透明转发”；**但尚无证据说明其理解技能或伤害的业务内容**。

`df_game_r` 约 36 MB。此段描述 **v0.2 的历史连接器限制**；v0.5 已通过 GitHub Actions 验证 Game ELF 和若干 Frida 入口。已附带 [只读 ELF 检查脚本](tools/inspect-game-elf.sh) 供本地运行，核心研究问题仍见 [open-questions.md](open-questions.md)。

## v0.3：Relay 消息控制流确认

[Relay 机器码调用链](relay-control-flow.md) 已实证：`UDPHandlerRelay::dispatch(0x805E4C0)` 在首字段为 0 的分支调用 `relayToTCP`；后者将消息首 16 位改成 3，从偏移 +8 读取标识，用 `getTCPUser` 找到 TCP 目标后调用 `TCPUser::send`。`TCPHandlerRelay::dispatch` 具有账号绑定 / 鉴权及另一条转发路径；`UDPHandlerS2S::dispatch` 具有授权和断开事件分支。

**此结果把 Relay 的“UDP 到 TCP 路由能力”提升到已由反汇编支持，但还未说明地下城战斗同步的路径及权威方。** 详见 [E26–E28](evidence.md#e26)。

## v0.4：STUN 内存级响应结构与端口已核验

从当前 `df_stun_r` 的实际 ELF64 机器码反汇编，已确认 `main` 用立即数 `2311/2312/2313` 依次创建 `RealIP/NAT/MTU` Socket 并创建 3 条对应处理线程。`msgProcess(0x401584)` 检查入站数据第一个字节：`0x01` 与 `0x05` 均生成 `0x02 + 4 字节源 IP + 2 字节源端口` 的七字节响应，其中 `0x05` 通过 2313 对应的第三 Socket 发送；`0x00` 直接成功返回。`stunProcess3` 则通过 UDP 回送实际接收长度的两字节字段。

**这是经 ELF 反汇编证实的代码逻辑，不是抓包后的完整协议规范。** 详见 [stun-protocol.md](stun-protocol.md)、[E29–E31](evidence.md#e29)。无法据此确认客户端 NAT 分类、打洞重试次数、P2P/Relay 切换机制及地下城战斗同步边界。

## 云端研究环境（Codespaces / Codex Cloud）

仓库已提供独立的 [GitHub Codespaces 开发容器](../../.devcontainer/dungeon-research/devcontainer.json) 和 [Codex Cloud 安装/研究任务](cloud/README.md)，用于克服 GitHub 文本接口无法读取大型 `df_game_r` ELF 的限制。云端首次启动需在本人账号内手动授权/发布；配置文件已提交并不等于云服务器实例已经运行。

先在专用研究分支上创建环境，然后执行：

```bash
bash research/dungeon-sync/cloud/verify-env.sh
bash research/dungeon-sync/cloud/scan-static.sh
```

该扫描只读取二进制并生成本地 gitignored 报告，不执行 `df_game_r`。下一步优先检查 `frida-address-map.csv` 与 `CParty/CDungeon/MapInfo` 调用者。

## v0.7：伤害校验已定位到实质数据字段

[详细研究](damage-check-v0.7.md) | [最新静态验证工作流](https://github.com/hustuhao/dnf/actions/runs/38507418346) | [证据 E44–E46](evidence.md#e44)

`Dispatcher_SDC_Damage_Check` 会解压输入，调用 `computeHpDamageSDC` 重算并以 **±1** 容差检查报告的伤害值，异常进入 `CHackAnalyzer::addServerHackCnt`；随后在 Game 内部根据队伍找到当前怪物记录，将 `map_monster+0x20` 计数加一、`map_monster+0x24` 增加**报告的伤害值**。两个 Setter **不是直接扣除怪物 HP**；实时伤害与怪物 AI 的权威仍需客户端/P2P 证据。
