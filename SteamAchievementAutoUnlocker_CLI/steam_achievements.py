#!/usr/bin/env python3
"""
Steam Achievement Auto-Unlocker
Analisa conquistas com base no tempo de jogo e desbloqueia diretamente via Steamworks API.
Requer: Steam aberto e logado. O steam_api64.dll e detectado automaticamente nos jogos instalados.
"""

import os, sys, json, math, ctypes, time, subprocess, tempfile, requests, winreg
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "steam_config.json")
APPID_FILE  = os.path.join(SCRIPT_DIR, "steam_appid.txt")


# ─── Internacionalizacao ─────────────────────────────────────────────────────

_lang = "pt"

_STRINGS = {
    "pt": {
        "lang_prompt":        "Selecione o idioma / Select language:",
        "lang_opt_en":        "  [1] English",
        "lang_opt_pt":        "  [2] Portugues  (padrao)",
        "lang_choice":        "Opcao (1/2, Enter = Portugues): ",
        "setup_header":       "CONFIGURACAO",
        "api_key_hint":       "Obtenha sua chave em: https://steamcommunity.com/dev/apikey",
        "api_key_prompt":     "Steam API Key: ",
        "steamid_hint":       "Encontre seu Steam ID (64-bit) em: https://www.steamidfinder.com/",
        "steamid_prompt":     "Steam ID (76561198...): ",
        "dll_missing_warn":   "\n[AVISO] DLL anterior nao encontrado ({path})",
        "dll_searching":      "  Buscando automaticamente...",
        "dll_found":          "\nsteam_api64.dll encontrado em: {dll}",
        "dll_not_found":      "\nsteam_api64.dll nao encontrado automaticamente.",
        "dll_hint1":          "O arquivo esta presente na pasta de qualquer jogo Steam instalado.",
        "dll_hint2":          "Exemplo: C:\\SteamLibrary\\steamapps\\common\\NomeDoJogo\\steam_api64.dll",
        "dll_prompt":         "Caminho completo: ",
        "games_header":       "\nJOGOS ({start}-{end} de {total}) — por tempo de jogo",
        "col_num":            "#",
        "col_name":           "Nome",
        "col_time":           "Tempo",
        "nav_next":           "[N] Proxima",
        "nav_prev":           "[A] Anterior",
        "nav_search":         "[B] Buscar",
        "nav_farm":           "[F] Farmar horas",
        "nav_reconfig":       "[R] Reconfigurar",
        "nav_quit":           "[S] Sair",
        "choice_prompt":      "\nNumero ou opcao: ",
        "goodbye":            "\nAte logo!",
        "search_prompt":      "Nome (parcial): ",
        "no_results":         "Nenhum resultado.",
        "select_prompt":      "Selecione: ",
        "invalid_choice":     "Opcao invalida.",
        "farm_no_dll":        "\n  [ERRO] steam_api64.dll nao configurado.",
        "press_enter_back":   "  Enter para voltar...",
        "farm_header":        "\nFARM — Selecione os jogos ({start}-{end} de {total})",
        "nav_confirm":        "[C] Confirmar",
        "nav_cancel":         "[X] Cancelar",
        "farm_selected":      "\n  Selecionados ({n}): {names}",
        "farm_select_one":    "  Selecione ao menos um jogo.",
        "farm_toggle_prompt": "Numero para (des)selecionar (Enter para cancelar): ",
        "farm_hours_prompt":  "  Quantas horas deseja farmar? (ex: 2.5): ",
        "invalid_value":      "  Valor invalido.",
        "farm_collecting":    "\n  Coletando dados de conquistas ({n} jogo(s))...",
        "farm_ach_info":      "{n} conquistas ({unlocked} desbloqueadas, {src})",
        "farm_ach_info_skip": "{n} conquistas ({unlocked} desbloqueadas, {src}, {skip} inobtainiveis ignoradas)",
        "farm_no_ach":        "sem conquistas",
        "farm_starting":      "\n  Iniciando farm de {h}h em {n} jogo(s)...",
        "farm_ctrl_c":        "  Pressione Ctrl+C para parar antecipadamente.\n",
        "farm_done":          "concluido ✓",
        "farm_interrupted":   "\n\n  Farm interrompido.",
        "farm_finished":      "\n  Encerrado. Tempo farmado: {h:.2f}h",
        "press_enter_list":   "  Enter para voltar a lista...",
        "sw_loading_dll":     "\n  Carregando steam_api64.dll...",
        "sw_connecting":      "  Conectando ao Steam como AppID {id}...",
        "sw_requesting":      "  Solicitando stats atuais (aguarde ~3s)...",
        "sw_dll_fail":        "Falha ao carregar DLL: {err}",
        "sw_resetting":       "  Resetando conquistas via ResetAllStats...",
        "sw_reapplying":      "  Re-aplicando {n} conquistas a manter/desbloquear...",
        "sw_unlocking":       "  Desbloqueando {n} conquistas...",
        "sw_saving":          "  Salvando no servidor Steam...",
        "sw_success":         "Alteracoes salvas com sucesso.",
        "sw_store_fail":      "StoreStats falhou — alteracoes podem nao ter sido salvas.",
        "sw_reset_fail":      "ResetAllStats falhou.",
        "sw_no_stats":        "Nao foi possivel obter ISteamUserStats.",
        "sw_init_fail":       "SteamAPI_Init falhou. Steam esta aberto e logado?",
        "sw_initflat_fail":   "SteamAPI_InitFlat falhou: {msg}",
        "sw_no_ach_read":     "Nenhuma conquista lida via Steamworks.",
        "app_subtitle":       "    Desbloqueio Automatico por Tempo de Jogo",
        "creds_incomplete":   "Credenciais incompletas. Exclua steam_config.json e tente novamente.",
        "press_enter_exit":   "Enter para sair...",
        "loading_library":    "\nCarregando biblioteca Steam...",
        "load_error":         "\n[ERRO] Nao foi possivel carregar jogos.",
        "load_check_key":     "  - API Key correta?",
        "load_check_id":      "  - Steam ID correto (64-bit)?",
        "load_check_public":  "  - Perfil Steam publico?",
        "press_enter":        "Enter...",
        "games_loaded":       "  {n} jogos com tempo de jogo.",
        "game_label":         "  Jogo  : {name}",
        "appid_label":        "  AppID : {id}",
        "time_label":         "  Tempo : {h:.1f} horas",
        "loading_ach":        "\nCarregando conquistas...",
        "no_ach_registered":  "  Este jogo nao tem conquistas registradas no Steam.",
        "reading_steamworks": "  Lendo estado via Steamworks (sem cache)...",
        "warn_steamworks":    "  [AVISO Steamworks] {msg}",
        "trying_webapi":      "  Tentando Web API (pode ter cache de horas)...",
        "warn_403":           "  [AVISO] Web API retornou 403 — tratando todas como bloqueadas.",
        "warn_webapi_down":   "  [AVISO] Web API indisponivel — tratando todas como bloqueadas.",
        "no_ach":             "  Este jogo nao tem conquistas.",
        "total_ach":          "  Total de conquistas : {n}",
        "unlocked_ach":       "  Ja desbloqueadas    : {n}",
        "locked_ach":         "  Bloqueadas          : {n}",
        "total_ach_unknown":  "  Total de conquistas : {n}  (estado atual indisponivel)",
        "warn_no_pct":        "  [AVISO] Percentuais globais indisponiveis.",
        "querying_sh":        "  Consultando SteamHunters...",
        "sh_no_data":         "sem dados — usando estimativa",
        "sh_median":          "mediana {h:.0f}h",
        "sh_ach_count":       "{n} conquistas",
        "sh_unob_count":      "{n} inobtainiveis",
        "src_estimate":       "estimativa",
        "est_hours":          "\n  Horas estimadas p/ 100% : ~{h:.0f}h  [{src}]",
        "est_progress":       "  Seu progresso estimado  : {pct:.1f}%",
        "should_have":        "  Deveria ter             : {n}/{total} conquistas",
        "to_unlock":          "  A desbloquear           : {n}",
        "skipped_unob":       "  Inobtainiveis ignoradas : {n}  (evento expirado / DLC removido)",
        "to_remove":          "  A remover               : {n}",
        "profile_private":    "  (indisponivel — perfil privado)",
        "forecast_header":    "  Horas para proximas conquistas:",
        "forecast_step":      "+{n} conquista",
        "forecast_steps":     "+{n} conquistas",
        "all_good":           "\n  Tudo em ordem — conquistas ja correspondem ao seu tempo de jogo.",
        "all_good_100":       "  (Tempo suficiente para TODAS as conquistas!)",
        "list_unlock_header": "  CONQUISTAS A DESBLOQUEAR ({n})",
        "col_global":         "Global",
        "list_remove_header": "  CONQUISTAS A REMOVER ({n})  — acima do esperado para {h:.0f}h",
        "attention":          "\n  ATENCAO: O Steam precisa estar aberto e logado na sua conta.",
        "confirm_unlock":     "\n  Desbloquear {n} conquistas? (s/n): ",
        "warn_reset":         "\n  AVISO: a remocao usa ResetAllStats.",
        "warn_reset2":        "  Isso tambem zera suas estatisticas de jogo (contadores, etc.).",
        "confirm_remove":     "  Remover {n} conquistas? (s/n): ",
        "no_action":          "  Nenhuma acao selecionada.",
        "dll_error":          "\n  [ERRO] steam_api64.dll nao encontrado.",
        "dll_error2":         "  Reconecte e tente novamente ou edite dll_path em steam_config.json.",
        "result_unlocked":    "  Desbloqueadas : {ok}/{total}",
        "result_failed":      "  Falharam      : {names}",
        "result_removed":     "  Removidas     : {ok}/{total}",
        "restart_steam":      "  Reinicie o Steam para as alteracoes aparecerem no perfil.",
        "log_saved":          "  Log salvo em: {log}",
        "log_header":         "Steam Achievement Manager — {date}",
        "log_game":           "Jogo: {name} (AppID {id})",
        "log_time":           "Tempo: {h:.1f}h | Progresso estimado: {pct:.1f}%",
        "log_unlocked":       "Desbloqueadas ({n}):",
        "log_removed":        "Removidas ({n}):",
        "cancelled":          "\nCancelado.",
        "unexpected_error":   "  ERRO INESPERADO:",
        "press_enter_list2":  "\n  Enter para voltar a lista...",
        "nav_all":            "[T] Todos",
        "batch_header":       "\nPROCESSAR TODOS — {n} jogos com tempo de jogo",
        "batch_note":         "  Isso pode levar varios minutos. Usando Web API para leitura.",
        "batch_loading":      "  Carregando {i}/{n}: {name}...",
        "batch_no_actions":   "  Tudo em ordem — nenhum jogo requer acoes.",
        "batch_summary":      "  RESUMO DE ACOES",
        "col_unlock":         "Desbloquear",
        "col_remove":         "Remover",
        "batch_has_remove":   "  {n} jogo(s) usara(o) ResetAllStats (zera estatisticas de jogo).",
        "batch_confirm":      "\n  Aplicar em {n} jogo(s)? (s/n): ",
        "batch_processing":   "  [{i}/{n}] {name}",
        "batch_done":         "\n  Concluido: {ok}/{total} jogos processados.",
    },
    "en": {
        "lang_prompt":        "Selecione o idioma / Select language:",
        "lang_opt_en":        "  [1] English  (default)",
        "lang_opt_pt":        "  [2] Portugues",
        "lang_choice":        "Choice (1/2, Enter = English): ",
        "setup_header":       "CONFIGURATION",
        "api_key_hint":       "Get your key at: https://steamcommunity.com/dev/apikey",
        "api_key_prompt":     "Steam API Key: ",
        "steamid_hint":       "Find your Steam ID (64-bit) at: https://www.steamidfinder.com/",
        "steamid_prompt":     "Steam ID (76561198...): ",
        "dll_missing_warn":   "\n[WARNING] Previous DLL not found ({path})",
        "dll_searching":      "  Searching automatically...",
        "dll_found":          "\nsteam_api64.dll found at: {dll}",
        "dll_not_found":      "\nsteam_api64.dll not found automatically.",
        "dll_hint1":          "The file is present in any installed Steam game folder.",
        "dll_hint2":          "Example: C:\\SteamLibrary\\steamapps\\common\\GameName\\steam_api64.dll",
        "dll_prompt":         "Full path: ",
        "games_header":       "\nGAMES ({start}-{end} of {total}) — by playtime",
        "col_num":            "#",
        "col_name":           "Name",
        "col_time":           "Time",
        "nav_next":           "[N] Next",
        "nav_prev":           "[A] Previous",
        "nav_search":         "[B] Search",
        "nav_farm":           "[F] Farm hours",
        "nav_reconfig":       "[R] Reconfigure",
        "nav_quit":           "[Q] Quit",
        "choice_prompt":      "\nNumber or option: ",
        "goodbye":            "\nGoodbye!",
        "search_prompt":      "Name (partial): ",
        "no_results":         "No results.",
        "select_prompt":      "Select: ",
        "invalid_choice":     "Invalid option.",
        "farm_no_dll":        "\n  [ERROR] steam_api64.dll not configured.",
        "press_enter_back":   "  Press Enter to go back...",
        "farm_header":        "\nFARM — Select games ({start}-{end} of {total})",
        "nav_confirm":        "[C] Confirm",
        "nav_cancel":         "[X] Cancel",
        "farm_selected":      "\n  Selected ({n}): {names}",
        "farm_select_one":    "  Select at least one game.",
        "farm_toggle_prompt": "Number to (de)select (Enter to cancel): ",
        "farm_hours_prompt":  "  How many hours to farm? (e.g. 2.5): ",
        "invalid_value":      "  Invalid value.",
        "farm_collecting":    "\n  Collecting achievement data ({n} game(s))...",
        "farm_ach_info":      "{n} achievements ({unlocked} unlocked, {src})",
        "farm_ach_info_skip": "{n} achievements ({unlocked} unlocked, {src}, {skip} unobtainable skipped)",
        "farm_no_ach":        "no achievements",
        "farm_starting":      "\n  Starting {h}h farm on {n} game(s)...",
        "farm_ctrl_c":        "  Press Ctrl+C to stop early.\n",
        "farm_done":          "done ✓",
        "farm_interrupted":   "\n\n  Farm stopped.",
        "farm_finished":      "\n  Finished. Time farmed: {h:.2f}h",
        "press_enter_list":   "  Press Enter to return to list...",
        "sw_loading_dll":     "\n  Loading steam_api64.dll...",
        "sw_connecting":      "  Connecting to Steam as AppID {id}...",
        "sw_requesting":      "  Requesting current stats (wait ~3s)...",
        "sw_dll_fail":        "Failed to load DLL: {err}",
        "sw_resetting":       "  Resetting achievements via ResetAllStats...",
        "sw_reapplying":      "  Re-applying {n} achievements to keep/unlock...",
        "sw_unlocking":       "  Unlocking {n} achievements...",
        "sw_saving":          "  Saving to Steam servers...",
        "sw_success":         "Changes saved successfully.",
        "sw_store_fail":      "StoreStats failed — changes may not have been saved.",
        "sw_reset_fail":      "ResetAllStats failed.",
        "sw_no_stats":        "Could not obtain ISteamUserStats.",
        "sw_init_fail":       "SteamAPI_Init failed. Is Steam open and logged in?",
        "sw_initflat_fail":   "SteamAPI_InitFlat failed: {msg}",
        "sw_no_ach_read":     "No achievements read via Steamworks.",
        "app_subtitle":       "    Automatic Unlock by Playtime",
        "creds_incomplete":   "Incomplete credentials. Delete steam_config.json and try again.",
        "press_enter_exit":   "Press Enter to exit...",
        "loading_library":    "\nLoading Steam library...",
        "load_error":         "\n[ERROR] Could not load games.",
        "load_check_key":     "  - Is the API Key correct?",
        "load_check_id":      "  - Is the Steam ID correct (64-bit)?",
        "load_check_public":  "  - Is your Steam profile public?",
        "press_enter":        "Press Enter...",
        "games_loaded":       "  {n} games with playtime.",
        "game_label":         "  Game  : {name}",
        "appid_label":        "  AppID : {id}",
        "time_label":         "  Time  : {h:.1f} hours",
        "loading_ach":        "\nLoading achievements...",
        "no_ach_registered":  "  This game has no achievements on Steam.",
        "reading_steamworks": "  Reading state via Steamworks (no cache)...",
        "warn_steamworks":    "  [WARNING Steamworks] {msg}",
        "trying_webapi":      "  Trying Web API (may have hour cache)...",
        "warn_403":           "  [WARNING] Web API returned 403 — treating all as locked.",
        "warn_webapi_down":   "  [WARNING] Web API unavailable — treating all as locked.",
        "no_ach":             "  This game has no achievements.",
        "total_ach":          "  Total achievements  : {n}",
        "unlocked_ach":       "  Already unlocked    : {n}",
        "locked_ach":         "  Locked              : {n}",
        "total_ach_unknown":  "  Total achievements  : {n}  (current state unavailable)",
        "warn_no_pct":        "  [WARNING] Global percentages unavailable.",
        "querying_sh":        "  Querying SteamHunters...",
        "sh_no_data":         "no data — using estimate",
        "sh_median":          "median {h:.0f}h",
        "sh_ach_count":       "{n} achievements",
        "sh_unob_count":      "{n} unobtainable",
        "src_estimate":       "estimate",
        "est_hours":          "\n  Est. hours for 100%     : ~{h:.0f}h  [{src}]",
        "est_progress":       "  Your estimated progress : {pct:.1f}%",
        "should_have":        "  Should have             : {n}/{total} achievements",
        "to_unlock":          "  To unlock               : {n}",
        "skipped_unob":       "  Unobtainable skipped    : {n}  (expired event / removed DLC)",
        "to_remove":          "  To remove               : {n}",
        "profile_private":    "  (unavailable — private profile)",
        "forecast_header":    "  Hours to next achievements:",
        "forecast_step":      "+{n} achievement",
        "forecast_steps":     "+{n} achievements",
        "all_good":           "\n  All good — achievements match your playtime.",
        "all_good_100":       "  (Enough time for ALL achievements!)",
        "list_unlock_header": "  ACHIEVEMENTS TO UNLOCK ({n})",
        "col_global":         "Global",
        "list_remove_header": "  ACHIEVEMENTS TO REMOVE ({n})  — above expected for {h:.0f}h",
        "attention":          "\n  NOTICE: Steam must be open and logged into your account.",
        "confirm_unlock":     "\n  Unlock {n} achievement(s)? (y/n): ",
        "warn_reset":         "\n  WARNING: removal uses ResetAllStats.",
        "warn_reset2":        "  This also resets your in-game statistics (counters, kills, etc.).",
        "confirm_remove":     "  Remove {n} achievement(s)? (y/n): ",
        "no_action":          "  No action selected.",
        "dll_error":          "\n  [ERROR] steam_api64.dll not found.",
        "dll_error2":         "  Reconnect and try again or update dll_path in steam_config.json.",
        "result_unlocked":    "  Unlocked : {ok}/{total}",
        "result_failed":      "  Failed   : {names}",
        "result_removed":     "  Removed  : {ok}/{total}",
        "restart_steam":      "  Restart Steam for changes to appear on your profile.",
        "log_saved":          "  Log saved at: {log}",
        "log_header":         "Steam Achievement Manager — {date}",
        "log_game":           "Game: {name} (AppID {id})",
        "log_time":           "Time: {h:.1f}h | Estimated progress: {pct:.1f}%",
        "log_unlocked":       "Unlocked ({n}):",
        "log_removed":        "Removed ({n}):",
        "cancelled":          "\nCancelled.",
        "unexpected_error":   "  UNEXPECTED ERROR:",
        "press_enter_list2":  "\n  Press Enter to return to list...",
        "nav_all":            "[T] All",
        "batch_header":       "\nPROCESS ALL — {n} games with playtime",
        "batch_note":         "  This may take several minutes. Using Web API for reading.",
        "batch_loading":      "  Loading {i}/{n}: {name}...",
        "batch_no_actions":   "  All good — no games require actions.",
        "batch_summary":      "  ACTION SUMMARY",
        "col_unlock":         "Unlock",
        "col_remove":         "Remove",
        "batch_has_remove":   "  {n} game(s) will use ResetAllStats (resets in-game stats).",
        "batch_confirm":      "\n  Apply to {n} game(s)? (y/n): ",
        "batch_processing":   "  [{i}/{n}] {name}",
        "batch_done":         "\n  Done: {ok}/{total} games processed.",
    },
}


