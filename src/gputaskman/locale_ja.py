"""Japanese catalog: each key is an English string exactly as it appears in the source.

A key with no entry falls back to English. tests/test_i18n.py names the missing and the stale keys.
"""

from __future__ import annotations

_UI = {
    "Quit": "終了",
    "Sort": "並べ替え",
    "Chart": "グラフ",
    "All/Top": "全部/上位",
    "Pause": "一時停止",
    "Explain": "説明",
    "Close": "閉じる",
    "palette": "コマンドパレット",
    "Sampling GPU counters...": "GPUカウンターをサンプリング中...",
    "Charts": "グラフ",
    "All charts": "すべてのグラフ",
    "Click to choose · c cycles": "クリックで選択 ・ cキーで切り替え",
    "GPU": "GPU",
    "SM clock": "SMクロック",
    "GFX clock": "GFXクロック",
    "SM/GFX clock": "SM/GFXクロック",
    "VRAM": "VRAM",
    "Mem activity": "メモリ稼働",
    "Temperature": "温度",
    "Power": "電力",
    "Encoder": "エンコーダー",
    "Decoder": "デコーダー",
    "GPU%": "GPU%",
    "spill": "共有RAM",
    "paged": "非常駐",
    "name": "名前",
    "PID": "PID",
    "Process": "プロセス",
    "Kind": "種類",
    "Runtime": "ランタイム",
    "Spill": "共有RAM",
    "Paged": "非常駐",
    "3D": "3D",
    "Copy": "Copy",
    "Video": "Video",
    "What's inside": "中身",
    "model": "モデル",
    "arch": "アーキテクチャ",
    "params": "パラメーター数",
    "quant": "量子化",
    "layers": "レイヤー数",
    "train ctx": "学習時ctx",
    "on GPU (est)": "GPU上(推定)",
    "evidence": "根拠",
    "file": "ファイル",
    "unified memory": "ユニファイドメモリ",
    "driver {version}": "ドライバー {version}",
    "[PAUSED]": "[一時停止中]",
    "GPU mem": "GPUメモリ",
    "unattributed {size}": "未帰属 {size}",
    "free {size}": "空き {size}",
    "shared(RAM) {size}": "共有RAM {size}",
    "[bar normalized; labels are raw]": "[バーは合計に合わせて正規化。ラベルは生の値]",
    "throttle: {reasons}": "スロットリング: {reasons}",
    "Recent samples · blank = no reading": "直近のサンプル ・ 空白 = 読み取りなし",
    "Recent samples · blank = no reading · power 0–{power_scale:.0f} W · {clock} clock 0–{clock_scale:.0f} MHz":
        "直近のサンプル ・ 空白 = 読み取りなし ・ 電力 0-{power_scale:.0f} W ・ {clock}クロック 0-{clock_scale:.0f} MHz",
    "sort: {sort}  ·  all processes": "並べ替え: {sort}  ・  すべてのプロセス",
    "sort: {sort}  ·  top processes": "並べ替え: {sort}  ・  上位のプロセス",
    "No Linux process in this distro has the GPU open (other WSL distros and Docker Desktop "
    "are not visible from here).":
        "このディストリビューションには、GPUを開いているLinuxプロセスがありません"
        "（他のWSLディストリビューションやDocker Desktopはここからは見えません）。",
    "macOS: unified memory, so GPU memory is part of system RAM. Rows show each process's graphics "
    "footprint; other users' processes (WindowServer, daemons) show GPU% only, since reading their "
    "memory needs root.":
        "macOS: ユニファイドメモリのため、GPUメモリはシステムRAMの一部です。各行にはプロセスごとのグラフィックスの"
        "footprintを表示します。他のユーザーのプロセス（WindowServer、デーモン）はメモリの読み取りにrootが必要なため、"
        "GPU%のみを表示します。",
}
_INSPECTOR = {
    "Select a process (↑/↓) to see what's inside its GPU memory.  Press ? to learn what's knowable.":
        "↑/↓キーでプロセスを選択すると、そのGPUメモリの中身を表示します。?キーで、わかること・わからないことを説明します。",
    "host PID": "ホストPID",
    "GPU unknown": "GPU不明",
    "idle": "アイドル",
    "spill(RAM)": "共有RAM",
    "paged(est)": "非常駐(推定)",
    "engines": "エンジン",
    "runtime": "ランタイム",
    "No per-process VRAM: {reason}.": "プロセスごとのVRAMは取得できません: {reason}。",
    "GPU memory n/a: footprint can't read other users' processes without root "
    "(or hasn't measured this one yet). GPU% comes from Metal's per-process GPU time.":
        "GPUメモリはn/aです。footprintはroot権限がないと他のユーザーのプロセスを読み取れません"
        "（このプロセスをまだ測定していない場合もあります）。GPU%はMetalのプロセスごとのGPU時間に基づく値です。",
    "Resident VRAM {vram}, GTT {gtt}. {note}": "常駐VRAM {vram}、GTT {gtt}。{note}",
    "Resident: every buffer the process can reach, shared ones included. The same buffer can "
    "appear under several processes, so these are not added up.":
        "常駐: プロセスが到達できるすべてのバッファー（プロセス間共有バッファーを含む）。同じバッファーが"
        "複数のプロセスに現れることがあるため、合算はしません。",
    "Engines n/a: this process uses ROCm/HIP (/dev/kfd), whose compute queues the kernel doesn't "
    "time per process. The device's AMD gfx load includes its work.":
        "エンジンはn/aです。このプロセスはROCm/HIP(/dev/kfd)を使っており、そのコンピュートキューはカーネルが"
        "プロセスごとには計時しません。デバイス全体のAMD gfx負荷には、このプロセスの処理も含まれます。",
    "{paged} of {committed} committed is not accounted for by local/non-local "
    "usage. Estimated non-residency, not proof of eviction or disk paging.":
        "コミット済みの{committed}のうち、{paged}はLocal UsageにもNon Local Usageにも計上されていません。"
        "推定の非常駐であり、退避やディスクへのページングの証拠ではありません。",
    "Handy selected (settings; not load proof): {model}":
        "Handyで選択中（設定ファイルの値。ロードの証拠ではありません）: {model}",
    "Handy last event: {event} {model} at {time} (runtime-reported history, not current GPU residency)":
        "Handyの最新イベント: {event} {model}、{time}（ランタイム報告の履歴であり、現在のGPU常駐を示すものではありません）",
    "Model files, launch flags and runtime buffer logs can span GPUs. "
    "The breakdown below is not a measured per-device model placement.":
        "モデルファイル、起動フラグ、ランタイムのバッファーログは、複数のGPUにまたがることがあります。"
        "以下の内訳は、デバイスごとのモデル配置を実測したものではありません。",
    "(allocated sizes from {log})": "（割り当てサイズの出典: {log}）",
    "server": "サーバー",
    "slots busy {busy}/{total}": "スロット使用中 {busy}/{total}",
    "gen {rate:.1f} tok/s": "生成 {rate:.1f} tok/s",
    "prompt {rate:.0f} tok/s": "プロンプト {rate:.0f} tok/s",
    "loaded: {name} {type} {quant} ctx {ctx}": "ロード済み: {name} {type} {quant} ctx {ctx}",
    ", {kind}": "、{kind}",
    "file: {name}  ({size}, {evidence}{kind})": "ファイル: {name}（{size}、{evidence}{kind}）",
    "No mapped model file was observed. Some runtimes read then close model files. "
    "Installed candidates (not proven loaded):":
        "マップされたモデルファイルは確認できませんでした。モデルファイルを読み込んだあと閉じるランタイムもあります。"
        "インストール済みの候補（ロードされているかは未確認）:",
    "{name}  ({size}{kind})": "{name}（{size}{kind}）",
    "listening: {ports}": "待ち受けポート: {ports}",
    "(protected process - run elevated for runtime/file details)":
        "（保護されたプロセスです。ランタイムやファイルの詳細を見るには、管理者として実行してください）",
    "DRM process scan: {status}.": "DRMプロセススキャン: {status}。",
}
_KINDS = {
    "LLM": "LLM",
    "decision": "意思決定",
    "decision?": "意思決定?",
    "embedding": "埋め込み",
    "speech": "音声",
    "diffusion": "拡散",
    "AI": "AI",
    "compute": "コンピュート",
    "3D/game": "3D/ゲーム",
    "video": "ビデオ",
    "browser": "ブラウザー",
    "app": "アプリ",
    "compositor": "コンポジター",
    "kernel": "カーネル",
    "system": "システム",
    "wsl-vm": "WSL VM",
    "external": "外部",
}
_EXPLAIN = {
    "The WSL virtual machine as Windows sees it. Windows charges all GPU memory used by Linux processes "
    "in every WSL distro (and WSLg) to vmwp.exe, so this is the exact total. The split across Linux "
    "processes is not exposed.":
        "Windowsから見たWSL仮想マシンです。Windowsは、すべてのWSLディストリビューション（およびWSLg）の"
        "Linuxプロセスが使うGPUメモリをまとめてvmwp.exeに計上するため、この値が正確な合計になります。"
        "Linuxプロセスごとの内訳は取得できません。",
    "Desktop Window Manager: its own back buffers and the composed image for each monitor. "
    "Windows' 'Dedicated Usage' counter shows dwm as huge (it counts every app surface it can see); "
    "this tool prefers Local Usage for attribution. The adapter counter is the total; "
    "per-process samples can overlap or differ in timing.":
        "デスクトップウィンドウマネージャー: 自身のバックバッファーと、モニターごとの合成済みイメージです。"
        "Windowsの「Dedicated Usage」カウンターは、見えているすべてのアプリのサーフェスを数えるため、"
        "dwmを巨大に表示します。このツールは、プロセスへの帰属にLocal Usageを優先して使います。"
        "合計の基準はアダプターのカウンターで、プロセスごとのサンプルは重複したり、取得タイミングがずれたりすることがあります。",
    "Driver/kernel-owned allocations: paging buffers, display scan-out, firmware, scheduler state.":
        "ドライバー/カーネルが所有する割り当て: ページングバッファー、ディスプレイのスキャンアウト、"
        "ファームウェア、スケジューラーの状態。",
    "Session/system process holding display and cursor surfaces.":
        "ディスプレイとカーソルのサーフェスを保持するセッション/システムプロセス。",
    "Chromium GPU process: page tiles, images, video frames, canvas, WebGL/WebGPU buffers. "
    "Deeper: edge://gpu, or DevTools > Performance with the GPU track.":
        "ChromiumのGPUプロセス: ページのタイル、画像、ビデオフレーム、canvas、WebGL/WebGPUのバッファー。"
        "詳しくはedge://gpu、またはDevToolsの「パフォーマンス」でGPUトラックを確認してください。",
    "Textures, meshes, render targets and descriptor heaps. Windows only sees opaque allocations; "
    "per-resource names need a graphics debugger (PIX on Windows, NVIDIA Nsight Graphics).":
        "テクスチャ、メッシュ、レンダーターゲット、ディスクリプターヒープ。Windowsから見えるのは中身の分からない"
        "割り当てだけで、リソースごとの名前を知るにはグラフィックスデバッガー（WindowsではPIX、NVIDIA Nsight Graphics）が必要です。",
    "Decoded/encoded video frames and codec surfaces (NVIDIA NVDEC/ENC)":
        "デコード/エンコードされたビデオフレームとコーデックのサーフェス(NVIDIA NVDEC/ENC)",
    "Compute allocations are opaque to the OS. Runtime-specific profilers can provide more detail "
    "(CUDA: cudaMalloc with Nsight Systems).":
        "コンピュートの割り当ては、OSからは中身が分かりません。詳細はランタイム固有のプロファイラーで確認できます"
        "（CUDA: Nsight SystemsでcudaMallocを確認）。",
    "Model components are identified from launch arguments; GPU allocations cannot be split by component.":
        "モデルのコンポーネントは起動引数から識別しています。GPU上の割り当てを、コンポーネントごとに分けることはできません。",
    "ML runtime allocations (tensors, workspaces). PyTorch: torch.cuda.memory_summary(); "
    "ONNX Runtime/DirectML pools are opaque from outside.":
        "MLランタイムの割り当て（テンソル、ワークスペース）。PyTorchではtorch.cuda.memory_summary()で確認できます。"
        "ONNX Runtime/DirectMLのプールは、外部からは中身が分かりません。",
    "UI surfaces: swap chains, window back-buffers, cached bitmaps/glyphs.":
        "UIのサーフェス: スワップチェーン、ウィンドウのバックバッファー、キャッシュされたビットマップ/グリフ。",
}
_HELP = {
    "# What can be known about GPU memory?": "# GPUメモリについて何がわかるのか?",
    (
        '| Layer | Source | Works for |\n'
        '|---|---|---|\n'
        '| **Device** telemetry | NVML, AMD ADL, or optional AMD SMI; amdgpu sysfs on Linux | availability varies by GPU and driver |\n'
        '| **Per-process** VRAM, spill to RAM, per-engine load | Windows WDDM counters (dxgkrnl); DRM fdinfo for amdgpu on Linux | workloads visible to WDDM or DRM |\n'
        '| **Which runtime** (CUDA, HIP, Vulkan, D3D12, ggml, ONNX, PyTorch...) | DLLs mapped in the process | everything |\n'
        '| **Which model file** | memory-mapped files + command line | llama.cpp, stable-diffusion.cpp, LM Studio, Ollama |\n'
        '| **Model name & kind** (LLM, decision, embedding, speech) | GGUF header, Ollama/LM Studio/Hugging Face stores, local server APIs | GGUF family |\n'
        '| **Weights / KV cache / compute** split | GGUF header math, llama.cpp/Ollama logs, local server APIs | GGUF/llama.cpp family |\n'
        '| Per-texture / per-buffer names | needs a debugger (PIX, Nsight) attached to the app | games, 3D apps |'
    ): (
        '| 階層 | 情報源 | 対象 |\n'
        '|---|---|---|\n'
        '| **デバイス**のテレメトリ | NVML、AMD ADL、または任意のAMD SMI。Linuxではamdgpuのsysfs | GPUとドライバーによって 利用可否が異なる |\n'
        '| **プロセスごと**のVRAM、 共有RAMへのスピル、 エンジンごとの負荷 | Windows WDDMカウンター(dxgkrnl)。 LinuxのamdgpuではDRM fdinfo | WDDMまたはDRMから 見えるワークロード |\n'
        '| **どのランタイムか** (CUDA, HIP, Vulkan, D3D12, ggml, ONNX, PyTorch...) | プロセスにマップされているDLL | すべて |\n'
        '| **どのモデルファイルか** | メモリマップされたファイル + コマンドライン | llama.cpp, stable-diffusion.cpp, LM Studio, Ollama |\n'
        '| **モデル名と種類** （LLM、意思決定、 埋め込み、音声） | GGUFヘッダー、Ollama/LM Studio/Hugging Faceのストア、 ローカルサーバーのAPI | GGUF系 |\n'
        '| **重み / KVキャッシュ / 計算バッファー**の内訳 | GGUFヘッダーからの算出、 llama.cpp/Ollamaのログ、 ローカルサーバーのAPI | GGUF/llama.cpp系 |\n'
        '| テクスチャ・バッファーごとの名前 | アプリにデバッガー(PIX, Nsight)をアタッチする必要がある | ゲーム、3Dアプリ |'
    ),
    (
        '**Evidence** shows how a model was identified: `api` (the runtime says it is loaded), `mapped`\n'
        '(Windows shows the file mapped into the process right now), `cmdline` (a launch argument only).\n'
        'Two sources, including `api` or `mapped`, is shown as *confirmed*.'
    ): (
        '**根拠**は、モデルをどのように特定したかを示します。`api`（ランタイムがロード済みだと報告している）、'
        '`mapped`（Windowsが、そのファイルが今プロセスにマップされていると示している）、'
        '`cmdline`（起動引数に指定されているだけ）。`api`または`mapped`を含む2つ以上の情報源がそろった場合は、'
        '「確認済み」と表示します。'
    ),
    (
        '**Local workloads only:** inference, decision models, vision, speech, training, graphics and video.\n'
        "Cloud-hosted models are outside this monitor's scope. DLLs identify runtimes, not models or tasks.\n"
        '`decision?` / *likely decision model (name)* is a filename or model-folder hint when a specific\n'
        'GGUF kind is missing. It does not confirm the kind, GPU residency, or execution. Installed\n'
        'candidates remain unproven; engine activity is measured per process, not per model.'
    ): (
        '**ローカルのワークロードのみ:** 推論、意思決定モデル、ビジョン、音声、学習、グラフィックス、ビデオ。'
        'クラウドでホストされているモデルは、このモニターの対象外です。DLLから特定できるのはランタイムであり、'
        'モデルやタスクではありません。種類列の「意思決定?」と「意思決定モデルの可能性（名前から）」は、'
        '具体的なGGUFの種類がないときに、ファイル名またはモデルフォルダー名から出すヒントです。'
        '種類、GPU上の常駐、実行のいずれも確認するものではありません。インストール済みの候補は未確認のままで、'
        'エンジンの稼働はプロセスごとに実測しており、モデルごとではありません。'
    ),
    (
        '**Linux / WSL:** on native Linux, per-process VRAM and SM/encoder/decoder load come from NVML\n'
        '(no spill or commit counters exist there, so those columns stay blank). **AMD GPUs on Linux**\n'
        '(`amdgpu`) use sysfs for the device and DRM fdinfo (`/proc/<pid>/fdinfo`) per process: VRAM,\n'
        "GTT (GPU memory in system RAM, shown as SPILL), and gfx/compute/video engine time (`n/a` for a new client's\n"
        "first sample and for ROCm/HIP processes: their compute runs on `/dev/kfd` queues the kernel doesn't time per\n"
        'process). VRAM and SPILL are charged to a process only when its DRM clients are provably private: one holder,\n'
        'opened through a render node, and no shared buffers. Otherwise they show `n/a` and the bytes stay unattributed;\n'
        'the inspector still shows the resident bytes it can reach (shared buffers included, so not added up). Only processes you can inspect are\n'
        "listed, and the header says how many it couldn't; run with `sudo` to see other users'. Under **WSL**, Windows\n"
        'charges all Linux GPU memory to the VM (`vmwp.exe`), so VRAM and load are device-wide only; rows\n'
        'are Linux processes with `/dev/dxg` open and show `n/a` rather than a made-up share. When WSL\n'
        "interop is enabled, the Windows host's counters are read through `powershell.exe`: **WSL VM**\n"
        '(`vmwp.exe`) is then the exact total of Linux GPU memory, and Windows apps appear as `W:<pid>`\n'
        "rows. `--no-host` turns this off. Linux rows get their VRAM by matching the VM's GPU contexts\n"
        '(newest first) to Linux processes: `*` when candidates agree on the size, `?` for a heuristic owner.\n'
        'Cached foreign sizes only help rank guesses; they never prove ownership across runs.'
    ): (
        '**Linux / WSL:** ネイティブLinuxでは、プロセスごとのVRAMとSM/エンコーダー/デコーダーの負荷はNVMLから取得します'
        '（共有RAMやコミットのカウンターは存在しないため、それらの列は空欄のままです）。'
        '**LinuxのAMD GPU**(`amdgpu`)では、デバイスにはsysfsを、プロセスごとにはDRM fdinfo(`/proc/<pid>/fdinfo`)を使い、'
        'VRAM、GTT（システムRAM上のGPUメモリ。共有RAMとして表示）、gfx/コンピュート/ビデオの各エンジン時間を取得します'
        '（新しいクライアントの最初のサンプルと、ROCm/HIPのプロセスでは`n/a`です。後者のコンピュートは'
        '`/dev/kfd`のキューで実行され、カーネルがプロセスごとには計時しないためです）。'
        'VRAMと共有RAMは、そのプロセスのDRMクライアントが他と共有されていないと確認できる場合'
        '（保持者が1つで、レンダーノード経由で開かれ、プロセス間共有バッファーがない場合）にだけ、そのプロセスに計上します。'
        'それ以外は`n/a`と表示し、そのバイト数は未帰属のままにします。'
        'インスペクターには、到達できる常駐バイト数（プロセス間共有バッファーを含むため、合算はしません）を引き続き表示します。'
        '検査できるプロセスだけを一覧に表示し、検査できなかった数はヘッダーに表示します。'
        '他のユーザーのプロセスを見るには`sudo`で実行してください。'
        '**WSL**では、WindowsがLinuxのGPUメモリをすべてVM(`vmwp.exe`)に計上するため、VRAMと負荷はデバイス全体の値しか得られません。'
        '行は`/dev/dxg`を開いているLinuxプロセスで、根拠のない割合は示さず`n/a`と表示します。'
        'WSLの相互運用が有効な場合は、Windowsホストのカウンターを`powershell.exe`経由で読み取り、'
        '**WSL VM**(`vmwp.exe`)がLinuxのGPUメモリの正確な合計になり、Windowsのアプリは`W:<pid>`の行として表示されます。'
        '`--no-host`でこれを無効にできます。LinuxのプロセスのVRAMは、VMのGPUコンテキスト（新しい順）をLinuxプロセスに'
        '対応付けて求めます。候補のサイズが一致する場合は`*`、ヒューリスティックな所有者の場合は`?`を付けます。'
        'キャッシュされた外部サイズは推測の順位付けに使うだけで、実行をまたいで所有を証明することはありません。'
    ),
    (
        '**Why does nvidia-smi say N/A?** GeForce cards on Windows run in *WDDM* mode: Windows, not the\n'
        "NVIDIA driver, owns video memory, so NVML can't attribute it to processes. The Windows counters can."
    ): (
        '**nvidia-smiがN/Aと表示するのはなぜですか?** Windows上のGeForceは*WDDM*モードで動作します。'
        'ビデオメモリを管理するのはNVIDIAドライバーではなくWindowsなので、NVMLはメモリをプロセスに帰属させられません。'
        'Windowsのカウンターなら帰属させられます。'
    ),
    (
        '**dwm.exe looks huge elsewhere?** Windows\' per-process "Dedicated Usage" counts every surface a\n'
        "process can *see*, so dwm can show nearly the whole card. VRAM here is what's charged to each\n"
        'process ("Local Usage" when available). The adapter counter is the total, not the sum of rows.'
    ): (
        '**他のツールでdwm.exeが巨大に見えるのはなぜですか?** Windowsのプロセスごとの「Dedicated Usage」は、'
        'そのプロセスから*見える*すべてのサーフェスを数えるため、dwmがカード全体に近い量を使っているように見えることがあります。'
        'ここでのVRAMは、各プロセスに計上された分です（利用できる場合は「Local Usage」）。'
        '合計の基準はアダプターのカウンターであり、各行の合計ではありません。'
    ),
    (
        '**SPILL** = GPU-accessible system RAM. This can include pinned host buffers or intentional\n'
        'allocations, not just overflow. Large usage under VRAM pressure can indicate fallback;\n'
        'the counter alone does not prove it.'
    ): (
        '**共有RAM**（SPILL）= GPUからアクセスできるシステムRAM。ピン留めされたホストバッファーや意図的に確保した領域も'
        '含まれるため、あふれ分だけとは限りません。VRAMが逼迫しているときに使用量が大きい場合は、'
        'フォールバックを示している可能性がありますが、このカウンターだけでは断定できません。'
    ),
    (
        '**PAGED** = max(Total Committed - Local Usage - Non Local Usage, 0). This is an estimate of\n'
        'non-resident committed memory, not a measured eviction count or proof of pagefile activity.'
    ): (
        '**非常駐**（PAGED）= max(Total Committed - Local Usage - Non Local Usage, 0)。'
        'コミット済みのうち非常駐のメモリを推定した値であり、退避回数の実測値でも、ページファイルが使われた証拠でもありません。'
    ),
    (
        '**Inside** labels are inferred from runtimes and files. Log sizes describe allocated buffers,\n'
        "not necessarily current residency. A game's textures cannot be enumerated here."
    ): (
        '**中身**の表示は、ランタイムとファイルからの推測です。ログのサイズは割り当て済みのバッファーを表すもので、'
        '現在の常駐量とは限りません。ゲームのテクスチャは、ここでは列挙できません。'
    ),
    (
        '**GPU%** = busiest engine (like Task Manager). On GeForce/WDDM, CUDA kernels are usually reported\n'
        'on the **3D** engine. AMD device GPU charts show graphics-engine activity, which is not\n'
        "necessarily equivalent to NVML GPU utilization. Vulkan does not expose another process's HIP internals."
    ): (
        '**GPU%** = 最も使用率の高いエンジンの値（タスク マネージャーと同様）。GeForce/WDDMでは、CUDAカーネルは通常'
        '**3D**エンジンとして報告されます。AMDデバイスのGPUグラフはグラフィックスエンジンの稼働を示しており、'
        'NVMLのGPU使用率と同等とは限りません。Vulkanでは、他のプロセスのHIP内部は見えません。'
    ),
    'Keys: `↑/↓` select · `s` sort · `c` chart · `a` show all · `p` pause · `?` this help · `q` quit':
        'キー: `↑/↓` 選択 ・ `s` 並べ替え ・ `c` グラフ ・ `a` 全部/上位 ・ `p` 一時停止 ・ `?` このヘルプ ・ `q` 終了',
    (
        'All eight trend charts are visible by default. They stack in narrow terminals and\n'
        'share rows when there is room. Click the **Charts** dropdown to show all charts or\n'
        'one metric; `c` cycles the same choices. A blank sample means no reading; zero is\n'
        'drawn at the baseline. Percentage charts use 0–100%, temperature uses 0–120°C,\n'
        'and the power and SM clock scales are shown below the charts. In short terminals,\n'
        'scroll the dashboard or inspector without losing the process list.'
    ): (
        '8つの推移グラフは、既定ですべて表示されます。幅の狭いターミナルでは縦に積み重なり、余裕があるときは同じ行に並びます。'
        '**グラフ**のドロップダウンをクリックすると、すべてのグラフまたは1つの指標だけを表示できます。'
        '`c`キーでも同じ選択肢を順に切り替えられます。空白のサンプルは読み取りなしを意味し、0は基線に描かれます。'
        '割合のグラフは0-100%、温度は0-120°Cの範囲で、電力とSMクロックのスケールはグラフの下に表示されます。'
        '高さが足りないターミナルでは、プロセス一覧を保ったまま、ダッシュボードやインスペクターをスクロールできます。'
    ),
}

