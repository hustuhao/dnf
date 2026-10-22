# Codex Cloud：DNF 多人地下城同步的第二阶段研究

仓库：https://github.com/hustuhao/dnf
工作分支：research/dungeon-sync-static-v1-20261011
研究目录：research/dungeon-sync/
已有 PR：https://github.com/hustuhao/dnf/pull/1

目标：在云端 x86-64 Linux 环境中，**用真实 `df_game_r` ELF 证据**识别普通多人副本状态、角色、怪物和游戏发包相关函数，补全目前以 Relay/STUN 为主的研究。

执行：
1. 阅读 research/dungeon-sync/AGENTS.md、README.md、evidence.md、open-questions.md。
2. 执行 bash research/dungeon-sync/cloud/verify-env.sh 并确认 Git HEAD、ELF 的 git blob/sha256、ELF32/ELF64、基址。
3. 执行 bash research/dungeon-sync/cloud/scan-static.sh（仅静态分析）。重点检查输出的 game/frida-address-map.csv 和 game/frida-disassembly/。
4. 将 frida.js 中 `CParty::UseAncientDungeonItems`、`CDungeon_get_index`、`MapInfo::Add_Mob`、`CUser_Send`、`PacketBuf_get_int` 的地址与 ELF 真实代码段、入口指令、调用者交叉引用。
5. 如果二进制符号被剥离，以准确指令地址和证据引用命名“候选函数”，不能虚构函数名；如果地址不匹配，优先定位版本差异，而非强行解释。
6. 判断是否能以代码事实支持“队伍/地下城运行时实例保存在 Game 进程”、“Game 转发或校验某些玩家数据”。请明确未知：移动、技能、伤害、怪物 AI、Host、掉落结算哪些未能从静态证据确认。
7. 只提交证据充分的 Markdown 研究增量、函数索引、Mermaid 调用图与新的验证任务，不提交游戏二进制副本、敏感字符串或原始 dump。
8. 在现有研究 PR 上提交变更，报告新增事实、证据等级、仍未知项及下一步实验方案。

限制：不要运行服务端二进制，不主动扫描公网、不连接生产/第三方服务器。遵循授权的隔离实验边界。