def T(key, **kw):
    s = _STRINGS.get(_lang, _STRINGS["pt"]).get(key, key)
    return s.format(**kw) if kw else s


def is_yes(resp):
    return resp.strip().lower() in ("s", "y")


# ─── Steamworks via ctypes ───────────────────────────────────────────────────

class SteamAPI:
    """
    Wrapper para a Steamworks Flat API.
    Suporta SDK antigo (SteamAPI_Init) e novo (SteamAPI_InitFlat, SDK 1.54+).
    """

    def __init__(self, dll_path):
        # Garante que dependencias do DLL sejam encontradas
        os.add_dll_directory(os.path.dirname(os.path.abspath(dll_path)))
        self._dll   = ctypes.CDLL(dll_path)
        self._stats = None
        self._new_sdk = self._has("SteamAPI_InitFlat")
        self._setup()

    def _has(self, name):
        try:
            getattr(self._dll, name)
            return True
        except AttributeError:
            return False

    def _setup(self):
        d = self._dll

        if self._new_sdk:
            # SDK 1.54+ — InitFlat retorna ESteamAPIInitResult (int), 0 = OK
            d.SteamAPI_InitFlat.restype  = ctypes.c_int
            d.SteamAPI_InitFlat.argtypes = [ctypes.c_char_p]
        else:
            d.SteamAPI_Init.restype  = ctypes.c_bool
            d.SteamAPI_Init.argtypes = []

        d.SteamAPI_Shutdown.restype  = None
        d.SteamAPI_Shutdown.argtypes = []

        d.SteamAPI_RunCallbacks.restype  = None
        d.SteamAPI_RunCallbacks.argtypes = []

        # Accessor versionado (SDK novo) ou generico (SDK antigo)
        if self._has("SteamAPI_SteamUserStats_v013"):
            d.SteamAPI_SteamUserStats_v013.restype  = ctypes.c_void_p
            d.SteamAPI_SteamUserStats_v013.argtypes = []
            self._user_stats_fn = d.SteamAPI_SteamUserStats_v013
        else:
            d.SteamAPI_SteamUserStats.restype  = ctypes.c_void_p
            d.SteamAPI_SteamUserStats.argtypes = []
            self._user_stats_fn = d.SteamAPI_SteamUserStats

        # RequestCurrentStats — ausente no SDK novo (feito automaticamente no Init)
        self._has_request = self._has("SteamAPI_ISteamUserStats_RequestCurrentStats")
        if self._has_request:
            d.SteamAPI_ISteamUserStats_RequestCurrentStats.restype  = ctypes.c_bool
            d.SteamAPI_ISteamUserStats_RequestCurrentStats.argtypes = [ctypes.c_void_p]

        d.SteamAPI_ISteamUserStats_SetAchievement.restype  = ctypes.c_bool
        d.SteamAPI_ISteamUserStats_SetAchievement.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

        d.SteamAPI_ISteamUserStats_GetAchievement.restype  = ctypes.c_bool
        d.SteamAPI_ISteamUserStats_GetAchievement.argtypes = [
            ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_bool)
        ]

        d.SteamAPI_ISteamUserStats_ClearAchievement.restype  = ctypes.c_bool
        d.SteamAPI_ISteamUserStats_ClearAchievement.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

        d.SteamAPI_ISteamUserStats_ResetAllStats.restype  = ctypes.c_bool
        d.SteamAPI_ISteamUserStats_ResetAllStats.argtypes = [ctypes.c_void_p, ctypes.c_bool]

        d.SteamAPI_ISteamUserStats_StoreStats.restype  = ctypes.c_bool
        d.SteamAPI_ISteamUserStats_StoreStats.argtypes = [ctypes.c_void_p]

    def connect(self, app_id):
        """Inicializa o Steamworks como se fosse o jogo com app_id."""
        os.environ["SteamAppId"] = str(app_id)
        os.chdir(SCRIPT_DIR)
        with open(APPID_FILE, "w") as f:
            f.write(str(app_id))

        if self._new_sdk:
            err_buf = ctypes.create_string_buffer(1024)
            result  = self._dll.SteamAPI_InitFlat(err_buf)
            if result != 0:
                msg = err_buf.value.decode("utf-8", errors="replace") or f"code {result}"
                return False, T("sw_initflat_fail", msg=msg)
        else:
            if not self._dll.SteamAPI_Init():
                return False, T("sw_init_fail")

        self._stats = self._user_stats_fn()
        if not self._stats:
            return False, T("sw_no_stats")

        return True, "OK"

    def request_stats(self):
        """Solicita stats atuais. No SDK novo isso e feito automaticamente no Init."""
        if self._has_request and self._stats:
            return self._dll.SteamAPI_ISteamUserStats_RequestCurrentStats(self._stats)
        return True

    def pump(self, seconds=3.0, interval=0.1):
        """Processa callbacks do Steam por N segundos."""
        steps = int(seconds / interval)
        for _ in range(steps):
            self._dll.SteamAPI_RunCallbacks()
            time.sleep(interval)

    def unlock(self, name: str) -> bool:
        return self._dll.SteamAPI_ISteamUserStats_SetAchievement(
            self._stats, name.encode("utf-8")
        )

    def get_achievement(self, name: str):
        """Retorna (sucesso, desbloqueada). Leitura direta do cliente Steam."""
        achieved = ctypes.c_bool(False)
        ok = self._dll.SteamAPI_ISteamUserStats_GetAchievement(
            self._stats, name.encode("utf-8"), ctypes.byref(achieved)
        )
        return bool(ok), achieved.value

    def clear(self, name: str) -> bool:
        return self._dll.SteamAPI_ISteamUserStats_ClearAchievement(
            self._stats, name.encode("utf-8")
        )

    def reset_all(self, achievements_too: bool = True) -> bool:
        """Zera todas as estatisticas e (opcionalmente) conquistas."""
        return self._dll.SteamAPI_ISteamUserStats_ResetAllStats(
            self._stats, ctypes.c_bool(achievements_too)
        )

    def store(self) -> bool:
        """Salva as alteracoes no servidor Steam."""
        return self._dll.SteamAPI_ISteamUserStats_StoreStats(self._stats)

    def shutdown(self):
        try:
            self._dll.SteamAPI_Shutdown()
        except Exception:
            pass
        if os.path.exists(APPID_FILE):
            os.remove(APPID_FILE)


