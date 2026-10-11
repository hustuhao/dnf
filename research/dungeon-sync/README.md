# DNF 多人地下城实时同步机制研究（静态研究 v0.4）

> 基线：hustuhao/dnf，`main` @ `1d59eeafeaa105a3c109091c3d5fc061a30bbf19`；分析日期：2026-10-11。  
> 状态：**研究 v0.4**。已分析配置/Frida、Relay/STUN ELF 基本符号，并对 Relay 几个确定函数进行了机器码反汇编；未获得 Game ELF、未运行服务端或抓包。本文讨论的是**本仓库封装的 DNF 服务端版本**，不是所有 DNF 官方版本的通用结论。

## 先说结论

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

- 核心 `df_game_r` 是约 36 MB 预编译程序。**本版尚未读取 Game ELF 的符号、段信息、CFG 或反汇编**；`frida.js` 中的硬编码地址仅作为脚本中存在的线索。
- `doc/台服dnf服务架构.docx` 确实位于仓库，但本轮连接未能获取其二进制正文，未将其内容作为证据。
- 未验证客户端版本、PVF 内容、客户端发包代码、协议 ID、实测 UDP/TCP 流量。
- 请勿把 `frida.js` 中“怪物攻城”活动奖励逻辑扩展成普通地下城掉落、结算机制。
- 2026 年部署模板和历史架构文档有端口差异；优先保留具体配置上下文，不混用实例配置和历史默认值。

## 后续研究的成功判据

能使用**至少一条真实的两客户端实验捕获与对应的服务端处理证据**，明确：（1）副本实例状态在哪个进程；（2）移动消息的真实路由；（3）怪物/伤害权威；（4）掉落拾取及数据库持久化边界。实验前所有通关全链路图均属于候选模型。

本目录仅保存研究笔记、脱敏字段和测试设计；不提交真实账号、密钥、原始敏感封包或游戏客户端专有资源。

## 第二阶段结果：Relay/STUN 二进制静态解析

在 [binary-static.md](binary-static.md) 中已记录 Relay/STUN 的真实 ELF 格式、Blob SHA 与符号表地址。Relay 的 `TCPUser::onPacketParse`、`PacketHeaderS2S`、TCP/UDP/S2S `dispatch`、`setAuthenticated` 符号确实存在，STUN 也存在三个 `stunProcess` 入口及 RealIP/NAT/MTU 线程日志。这说明 Relay 有包解析和鉴权相关代码，而不能再仅根据服务名称概括为“透明转发”；**但尚无证据说明其理解技能或伤害的业务内容**。

`df_game_r` 约 36 MB，其文件正文受当前 GitHub 读取接口限制，**没有验证 Game ELF 的任何 Frida 地址**。已附带 [只读 ELF 检查脚本](tools/inspect-game-elf.sh) 供本地运行，核心研究问题仍见 [open-questions.md](open-questions.md)。

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
