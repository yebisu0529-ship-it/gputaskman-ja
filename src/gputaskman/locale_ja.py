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

MESSAGES: dict[str, str] = {**_UI, **_INSPECTOR, **_KINDS, **_EXPLAIN, **_HELP}