def get_steam_install_path():
    """Le o caminho de instalacao do Steam via registro do Windows."""
    keys = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Valve\Steam"),
        (winreg.HKEY_CURRENT_USER,  r"SOFTWARE\Valve\Steam"),
    ]
    for hive, path in keys:
        try:
            with winreg.OpenKey(hive, path) as k:
                value, _ = winreg.QueryValueEx(k, "InstallPath")
                if value and os.path.isdir(value):
                    return value
        except OSError:
            pass
    return r"C:\Program Files (x86)\Steam"


def _dll_is_valid(path):
    """
    Verifica se o DLL é um Steamworks real checando Init E UserStats.
    DLLs stub (Unity, Wallpaper Engine) podem ter Init mas nao UserStats.
    """
    try:
        os.add_dll_directory(os.path.dirname(os.path.abspath(path)))
        dll = ctypes.CDLL(path)

        # Precisa de funcao de inicializacao
        has_init = any(
            _try_attr(dll, n)
            for n in ("SteamAPI_Init", "SteamAPI_InitFlat", "SteamAPI_InitSafe")
        )
        if not has_init:
            return False

        # Precisa de accessor do UserStats (validacao real)
        has_stats = any(
            _try_attr(dll, n)
            for n in ("SteamAPI_SteamUserStats_v013", "SteamAPI_SteamUserStats")
        )
        return has_stats
    except OSError:
        return False


