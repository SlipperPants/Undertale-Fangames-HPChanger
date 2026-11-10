import ctypes
from ctypes import wintypes
import json
import os
import threading
import time
import tkinter as tk
from tkinter import messagebox, ttk
import winsound

PROCESS_VM_READ = 0x0010
PROCESS_VM_WRITE = 0x0020
PROCESS_VM_OPERATION = 0x0008
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
PROCESS_SUSPEND_RESUME = 0x0800
TH32CS_SNAPPROCESS = 0x00000002
MEM_COMMIT = 0x1000
WRITABLE_FLAGS = 0x04 | 0x08 | 0x40
PAGE_GUARD = 0x100
VK_BACK = 0x08

GAME_KEYWORDS = [
    "undertale", "deltarune", "survey_program", "kristal", "kris", "susie",
    "ralsei", "noelle", "berdly", "lancer", "queen", "jevil", "spamton",
    "tenna", "gaster", "sans", "papyrus", "chara", "frisk", "flowey",
    "asriel", "toriel", "undyne", "alphys", "mettaton", "asgore", "muffet",
    "void", "cotv", "dust", "breath", "disbelief", "yellow", "clover",
    "martlet", "ceroba", "starlo", "axis", "swap", "fell", "outer", "ink",
    "error", "trio", "megalovania", "bad time", "determination", "timeline",
    "genocide", "pacifist", "snowgrave", "cyf", "unitale", "underverse",
    "x-event", "underswap", "deltatraveler", "ribbit", "dark world", "stdrt"
]

IGNORED_PROCESSES = {
    "explorer.exe", "python.exe", "pythonw.exe", "chrome.exe", "msedge.exe",
    "firefox.exe", "opera.exe", "brave.exe", "discord.exe", "spotify.exe",
    "steam.exe", "steamwebhelper.exe", "nvcontainer.exe", "code.exe",
    "idea64.exe", "capcut.exe", "obs64.exe", "taskmgr.exe", "cmd.exe",
    "powershell.exe", "conhost.exe", "svchost.exe", "onedrive.exe",
    "searchhost.exe", "widgets.exe", "applicationframehost.exe", "system",
    "idle", "audiodg.exe", "dwm.exe", "csrss.exe", "lsass.exe",
    "services.exe", "wininit.exe", "winlogon.exe", "spoolsv.exe",
    "sihost.exe", "taskhostw.exe", "runtimebroker.exe", "textinputhost.exe"
}

LANG = {
    "EN": {
        "game": "Game:",
        "waiting": "Waiting for Undertale Fangames...",
        "engine": "Engine:",
        "none": "None",
        "filter": "Filter:",
        "hp": "HP:",
        "clear": "Clear",
        "scan": "Scan",
        "next": "Next",
        "set_hp": "Set HP:",
        "apply": "Apply HP",
        "auto_off": "Auto-Heal: OFF",
        "auto_on": "Auto-Heal: ON (1ms)",
        "frz_off": "Freeze Game: OFF",
        "frz_on": "Freeze Game: ON",
        "keybinds": "Keybinds:",
        "hk_on": "Hotkeys: ON",
        "hk_off": "Hotkeys: OFF",
        "k_clear": "Clear:",
        "k_scan": "Scan:",
        "k_next": "Next:",
        "k_apply": "Apply:",
        "k_auto": "Auto:",
        "k_frz": "Freeze:",
        "ready": "Ready",
        "msg_clear": "Cleared. Type HP value.",
        "msg_err": "Invalid number or game not connected.",
        "msg_scan": "Scanned {0}: {1} addresses found.",
        "msg_next": "Filtered: {0} addresses remaining.",
        "msg_apply": "HP boosted to {0} ({1} addresses).",
        "msg_auto_on": "1ms Auto-Heal: ON",
        "msg_auto_off": "1ms Auto-Heal: OFF",
        "msg_frz_on": "Game Process Frozen (Paused).",
        "msg_frz_off": "Game Process Resumed.",
    },
    "TR": {
        "game": "Oyun:",
        "waiting": "Undertale Fangames bekleniyor...",
        "engine": "Motor:",
        "none": "Yok",
        "filter": "Filtre:",
        "hp": "Can:",
        "clear": "Sil",
        "scan": "Tara",
        "next": "Filtre",
        "set_hp": "Yeni Can:",
        "apply": "Can Ver",
        "auto_off": "Oto-Yenile: KAPALI",
        "auto_on": "Oto-Yenile: ACIK (1ms)",
        "frz_off": "Oyunu Dondur: KAPALI",
        "frz_on": "Oyunu Dondur: ACIK",
        "keybinds": "Tuslar:",
        "hk_on": "Kisayol: ACIK",
        "hk_off": "Kisayol: KAPALI",
        "k_clear": "Sil:",
        "k_scan": "Tara:",
        "k_next": "Bul:",
        "k_apply": "Ver:",
        "k_auto": "Oto:",
        "k_frz": "Dondur:",
        "ready": "Hazir",
        "msg_clear": "Silindi. Can degerini yazin.",
        "msg_err": "Gecersiz sayi veya oyun bagli degil.",
        "msg_scan": "{0} tarandi: {1} adres bulundu.",
        "msg_next": "Filtrelendi: {0} adres kaldi.",
        "msg_apply": "Can {0} yapildi ({1} adres).",
        "msg_auto_on": "1ms Oto-Yenileme: ACIK",
        "msg_auto_off": "1ms Oto-Yenileme: KAPALI",
        "msg_frz_on": "Oyun Donduruldu (Duraklatildi).",
        "msg_frz_off": "Oyun Devam Ediyor.",
    },
}


