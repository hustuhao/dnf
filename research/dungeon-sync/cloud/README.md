# DNF 多人地下城逆向研究 — 云端环境

本目录为 **hustuhao/dnf** 的隔离式静态研究工作环境服务，默认**不启动** `df_game_r` / `df_stun_r` / `df_relay_r`，不开放游戏端口、不连接游戏玩家、不进行未授权动态探测。

**当前研究分支：** `research/dungeon-sync-static-v1-20261011`；研究结果提交到 [PR #1](https://github.com/hustuhao/dnf/pull/1)，不用修改 `main`。

## 方案 A：GitHub Codespaces（有云端 Linux + 终端）

1. 打开仓库 [hustuhao/dnf](https://github.com/hustuhao/dnf)，切换至 `research/dungeon-sync-static-v1-20261011`。
2. 点击 **Code → Codespaces → Create codespace**，高级选项选择 Dev Container 配置文件 `.devcontainer/dungeon-research/devcontainer.json`。该文件属于**非默认配置**，不会改变仓库原有开发/部署环境。
3. 机器推荐 **4 vCPU / 16 GiB**（ELF/大型反编译更从容）；只跑 `readelf`/小范围 `objdump` 可以从更低规格开始。按你的 Codespaces 配额/计费确认用量。
4. Codespace 创建后会自动安装 `binutils`、`gdb`、`python3`、`graphviz`、`file`、`ripgrep` 等，并运行 `verify-env.sh` 校验 ELF 文件是否完整。
5. 开始第一轮全量静态扫描：

   ```bash
   bash research/dungeon-sync/cloud/scan-static.sh
   ```

6. 阅读本地生成的 `research/dungeon-sync/artifacts-local/cloud-scan/<UTC>/game/frida-address-map.csv` 和 `.../game/frida-disassembly/`，重点检查 `CParty` / `CDungeon` / `MapInfo` / `CUser_Send`。后续由 AI 将可复核、脱敏的结论写入 `evidence.md` / `architecture.md` / `open-questions.md`。

**云端持久性：** Codespace 停止后持久保存工作目录，但停止/删除策略取决于账户配置；建议频繁 `git commit`/推送已验证 Markdown，切勿只存云端临时磁盘。

## 方案 B：Codex Cloud（云端 AI 自动研究）

Codex Cloud 需要先在它的 Web/桌面界面**创建并发布可复用 Environment**；本仓库只提供可复用的 setup 脚本，不能代替在用户账号内真正完成发布。官方指南：[Using Codex Cloud](https://help.openai.com/en/articles/20001545-using-codex-cloud)。

1. 在 Codex Cloud 的 **Environments** 中连接 `hustuhao/dnf`；环境建议命名 `dnf-dungeon-sync-research`。
2. 选择任务工作分支 `research/dungeon-sync-static-v1-20261011`。如果环境设置时能访问该分支，setup 命令用：

   ```bash
   bash research/dungeon-sync/cloud/setup-codex.sh
   ```

   **如果 Setup 在默认分支 `main` 上运行、看不到上述脚本**，直接在 Cloud 环境 Setup 命令中粘贴以下等价的独立依赖安装命令（不依赖本仓库脚本）：

   ```bash
   sudo apt-get update && sudo apt-get install -y --no-install-recommends binutils file gdb git graphviz jq python3 python3-venv ripgrep strace ca-certificates curl
   ```

3. 选择环境网络访问策略：静态分析仅需要初始化时下载系统依赖和访问 GitHub，**研究任务执行时不需要任意公网扫描权限**。不要注入真实游戏账号、数据库密码或生产密钥。
4. 发布环境，启动新 Codex Cloud 研究任务，将 [`agent-task.md`](agent-task.md) 的提示词复制进去。要求 Codex 先核验完整二进制、运行只读扫描、整理函数调用证据并形成 PR。别把任务执行空间与环境创建空间混为一谈。
5. 云端任务完成后审查提交和证据；任务之间的未提交文件不一定可复用，因此将结论及时推送到研究分支。

## 提供的脚本

| 文件 | 用途 |
|---|---|
| `setup-codex.sh` | 用于 apt Linux / Codex Cloud 的工具安装（需要 root 或免密 sudo） |
| `verify-env.sh` | 验证工具存在及 Game/Relay/STUN 文件是有效 ELF，打印 Git blob SHA |
| `scan-static.sh` | 生成 ELF headers、segments、symbols、hash、Frida 地址映射和局部反汇编 |
| `check-frida-addresses.py` | 纯 Python 按 ELF 的 `PT_LOAD` 段标注 Frida 中的硬编码指针 |
| `agent-task.md` | 可交给 Codex Cloud 的一次性研究任务 |

## 研究规范

- **代码段命中不代表函数身份已确认。** Frida 对象名称和 hardcoded 地址需要 ELF 反汇编、调用者、运行时观测才能验证。
- 所有大型 ELF 解析产物与抓包数据都保存在被 `research/dungeon-sync/.gitignore` 忽略的 `artifacts-local/` 内，**不可未经审查将原始二进制字符串或网络捕获上传 GitHub**。
- 每条结论应包括 ELF 的 Git blob / SHA256、符号 VA、指令/代码行号、证据级别，以及还未验证的部分。
- 研究范围是授权的本地/云端静态分析；动态实验必须在获授权的隔离网络中。
- 当前仓库规模较大，首次 Codespaces 检出可能耗时较长；无需为了研究将完整数据搬到新仓库。

## 方案 C：GitHub Actions 可复现的只读 Game ELF 扫描（v0.5 已验证）

当 Codex Cloud Runner 当前会话无法连接时，可在原研究分支通过 [`.github/workflows/dungeon-game-static-evidence.yml`](../../../.github/workflows/dungeon-game-static-evidence.yml) 运行**无需启动服务器**的静态扫描。工作流 `contents: read`，以 sparse checkout 仅取 Game/Relay/STUN 三个 ELF、Frida 与研究脚本；依次执行 `verify-env.sh`、`scan-static.sh`、`probe-game-ownership.py`、`probe-game-paths.py`，在 Actions 日志输出有限的符号地址、函数机器码与直接调用交叉引用，不上传 ELF 或原始抓包。

**2026-10-12 已验证**：[第一次成功扫描](https://github.com/hustuhao/dnf/actions/runs/38208637857)、[含对象结构与业务入口的成功扫描](https://github.com/hustuhao/dnf/actions/runs/38208943902)。完整成果在 [Game ELF 静态报告](../game-owner-static.md)、[E32–E39](../evidence.md#v05完整-game-elf-只读反汇编2026-10-12)。注意 Actions 日志也可被仓库读者看到，输出只能包含已人工限定的非敏感函数名、指令和摘要信息。

`probe-game-ownership.py`：输出 `CGameManager/CParty/CBattle_Field/Dispatcher` 相关符号及少量函数边界内指令。  
`probe-game-paths.py`：输出入本、换图、怪物死亡、拾取、结算和发包函数的地址及静态直接调用引用。  
**两者只读、不加载执行 `df_game_r`，且只证明 ELF 静态调用路径。** 要确定真实多人对局共享地址、P2P/Host 与 Game 权威边界，仍须独立授权动态环境。