def _try_attr(dll, name):
    try:
        getattr(dll, name)
        return True
    except AttributeError:
        return False


def find_steam_api_dll(sam_path=None):
    """
    Localiza e valida steam_api64.dll.
    Ordem: pasta do SAM → jogos instalados (todas as subpastas) → caminhos fixos.
    Valida que o DLL exporta SteamAPI_Init antes de retornar.
    """
    # Candidatos fixos
    fixed = []
    if sam_path and os.path.exists(sam_path):
        fixed.append(os.path.join(os.path.dirname(sam_path), "steam_api64.dll"))
    for d in [
        r"C:\Program Files (x86)\Steam Achievement Manager",
        r"C:\Program Files\Steam Achievement Manager",
        r"C:\SAM",
        os.path.join(os.path.expanduser("~"), "Desktop", "SAM"),
        os.path.join(os.path.expanduser("~"), "Downloads", "SAM"),
        os.path.join(os.path.expanduser("~"), "Documents", "SAM"),
    ]:
        fixed.append(os.path.join(d, "steam_api64.dll"))

    for p in fixed:
        if os.path.exists(p) and _dll_is_valid(p):
            return p

    # Busca em todos os jogos instalados (todas bibliotecas Steam)
    steam_root  = get_steam_install_path()
    steam_bases = [steam_root]

    vdf = os.path.join(steam_root, "steamapps", "libraryfolders.vdf")
    if os.path.exists(vdf):
        with open(vdf, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if '"path"' in line.lower():
                    parts = line.split('"')
                    val = parts[-2] if len(parts) >= 4 else ""
                    val = val.replace("\\\\", "\\")
                    if os.path.isdir(val):
                        steam_bases.append(val)

    for base in steam_bases:
        common = os.path.join(base, "steamapps", "common")
        if not os.path.isdir(common):
            continue
        for game in os.listdir(common):
            game_dir = os.path.join(common, game)
            for root, dirs, files in os.walk(game_dir):
                depth = root[len(game_dir):].count(os.sep)
                if depth > 3:
                    dirs.clear()
                    continue
                if "steam_api64.dll" in files:
                    candidate = os.path.join(root, "steam_api64.dll")
                    if _dll_is_valid(candidate):
                        return candidate
                    # DLL invalido (stub) — continua procurando

    return None


# ─── Steam Web API ───────────────────────────────────────────────────────────

def steam_get(endpoint, params, timeout=15):
    url = f"https://api.steampowered.com/{endpoint}"
    try:
        r = requests.get(url, params=params, timeout=timeout)
        if r.status_code == 403:
            raise PermissionError("403")
        r.raise_for_status()
        return r.json()
    except PermissionError:
        raise
    except requests.RequestException as e:
        # Oculta a API key na mensagem de erro
        msg = str(e)
        if "key=" in msg:
            msg = msg.split("key=")[0] + "key=***"
        print(f"  [ERRO API] {msg}")
        return None


def get_owned_games(api_key, steam_id):
    data = steam_get("IPlayerService/GetOwnedGames/v1/", {
        "key": api_key, "steamid": steam_id,
        "include_appinfo": True, "include_played_free_games": True,
    })
    return (data or {}).get("response", {}).get("games", [])


def get_player_achievements(api_key, steam_id, app_id):
    try:
        data = steam_get("ISteamUserStats/GetPlayerAchievements/v1/", {
            "key": api_key, "steamid": steam_id, "appid": app_id, "l": "brazilian",
        })
    except PermissionError:
        return "private"   # perfil/jogo privado
    if data:
        ps = data.get("playerstats", {})
        if ps.get("success") and "achievements" in ps:
            return ps["achievements"]
    return None


def get_achievement_schema(api_key, app_id):
    data = steam_get("ISteamUserStats/GetSchemaForGame/v2/", {
        "key": api_key, "appid": app_id, "l": "brazilian",
    })
    if data and "game" in data:
        ach = data["game"].get("availableGameStats", {}).get("achievements", [])
        return {a["name"]: a for a in ach}
    return {}


def get_global_percentages(app_id):
    try:
        data = steam_get("ISteamUserStats/GetGlobalAchievementPercentagesForApp/v2/", {
            "gameid": app_id,
        })
    except PermissionError:
        return {}
    if data and "achievementpercentages" in data:
        items = data["achievementpercentages"].get("achievements", [])
        return {a["name"]: float(a["percent"]) for a in items}
    return {}


def get_steamhunters_data(app_id):
    """
    Busca dados reais da API publica do SteamHunters.
    Retorna (median_hours, local_pct_map, unobtainable_set):
      median_hours      — tempo mediano real (em horas) para 100%, ou None
      local_pct_map     — {apiName: localPercentage} por conquista
      unobtainable_set  — set de apiNames com obtainability != 0
    """
    median_h     = None
    local_pct    = {}
    unobtainable = set()
    base         = "https://steamhunters.com/api/apps"

    try:
        r = requests.get(f"{base}/{app_id}", timeout=10)
        if r.status_code == 200:
            d = r.json()
            m = d.get("medianCompletionTime")
            if m and m > 0:
                median_h = m / 60.0
    except Exception:
        pass

    try:
        r = requests.get(f"{base}/{app_id}/achievements", timeout=10)
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, list):
                for a in data:
                    name = a.get("apiName")
                    if not name:
                        continue
                    pct = a.get("localPercentage")
                    if pct is not None:
                        local_pct[name] = float(pct)
                    if a.get("obtainability", 0) != 0:
                        unobtainable.add(name)
    except Exception:
        pass

    return median_h, local_pct, unobtainable


# ─── Logica de estimativa ────────────────────────────────────────────────────

def blend_achievement_percentages(steam_pct, sh_local_pct):
    """
    Combina Steam global % com SteamHunters local % em um score de ordenacao.
    Ambas as fontes sao normalizadas para [0,1] antes de serem mediadas para
    eliminar a diferenca de escala (usuarios do SH desbloqueiam muito mais).
    Retorna {nome: score} — maior = conquista desbloqueada mais cedo no jogo.
    """
    all_names = set(steam_pct.keys()) | set(sh_local_pct.keys())
    if not all_names:
        return {}

    max_steam = max(steam_pct.values(), default=1.0) or 1.0
    max_sh    = max(sh_local_pct.values(), default=1.0) or 1.0

    result = {}
    for name in all_names:
        sv       = steam_pct.get(name, 0.0)    / max_steam
        shv      = sh_local_pct.get(name, 0.0) / max_sh
        in_steam = name in steam_pct
        in_sh    = name in sh_local_pct

        if in_steam and in_sh:
            result[name] = (sv + shv) / 2
        elif in_steam:
            result[name] = sv
        else:
            result[name] = shv

    return result


def estimate_completion_hours(global_pct, sh_median_h=None):
    """
    Retorna horas estimadas para 100% das conquistas.
    Usa mediana real do SteamHunters quando disponivel; fallback para heuristica.
    """
    if sh_median_h:
        return min(600.0, max(5.0, sh_median_h))
    if not global_pct:
        return 30.0
    vals = [v for v in global_pct.values() if v > 0]
    if not vals:
        return 30.0
    min_pct = min(vals)
    return max(5.0, min(600.0, -40.0 * math.log(min_pct / 100.0) + 3.0))


def playtime_to_ratio(hours, completion_hours):
    """
    Fracao [0,1] de conquistas que um jogador medio teria com esse tempo.
    Curva logaritmica: progresso rapido no inicio, lento no fim.
    """
    if hours <= 0:
        return 0.0
    if hours >= completion_hours:
        return 1.0
    r = hours / completion_hours
    return max(0.0, min(1.0, math.log(1.0 + r * (math.e - 1.0))))


def hours_for_ratio(ratio, completion_hours):
    """Inversa de playtime_to_ratio — horas necessarias para atingir um dado ratio."""
    if ratio <= 0:
        return 0.0
    if ratio >= 1.0:
        return completion_hours
    r = (math.exp(ratio) - 1.0) / (math.e - 1.0)
    return r * completion_hours


def select_to_unlock(user_ach, ordering_scores, ratio):
    """
    Retorna conquistas que deveriam estar desbloqueadas dado o ratio.
    Ordenadas por ordering_scores (maior = desbloqueada mais cedo no jogo).
    """
    ranked = sorted(user_ach, key=lambda a: ordering_scores.get(a["apiname"], 0.0), reverse=True)
    n = round(len(ranked) * ratio)
    return ranked[:n]


# ─── UI helpers ─────────────────────────────────────────────────────────────

def fmt_h(minutes):
    h = minutes / 60.0
    return f"{int(minutes)}min" if h < 1 else f"{h:.1f}h"


def hr(c="=", w=64):
    print(c * w)


# ─── Config ──────────────────────────────────────────────────────────────────

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_config(cfg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)


