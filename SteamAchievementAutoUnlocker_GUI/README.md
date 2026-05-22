# Steam Achievement Auto-Unlocker — GUI

**[English](#english) | [Português](#português)**

---

## English

Graphical interface tool that automatically unlocks and removes Steam achievements based on your actual playtime. Uses SteamHunters data to calculate expected progress and orders achievements by global unlock frequency.

### Features

- **Dark-themed graphical interface** — game search, dual achievement lists, live status bar, and progress forecast all in one window
- **Playtime-based unlocking** — calculates how many achievements you should have based on hours played and unlocks the difference
- **Real data via SteamHunters** — uses actual median completion time and local unlock percentages
- **Combined ordering** — blends Steam's global percentage with SteamHunters' local percentage to determine the natural unlock order
- **Unobtainable filter** — achievements from expired events or removed DLCs are automatically skipped
- **Progress forecast** — shows how many more hours are needed for the next +1, +5, +10 achievements and for 100%, displayed directly in the game panel
- **Hour farming** — simultaneous Steamworks sessions on multiple games, each with an individual time setting and a live progress bar
- **Batch mode** — process achievements across the entire library with one click
- **Direct Steamworks reading** — reads real achievement state without relying on API cache
- **Settings dialog** — configure API key, Steam ID, DLL path, and language without restarting
- **Bilingual** — Portuguese and English, selectable from Settings

### Requirements

- Windows 10/11
- Python 3.8 or higher
- Steam installed, running, and logged into your account
- At least one Steam game installed (`steam_api64.dll` is detected automatically)
- Steam profile set to **public** (or use Steamworks for direct reading)

### Installation

```bash
pip install requests customtkinter Pillow
```

All other modules (`ctypes`, `winreg`, `json`, `math`) are part of the Python standard library.

### Configuration

On first run the app opens with an empty game list. Click the **Settings** button (bottom-left) and fill in:

| Field | Where to get it |
|---|---|
| **Steam API Key** | [steamcommunity.com/dev/apikey](https://steamcommunity.com/dev/apikey) |
| **Steam ID (64-bit)** | [steamidfinder.com](https://www.steamidfinder.com/) |
| **steam_api64.dll** | Auto-detected from installed games; use Browse if not found |

Settings are saved to `steam_config.json` in the script's folder.

### Usage

```bash
python steam_achievements.py
```

The console window is hidden automatically.

#### Layout

```
┌─────────────────┬──────────────────────────────────────────────┐
│  Search box     │  Game name                                    │
│                 │  AppID · Playtime · Est. completion time      │
│  Game list      │  ████████████░░░░  Progress bar              │
│  (scrollable)   ├──────────────────────────────────────────────┤
│                 │  Progress %  |  Forecast: +1: ~0.5h  100%... │
│                 ├──────────────────────────────────────────────┤
│                 │  [Unlock]  [Remove]  [Refresh]               │
│                 ├──────────────┬───────────────────────────────┤
│  [Process All]  │ To Unlock(n) │ To Remove (n)                 │
│  [Farm Hours]   │  Achievement │  Achievement                  │
│  [Settings]     │  ...         │  ...                          │
├─────────────────┴──────────────┴───────────────────────────────┤
│  Status bar                                                     │
└─────────────────────────────────────────────────────────────────┘
```

#### Main flow

1. Select a game from the left panel — search by name if needed
2. The app queries Steam and SteamHunters **in parallel** to calculate your expected progress
3. Achievements to unlock and to remove appear in the right panel alongside the forecast
4. Click **Unlock** or **Remove** — Steam must be open during the process
5. The panel refreshes automatically after applying

#### Hour farming

1. Click **Farm Hours** to open the farm dialog
2. Each game row has a checkbox and an individual **hours** field (default: `1.0`)
3. Select games, set a duration per game, click **Start Farm**
4. All selected games are farmed **simultaneously**
5. Each row shows a live progress bar with elapsed / target time
6. Color coding: blue = running · green = done · red = stopped
7. Click **Stop Farm** at any time; click **Start Farm** again to run a new batch without closing the dialog

#### Process All

Click **Process All** to analyze and apply achievements across your entire library. A confirmation dialog is shown before starting.

### Generated files

| File | Description |
|---|---|
| `steam_config.json` | User settings (API key, Steam ID, DLL path, language) |
| `logs/` | Per-game unlock history with timestamps |

### Notes

- Steam must be **open and logged in** during any unlock or farm operation
- Removing achievements uses `ResetAllStats`, which also **resets in-game statistics** (counters, kills, etc.)
- Achievements marked as unobtainable by SteamHunters are automatically skipped
- SteamHunters data is optional — if unavailable, the app falls back to a rarity-based estimate
- API calls are made in parallel to minimize loading time

### Disclaimer

This project is for educational purposes. Using tools that manipulate Steam achievements may violate the [Steam Subscriber Agreement](https://store.steampowered.com/subscriber_agreement/). Use at your own risk.

---

## Português

Ferramenta com interface gráfica que desbloqueia e remove conquistas Steam automaticamente com base no seu tempo de jogo real. Utiliza dados do SteamHunters para calcular o progresso esperado e ordena as conquistas pela frequência global de desbloqueio.

### Funcionalidades

- **Interface gráfica com tema escuro** — busca de jogos, listas duplas de conquistas, barra de status ao vivo e previsão de progresso em uma única janela
- **Desbloqueio por tempo de jogo** — calcula quantas conquistas você deveria ter com base nas horas jogadas e desbloqueia a diferença
- **Dados reais via SteamHunters** — usa o tempo mediano real de conclusão e percentuais locais de desbloqueio
- **Ordenação combinada** — combina o percentual global do Steam com o percentual local do SteamHunters para determinar a ordem natural de desbloqueio
- **Filtro de inobtaináveis** — conquistas de eventos expirados ou DLCs removidos são ignoradas automaticamente
- **Previsão de progresso** — mostra quantas horas faltam para as próximas +1, +5, +10 conquistas e para 100%, exibido diretamente no painel do jogo
- **Farm de horas** — sessões Steamworks simultâneas em múltiplos jogos, cada um com tempo individual e barra de progresso ao vivo
- **Modo em lote** — processa conquistas de toda a biblioteca com um clique
- **Leitura direta via Steamworks** — lê o estado real das conquistas sem depender de cache da API
- **Diálogo de configurações** — edite API key, Steam ID, caminho do DLL e idioma sem reiniciar
- **Bilíngue** — Português e Inglês, selecionável nas Configurações

### Requisitos

- Windows 10/11
- Python 3.8 ou superior
- Steam instalado, aberto e logado na sua conta
- Pelo menos um jogo Steam instalado (o `steam_api64.dll` é detectado automaticamente)
- Conta Steam com perfil **público** (ou use Steamworks para leitura direta)

### Instalação

```bash
pip install requests customtkinter Pillow
```

Os demais módulos (`ctypes`, `winreg`, `json`, `math`) são parte da biblioteca padrão do Python.

### Configuração

Na primeira execução o app abre com a lista de jogos vazia. Clique em **Configurações** (canto inferior esquerdo) e preencha:

| Campo | Onde obter |
|---|---|
| **Steam API Key** | [steamcommunity.com/dev/apikey](https://steamcommunity.com/dev/apikey) |
| **Steam ID (64-bit)** | [steamidfinder.com](https://www.steamidfinder.com/) |
| **steam_api64.dll** | Detectado automaticamente nos jogos instalados; use Procurar se não encontrado |

As configurações são salvas em `steam_config.json` na pasta do script.

### Como usar

```bash
python steam_achievements.py
```

A janela do terminal é ocultada automaticamente.

#### Layout

```
┌─────────────────┬──────────────────────────────────────────────┐
│  Campo de busca │  Nome do jogo                                 │
│                 │  AppID · Tempo jogado · Tempo est. conclusão  │
│  Lista de jogos │  ████████████░░░░  Barra de progresso        │
│  (rolável)      ├──────────────────────────────────────────────┤
│                 │  Progresso %  |  Previsão: +1: ~0.5h  100%.. │
│                 ├──────────────────────────────────────────────┤
│                 │  [Desbloquear]  [Remover]  [Atualizar]       │
│                 ├──────────────┬───────────────────────────────┤
│  [Proc. Todos]  │ Para Desbl.  │ Para Remover                  │
│  [Farm Horas]   │  Conquista   │  Conquista                    │
│  [Configurações]│  ...         │  ...                          │
├─────────────────┴──────────────┴───────────────────────────────┤
│  Barra de status                                                │
└─────────────────────────────────────────────────────────────────┘
```

#### Fluxo principal

1. Selecione um jogo no painel esquerdo — use a busca se necessário
2. O app consulta o Steam e o SteamHunters **em paralelo** para calcular o progresso esperado
3. As conquistas a desbloquear e remover aparecem no painel direito junto com a previsão
4. Clique em **Desbloquear** ou **Remover** — o Steam precisa estar aberto durante o processo
5. O painel atualiza automaticamente após aplicar

#### Farm de horas

1. Clique em **Farm Horas** para abrir o diálogo de farm
2. Cada linha de jogo tem uma caixa de seleção e um campo individual de **horas** (padrão: `1.0`)
3. Selecione os jogos, defina um tempo para cada um, clique em **Iniciar Farm**
4. Todos os jogos selecionados são farmados **simultaneamente**
5. Cada linha mostra uma barra de progresso ao vivo com tempo decorrido / tempo definido
6. Cores: azul = rodando · verde = concluído · vermelho = parado
7. Clique em **Parar Farm** a qualquer momento; clique em **Iniciar Farm** novamente para um novo lote sem fechar o diálogo

#### Processar Todos

Clique em **Processar Todos** para analisar e aplicar conquistas em toda a biblioteca. Uma confirmação é exibida antes de iniciar.

### Arquivos gerados

| Arquivo | Descrição |
|---|---|
| `steam_config.json` | Configurações do usuário (API key, Steam ID, caminho do DLL, idioma) |
| `logs/` | Histórico de desbloqueios por jogo com timestamp |

### Observações

- O Steam deve estar **aberto e logado** durante qualquer operação de desbloqueio ou farm
- A remoção de conquistas usa `ResetAllStats`, o que também **zera estatísticas de jogo** (contadores, kills, etc.)
- Conquistas marcadas como inobtaináveis pelo SteamHunters são ignoradas automaticamente
- Os dados do SteamHunters são opcionais — se indisponíveis, o app usa uma estimativa baseada na raridade
- As chamadas de API são feitas em paralelo para minimizar o tempo de carregamento

### Aviso

Este projeto é para fins educacionais. O uso de ferramentas que manipulam conquistas Steam pode violar os [Termos de Serviço da Steam](https://store.steampowered.com/subscriber_agreement/). Use por sua conta e risco.