class PROCESSENTRY32(ctypes.Structure):
    _fields_ = [
        ("dwSize", wintypes.DWORD),
        ("cntUsage", wintypes.DWORD),
        ("th32ProcessID", wintypes.DWORD),
        ("th32DefaultHeapID", ctypes.c_void_p),
        ("th32ModuleID", wintypes.DWORD),
        ("cntThreads", wintypes.DWORD),
        ("th32ParentProcessID", wintypes.DWORD),
        ("pcPriClassBase", wintypes.LONG),
        ("dwFlags", wintypes.DWORD),
        ("szExeFile", ctypes.c_char * 260),
    ]


class MEMORY_BASIC_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("BaseAddress", ctypes.c_void_p),
        ("AllocationBase", ctypes.c_void_p),
        ("AllocationProtect", wintypes.DWORD),
        ("RegionSize", ctypes.c_size_t),
        ("State", wintypes.DWORD),
        ("Protect", wintypes.DWORD),
        ("Type", wintypes.DWORD),
    ]


kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
user32 = ctypes.WinDLL("user32", use_last_error=True)
ntdll = ctypes.WinDLL("ntdll", use_last_error=True)

kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
kernel32.OpenProcess.restype = wintypes.HANDLE
kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
kernel32.CloseHandle.restype = wintypes.BOOL
kernel32.VirtualQueryEx.argtypes = [
    wintypes.HANDLE,
    ctypes.c_void_p,
    ctypes.POINTER(MEMORY_BASIC_INFORMATION),
    ctypes.c_size_t,
]
kernel32.VirtualQueryEx.restype = ctypes.c_size_t
kernel32.ReadProcessMemory.argtypes = [
    wintypes.HANDLE,
    ctypes.c_void_p,
    ctypes.c_void_p,
    ctypes.c_size_t,
    ctypes.POINTER(ctypes.c_size_t),
]
kernel32.ReadProcessMemory.restype = wintypes.BOOL
kernel32.WriteProcessMemory.argtypes = [
    wintypes.HANDLE,
    ctypes.c_void_p,
    ctypes.c_void_p,
    ctypes.c_size_t,
    ctypes.POINTER(ctypes.c_size_t),
]
kernel32.WriteProcessMemory.restype = wintypes.BOOL

ntdll.NtSuspendProcess.argtypes = [wintypes.HANDLE]
ntdll.NtSuspendProcess.restype = wintypes.LONG
ntdll.NtResumeProcess.argtypes = [wintypes.HANDLE]
ntdll.NtResumeProcess.restype = wintypes.LONG

WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)