def setup(cfg):
    global _lang
    changed = False

    if "lang" not in cfg:
        print()
        print(_STRINGS["pt"]["lang_prompt"])
        print(_STRINGS["pt"]["lang_opt_en"])
        print(_STRINGS["pt"]["lang_opt_pt"])
        raw = input(_STRINGS["pt"]["lang_choice"]).strip()
        cfg["lang"] = "en" if raw == "1" else "pt"
        changed = True

    _lang = cfg["lang"]

    print(f"\n{T('setup_header')}")
    hr("-")

    if not cfg.get("api_key"):
        print(T("api_key_hint"))
        cfg["api_key"] = input(T("api_key_prompt")).strip()
        changed = True

    if not cfg.get("steam_id"):
        print(f"\n{T('steamid_hint')}")
        cfg["steam_id"] = input(T("steamid_prompt")).strip()
        changed = True

    if cfg.get("dll_path") and not os.path.exists(cfg["dll_path"]):
        print(T("dll_missing_warn", path=cfg["dll_path"]))
        print(T("dll_searching"))
        cfg["dll_path"] = ""
        changed = True

    if not cfg.get("dll_path"):
        dll = find_steam_api_dll()
        if dll:
            print(T("dll_found", dll=dll))
            cfg["dll_path"] = dll
            changed = True
        else:
            print(T("dll_not_found"))
            print(T("dll_hint1"))
            print(T("dll_hint2"))
            inp = input(T("dll_prompt")).strip().strip('"')
            if inp and os.path.exists(inp):
                cfg["dll_path"] = inp
                changed = True

    if changed:
        save_config(cfg)
    return cfg


# ─── Selecao de jogo ─────────────────────────────────────────────────────────

def pick_game(games):
    PAGE = 15
    page = 0
    while True:
        start = page * PAGE
        end   = min(start + PAGE, len(games))

        print(T("games_header", start=start+1, end=end, total=len(games)))
        hr("-")
        print(f"  {T('col_num'):>3}  {T('col_name'):<43} {T('col_time'):>7}")
        hr("-")
        for i, g in enumerate(games[start:end], start + 1):
            name = g.get("name", f"AppID {g['appid']}")
            print(f"  {i:>3}. {name[:43]:<43} {fmt_h(g.get('playtime_forever', 0)):>7}")

        print()
        nav = []
        if end < len(games):  nav.append(T("nav_next"))
        if page > 0:          nav.append(T("nav_prev"))
        nav += [T("nav_search"), T("nav_farm"), T("nav_all"), T("nav_reconfig"), T("nav_quit")]
        print("  " + "  |  ".join(nav))

        choice = input(T("choice_prompt")).strip().upper()

        if choice in ("S", "Q"):
            print(T("goodbye"))
            sys.exit(0)
        elif choice == "F":
            return "FARM"
        elif choice == "T":
            return "ALL"
        elif choice == "N" and end < len(games):
            page += 1
        elif choice == "A" and page > 0:
            page -= 1
        elif choice == "R":
            return None
        elif choice == "B":
            term = input(T("search_prompt")).strip().lower()
            hits = [(i, g) for i, g in enumerate(games) if term in g.get("name", "").lower()]
            if not hits:
                print(T("no_results"))
                continue
            print()
            for idx, (_, g) in enumerate(hits[:10], 1):
                print(f"  {idx}. {g.get('name','')} ({fmt_h(g.get('playtime_forever',0))})")
            try:
                sel = int(input(T("select_prompt"))) - 1
                if 0 <= sel < len(hits):
                    return hits[sel][1]
            except ValueError:
                pass
        else:
            try:
                n = int(choice) - 1
                if start <= n < end:
                    return games[n]
                elif 0 <= n < len(games):
                    return games[n]
            except ValueError:
                pass
        print(T("invalid_choice"))


# ─── Desbloqueio via Steamworks ───────────────────────────────────────────────

def read_state_via_steamworks(dll_path, app_id, achievement_names):
    """
    Lê o estado real das conquistas direto do cliente Steam (sem cache).
    Retorna lista no mesmo formato de get_player_achievements, ou None em caso de erro.
    """
    try:
        api = SteamAPI(dll_path)
    except Exception as e:
        return None, T("sw_dll_fail", err=e)

    ok, msg = api.connect(app_id)
    if not ok:
        return None, msg

    api.request_stats()
    api.pump(seconds=3.0)

    result = []
    for name in achievement_names:
        ok_get, achieved = api.get_achievement(name)
        if ok_get:
            result.append({"apiname": name, "achieved": 1 if achieved else 0})

    api.shutdown()

    if not result:
        return None, T("sw_no_ach_read")
    return result, "OK"


def apply_via_steamworks(dll_path, app_id, to_unlock, to_remove, currently_unlocked):
    """
    Aplica desbloqueios e/ou remoções via Steamworks.

    Quando há remoções usa a mesma estratégia do SAM:
      ResetAllStats → re-aplica as conquistas que devem ficar.
    Isso é necessário pois ClearAchievement por si só é rejeitado
    pelo servidor Steam em muitos jogos.

    currently_unlocked: set com os IDs já desbloqueados antes desta operação.
    """
    print(T("sw_loading_dll"))
    try:
        api = SteamAPI(dll_path)
    except Exception as e:
        return False, T("sw_dll_fail", err=e), [], []

    print(T("sw_connecting", id=app_id))
    ok, msg = api.connect(app_id)
    if not ok:
        return False, msg, [], []

    print(T("sw_requesting"))
    api.request_stats()
    api.pump(seconds=3.0)

    err_unlock = []
    err_remove = []

    if to_remove:
        remove_set = set(to_remove)
        unlock_set = set(to_unlock)
        final_state = (currently_unlocked - remove_set) | unlock_set

        print(T("sw_resetting"))
        ok_reset = api.reset_all(achievements_too=True)
        if not ok_reset:
            api.shutdown()
            return False, T("sw_reset_fail"), [], []
        api.pump(seconds=1.0)

        print(T("sw_reapplying", n=len(final_state)))
        for name in final_state:
            if api.unlock(name):
                marker = "[+]" if name in unlock_set else "[=]"
                print(f"    {marker} {name}")
            else:
                print(f"    [FAILED] {name}")
                if name in unlock_set:
                    err_unlock.append(name)
                else:
                    err_remove.append(name)

    else:
        if to_unlock:
            print(T("sw_unlocking", n=len(to_unlock)))
            for name in to_unlock:
                if api.unlock(name):
                    print(f"    [+] {name}")
                else:
                    print(f"    [FAILED] {name}")
                    err_unlock.append(name)

    print(T("sw_saving"))
    stored = api.store()
    api.pump(seconds=3.0)
    api.shutdown()

    if stored:
        return True, T("sw_success"), err_unlock, err_remove
    else:
        return False, T("sw_store_fail"), err_unlock, err_remove


# ─── Farm de horas ───────────────────────────────────────────────────────────

def _farm_worker(dll_path, app_id, duration_sec, data_file, status_file):
    """
    Subprocesso de farm: mantém sessão Steamworks ativa e desbloqueia
    conquistas progressivamente a cada 120s conforme as horas efetivas crescem.
    """
    os.environ["SteamAppId"] = str(app_id)

    ach_data = None
    try:
        if data_file and os.path.exists(data_file):
            with open(data_file, "r", encoding="utf-8") as fh:
                ach_data = json.load(fh)
    except Exception:
        ach_data = None

    has_ach = bool(
        ach_data
        and ach_data.get("achievements")
        and ach_data.get("completion_hours", 0) > 0
    )

    try:
        os.add_dll_directory(os.path.dirname(os.path.abspath(dll_path)))
        dll = ctypes.CDLL(dll_path)

        try:
            dll.SteamAPI_InitFlat.restype  = ctypes.c_int
            dll.SteamAPI_InitFlat.argtypes = [ctypes.c_char_p]
            err = ctypes.create_string_buffer(1024)
            if dll.SteamAPI_InitFlat(err) != 0:
                sys.exit(1)
        except AttributeError:
            dll.SteamAPI_Init.restype  = ctypes.c_bool
            dll.SteamAPI_Init.argtypes = []
            if not dll.SteamAPI_Init():
                sys.exit(1)

        dll.SteamAPI_RunCallbacks.restype  = None
        dll.SteamAPI_RunCallbacks.argtypes = []
        dll.SteamAPI_Shutdown.restype      = None
        dll.SteamAPI_Shutdown.argtypes     = []

        # Configurar UserStats para desbloqueio progressivo
        stats = None
        if has_ach:
            try:
                if _try_attr(dll, "SteamAPI_SteamUserStats_v013"):
                    dll.SteamAPI_SteamUserStats_v013.restype  = ctypes.c_void_p
                    dll.SteamAPI_SteamUserStats_v013.argtypes = []
                    stats = dll.SteamAPI_SteamUserStats_v013()
                else:
                    dll.SteamAPI_SteamUserStats.restype  = ctypes.c_void_p
                    dll.SteamAPI_SteamUserStats.argtypes = []
                    stats = dll.SteamAPI_SteamUserStats()

                if stats:
                    dll.SteamAPI_ISteamUserStats_SetAchievement.restype  = ctypes.c_bool
                    dll.SteamAPI_ISteamUserStats_SetAchievement.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
                    dll.SteamAPI_ISteamUserStats_StoreStats.restype      = ctypes.c_bool
                    dll.SteamAPI_ISteamUserStats_StoreStats.argtypes     = [ctypes.c_void_p]
                    if _try_attr(dll, "SteamAPI_ISteamUserStats_RequestCurrentStats"):
                        dll.SteamAPI_ISteamUserStats_RequestCurrentStats.restype  = ctypes.c_bool
                        dll.SteamAPI_ISteamUserStats_RequestCurrentStats.argtypes = [ctypes.c_void_p]
                        dll.SteamAPI_ISteamUserStats_RequestCurrentStats(stats)
            except Exception:
                stats = None

        orig_h      = ach_data.get("orig_playtime_hours", 0.0) if ach_data else 0.0
        comp_h      = ach_data.get("completion_hours", 30.0)   if ach_data else 30.0
        sorted_achs = ach_data.get("achievements", [])          if ach_data else []
        total_achs  = len(sorted_achs)
        already_set = set(ach_data.get("already_unlocked", [])) if ach_data else set()
        newly_set   = set()
        last_ach_t  = 0.0
        ACH_INTERVAL = 120  # segundos entre verificacoes de conquistas

        # Pump inicial para receber callbacks de stats
        for _ in range(30):
            dll.SteamAPI_RunCallbacks()
            time.sleep(0.1)

        start = time.time()
        while True:
            elapsed = time.time() - start
            if elapsed >= duration_sec:
                break
            dll.SteamAPI_RunCallbacks()

            # Verificar e desbloquear novas conquistas a cada ACH_INTERVAL s
            if has_ach and stats and (elapsed - last_ach_t) >= ACH_INTERVAL:
                last_ach_t = elapsed
                eff_h  = orig_h + elapsed / 3600.0
                ratio  = playtime_to_ratio(eff_h, comp_h)
                n_have = round(total_achs * ratio)
                should = {a["apiname"] for a in sorted_achs[:n_have]}
                new_now = should - already_set - newly_set

                if new_now:
                    for name in new_now:
                        dll.SteamAPI_ISteamUserStats_SetAchievement(
                            stats, name.encode("utf-8")
                        )
                        newly_set.add(name)
                    dll.SteamAPI_ISteamUserStats_StoreStats(stats)
                    try:
                        with open(status_file, "w", encoding="utf-8") as fh:
                            json.dump({"newly_unlocked": len(newly_set)}, fh)
                    except Exception:
                        pass

            time.sleep(1)

        dll.SteamAPI_Shutdown()
        sys.exit(0)
    except Exception:
        sys.exit(1)


