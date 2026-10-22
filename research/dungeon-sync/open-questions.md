# 未解决问题与验证计划（按价值排序）

> 2026-10-22 更新：已补齐 v0.6 对象所有权任务；保留既有 v0.7。新结论以 [E47–E56](evidence.md#e47) 和 [对象布局补充](game-owner-static.md#instance-ownership-v06) 为准，以下旧版本段落保留研究历史。

每个问题遵循“假设 → 最小实验 → 能够证伪的观察 → 所需证据”，优先使用授权本地环境。当前所有实验均**尚未执行**。

## Q01：副本状态究竟保存在什么对象/进程？（P0）

**候选：** 频道 `df_game_r` 内的 `CParty` / 独立 dungeon-run 对象；或客户端/Host 持有重要实时状态。  
**切入点：** [E01](evidence.md#e01)、[E05](evidence.md#e05)、[E12](evidence.md#e12)、[E16](evidence.md#e16)。  
**步骤：** `file/readelf` 核对二进制版本 → 以 `CParty::UseAncientDungeonItems`、`CDungeon_get_index` 找调用者 → 在隔离测试服记录两支队伍进入同副本时对象内存/PID/实例 ID（如存在）。  
**判定：** 确定队伍↔副本状态映射，区分“地下城种类 ID”和“运行实例 ID”；检查队伍断线后对象存续。

## Q02：移动究竟经 Game 还是 Peer/Relay？（P0）

**候选：** Game 路径、P2P/Relay 路径或混合路径。  
**实验：** 两客户端+抓包静止基线、移动动作、测试网络直连 UDP 阻断、Relay 端流量校验，另记录 `CUser_Send` 关联栈。  
**证伪：** 直接观察 Game 产生的移动广播可削弱“完全 Peer-only”；客户端互通 UDP 可削弱“完全 Game-only”，但需从业务消息确认。

## Q03：谁决定普通伤害和怪物 HP？（P0）

**候选：** 客户端本地报告、Host、服务器或混合二阶段确认。  
**实验：** 匹配同一怪物的两玩家同步攻击，关联结果包、内存 HP/死亡回调和时序；勿使用对公网有影响的改包/攻击。  
**证伪：** 无证据前禁止断言服务器权威或客户端权威。`MapInfo::Add_Mob` 修改刷怪参数并非伤害计算证明。

## Q04：普通怪物 AI 在哪里运行，Host 掉线是否迁移？（P1）

**实验：** A/B 同步录屏和抓包，分别模拟队长与普通队员掉线，对比怪物位置、选目标、攻击事件是否继续；核对服务端 monster-update 调用栈。  
**需要：** 明确 Host 的判定信号，而不是假定队长等于 Host。

## Q05：技能表现、MP/CD 校验与广播如何拆分？（P1）

**实验：** 反向交叉引用 `PacketBuf_get_*` 和 `CUser_Send`；客户端技能输入与渲染时间测量；独立映射表现和结果事件。  
**需要：** 包类型由重复性捕获+解码/代码证据共同确认，不从大小猜测。

## Q06：普通掉落谁生成、拾取如何防重与结算如何幂等？（P1）

**实验：** 两客户端同时拾取一个可拾取物，比较操作完成确认与库存数据库；在本地可恢复快照执行提交前后进程重启测试。  
**需要：** 实际物品实例标识、事件处理函数、SQL 事务/索引、失败重试代码（均未发现）。

## Q07：切房间、失败/退出与副本实例销毁的时机？（P2）

**实验：** 每次切房与退出采集内存对象/世界状态/服务端日志和连接变化；区分资源回收与单纯玩家离开。

## Q08：断线重连是否保持原副本状态？（P2）

**实验：** 双人副本，一人断线、两人断线、队长断线、Game 崩溃四组；对比时限、队伍 ID、怪物/角色当前状态和奖励。  
**需要：** 客户端对“断线”定义、Game session 状态转移与恢复调用栈。

## Q09：Frida 的硬编码地址是否与仓库 ELF 对应？（P0，其他逆向工作前置）

**实验：** 读取 `sha256sum`、`file`、`readelf -h -l -S -Ws`；核对 32 位基址与所述地址所在可执行映射、函数边界和 Hook 成功日志；必要时 Ghidra。  
**重要：** 先完成版本核对，避免将其他 DNF 私服版本的地址/名称强行映射到本仓库。

## Q10：历史端口/官方 docx 与当前部署差异是什么？（P2）

**实验：** 完整提取 `doc/台服dnf服务架构.docx`、比较 `ArchitectureDiagram.md`、当前模板与真实部署环境展开值；分清 7200 vs 7300 与游戏频道 TCP/UDP 实际映射。

## 最小执行顺序

1. **静态 P0：** 校验 ELF 版本、整理反汇编交叉引用，确认 `CParty` / `CDungeon` 生命周期入口。
2. **联机 P0：** 两客户端建立稳定的 UDP/TCP/P2P 流量基线；先研究移动与 Game/Peer 边界。
3. **战斗 P0：** 技能、怪物受击、死亡分别同步录屏+流量+进程 Hook。
4. **持久化 P1：** 仅在隔离数据库快照做拾取并发与崩溃恢复。
5. **回填证据：** 每次实验为 `evidence.md` 增加编号、版本、测试环境、操作步骤、时序、pcap 哈希、Hook 调用栈、否定性观察与置信度；只有完成核验后才将结论从假设提升至已证实。

**不做：** 未经授权扫描公网、对真实玩家/第三方服务进行流量拦截、上传明文凭证或冒充运行实验结果。

## Q11：Relay 的报文解析深度和 S2S 实际含义是什么？（P0）

通过 [E23](evidence.md#e23) 已找到 `TCPUser::onPacketParse`、`TCPHandlerRelay::dispatch`、`UDPHandlerRelay::dispatch` 与 `UDPHandlerS2S::dispatch` 的实际 ELF 符号地址。下一步用 `objdump/Ghidra` 查分支与调用者，确认只是包长/认证/路由处理，还是具有游戏消息分类；之后在授权本地环境抓包交叉验证。

## Q12：STUN 三线程与三个端口怎样对应？（P1）

[E25](evidence.md#e25) 只证明三个 `stunProcess` 函数和 `RealIP/NAT/MTU_CHECKER` 标签存在。需反汇编线程创建者与 UDP 收发函数，不能仅凭端口号推定业务。

## Q13：客户端如何使用 STUN 的 0x01 / 0x05 / 0x02 消息？（P1）

在当前 STUN ELF 中已反汇编确认这三类数值的处理路径及 7 字节来源地址应答。[E30](evidence.md#e30) 但客户端是否依次请求不同 Socket、如何判断 NAT 映射与过滤方式、是否根据结果执行 Peer 握手，均未知。下一步通过客户端程序和已授权本地双端 pcap 做消息时序与字段字节序的交叉验证。

## Q14：端口模板是否真正支配当前 STUN ELF？（P1）

`stun/cfg/udp_server.cfg` 使用 `2__SERVER_GROUP__11/12/13`，但此 ELF 的 `main` 确实用 2311/2312/2313 立即数调用 `openPort`。[E29](evidence.md#e29) 检查部署脚本是否对二进制或端口做替换，确认是否存在通过环境变量、参数或补丁改写端口的路径。不能在未验证时宣称动态配置对所有部署无效。


## v0.5：P0 静态研究已经解答的部分（2026-10-12）

**Q09 的 ELF 版本前置检查已完成**：Git blob `f7a65ba7bc723e96fadeae07e87b72e05560d989`、SHA256 `8859c99d8290dc5fb58151444138cf2697b2bfff12d47d6159596a03f20b5261`；ELF32/x86 ET_EXEC，Frida `ptr` 162 次中 156 次处于可执行 PT_LOAD，重要函数通过真实符号与机器码确认（[E32](evidence.md#e32)）。地址落段不等于 Hook ABI 正确，也不代表所有声明均有效。

**Q01 的基础结构已得到高置信静态答案**：频道 `df_game_r` 内 `CGameManager::GetParty() 0x08294E10` 在 `0x08294E21` 获取 `StaticPool<CParty,600>` 对象，`GetParty(int) 0x08294F32` 在 `0x08294F52` 查 `hash_map<int,CParty*>`；`CUser::GetParty 0x0865514C` 的 `0x0865517B` 调用后者。`CParty` 构造函数在 `0x082A565A` 设置战场对象的队伍回指针；`CBattle_Field::GetDungeon 0x080FDCFC` 的 `0x080FDD02` 读取 CDungeon*。详见 [E33–E35](evidence.md#e33) / [v0.5 完整报告](game-owner-static.md)。

**新 P0 静态问题（按收益排序）：**

1. **准确锁定战场实例数据布局：** 从 `CParty::CParty` 的 `0x082A565A` 反向追踪实参，确定 `CBattle_Field` 对象实例是内嵌字段还是堆分配、何时初始化与销毁；静态推导 `CParty*` 和战场对象的地址关系。仅取匿名偏移，不上传内存 dump。
2. **包入口、字段、权限：** `DisPatcher_SelectDungeon::process` 的 `0x081C8E0F`、`DisPatcher_MoveMap::process` 的 `0x081C54D4`、`DisPatcher_DieMob::dispatch_sig` 的 `0x081EBB73`、`DisPatcher_GetItem::process` 的 `0x081C3905` 的上游解包及注册表。优先取出消息真实 ID 和参数布局；当前只确认直接 call。
3. **Host/P2P 与权威：** `CParty::set_host 0x0859CDBC` 的 `0x0859CDC8 mov [eax+0x70],edx` 与 `CParty::ConnectP2P 0x0859A48C`；调查 `DisPatcher_ResPeer`，辨明是否由某个客户端模拟实时怪物行为；**不能**因 `kill_monster` 存在而断言血量由服务端计算。
4. **共享对象运行验证（需单独授权的隔离服；本阶段不执行）：** 两个同队客户端读 `CUser` 队伍索引、`CParty*`、`CBattle_Field*`、Game PID；另用同频道不同队伍对照，检验“同队共享战场状态”和断线生命周期。

Q02–Q08 的实时模拟权威、网络时序、幂等与动态恢复 **仍然未知**，不可将当前 ELF 符号、函数名当作运行时证据。工作流扫描：[2026-10-12](https://github.com/hustuhao/dnf/actions/runs/38208943902)。

## v0.6 新增 P0：多人实时战斗权威边界

**Q15：`computeHpDamageSDC` 具体计算什么？** [E41](evidence.md#e41) 证明它被 `Dispatcher_SDC_Damage_Check` 调用，但必须反编译该函数的数据输入、结果使用和附近 `SetDamageValue` 的字段写入，区分“服务器重算或校验伤害”与“服务端拥有并扣减权威 HP”。建议针对 `0x08095C32` 和 `0x08308FF8` 做局部 CFG 与类型恢复。

**Q16：技能表现/命中/怪物位置哪些通过 P2P/Host？** Game 已有技能上报及 Host 信息代码，但仍需已授权双客户端在不同 NAT 条件下进行录屏+pcap 对齐，并分析客户端发送游戏消息与 peer 传输实现。只凭 Game ELF 不得宣称所有实时动作都经过服务器。

**Q17：`MSG_MONSTER_DIE` 的接受条件和去重机制是什么？** 根据 [E42](evidence.md#e42) 对 `DisPatcher_DieMob`、`CParty::kill_monster`、`CBattle_Field::kill_monster` 做控制流/状态字段与协议解析研究，检查 monster UID、重复死亡、damage check、可能的 Host 检查与结算唯一性。不可将存在检查函数等同于防作弊和幂等性已经完全有效。

**排除误判：** `Dispatcher_ChangeHp` 直接调用的是 PvP Assault 处理器，不能替代上述普通地下城 HP 研究。[v0.6 战斗专报](combat-authority-v0.6.md)。

## Q18：普通怪物 HP 的实际写入地址在哪里？（P0）

[E45](evidence.md#e45) 已证实 `SetDamageValue` 仅增加怪物对象 `+0x24` 的累计量，不是减血。下一步用 `map_monster` 的全部交叉引用找到 HP 字段、扣减操作的实际调用者，并比对 `DisPatcher_DieMob` 条件检查及可能的 Host 参与。

## Q19：伤害校验失败会阻止继续计入伤害吗？（P0）

`Dispatcher_SDC_Damage_Check` 使用 ±1 检查，并将异常交给 `CHackAnalyzer::addServerHackCnt`，但代码继续存在到 `SetDamageValue` 的路径。需精确分析反作弊阈值、是否会拒绝后续消息、是否影响战斗 HP 或仅记录处罚。

## Q20：多人客户端的实时命中/动画/AI 状态通过哪个网络路径同步？（P0）

Game 的 SDC 处理已证实，但不能据此得出最终判定由 Game、Host 还是客户端生成。需在授权隔离环境对两台客户端、Game TCP/UDP、P2P 与 Relay 实时抓包及录屏对齐，反查命中和怪物 HP 的真正来源。

## 2026-10-22：v0.6 所有权补充的解决项与剩余缺口

本节更新此前待办状态，不覆盖 v0.7 的伤害研究（E40–E46 已占用，本轮 E47–E56）。

| 旧问题 | 更新 |
|---|---|
| v0.5 P0：战场是否内嵌、偏移 | **已解决（静态 H）**：B=P+0xB24，构造/析构/SetParty 一致；E47 |
| v0.5 P0：MapInfo 保存何处 | **普通路径已解决（H）**：B+0x78 的 map<int,MapInfo> 按值节点，key=100*x+y；layered 分支及 P+0x1AF4 vector 用途待研究；E49 |
| Q01：同队共享与不同队隔离 | **Game 静态对象关系已解决**；相同索引查相同 P/B，不同活跃 P 的容器不同；实测、复用世代、跨进程恢复仍未知 |
| v0.5 P0：入本资源初始化 | **闭合至 Game 发包**：SelectDungeon → dungeon_start → B::SelectDungeon → 地图选择/插入 → ConsistMap → MakePacket/send_to_party；客户端 ACK 未闭合；E52 |
| v0.5 P0：opcode/注册 | **五项已解决**：command 16/42/46/48/74；固定前缀已列，复杂数组未全恢复；E51/E53 |
| Q17：普通怪物死亡接受/去重 | **部分解决**：状态/队伍/当前怪物查找、成功后 erase 已确认；位置/伤害/归属权限、所有特殊模式与奖励事务去重未解决；E53/E54 |
| v0.5 P0：Host 记录/迁移 | **部分解决**：+0x70 Host、+0x74 manager；set_host 复制后者；manager 离队选择首个有效成员并发通知。Host 独立断线与完整入口待查；E56 |
| 服务端是否存在主动死亡路径 | **存在（H）**：TimerBossDieTimeout → OnTimeoutBossDie → kill_monster；触发业务条件与适用模式仍未知；E55 |
| Q18/Q20：普通 current HP、AI、peer 战斗消息 | **仍未解决**，累计伤害与超时死亡不等于完整服务端实时模拟 |

新增按优先级排列：

1. **P0 / 尚未找到代码闭环**：反查 OnTimeoutBossDie 对应计时器的所有 InsertTimer
   来源和 map_monster+0x2C 的全部写入，明确“超时死亡”由谁启动；
   再找 current HP 的读写，与 E45 累计伤害严格区分。
2. **P0 / 只有间接证据**：找 Host+0x70 全部写入、断线入口至 leave_user 的
   分支和独立 Host 迁移；查 ConnectP2P 四字节结果与 ResPeer 的对应关系，
   确认 peer 连接控制与战斗数据之间的边界。
3. **P0 / 尚未完整解码**：DieMob 变长字段、STKillMonsterData 与 MSG_MONSTER_DIE
   的转换、位置/击杀归属/报告伤害检查条件；MapInfo 删除不等于结算事务幂等。
4. **P1 / 尚未找到**：独立运行实例 ID、池复用的 generation、加载 ACK 与
   地下城开始可战斗状态；P+0x1AF4 vector<MapInfo> 的用途。
5. **P1 / 必须动态验证才能回答实际运行问题**：获授权隔离双客户端记录同队
   P/B 与不同队对照、Host/manager 断线迁移、P2P/Relay 的物理路由和消息时序；
   本轮未运行服务端，不以静态可达当作实际触发。