_REPORT = {
    "WSL + Windows host counters: 'WSL VM' is the exact total of Linux GPU memory (all distros). "
    "Linux rows get their size by matching the VM's GPU contexts (* matched, ? guess). "
    "W: rows are Windows processes.":
        "WSL + Windowsホストのカウンター: 「WSL VM」はLinuxのGPUメモリ（全ディストリビューション）の正確な合計です。"
        "Linuxの行のサイズは、VMのGPUコンテキストとの対応付けで求めます（* は対応付け済み、? は推測）。"
        "W: の行はWindowsのプロセスです。",
    "WSL: VRAM and engine load are device-wide. The Windows host charges every Linux process's "
    "VRAM to the VM, so rows below are processes using the GPU, not their share of it.":
        "WSL: VRAMとエンジン負荷はデバイス全体の値です。WindowsホストはLinuxプロセスのVRAMをすべてVMに計上するため、"
        "以下の行はGPUを使っているプロセスを示すだけで、各プロセスの取り分ではありません。",
    "{note} Windows host counters: {status}.": "{note}Windowsホストのカウンター: {status}。",
    "* matched: the size is exact (Windows' counter for a WSL VM GPU context, or NVML for a host PID "
    "seen from a container); which local process owns it is inferred, and only one explanation fits "
    "(or every one that fits gives the same size).":
        "* 対応付け済み: サイズは正確です（WSL VMのGPUコンテキストに対するWindowsのカウンター、"
        "またはコンテナーから見えるホストPIDに対するNVML）。どのローカルプロセスが所有しているかは推測ですが、"
        "成り立つ説明が1つだけ（または成り立つ説明がどれも同じサイズ）の場合です。",
    "? order guess: the size is exact but several owners fit, so newer processes are paired with newer "
    "GPU contexts / PIDs and outside ones are assumed oldest. Cached foreign-size hints only rank extra "
    "candidates; they never prove ownership. Becomes * with evidence, such as a process starting while "
    "gputaskman runs.":
        "? 順序による推測: サイズは正確ですが、当てはまる所有者が複数あるため、新しいプロセスを新しいGPUコンテキスト/PIDに"
        "対応付け、外部のプロセスは最も古いと仮定しています。キャッシュされた外部サイズのヒントは、"
        "追加の候補の順位付けに使うだけで、所有を証明することはありません。"
        "gputaskmanの実行中にプロセスが起動するなどの根拠が得られると、* になります。",
    "VRAM n/a: this kernel's amdgpu fdinfo has incomplete or unparseable drm-shared-* stats, so resident "
    "memory may include buffers imported from other processes and would be counted once per importer.":
        "VRAMはn/a: このカーネルのamdgpu fdinfoには、不完全または解析できないdrm-shared-*の統計があります。"
        "そのため常駐メモリには他のプロセスからインポートされたバッファーが含まれている可能性があり、"
        "インポートしたプロセスごとに1回ずつ数えられてしまいます。",
    "VRAM and GPU% n/a: this process holds a DRM client other processes hold too (fd passing, "
    "fork). fdinfo counts the client once and doesn't say which of them uses it.":
        "VRAMとGPU%はn/a: このプロセスが保持しているDRMクライアントは、他のプロセスも保持しています（fdの受け渡し、fork）。"
        "fdinfoはクライアントを1つとして数え、どのプロセスが使っているかは示しません。",
    "VRAM n/a: this process's DRM client shares buffers with other clients (dma-buf, e.g. "
    "windows and video frames). fdinfo counts shared buffers by where they prefer to live, not "
    "where they are, so its private part can't be measured.":
        "VRAMはn/a: このプロセスのDRMクライアントは、他のクライアントとバッファーを共有しています（dma-buf。例: ウィンドウやビデオフレーム）。"
        "fdinfoはプロセス間共有バッファーを、実際の配置場所ではなく配置の優先先で数えるため、"
        "このプロセス固有の分は測定できません。",
    "VRAM n/a: this process opened the GPU through /dev/dri/card*, which root-owned services such as "
    "logind may also hold where a normal user can't see them; run as root to check.":
        "VRAMはn/a: このプロセスは/dev/dri/card*経由でGPUを開いています。通常のユーザーからは見えない場所で、"
        "logindなどrootが所有するサービスも同じものを保持している可能性があります。確認するにはrootで実行してください。",
    "VRAM and GPU% n/a: some of this process's file descriptors or fdinfo couldn't be read.":
        "VRAMとGPU%はn/a: このプロセスのファイルディスクリプターまたはfdinfoの一部を読み取れませんでした。",
    "VRAM and GPU% n/a this refresh: the scan budget ran out before every process's fds were "
    "listed, so another holder of this DRM client can't be ruled out.":
        "今回の更新ではVRAMとGPU%はn/a: すべてのプロセスのfdを列挙する前にスキャン予算が尽きたため、"
        "このDRMクライアントの別の保持者を除外できません。",
    "starting": "開始中",
    "ok": "正常",
    "off": "オフ",
    "off (--no-host)": "オフ (--no-host)",
    "off (WSL interop is disabled)": "オフ（WSLの相互運用が無効です）",
    "off (multi-GPU WSL host matching is not validated; use --gpu N)":
        "オフ（複数GPUでのWSLホスト照合は未検証です。--gpu Nを指定してください）",
    "unmatched (no Windows adapter matches this GPU's usage)":
        "未照合（このGPUの使用量に一致するWindowsアダプターがありません）",
    "unavailable (powershell.exe not found)": "利用不可（powershell.exeが見つかりません）",
    "unavailable (counter stream ended)": "利用不可（カウンターのストリームが終了しました）",
    "GPU memory {used} allocated / {total} unified": "GPUメモリ {used} 割り当て済み / ユニファイド {total}",
    "shared (in system RAM) {size}": "共有RAM {size}",
    "mem-bandwidth": "メモリ稼働",
    "PROCESS": "プロセス",
    "KIND": "種類",
    "RUNTIME": "ランタイム",
    "SPILL": "共有RAM",
    "PAGED": "非常駐",
    "INSIDE": "中身",
    "Linux VRAM split: {reason}": "LinuxのVRAM配分: {reason}",
    "== {name} ({pid}) Handy selected (settings, not load proof): {model}":
        "== {name} ({pid}) Handyで選択中（設定ファイルの値。ロードの証拠ではありません）: {model}",
    "last Handy event: {event} {model} at {time} (runtime-reported history, not current GPU residency)":
        "Handyの最新イベント: {event} {model}、{time}（ランタイム報告の履歴であり、現在のGPU常駐を示すものではありません）",
    "{kind}: {label}  [{arch}, {params} params, {quant}, {layers} layers, ctx_train {ctx_train}]  {file}  "
    "evidence: {evidence}":
        "{kind}: {label}  [{arch}、{params}パラメーター、{quant}、{layers}レイヤー、ctx_train {ctx_train}]  {file}  "
        "根拠: {evidence}",
    "file: {name}  ({size}{kind})  evidence: {evidence}": "ファイル: {name}（{size}{kind}）  根拠: {evidence}",
    "server:": "サーバー:",
    "exact sizes from log: {path}": "ログ由来の正確なサイズ: {path}",
}
_CLI = {
    "--gpu must be a non-negative index": "--gpuには0以上のインデックスを指定してください",
    "--interval must be a finite number greater than zero": "--intervalには0より大きい有限の数値を指定してください",
    "gputaskman supports Windows (WDDM), Linux/WSL (NVML, or amdgpu DRM) and macOS (Apple Silicon) only.":
        "gputaskmanが対応しているのは、Windows (WDDM)、Linux/WSL（NVML、またはamdgpuのDRM）、macOS (Apple Silicon)のみです。",
}
_DIFF = {
    "{path} is not a gputaskman --json snapshot": "{path}はgputaskmanの--jsonスナップショットではありません",
    "snapshots are from different GPUs or backends: {before_gpu} ({before_backend}) "
    "vs {after_gpu} ({after_backend})":
        "スナップショットが別々のGPUまたはバックエンドのものです: {before_gpu} ({before_backend}) と {after_gpu} ({after_backend})",
    ", {seconds} s apart": "、{seconds}秒間隔",
    "unknown GPU": "不明なGPU",
    "Measured counters are compared directly. Runtime-reported and estimated values are listed\n"
    "separately and are not added to measured totals.":
        "実測カウンターは直接比較します。ランタイム報告値と推定値は別に一覧し、\n実測の合計には加算しません。",
    "DEVICE (measured)": "デバイス（実測）",
    "BEFORE": "変更前",
    "AFTER": "変更後",
    "CHANGE": "増減",
    "dedicated used": "専用GPUメモリ使用量",
    "shared used": "共有RAM使用量",
    "attributed to processes": "プロセスへの帰属分",
    "unattributed": "未帰属",
    "PROCESSES (dedicated)": "プロセス（専用）",
    "MATCH": "照合",
    "SHARED +/-": "共有増減",
    "not listed": "一覧になし",
    "(no process changed by 16 MB or more)": "（16 MB以上変化したプロセスはありません）",
    "{count} process(es) changed by less than 16 MB are not shown; --json lists all.":
        "16 MB未満しか変化していない{count}個のプロセスは表示していません。--jsonではすべて出力します。",
    "inferred VRAM (WSL context match)": "推測VRAM（WSLコンテキストの照合）",
    "context length": "コンテキスト長",
    "weights": "重み",
    "kv": "KVキャッシュ",
    "unknown": "不明",
    "runtime-reported": "ランタイム報告",
    "estimated": "推定",
    "model file added: {path} [{sources}]": "モデルファイルを新たに検出: {path} [{sources}]",
    "model file removed: {path} [{sources}]": "モデルファイルを検出しなくなった: {path} [{sources}]",
    "Model files show what a process opened or named, not what is resident in GPU memory.":
        "モデルファイルが示すのは、プロセスが開いた、または指定したファイルであり、GPUメモリに常駐しているものではありません。",
    "'not listed' means the process was absent from that snapshot: not running, or using too "
    "little GPU to be listed.":
        "「一覧になし」は、そのスナップショットにプロセスが含まれていなかったことを示します。"
        "実行していなかったか、GPU使用量が小さすぎて一覧に載らなかったかのどちらかです。",
}