def _pbar(current, total, width=22):
    filled = int(width * min(current / total, 1.0)) if total > 0 else width
    return "[" + "█" * filled + "░" * (width - filled) + "]"


def _fmt_t(seconds):
    seconds = max(0, int(seconds))
    h, r = divmod(seconds, 3600)
    m, s = divmod(r, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def farm_mode(games, dll_path, api_key, steam_id):
    """Modo interativo de farm de horas com desbloqueio progressivo de conquistas."""

    if not dll_path or not os.path.exists(dll_path):
        print(T("farm_no_dll"))
        input(T("press_enter_back")); return

    # Habilitar ANSI no terminal Windows
    try:
        ctypes.windll.kernel32.SetConsoleMode(
            ctypes.windll.kernel32.GetStdHandle(-11), 7
        )
    except Exception:
        pass

    # ── Selecionar jogos (multi) ──
    PAGE = 15
    page = 0
    selected = set()

    while True:
        s = page * PAGE
        e = min(s + PAGE, len(games))

        print(T("farm_header", start=s+1, end=e, total=len(games)))
        hr("-")
        for i, g in enumerate(games[s:e], s + 1):
            mark = "[x]" if (i - 1) in selected else "[ ]"
            name = g.get("name", f"AppID {g['appid']}")
            print(f"  {mark} {i:>3}. {name[:43]:<43} {fmt_h(g.get('playtime_forever',0)):>7}")

        print()
        nav = []
        if e < len(games): nav.append(T("nav_next"))
        if page > 0:       nav.append(T("nav_prev"))
        nav += [T("nav_search"), T("nav_all"), T("nav_confirm"), T("nav_cancel")]
        print("  " + "  |  ".join(nav))
        if selected:
            sel_names = [games[i].get("name", "?")[:20] for i in sorted(selected)]
            print(T("farm_selected", n=len(selected), names=', '.join(sel_names)))

        choice = input(T("choice_prompt")).strip().upper()

        if choice == "X":
            return
        elif choice == "T":
            if len(selected) == len(games):
                selected.clear()
            else:
                selected.update(range(len(games)))
        elif choice == "C":
            if selected: break
            print(T("farm_select_one"))
        elif choice == "N" and e < len(games):
            page += 1
        elif choice == "A" and page > 0:
            page -= 1
        elif choice == "B":
            term = input(T("search_prompt")).strip().lower()
            hits = [(i, g) for i, g in enumerate(games)
                    if term in g.get("name", "").lower()]
            if not hits:
                print(T("no_results")); continue
            for idx, (gi, g) in enumerate(hits[:10], 1):
                mark = "[x]" if gi in selected else "[ ]"
                print(f"  {mark} {idx}. {g.get('name','')} ({fmt_h(g.get('playtime_forever',0))})")
            inp = input(T("farm_toggle_prompt")).strip()
            if inp:
                try:
                    gi = hits[int(inp) - 1][0]
                    if gi in selected: selected.discard(gi)
                    else: selected.add(gi)
                except (ValueError, IndexError): pass
        else:
            try:
                n = int(choice) - 1
                if 0 <= n < len(games):
                    if n in selected: selected.discard(n)
                    else: selected.add(n)
            except ValueError:
                pass

    sel_games = [games[i] for i in sorted(selected)]

    # ── Quantidade de horas ──
    print()
    for g in sel_games:
        print(f"  + {g.get('name','')[:50]} ({fmt_h(g.get('playtime_forever',0))} atual)")
    print()
    try:
        raw = input(T("farm_hours_prompt")).strip().replace(",", ".")
        target_h = float(raw)
        if target_h <= 0: raise ValueError
    except ValueError:
        print(T("invalid_value")); input(T("press_enter_back")); return

    target_sec = target_h * 3600

    # ── Coletar dados de conquistas por jogo ──
    print(T("farm_collecting", n=len(sel_games)))
    tmp_files  = []   # (data_file, status_file) para limpeza posterior
    game_files = {}   # app_id -> (data_file, status_file)

    for g in sel_games:
        gid    = g["appid"]
        play_h = g.get("playtime_forever", 0) / 60.0
        label  = g.get("name", str(gid))[:30]
        print(f"    {label}...", end=" ", flush=True)

        gp                            = get_global_percentages(gid)
        schema                        = get_achievement_schema(api_key, gid) if api_key else {}
        sh_median_h, sh_lp, sh_unob  = get_steamhunters_data(gid)

        data_payload = None
        if schema and (gp or sh_lp):
            ach_names = list(schema.keys())

            # Estado atual via Web API (suficiente para farm — apenas adicoes)
            user_ach = None
            if api_key and steam_id:
                try:
                    web = get_player_achievements(api_key, steam_id, gid)
                    if web not in ("private", None):
                        user_ach = web
                except Exception:
                    pass
            if user_ach is None:
                user_ach = [{"apiname": n, "achieved": 0} for n in ach_names]

            already_unlocked = [a["apiname"] for a in user_ach if a.get("achieved") == 1]
            comp_h           = estimate_completion_hours(gp, sh_median_h)
            ord_scores       = blend_achievement_percentages(gp, sh_lp)
            sorted_achs      = sorted(
                [{"apiname": n} for n in ach_names if n not in sh_unob],
                key=lambda x: ord_scores.get(x["apiname"], 0.0), reverse=True,
            )
            src    = "SteamHunters" if sh_median_h else T("src_estimate")
            n_skip = len(ach_names) - len(sorted_achs)
            data_payload = {
                "orig_playtime_hours": play_h,
                "completion_hours": comp_h,
                "achievements": sorted_achs,
                "already_unlocked": already_unlocked,
            }
            if n_skip:
                print(T("farm_ach_info_skip", n=len(sorted_achs), unlocked=len(already_unlocked), src=src, skip=n_skip))
            else:
                print(T("farm_ach_info", n=len(sorted_achs), unlocked=len(already_unlocked), src=src))
        else:
            print(T("farm_no_ach"))

        # Criar arquivos temporarios
        fd_d, data_file   = tempfile.mkstemp(suffix=".json", prefix=f"farm_d_{gid}_")
        fd_s, status_file = tempfile.mkstemp(suffix=".json", prefix=f"farm_s_{gid}_")
        os.close(fd_d)
        os.close(fd_s)
        tmp_files.append((data_file, status_file))

        if data_payload:
            with open(data_file, "w", encoding="utf-8") as fh:
                json.dump(data_payload, fh)
        with open(status_file, "w", encoding="utf-8") as fh:
            json.dump({"newly_unlocked": 0}, fh)

        game_files[gid] = (data_file, status_file)

    print(T("farm_starting", h=target_h, n=len(sel_games)))
    print(T("farm_ctrl_c"))

    # ── Lançar subprocessos ──
    start_time = time.time()
    procs = []
    for g in sel_games:
        gid = g["appid"]
        data_file, status_file = game_files[gid]
        env = os.environ.copy()
        env["SteamAppId"] = str(gid)
        p = subprocess.Popen(
            [sys.executable, os.path.abspath(__file__),
             "--farm", dll_path, str(gid), str(target_sec),
             data_file, status_file],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=env,
        )
        procs.append((g, p, status_file))

    # ── Loop de progresso ──
    n_rows = len(procs)
    first  = True
    try:
        while True:
            elapsed   = time.time() - start_time
            remaining = target_sec - elapsed
            all_done  = all(p.poll() is not None for _, p, _ in procs)

            if not first:
                sys.stdout.write(f"\033[{n_rows}A")
            first = False

            for g, p, sf in procs:
                name = g.get("name", f"AppID {g['appid']}")[:30]
                bar  = _pbar(elapsed, target_sec)
                done = p.poll() is not None

                newly = 0
                try:
                    with open(sf, "r", encoding="utf-8") as fh:
                        newly = json.load(fh).get("newly_unlocked", 0)
                except Exception:
                    pass

                ach_str = f" +{newly}ach" if newly > 0 else ""
                status  = T("farm_done") if done else _fmt_t(remaining)
                sys.stdout.write(
                    f"\033[2K  {name:<30} {bar}  "
                    f"{elapsed/3600:.2f}h/{target_h:.1f}h{ach_str}  {status}\n"
                )
            sys.stdout.flush()

            if all_done or elapsed >= target_sec:
                break
            time.sleep(1)

    except KeyboardInterrupt:
        print(T("farm_interrupted"))
    finally:
        for _, p, _ in procs:
            if p.poll() is None:
                p.terminate()
        for df, sf in tmp_files:
            for fp in (df, sf):
                try:
                    os.remove(fp)
                except OSError:
                    pass

    total_h = (time.time() - start_time) / 3600
    print(T("farm_finished", h=total_h))
    input(T("press_enter_list"))


# ─── Modo em lote ────────────────────────────────────────────────────────────

def batch_achievements_mode(games, dll_path, api_key, steam_id):
    """Processa conquistas de todos os jogos com tempo de jogo de uma vez."""
    hr()
    print(T("batch_header", n=len(games)))
    hr("-")
    print(T("batch_note"))
    hr("-")

    # ── Fase 1: coletar dados de todos os jogos ──
    pending = []
    for i, g in enumerate(games, 1):
        app_id = g["appid"]
        play_h = g.get("playtime_forever", 0) / 60.0
        name   = g.get("name", f"AppID {app_id}")

        print(T("batch_loading", i=i, n=len(games), name=name[:45]), end="\r", flush=True)

        global_pct = get_global_percentages(app_id)
        schema     = get_achievement_schema(api_key, app_id)
        if not schema:
            continue

        achievement_names = list(schema.keys())

        web_ach = get_player_achievements(api_key, steam_id, app_id)
        if web_ach in ("private", None):
            user_ach         = [{"apiname": n, "achieved": 0} for n in achievement_names]
            profile_readable = False
        else:
            user_ach         = web_ach
            profile_readable = True

        sh_median_h, sh_local_pct, sh_unobtainable = get_steamhunters_data(app_id)

        ordering_scores = blend_achievement_percentages(global_pct, sh_local_pct)
        completion_h    = estimate_completion_hours(global_pct, sh_median_h)
        ratio           = playtime_to_ratio(play_h, completion_h)
        should_have     = select_to_unlock(user_ach, ordering_scores, ratio)
        should_have_ids = {a["apiname"] for a in should_have}
        unlocked        = {a["apiname"] for a in user_ach if a.get("achieved") == 1}

        to_unlock = [
            a for a in should_have
            if a["apiname"] not in unlocked and a["apiname"] not in sh_unobtainable
        ]
        to_remove = (
            [a for a in user_ach if a.get("achieved") == 1 and a["apiname"] not in should_have_ids]
            if profile_readable else []
        )

        if to_unlock or to_remove:
            pending.append({
                "game":     g,
                "app_id":   app_id,
                "name":     name,
                "play_h":   play_h,
                "ratio":    ratio,
                "schema":   schema,
                "to_unlock": to_unlock,
                "to_remove": to_remove,
                "unlocked": unlocked,
                "global_pct": global_pct,
            })

    # Limpar linha de progresso
    print(" " * 70, end="\r")

    if not pending:
        print(T("batch_no_actions"))
        input(T("press_enter_list2"))
        return

    # ── Fase 2: exibir resumo ──
    hr("-")
    print(T("batch_summary"))
    hr("-")
    print(f"  {T('col_num'):>3}  {T('col_name'):<43} {T('col_unlock'):>10} {T('col_remove'):>8}")
    hr("-")
    for i, p in enumerate(pending, 1):
        print(f"  {i:>3}. {p['name'][:43]:<43} {len(p['to_unlock']):>10} {len(p['to_remove']):>8}")
    hr("-")

    n_with_remove = sum(1 for p in pending if p["to_remove"])
    if n_with_remove:
        print(T("batch_has_remove", n=n_with_remove))
        print(T("warn_reset2"))

    print(T("attention"))
    resp = input(T("batch_confirm", n=len(pending))).strip().lower()
    if not is_yes(resp):
        print(T("cancelled"))
        input(T("press_enter_list2"))
        return

    if not dll_path or not os.path.exists(dll_path):
        print(T("dll_error"))
        print(T("dll_error2"))
        input(T("press_enter_list2"))
        return

    # ── Fase 3: aplicar alteracoes ──
    hr()
    logs_dir = os.path.join(SCRIPT_DIR, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    ok_count = 0

    for i, p in enumerate(pending, 1):
        print(T("batch_processing", i=i, n=len(pending), name=p["name"][:40]))

        ids_unlock = [a["apiname"] for a in p["to_unlock"]]
        ids_remove = [a["apiname"] for a in p["to_remove"]]

        ok, msg, err_unlock, err_remove = apply_via_steamworks(
            dll_path, p["app_id"], ids_unlock, ids_remove, p["unlocked"]
        )

        if ok:
            ok_count += 1
            if ids_unlock:
                print(T("result_unlocked", ok=len(ids_unlock)-len(err_unlock), total=len(ids_unlock)))
            if ids_remove:
                print(T("result_removed", ok=len(ids_remove)-len(err_remove), total=len(ids_remove)))

            safe_name = "".join(c if c.isalnum() or c in " -_()" else "_" for c in p["name"]).strip()
            ts  = datetime.now().strftime("%Y%m%d_%H%M%S")
            log = os.path.join(logs_dir, f"{safe_name}_{ts}.txt")
            with open(log, "w", encoding="utf-8") as f:
                f.write(T("log_header", date=datetime.now().strftime('%d/%m/%Y %H:%M')) + "\n")
                f.write(T("log_game", name=p["name"], id=p["app_id"]) + "\n")
                f.write(T("log_time", h=p["play_h"], pct=p["ratio"]*100) + "\n\n")
                if ids_unlock:
                    f.write(T("log_unlocked", n=len(ids_unlock)) + "\n")
                    for name in ids_unlock:
                        status  = ("FALHOU" if _lang == "pt" else "FAILED") if name in err_unlock else "OK"
                        display = p["schema"].get(name, {}).get("displayName", name)
                        f.write(f"  [{status}] {name} — {display}\n")
                    f.write("\n")
                if ids_remove:
                    f.write(T("log_removed", n=len(ids_remove)) + "\n")
                    for name in ids_remove:
                        status  = ("FALHOU" if _lang == "pt" else "FAILED") if name in err_remove else "OK"
                        display = p["schema"].get(name, {}).get("displayName", name)
                        f.write(f"  [{status}] {name} — {display}\n")
            print(T("log_saved", log=log))
        else:
            print(f"  {msg}")
        hr("-")

    hr()
    print(T("batch_done", ok=ok_count, total=len(pending)))
    print(T("restart_steam"))
    input(T("press_enter_list2"))


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    global _lang
    cfg = load_config()
    _lang = cfg.get("lang", "pt")

    hr()
    print("    STEAM ACHIEVEMENT AUTO-UNLOCKER")
    print(T("app_subtitle"))
    hr()

    cfg = setup(cfg)

    api_key  = cfg.get("api_key", "")
    steam_id = cfg.get("steam_id", "")
    dll_path = cfg.get("dll_path", "")

    if not api_key or not steam_id:
        print(T("creds_incomplete"))
        input(T("press_enter_exit")); sys.exit(1)

    # ── Carregar jogos ──
    print(T("loading_library"))
    all_games = get_owned_games(api_key, steam_id)
    if not all_games:
        print(T("load_error"))
        print(T("load_check_key"))
        print(T("load_check_id"))
        print(T("load_check_public"))
        input(T("press_enter")); sys.exit(1)

    games = sorted(
        [g for g in all_games if g.get("playtime_forever", 0) > 0],
        key=lambda g: g.get("playtime_forever", 0), reverse=True
    )
    print(T("games_loaded", n=len(games)))

    # ── Loop principal — processa um jogo por vez, volta a lista ao concluir ──
    while True:
        # Selecionar jogo
        selected = None
        while selected is None:
            selected = pick_game(games)
            if selected == "FARM":
                farm_mode(games, dll_path, api_key, steam_id)
                selected = None
            elif selected == "ALL":
                batch_achievements_mode(games, dll_path, api_key, steam_id)
                selected = None
            elif selected is None:
                cfg      = setup(cfg)
                dll_path = cfg.get("dll_path", "")

        app_id    = selected["appid"]
        play_min  = selected.get("playtime_forever", 0)
        play_h    = play_min / 60.0
        game_name = selected.get("name", f"AppID {app_id}")

        hr()
        print(T("game_label", name=game_name))
        print(T("appid_label", id=app_id))
        print(T("time_label", h=play_h))
        hr()

        # Carregar dados
        print(T("loading_ach"))
        global_pct = get_global_percentages(app_id)
        schema     = get_achievement_schema(api_key, app_id)

        if not schema:
            print(T("no_ach_registered"))
            input(T("press_enter_list2")); continue

        achievement_names = list(schema.keys())
        profile_readable  = True
        user_ach          = None

        # Fonte primária: Steamworks (leitura direta, sem cache)
        if dll_path and os.path.exists(dll_path):
            print(T("reading_steamworks"))
            user_ach, sw_msg = read_state_via_steamworks(dll_path, app_id, achievement_names)
            if user_ach is None:
                print(T("warn_steamworks", msg=sw_msg))

        # Fallback: Web API (pode ter cache)
        if user_ach is None:
            print(T("trying_webapi"))
            web_ach = get_player_achievements(api_key, steam_id, app_id)
            if web_ach not in ("private", None):
                user_ach = web_ach
            else:
                if web_ach == "private":
                    print(T("warn_403"))
                else:
                    print(T("warn_webapi_down"))
                user_ach = [{"apiname": n, "achieved": 0} for n in achievement_names]
                profile_readable = False

        if not user_ach:
            print(T("no_ach"))
            input(T("press_enter_list2")); continue

        total    = len(user_ach)
        unlocked = {a["apiname"] for a in user_ach if a.get("achieved") == 1}
        locked   = [a for a in user_ach if a.get("achieved") == 0]

        if profile_readable:
            print(T("total_ach", n=total))
            print(T("unlocked_ach", n=len(unlocked)))
            print(T("locked_ach", n=len(locked)))
        else:
            print(T("total_ach_unknown", n=total))

        if not global_pct:
            print(T("warn_no_pct"))

        # Dados reais do SteamHunters
        print(T("querying_sh"), end=" ", flush=True)
        sh_median_h, sh_local_pct, sh_unobtainable = get_steamhunters_data(app_id)
        if sh_median_h or sh_local_pct:
            sh_info = []
            if sh_median_h:
                sh_info.append(T("sh_median", h=sh_median_h))
            if sh_local_pct:
                sh_info.append(T("sh_ach_count", n=len(sh_local_pct)))
            if sh_unobtainable:
                sh_info.append(T("sh_unob_count", n=len(sh_unobtainable)))
            print("OK (" + ", ".join(sh_info) + ")")
        else:
            print(T("sh_no_data"))

        # Calcular conquistas recomendadas
        ordering_scores = blend_achievement_percentages(global_pct, sh_local_pct)
        completion_h    = estimate_completion_hours(global_pct, sh_median_h)
        ratio           = playtime_to_ratio(play_h, completion_h)
        should_have     = select_to_unlock(user_ach, ordering_scores, ratio)
        should_have_ids = {a["apiname"] for a in should_have}

        to_unlock = [
            a for a in should_have
            if a["apiname"] not in unlocked and a["apiname"] not in sh_unobtainable
        ]
        skipped_unobtainable = [
            a for a in should_have
            if a["apiname"] not in unlocked and a["apiname"] in sh_unobtainable
        ]
        # Remocao so e possivel quando o perfil e legivel (sabemos o que esta desbloqueado)
        to_remove = (
            [a for a in user_ach if a.get("achieved") == 1 and a["apiname"] not in should_have_ids]
            if profile_readable else []
        )

        src_label = "SteamHunters" if sh_median_h else T("src_estimate")
        print(T("est_hours", h=completion_h, src=src_label))
        print(T("est_progress", pct=ratio*100))
        print(T("should_have", n=len(should_have), total=total))
        print(T("to_unlock", n=len(to_unlock)))
        if skipped_unobtainable:
            print(T("skipped_unob", n=len(skipped_unobtainable)))
        print(T("to_remove", n=len(to_remove)), end="")
        if not profile_readable:
            print(T("profile_private"), end="")
        print()

        # Previsao de conquistas futuras
        n_current = round(total * ratio)
        if n_current < total and ratio < 1.0:
            print(T("forecast_header"))
            for step in [1, 5, 10]:
                n_target = n_current + step
                if n_target > total:
                    break
                ratio_target = (n_target - 0.5) / total
                delta = max(0.0, hours_for_ratio(ratio_target, completion_h) - play_h)
                label = T("forecast_step", n=step) if step == 1 else T("forecast_steps", n=step)
                print(f"    {label:<16} ~{delta:.1f}h")
            delta_100 = max(0.0, completion_h - play_h)
            if delta_100 > 0.1:
                print(f"    {'100%':<16} ~{delta_100:.1f}h")

        if not to_unlock and not to_remove:
            print(T("all_good"))
            if ratio >= 1.0:
                print(T("all_good_100"))
            input(T("press_enter_list2")); continue

        # ── Exibir lista de desbloqueio ──
        if to_unlock:
            hr()
            print(T("list_unlock_header", n=len(to_unlock)))
            hr("-")
            print(f"  {T('col_num'):>3}  {T('col_name'):<47} {T('col_global'):>7}")
            hr("-")
            for i, a in enumerate(to_unlock, 1):
                api_name = a["apiname"]
                display  = schema.get(api_name, {}).get("displayName", api_name)
                pct      = global_pct.get(api_name, 0.0)
                print(f"  {i:>3}. {display[:47]:<47} {pct:>6.1f}%")
            hr("-")

        # ── Exibir lista de remocao ──
        if to_remove:
            hr()
            print(T("list_remove_header", n=len(to_remove), h=play_h))
            hr("-")
            print(f"  {T('col_num'):>3}  {T('col_name'):<47} {T('col_global'):>7}")
            hr("-")
            for i, a in enumerate(to_remove, 1):
                api_name = a["apiname"]
                display  = schema.get(api_name, {}).get("displayName", api_name)
                pct      = global_pct.get(api_name, 0.0)
                print(f"  {i:>3}. {display[:47]:<47} {pct:>6.1f}%")
            hr("-")

        # ── Confirmar acoes ──
        print(T("attention"))
        do_unlock = False
        do_remove = False

        if to_unlock:
            resp = input(T("confirm_unlock", n=len(to_unlock))).strip().lower()
            do_unlock = is_yes(resp)

        if to_remove:
            print(T("warn_reset"))
            print(T("warn_reset2"))
            resp = input(T("confirm_remove", n=len(to_remove))).strip().lower()
            do_remove = is_yes(resp)

        if not do_unlock and not do_remove:
            print(T("no_action"))
            input(T("press_enter_list")); continue

        # ── Verificar DLL ──
        if not dll_path or not os.path.exists(dll_path):
            print(T("dll_error"))
            print(T("dll_error2"))
            input(T("press_enter_list2")); continue

        # ── Aplicar via Steamworks ──
        ids_unlock = [a["apiname"] for a in to_unlock] if do_unlock else []
        ids_remove = [a["apiname"] for a in to_remove] if do_remove else []

        ok, msg, err_unlock, err_remove = apply_via_steamworks(
            dll_path, app_id, ids_unlock, ids_remove, unlocked
        )

        hr()
        if ok:
            if ids_unlock:
                print(T("result_unlocked", ok=len(ids_unlock)-len(err_unlock), total=len(ids_unlock)))
                if err_unlock:
                    print(T("result_failed", names=', '.join(err_unlock)))
            if ids_remove:
                print(T("result_removed", ok=len(ids_remove)-len(err_remove), total=len(ids_remove)))
                if err_remove:
                    print(T("result_failed", names=', '.join(err_remove)))
            print(T("restart_steam"))
        else:
            print(f"  {msg}")
        hr()

        # ── Salvar log ──
        logs_dir = os.path.join(SCRIPT_DIR, "logs")
        os.makedirs(logs_dir, exist_ok=True)
        safe_name = "".join(c if c.isalnum() or c in " -_()" else "_" for c in game_name).strip()
        ts  = datetime.now().strftime("%Y%m%d_%H%M%S")
        log = os.path.join(logs_dir, f"{safe_name}_{ts}.txt")
        with open(log, "w", encoding="utf-8") as f:
            f.write(T("log_header", date=datetime.now().strftime('%d/%m/%Y %H:%M')) + "\n")
            f.write(T("log_game", name=game_name, id=app_id) + "\n")
            f.write(T("log_time", h=play_h, pct=ratio*100) + "\n\n")
            if ids_unlock:
                f.write(T("log_unlocked", n=len(ids_unlock)) + "\n")
                for name in ids_unlock:
                    status  = ("FALHOU" if _lang == "pt" else "FAILED") if name in err_unlock else "OK"
                    display = schema.get(name, {}).get("displayName", name)
                    f.write(f"  [{status}] {name} — {display}\n")
                f.write("\n")
            if ids_remove:
                f.write(T("log_removed", n=len(ids_remove)) + "\n")
                for name in ids_remove:
                    status  = ("FALHOU" if _lang == "pt" else "FAILED") if name in err_remove else "OK"
                    display = schema.get(name, {}).get("displayName", name)
                    f.write(f"  [{status}] {name} — {display}\n")
        print(T("log_saved", log=log))

        input(T("press_enter_list2"))


if __name__ == "__main__":
    # Modo subprocesso de farm: --farm <dll_path> <app_id> <seconds> <data_file> <status_file>
    if len(sys.argv) == 7 and sys.argv[1] == "--farm":
        _farm_worker(sys.argv[2], int(sys.argv[3]), float(sys.argv[4]), sys.argv[5], sys.argv[6])
    else:
        try:
            _cfg = load_config()
            _lang = _cfg.get("lang", "pt")
        except Exception:
            pass
        try:
            main()
        except KeyboardInterrupt:
            print(T("cancelled"))
            input(T("press_enter_exit"))
            sys.exit(0)
        except Exception as e:
            import traceback
            hr()
            print(T("unexpected_error"))
            hr()
            traceback.print_exc()
            hr()
            input(T("press_enter_exit"))