class MemoryScanner:

    def __init__(self):
        self.process_handle = None
        self.pid = None
        self.process_name = ""
        self.engine_name = "None"
        self.scan_types = ["int32", "double", "float"]
        self.is_64bit = False
        self.is_frozen = False
        self.candidates = []

    def _get_path(self, pid):
        h = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
        if not h:
            return ""
        buf = ctypes.create_unicode_buffer(1024)
        size = wintypes.DWORD(1024)
        path = ""
        if kernel32.QueryFullProcessImageNameW(h, 0, buf, ctypes.byref(size)):
            path = buf.value
        kernel32.CloseHandle(h)
        return path

    def _get_window_classes(self):
        pid_classes = {}

        def callback(hwnd, lparam):
            if user32.IsWindowVisible(hwnd):
                pid = wintypes.DWORD()
                user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
                cname = ctypes.create_unicode_buffer(128)
                if user32.GetClassNameW(hwnd, cname, 128):
                    pid_classes.setdefault(pid.value, set()).add(cname.value)
            return True

        user32.EnumWindows(WNDENUMPROC(callback), 0)
        return pid_classes

    def _detect_engine(self, exe_path, exe_name, wclasses):
        files = []
        if exe_path and os.path.exists(exe_path):
            try:
                files = [f.lower() for f in os.listdir(os.path.dirname(exe_path))]
            except Exception:
                files = []

        if (
            "YYGameMakerYY" in wclasses
            or any(f.endswith(".win") for f in files)
            or "options.ini" in files
            or "audiogroup1.dat" in files
        ):
            return "GameMaker", ["double", "int32"]

        if (
            "modules" in files
            or any(f.endswith(".dat") for f in files)
            or "mmfs2.dll" in files
            or exe_name.lower() == "stdrt.exe"
        ):
            return "Clickteam Fusion", ["int32", "double"]

        if (
            "UnityWndClass" in wclasses
            or "unityplayer.dll" in files
            or any(f.endswith("_data") for f in files)
        ):
            return "Unity / CYF", ["float", "double", "int32"]

        if (
            "love.dll" in files
            or "lua51.dll" in files
            or any(f.endswith(".love") for f in files)
        ):
            return "Kristal / Love2D", ["double", "int32"]

        if any(f.endswith(".pck") for f in files):
            return "Godot", ["int32", "double", "float"]

        return "Universal", ["int32", "double", "float"]

    def _matches_target(self, exe_name, exe_path, target_filter, wclasses):
        exe_l = exe_name.lower()
        if exe_l in IGNORED_PROCESSES:
            return False

        path_l = exe_path.lower() if exe_path else ""
        if path_l.startswith("c:\\windows") or "windowsapps" in path_l:
            return False

        if target_filter and target_filter.upper() not in ("AUTO", "OTOMATIK"):
            return target_filter.lower() in exe_l or target_filter.lower() in path_l

        if any(k in exe_l or k in path_l for k in GAME_KEYWORDS):
            return True

        if "YYGameMakerYY" in wclasses:
            return True

        if exe_path and os.path.exists(exe_path):
            try:
                files = [f.lower() for f in os.listdir(os.path.dirname(exe_path))]
                if (
                    "data.win" in files
                    or "modules" in files
                    or "love.dll" in files
                    or ("unityplayer.dll" in files and "mods" in files)
                ):
                    return True
            except Exception:
                pass

        return False

    def attach(self, target_filter="AUTO"):
        snap = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
        if snap == ctypes.c_void_p(-1).value:
            return False

        wclasses_map = self._get_window_classes()
        pe = PROCESSENTRY32()
        pe.dwSize = ctypes.sizeof(PROCESSENTRY32)
        found_pid = None
        found_name = ""
        found_path = ""
        found_wclasses = set()

        if kernel32.Process32First(snap, ctypes.byref(pe)):
            while True:
                pid = pe.th32ProcessID
                name = pe.szExeFile.decode("utf-8", errors="ignore")
                if pid > 4 and name.lower() not in IGNORED_PROCESSES:
                    path = self._get_path(pid)
                    wcls = wclasses_map.get(pid, set())
                    if self._matches_target(name, path, target_filter, wcls):
                        found_pid = pid
                        found_name = name
                        found_path = path
                        found_wclasses = wcls
                        break
                if not kernel32.Process32Next(snap, ctypes.byref(pe)):
                    break

        kernel32.CloseHandle(snap)

        if found_pid:
            flags = (
                PROCESS_VM_READ
                | PROCESS_VM_WRITE
                | PROCESS_VM_OPERATION
                | PROCESS_QUERY_INFORMATION
                | PROCESS_SUSPEND_RESUME
            )
            h = kernel32.OpenProcess(flags, False, found_pid)
            if h:
                self.process_handle = h
                self.pid = found_pid
                self.process_name = found_name
                self.is_frozen = False

                wow64 = wintypes.BOOL(False)
                if hasattr(kernel32, "IsWow64Process"):
                    kernel32.IsWow64Process(h, ctypes.byref(wow64))
                    self.is_64bit = not bool(wow64.value)

                eng, stypes = self._detect_engine(
                    found_path, found_name, found_wclasses
                )
                self.engine_name = eng
                self.scan_types = stypes
                self.candidates = []
                return True

        self.detach()
        return False

    def is_alive(self):
        if not self.process_handle:
            return False
        code = wintypes.DWORD()
        if kernel32.GetExitCodeProcess(self.process_handle, ctypes.byref(code)):
            return code.value == 259
        return False

    def set_freeze_game(self, freeze_state):
        if not self.process_handle:
            self.is_frozen = False
            return False
        if freeze_state and not self.is_frozen:
            ntdll.NtSuspendProcess(self.process_handle)
            self.is_frozen = True
            return True
        elif not freeze_state and self.is_frozen:
            ntdll.NtResumeProcess(self.process_handle)
            self.is_frozen = False
            return True
        return self.is_frozen

    def detach(self):
        if self.process_handle:
            if self.is_frozen:
                try:
                    ntdll.NtResumeProcess(self.process_handle)
                except Exception:
                    pass
            kernel32.CloseHandle(self.process_handle)
        self.process_handle = None
        self.pid = None
        self.process_name = ""
        self.engine_name = "None"
        self.is_frozen = False

    def read_val(self, addr, vtype):
        if not self.process_handle:
            return None
        read = ctypes.c_size_t()
        if vtype == "double":
            buf = ctypes.c_double()
            sz = 8
        elif vtype == "float":
            buf = ctypes.c_float()
            sz = 4
        else:
            buf = ctypes.c_int32()
            sz = 4

        if kernel32.ReadProcessMemory(
            self.process_handle,
            ctypes.c_void_p(addr),
            ctypes.byref(buf),
            sz,
            ctypes.byref(read),
        ):
            return buf.value
        return None

    def write_val(self, addr, val, vtype):
        if not self.process_handle or not addr:
            return False
        written = ctypes.c_size_t()
        if vtype == "double":
            buf = ctypes.c_double(float(val))
            sz = 8
        elif vtype == "float":
            buf = ctypes.c_float(float(val))
            sz = 4
        else:
            buf = ctypes.c_int32(int(val))
            sz = 4

        return bool(
            kernel32.WriteProcessMemory(
                self.process_handle,
                ctypes.c_void_p(addr),
                ctypes.byref(buf),
                sz,
                ctypes.byref(written),
            )
        )

    def first_scan(self, val):
        if not self.process_handle:
            return 0

        vi = int(val)
        vf = float(val)
        patterns = []
        if "int32" in self.scan_types:
            patterns.append(("int32", bytes(ctypes.c_int32(vi))))
        if "double" in self.scan_types:
            patterns.append(("double", bytes(ctypes.c_double(vf))))
        if "float" in self.scan_types:
            patterns.append(("float", bytes(ctypes.c_float(vf))))

        found = []
        addr = 0x00100000
        limit = 0x7FFFFFFFFFFF if self.is_64bit else 0x7FFFFFFF
        mbi = MEMORY_BASIC_INFORMATION()

        while addr < limit:
            res = kernel32.VirtualQueryEx(
                self.process_handle,
                ctypes.c_void_p(addr),
                ctypes.byref(mbi),
                ctypes.sizeof(mbi),
            )
            if not res:
                break

            base = mbi.BaseAddress or 0
            size = mbi.RegionSize or 4096

            if (
                mbi.State == MEM_COMMIT
                and (mbi.Protect & WRITABLE_FLAGS) != 0
                and (mbi.Protect & PAGE_GUARD) == 0
                and size <= 80 * 1024 * 1024
            ):
                buf = ctypes.create_string_buffer(size)
                read = ctypes.c_size_t()
                if kernel32.ReadProcessMemory(
                    self.process_handle,
                    ctypes.c_void_p(base),
                    buf,
                    size,
                    ctypes.byref(read),
                ):
                    raw = buf.raw[: read.value]
                    for vtype, pat in patterns:
                        pos = 0
                        while True:
                            idx = raw.find(pat, pos)
                            if idx == -1:
                                break
                            if idx % 4 == 0:
                                found.append((base + idx, vtype))
                            pos = idx + 4

            nxt = base + size
            if nxt <= addr:
                break
            addr = nxt

        self.candidates = found
        return len(self.candidates)

    def next_scan(self, val):
        if not self.process_handle or not self.candidates:
            return 0

        vi = int(val)
        vf = float(val)
        filtered = []

        for addr, vtype in list(self.candidates):
            curr = self.read_val(addr, vtype)
            if curr is None:
                continue
            if vtype == "int32" and curr == vi:
                filtered.append((addr, vtype))
            elif vtype in ("double", "float") and abs(curr - vf) < 0.01:
                filtered.append((addr, vtype))

        self.candidates = filtered
        return len(self.candidates)


class AppUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Undertale Fangames")
        self.root.geometry("485x335")
        self.root.resizable(False, False)
        self.root.configure(bg="#181818")
        self.root.attributes("-topmost", True)

        self.config_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "settings.json"
        )
        self.settings = self.load_settings()

        self.lang = "EN"
        self.mem = MemoryScanner()
        self.hotkeys_enabled = bool(self.settings.get("hotkeys_enabled", True))
        self.auto_refresh = False
        self.target_val = int(self.settings.get("target_hp", 99999))

        keys = self.settings.get("keys", ["V", "B", "N", "M", "O", "P"])
        if len(keys) < 6:
            keys = [
                keys[0] if len(keys) > 0 else "V",
                keys[1] if len(keys) > 1 else "B",
                keys[2] if len(keys) > 2 else "N",
                keys[3] if len(keys) > 3 else "M",
                "O",
                "P",
            ]
        self.keybinds = keys[:6]

        self._setup_style()
        self._build_ui()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        threading.Thread(target=self._loop, daemon=True).start()
        threading.Thread(target=self._heal_loop, daemon=True).start()

    def load_settings(self):
        defaults = {
            "filter": "AUTO",
            "target_hp": "99999",
            "hotkeys_enabled": True,
            "keys": ["V", "B", "N", "M", "O", "P"],
        }
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    defaults.update(data)
            except Exception:
                pass
        return defaults

    def save_settings(self):
        k1 = (self.ent_k1.get().strip().upper() or "V")[-1]
        k2 = (self.ent_k2.get().strip().upper() or "B")[-1]
        k3 = (self.ent_k3.get().strip().upper() or "N")[-1]
        k4 = (self.ent_k4.get().strip().upper() or "M")[-1]
        k5 = (self.ent_k5.get().strip().upper() or "O")[-1]
        k6 = (self.ent_k6.get().strip().upper() or "P")[-1]
        self.keybinds = [k1, k2, k3, k4, k5, k6]

        t_digits = "".join(c for c in self.ent_target.get() if c.isdigit())
        self.target_val = int(t_digits) if t_digits else 99999

        data = {
            "filter": self.ent_filter.get().strip() or "AUTO",
            "target_hp": str(self.target_val),
            "hotkeys_enabled": self.hotkeys_enabled,
            "keys": self.keybinds,
        }
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

    def on_close(self):
        self.mem.set_freeze_game(False)
        self.mem.detach()
        self.save_settings()
        self.root.destroy()

    def _setup_style(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("TFrame", background="#181818")
        s.configure(
            "TLabel",
            background="#181818",
            foreground="#D0D0D0",
            font=("Segoe UI", 9),
        )
        s.configure(
            "TButton",
            background="#262626",
            foreground="#FFFFFF",
            bordercolor="#383838",
            font=("Segoe UI", 9),
        )
        s.map("TButton", background=[("active", "#363636")])

    def _build_ui(self):
        t = LANG[self.lang]
        main = ttk.Frame(self.root, padding=14)
        main.pack(fill=tk.BOTH, expand=True)

        row_top = ttk.Frame(main)
        row_top.pack(fill=tk.X, pady=(0, 8))
        self.lbl_game_title = ttk.Label(row_top, text=t["game"])
        self.lbl_game_title.pack(side=tk.LEFT)
        self.lbl_proc = ttk.Label(
            row_top, text=t["waiting"], foreground="#FF6B6B"
        )
        self.lbl_proc.pack(side=tk.LEFT, padx=(6, 0))

        self.btn_lang = tk.Button(
            row_top,
            text=self.lang,
            bg="#2C2C2C",
            fg="#FFFFFF",
            relief=tk.FLAT,
            font=("Segoe UI", 8, "bold"),
            width=4,
            command=self.toggle_language,
        )
        self.btn_lang.pack(side=tk.RIGHT)

        row_eng = ttk.Frame(main)
        row_eng.pack(fill=tk.X, pady=(0, 12))
        self.lbl_eng_title = ttk.Label(row_eng, text=t["engine"])
        self.lbl_eng_title.pack(side=tk.LEFT)
        self.lbl_eng = ttk.Label(row_eng, text=t["none"], foreground="#888888")
        self.lbl_eng.pack(side=tk.LEFT, padx=(6, 16))

        self.lbl_flt_title = ttk.Label(row_eng, text=t["filter"])
        self.lbl_flt_title.pack(side=tk.LEFT)
        self.ent_filter = ttk.Entry(row_eng, width=16, font=("Segoe UI", 9))
        self.ent_filter.insert(0, self.settings.get("filter", "AUTO"))
        self.ent_filter.pack(side=tk.LEFT, padx=(6, 0))
        self.ent_filter.bind("<KeyRelease>", lambda e: self.save_settings())

        row_hp = ttk.Frame(main)
        row_hp.pack(fill=tk.X, pady=4)
        self.lbl_hp_title = ttk.Label(row_hp, text=t["hp"], width=9)
        self.lbl_hp_title.pack(side=tk.LEFT)
        self.ent_hp = ttk.Entry(row_hp, width=9, font=("Segoe UI", 10, "bold"))
        self.ent_hp.insert(0, "92")
        self.ent_hp.pack(side=tk.LEFT, padx=(0, 8))

        self.btn_clear = ttk.Button(
            row_hp, text=t["clear"], width=8, command=self.act_clear
        )
        self.btn_clear.pack(side=tk.LEFT, padx=2)
        self.btn_scan = ttk.Button(
            row_hp, text=t["scan"], width=8, command=self.act_scan
        )
        self.btn_scan.pack(side=tk.LEFT, padx=2)
        self.btn_next = ttk.Button(
            row_hp, text=t["next"], width=8, command=self.act_next
        )
        self.btn_next.pack(side=tk.LEFT, padx=2)

        row_set = ttk.Frame(main)
        row_set.pack(fill=tk.X, pady=(6, 8))
        self.lbl_set_title = ttk.Label(row_set, text=t["set_hp"], width=9)
        self.lbl_set_title.pack(side=tk.LEFT)
        self.ent_target = ttk.Entry(
            row_set, width=9, font=("Segoe UI", 10, "bold")
        )
        self.ent_target.insert(0, str(self.settings.get("target_hp", "99999")))
        self.ent_target.pack(side=tk.LEFT, padx=(0, 8))
        self.ent_target.bind("<KeyRelease>", lambda e: self.save_settings())

        self.btn_apply = ttk.Button(
            row_set, text=t["apply"], command=self.act_apply
        )
        self.btn_apply.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        row_toggles = ttk.Frame(main)
        row_toggles.pack(fill=tk.X, pady=(2, 10))

        self.btn_auto = tk.Button(
            row_toggles,
            text=t["auto_off"],
            bg="#262626",
            fg="#D0D0D0",
            relief=tk.FLAT,
            font=("Segoe UI", 8, "bold"),
            pady=4,
            command=self.act_toggle_auto,
        )
        self.btn_auto.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))

        self.btn_freeze_game = tk.Button(
            row_toggles,
            text=t["frz_off"],
            bg="#262626",
            fg="#D0D0D0",
            relief=tk.FLAT,
            font=("Segoe UI", 8, "bold"),
            pady=4,
            command=self.act_toggle_freeze_game,
        )
        self.btn_freeze_game.pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=(4, 0)
        )

        row_keys_hdr = ttk.Frame(main)
        row_keys_hdr.pack(fill=tk.X, pady=(2, 6))
        self.lbl_kb_title = ttk.Label(row_keys_hdr, text=t["keybinds"])
        self.lbl_kb_title.pack(side=tk.LEFT)

        self.btn_hk_toggle = tk.Button(
            row_keys_hdr,
            text=t["hk_on"] if self.hotkeys_enabled else t["hk_off"],
            bg="#2E5A36" if self.hotkeys_enabled else "#4A2525",
            fg="#FFFFFF",
            relief=tk.FLAT,
            font=("Segoe UI", 8, "bold"),
            padx=8,
            pady=2,
            command=self.toggle_hotkeys,
        )
        self.btn_hk_toggle.pack(side=tk.RIGHT)

        row_keys = ttk.Frame(main)
        row_keys.pack(fill=tk.X, pady=2)

        self.lbl_k1 = ttk.Label(row_keys, text=t["k_clear"])
        self.lbl_k1.pack(side=tk.LEFT)
        self.ent_k1 = ttk.Entry(
            row_keys, width=3, justify="center", font=("Segoe UI", 9, "bold")
        )
        self.ent_k1.insert(0, self.keybinds[0])
        self.ent_k1.pack(side=tk.LEFT, padx=(2, 6))

        self.lbl_k2 = ttk.Label(row_keys, text=t["k_scan"])
        self.lbl_k2.pack(side=tk.LEFT)
        self.ent_k2 = ttk.Entry(
            row_keys, width=3, justify="center", font=("Segoe UI", 9, "bold")
        )
        self.ent_k2.insert(0, self.keybinds[1])
        self.ent_k2.pack(side=tk.LEFT, padx=(2, 6))

        self.lbl_k3 = ttk.Label(row_keys, text=t["k_next"])
        self.lbl_k3.pack(side=tk.LEFT)
        self.ent_k3 = ttk.Entry(
            row_keys, width=3, justify="center", font=("Segoe UI", 9, "bold")
        )
        self.ent_k3.insert(0, self.keybinds[2])
        self.ent_k3.pack(side=tk.LEFT, padx=(2, 6))

        self.lbl_k4 = ttk.Label(row_keys, text=t["k_apply"])
        self.lbl_k4.pack(side=tk.LEFT)
        self.ent_k4 = ttk.Entry(
            row_keys, width=3, justify="center", font=("Segoe UI", 9, "bold")
        )
        self.ent_k4.insert(0, self.keybinds[3])
        self.ent_k4.pack(side=tk.LEFT, padx=(2, 6))

        self.lbl_k5 = ttk.Label(row_keys, text=t["k_auto"])
        self.lbl_k5.pack(side=tk.LEFT)
        self.ent_k5 = ttk.Entry(
            row_keys, width=3, justify="center", font=("Segoe UI", 9, "bold")
        )
        self.ent_k5.insert(0, self.keybinds[4])
        self.ent_k5.pack(side=tk.LEFT, padx=(2, 6))

        self.lbl_k6 = ttk.Label(row_keys, text=t["k_frz"])
        self.lbl_k6.pack(side=tk.LEFT)
        self.ent_k6 = ttk.Entry(
            row_keys, width=3, justify="center", font=("Segoe UI", 9, "bold")
        )
        self.ent_k6.insert(0, self.keybinds[5])
        self.ent_k6.pack(side=tk.LEFT, padx=(2, 0))

        for ent in (
            self.ent_k1,
            self.ent_k2,
            self.ent_k3,
            self.ent_k4,
            self.ent_k5,
            self.ent_k6,
        ):
            ent.bind(
                "<KeyRelease>", lambda e, w=ent: self._on_keybind_change(w)
            )

        self.lbl_status = ttk.Label(main, text=t["ready"], foreground="#70A1FF")
        self.lbl_status.pack(anchor=tk.W, pady=(12, 0))

    def toggle_language(self):
        self.lang = "TR" if self.lang == "EN" else "EN"
        t = LANG[self.lang]
        self.btn_lang.config(text=self.lang)
        self.lbl_game_title.config(text=t["game"])
        if not self.mem.is_alive():
            self.lbl_proc.config(text=t["waiting"])
            self.lbl_eng.config(text=t["none"])
        self.lbl_eng_title.config(text=t["engine"])
        self.lbl_flt_title.config(text=t["filter"])
        self.lbl_hp_title.config(text=t["hp"])
        self.btn_clear.config(text=t["clear"])
        self.btn_scan.config(text=t["scan"])
        self.btn_next.config(text=t["next"])
        self.lbl_set_title.config(text=t["set_hp"])
        self.btn_apply.config(text=t["apply"])
        self.btn_auto.config(
            text=t["auto_on"] if self.auto_refresh else t["auto_off"]
        )
        self.btn_freeze_game.config(
            text=t["frz_on"] if self.mem.is_frozen else t["frz_off"]
        )
        self.lbl_kb_title.config(text=t["keybinds"])
        self.btn_hk_toggle.config(
            text=t["hk_on"] if self.hotkeys_enabled else t["hk_off"]
        )
        self.lbl_k1.config(text=t["k_clear"])
        self.lbl_k2.config(text=t["k_scan"])
        self.lbl_k3.config(text=t["k_next"])
        self.lbl_k4.config(text=t["k_apply"])
        self.lbl_k5.config(text=t["k_auto"])
        self.lbl_k6.config(text=t["k_frz"])
        self.lbl_status.config(text=t["ready"], foreground="#70A1FF")

    def _on_keybind_change(self, widget):
        txt = widget.get().strip().upper()
        if txt:
            ch = txt[-1]
            widget.delete(0, tk.END)
            widget.insert(0, ch)
        self.save_settings()
        self.root.focus_set()

    def toggle_hotkeys(self):
        t = LANG[self.lang]
        self.hotkeys_enabled = not self.hotkeys_enabled
        if self.hotkeys_enabled:
            self.btn_hk_toggle.config(text=t["hk_on"], bg="#2E5A36")
        else:
            self.btn_hk_toggle.config(text=t["hk_off"], bg="#4A2525")
        self.save_settings()

    def _editing_text(self):
        return self.root.focus_get() in (
            self.ent_hp,
            self.ent_target,
            self.ent_filter,
            self.ent_k1,
            self.ent_k2,
            self.ent_k3,
            self.ent_k4,
            self.ent_k5,
            self.ent_k6,
        )

    def add_digit(self, d):
        if self._editing_text():
            return
        cur = self.ent_hp.get()
        if len(cur) < 6:
            self.ent_hp.insert(tk.END, d)

    def remove_digit(self):
        if self._editing_text():
            return
        cur = self.ent_hp.get()
        if cur:
            self.ent_hp.delete(len(cur) - 1, tk.END)

    def _set_auto_ui(self, state):
        t = LANG[self.lang]
        self.auto_refresh = state
        if self.auto_refresh:
            self.btn_auto.config(
                text=t["auto_on"], bg="#1E5631", fg="#FFFFFF"
            )
        else:
            self.btn_auto.config(
                text=t["auto_off"], bg="#262626", fg="#D0D0D0"
            )

    def _set_freeze_game_ui(self, state):
        t = LANG[self.lang]
        self.mem.set_freeze_game(state)
        if self.mem.is_frozen:
            self.btn_freeze_game.config(
                text=t["frz_on"], bg="#1B4F72", fg="#FFFFFF"
            )
        else:
            self.btn_freeze_game.config(
                text=t["frz_off"], bg="#262626", fg="#D0D0D0"
            )

    def act_clear(self):
        t = LANG[self.lang]
        self._set_auto_ui(False)
        self.ent_hp.delete(0, tk.END)
        winsound.Beep(700, 70)
        self.lbl_status.config(text=t["msg_clear"], foreground="#70A1FF")

    def act_scan(self):
        t = LANG[self.lang]
        self._set_auto_ui(False)
        digits = "".join(c for c in self.ent_hp.get() if c.isdigit())
        self.ent_hp.delete(0, tk.END)
        self.ent_hp.insert(0, digits)

        if not digits or not self.mem.is_alive():
            self.lbl_status.config(text=t["msg_err"], foreground="#FF6B6B")
            return

        cnt = self.mem.first_scan(int(digits))
        winsound.Beep(1000, 90)
        self.lbl_status.config(
            text=t["msg_scan"].format(digits, cnt), foreground="#FFA502"
        )

    def act_next(self):
        t = LANG[self.lang]
        digits = "".join(c for c in self.ent_hp.get() if c.isdigit())
        self.ent_hp.delete(0, tk.END)
        self.ent_hp.insert(0, digits)

        if not digits or not self.mem.is_alive():
            return

        cnt = self.mem.next_scan(int(digits))
        winsound.Beep(1300, 90)
        self.lbl_status.config(
            text=t["msg_next"].format(cnt), foreground="#2ED573"
        )

    def act_apply(self):
        t = LANG[self.lang]
        t_digits = "".join(c for c in self.ent_target.get() if c.isdigit())
        self.target_val = int(t_digits) if t_digits else 99999

        count = 0
        for addr, vtype in list(self.mem.candidates[:100]):
            if addr and self.mem.write_val(addr, self.target_val, vtype):
                count += 1

        winsound.Beep(1600, 150)
        self.lbl_status.config(
            text=t["msg_apply"].format(self.target_val, count),
            foreground="#2ED573",
        )

    def act_toggle_auto(self):
        t = LANG[self.lang]
        t_digits = "".join(c for c in self.ent_target.get() if c.isdigit())
        self.target_val = int(t_digits) if t_digits else 99999

        self._set_auto_ui(not self.auto_refresh)
        if self.auto_refresh:
            winsound.Beep(1800, 120)
            self.lbl_status.config(text=t["msg_auto_on"], foreground="#2ED573")
        else:
            winsound.Beep(600, 120)
            self.lbl_status.config(text=t["msg_auto_off"], foreground="#FFA502")

    def act_toggle_freeze_game(self):
        t = LANG[self.lang]
        if not self.mem.is_alive():
            self.lbl_status.config(text=t["msg_err"], foreground="#FF6B6B")
            return

        self._set_freeze_game_ui(not self.mem.is_frozen)
        if self.mem.is_frozen:
            winsound.Beep(500, 140)
            self.lbl_status.config(text=t["msg_frz_on"], foreground="#70A1FF")
        else:
            winsound.Beep(900, 140)
            self.lbl_status.config(text=t["msg_frz_off"], foreground="#2ED573")

    def _vk_from_char(self, ch):
        if not ch:
            return 0
        c = ch.upper()[0]
        if "A" <= c <= "Z" or "0" <= c <= "9":
            return ord(c)
        return user32.VkKeyScanW(ord(c)) & 0xFF

    def _heal_loop(self):
        while True:
            try:
                if (
                    self.auto_refresh
                    and self.mem.process_handle
                    and self.mem.candidates
                ):
                    val = self.target_val
                    for addr, vtype in list(self.mem.candidates[:100]):
                        if addr:
                            self.mem.write_val(addr, val, vtype)
                    time.sleep(0.001)
                else:
                    time.sleep(0.01)
            except Exception:
                time.sleep(0.01)

    def _loop(self):
        prev_keys = [False, False, False, False, False, False]
        prev_back = False
        prev_digits = {i: False for i in range(10)}

        while True:
            try:
                t = LANG[self.lang]
                flt = self.ent_filter.get().strip()
                if not self.mem.is_alive():
                    if self.auto_refresh:
                        self.root.after(0, self._set_auto_ui, False)
                    if self.mem.is_frozen:
                        self.root.after(0, self._set_freeze_game_ui, False)
                    if self.mem.attach(flt):
                        self.lbl_proc.config(
                            text=f"{self.mem.process_name} ({self.mem.pid})",
                            foreground="#2ED573",
                        )
                        self.lbl_eng.config(
                            text=self.mem.engine_name, foreground="#D0D0D0"
                        )
                    else:
                        self.lbl_proc.config(
                            text=t["waiting"], foreground="#FF6B6B"
                        )
                        self.lbl_eng.config(text=t["none"], foreground="#888888")

                if self.hotkeys_enabled and not self._editing_text():
                    for d in range(10):
                        top = bool(user32.GetAsyncKeyState(0x30 + d) & 0x8000)
                        num = bool(user32.GetAsyncKeyState(0x60 + d) & 0x8000)
                        cur_d = top or num
                        if cur_d and not prev_digits[d]:
                            self.root.after(0, self.add_digit, str(d))
                        prev_digits[d] = cur_d

                    cur_back = bool(user32.GetAsyncKeyState(VK_BACK) & 0x8000)
                    if cur_back and not prev_back:
                        self.root.after(0, self.remove_digit)
                    prev_back = cur_back

                    actions = [
                        self.act_clear,
                        self.act_scan,
                        self.act_next,
                        self.act_apply,
                        self.act_toggle_auto,
                        self.act_toggle_freeze_game,
                    ]
                    for idx in range(6):
                        vk = self._vk_from_char(self.keybinds[idx])
                        cur_k = (
                            bool(user32.GetAsyncKeyState(vk) & 0x8000)
                            if vk
                            else False
                        )
                        if cur_k and not prev_keys[idx]:
                            self.root.after(0, actions[idx])
                        prev_keys[idx] = cur_k
                else:
                    prev_keys = [False, False, False, False, False, False]
                    for d in range(10):
                        prev_digits[d] = False
            except Exception:
                pass

            time.sleep(0.02)


if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = AppUI(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", str(e))