_COLLECTOR = {
    "Handy last log ({event}): {model}": "Handyの最新ログ（{event}）: {model}",
    "Handy selected (not load proof): {model}": "Handyで選択中（ロードの証拠ではありません）: {model}",
    " ({kind})": "（{kind}）",
    "installed (unproven): {items}": "インストール済み（未確認）: {items}",
    "desktop back buffers + composed frames": "デスクトップのバックバッファーと合成済みフレーム",
    "all Linux GPU memory (every WSL distro + WSLg)": "LinuxのGPUメモリすべて（全WSLディストリビューションとWSLg）",
    "a process in another PID namespace (host or another container)":
        "別のPID名前空間のプロセス（ホストまたは別のコンテナー）",
    "driver/kernel allocations": "ドライバー/カーネルによる割り当て",
    "page textures, video, canvas/WebGL": "ページのテクスチャ、ビデオ、canvas/WebGL",
    "video frames (decode/encode)": "ビデオフレーム（デコード/エンコード）",
    "textures, meshes, render targets": "テクスチャ、メッシュ、レンダーターゲット",
    "(outside this container)": "（このコンテナーの外）",
    "--gpu {index} is out of range; {count} GPU adapter(s) available":
        "--gpu {index}は範囲外です。使用できるGPUアダプターは{count}個です",
    "Windows GPU counters could not be matched to the selected adapter; "
    "VRAM and processes are unavailable. This can occur in GPU-PV VMs.":
        "WindowsのGPUカウンターを、選択したアダプターに対応付けられませんでした。VRAMとプロセスは取得できません。"
        "GPU-PVのVMでは発生することがあります。",
    "Some Windows adapter memory counters are unavailable; GPU-PV VMs may not expose them.":
        "Windowsのアダプターメモリカウンターの一部が取得できません。GPU-PVのVMでは公開されないことがあります。",
}
_LLM = {
    "KV cache": "KVキャッシュ",
    "compute buffers": "計算バッファー",
    "runtime and other overhead": "ランタイムなどのオーバーヘッド",
    "weights ({count} files)": "重み（{count}ファイル）",
    "KV cache ({n_ctx:,} ctx, {kv_type}) est.": "KVキャッシュ ({n_ctx:,} ctx, {kv_type}) 推定",
    "KV cache ({n_ctx:,} ctx, {kv_type}) est. max": "KVキャッシュ ({n_ctx:,} ctx, {kv_type}) 推定（上限）",
    "compute buffers + runtime": "計算バッファー + ランタイム",
    "KV cache + compute + runtime": "KVキャッシュ + 計算バッファー + ランタイム",
    "{size} of weights are on the CPU side (partial offload or CPU-mapped).":
        "重みのうち{size}はCPU側にあります（部分オフロード、またはCPUにマップ済み）。",
    "Weights need ~{weights} but the process holds {total} of VRAM: "
    "partial offload, paging, or placement on another GPU may explain the gap.":
        "重みには約{weights}が必要ですが、このプロセスが保持しているVRAMは{total}です。"
        "部分オフロード、ページアウト、または別のGPUへの配置が、この差の理由かもしれません。",
    "This process's VRAM total is unknown (WSL charges it to the VM on the Windows host, "
    "or the driver hides per-process memory); segments are estimates from the model file and launch flags.":
        "このプロセスのVRAM合計は不明です（WSLではWindowsホスト側でVMに計上されるか、"
        "ドライバーがプロセスごとのメモリを公開していません）。各区分はモデルファイルと起動フラグからの推定です。",
    "Sliding-window attention ({swa} tokens): most layers keep a short KV window, "
    "so the real KV cache is smaller than this estimate.":
        "スライディングウィンドウアテンション（{swa}トークン）: 多くのレイヤーはKVを短いウィンドウ分しか保持しないため、"
        "実際のKVキャッシュはこの推定より小さくなります。",
    "No GGUF mapped. Model may be loaded with --no-mmap or via another format.":
        "マップされたGGUFはありません。モデルは--no-mmapで、または別の形式でロードされている可能性があります。",
    "Non-causal encoder ({kinds}): no KV cache grows with use; VRAM is weights + compute.":
        "非因果エンコーダー（{kinds}）: 使用に伴って大きくなるKVキャッシュはありません。VRAMの内訳は重みと計算バッファーです。",
    "KV cost {kb:.0f} KB/token ({kv_type}): 4k ctx = {at_4k}, 32k ctx = {at_32k}.":
        "KVコスト {kb:.0f} KB/token ({kv_type}): 4k ctx = {at_4k}、32k ctx = {at_32k}。",
    "! {size} is in SHARED GPU memory (system RAM over PCIe). "
    "May include pinned host buffers; under VRAM pressure, fallback can slow inference.":
        "! {size}が共有RAM（PCIe経由でGPUからアクセスするシステムRAM）にあります。ピン留めされたホストバッファーを含む場合があります。"
        "VRAMが逼迫すると、フォールバックによって推論が遅くなることがあります。",
    "Model is mapped but almost nothing is in VRAM: CPU inference, or another GPU.":
        "モデルはマップされていますが、VRAMにはほとんど載っていません。CPU推論か、別のGPUが考えられます。",
    "Ollama: {name} {total} total, {pct:.0f}% on GPU, ctx {ctx}.":
        "Ollama: {name} 合計{total}、GPU上{pct:.0f}%、ctx {ctx}。",
    "Ollama (not matched to this runner): {name} {total} total, {pct:.0f}% on GPU, ctx {ctx}.":
        "Ollama（このランナーとは対応付けられていません）: {name} 合計{total}、GPU上{pct:.0f}%、ctx {ctx}。",
    "LM Studio: {name} {type} {quant} ctx {ctx}.": "LM Studio: {name} {type} {quant} ctx {ctx}。",
}
_PROCINFO = {
    "likely {kind} (name)": "{kind}の可能性（名前から）",
    "confirmed ({how})": "確認済み ({how})",
    "installed, not proven loaded": "インストール済み、ロードは未確認",
    "in use (mapped)": "使用中（マップ済み）",
    "launch arg": "起動引数",
    "reported (api)": "ランタイム報告 (api)",
    "decision model": "意思決定モデル",
    "embedding model": "埋め込みモデル",
    "reranker": "リランカー",
    "speech model": "音声モデル",
    "vision projector": "ビジョンプロジェクター",
    "LoRA adapter": "LoRAアダプター",
}
_STATUS = {
    "{proc} is not readable": "{proc}を読み取れません",
    "scan budget reached, {count} processes not rescanned this refresh (last known GPU fds kept)":
        "スキャン予算に達したため、{count}個のプロセスは今回の更新で再スキャンしていません（最後に判明したGPU fdを保持）",
    "{count} processes not inspectable (other users' or kernel threads; sudo includes them)":
        "{count}個のプロセスは検査できません（他のユーザーのプロセスまたはカーネルスレッド。sudoを使うと含まれます）",
    "{count} processes whose fds or fdinfo couldn't all be read":
        "{count}個のプロセスでfdまたはfdinfoをすべては読み取れませんでした",
    "; ": "。",
    "{count} Linux GPU process(es) without a VM context to match "
    "(one may not have created its GPU context yet)":
        "VMコンテキストと対応付けられないLinux GPUプロセスが{count}個あります"
        "（GPUコンテキストをまだ作成していない可能性があります）",
    "loaded": "ロード済み",
    "streaming started": "ストリーミング開始",
    "preview": "プレビュー",
    "unloaded": "アンロード済み",
    "unloading": "アンロード中",
}

MESSAGES: dict[str, str] = {**_UI, **_INSPECTOR, **_KINDS, **_EXPLAIN, **_HELP, **_REPORT, **_CLI, **_DIFF,
                            **_COLLECTOR, **_LLM, **_PROCINFO, **_STATUS}
