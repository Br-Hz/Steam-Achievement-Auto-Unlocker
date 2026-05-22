# Steam Achievement Auto-Unlocker

**[English](#english) | [Português](#português)**

---

## English

Automatically unlocks and removes Steam achievements based on your actual playtime. Available in two modes: a **graphical interface (GUI)** and a **command-line interface (CLI)**.

---

### Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [GUI Mode](#gui-mode)
- [CLI Mode](#cli-mode)
- [Generated Files](#generated-files)
- [Notes](#notes-en)
- [Disclaimer](#disclaimer)

---

### Features

**Shared between GUI and CLI**

- **Playtime-based unlocking** — calculates how many achievements you should have based on hours played and unlocks the difference
- **Real data via SteamHunters** — uses actual median completion time and local unlock percentages
- **Combined ordering** — blends Steam's global percentage with SteamHunters' local percentage to determine the natural unlock order
- **Unobtainable filter** — achievements from expired events or removed DLCs are automatically skipped
- **Progress forecast** — shows how many more hours are needed for the next +1, +5, +10 achievements and for 100%
- **Hour farming** — keeps simultaneous Steamworks sessions on multiple games with progressive achievement unlocking
- **Direct Steamworks reading** — reads real achievement state without relying on API cache
- **Bilingual** — Portuguese and English

**GUI only**

- Dark-themed graphical interface with game search, dual achievement lists, and live status bar
- Per-game live progress bars and elapsed/target time during farm
- Batch mode button to process the entire library in one click
- Settings dialog — edit API key, Steam ID, DLL path, and language without restarting

**CLI only**

- Paginated game list with keyboard navigation
- Inline confirmation prompts before applying any change
- Detailed unlock log printed to the terminal and saved to file

---

### Requirements

- Windows 10/11
- Python 3.8 or higher
- Steam installed, running, and logged into your account
- At least one Steam game installed (`steam_api64.dll` is detected automatically)
- Steam profile set to **public** (or use Steamworks for direct reading)

---

### Installation

```bash
pip install requests customtkinter
```

`customtkinter` is only required for GUI mode. All other modules (`ctypes`, `winreg`, `json`, `math`) are part of the Python standard library.

---

### Configuration

Both modes share the same config file (`steam_config.json`).

| Field | Where to get it |
|---|---|
| **Steam API Key** | [steamcommunity.com/dev/apikey](https://steamcommunity.com/dev/apikey) |
| **Steam ID (64-bit)** | [steamidfinder.com](https://www.steamidfinder.com/) |
| **steam_api64.dll** | Auto-detected from installed games; any Steam game folder contains this file |

- **GUI**: open the **Settings** button (bottom-left) on first run
- **CLI**: the script prompts for missing values automatically on first run

Settings are saved to `steam_config.json` next to the script.

---

### GUI Mode

#### Launch

```bash
python steam_achievements.py
```

The GUI opens by default. The console window is hidden automatically.

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

1. Select a game from the left panel (search by name if needed)
2. The app queries Steam and SteamHunters **in parallel** and calculates your expected progress
3. Achievements to unlock and remove appear in the right panel
4. Click **Unlock** to unlock the listed achievements, or **Remove** to remove the excess ones
5. The panel refreshes automatically after applying

#### Hour farming

1. Click **Farm Hours** to open the farm dialog
2. Each game row has a checkbox and an individual **hours** field (default: `1.0`)
3. Select games, adjust hours per game, click **Start Farm**
4. All selected games are farmed **simultaneously** — each row shows a live progress bar with elapsed / target time
5. Color coding: blue = running · green = done · red = stopped
6. Click **Stop Farm** at any time; click **Start Farm** again to run a new batch without closing the dialog

#### Process All

Click **Process All** to analyze and apply achievements across your entire library. A confirmation dialog is shown before starting.

---

### CLI Mode

#### Launch

```bash
python steam_achievements.py --cli
```

#### Navigation

```
  #   Name                                          Time
  1.  Game Name                                    12.5h
  2.  Another Game                                  3.2h
  ...

  [N] Next  |  [A] Previous  |  [B] Search  |  [F] Farm hours  |  [T] All  |  [R] Reconfigure  |  [S] Quit
```

| Key | Action |
|---|---|
| Number | Select game |
| `B` | Search by name |
| `F` | Open farm mode |
| `T` | Batch mode (all games) |
| `N` / `A` | Next / previous page |
| `R` | Reconfigure settings |
| `S` / `Q` | Quit |

#### Main flow

1. Select a game by number or search
2. The script loads achievement data and displays:
   - Total / unlocked / locked count
   - Estimated completion time and current progress
   - Forecast (hours needed for next achievements)
   - Numbered list of achievements to unlock and remove
3. Confirm with `s`/`y` to apply, or press Enter to skip

#### Farm mode (CLI)

Select `[F]` from the main menu:

- Select one or more games (or `[T]` for all)
- Enter the number of hours to farm
- A live progress display updates in the terminal with elapsed time and achievement count per game
- Press `Ctrl+C` to stop

---

### Generated Files

| File | Description |
|---|---|
| `steam_config.json` | User settings (API key, Steam ID, DLL path, language) |
| `logs/` | Per-game unlock history with timestamps |

---

### Notes {#notes-en}

- Steam must be **open and logged in** during any unlock or farm operation
- Removing achievements uses `ResetAllStats`, which also **resets in-game statistics** (counters, kills, etc.)
- Achievements marked as unobtainable by SteamHunters are automatically skipped
- SteamHunters data is optional — if unavailable, the app falls back to a rarity-based estimate
- API calls are made in parallel to minimize loading time

---

### Disclaimer

This project is for educational purposes. Using tools that manipulate Steam achievements may violate the [Steam Subscriber Agreement](https://store.steampowered.com/subscriber_agreement/). Use at your own risk.

---
---

## Português

Desbloqueia e remove conquistas Steam automaticamente com base no seu tempo de jogo real. Disponível em dois modos: **interface gráfica (GUI)** e **interface de linha de comando (CLI)**.

---

### Índice

- [Funcionalidades](#funcionalidades)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Modo GUI](#modo-gui)
- [Modo CLI](#modo-cli)
- [Arquivos gerados](#arquivos-gerados)
- [Observações](#observações)
- [Aviso](#aviso)

---

### Funcionalidades

**Compartilhadas entre GUI e CLI**

- **Desbloqueio por tempo de jogo** — calcula quantas conquistas você deveria ter com base nas horas jogadas e desbloqueia a diferença
- **Dados reais via SteamHunters** — usa o tempo mediano real de conclusão e percentuais locais de desbloqueio
- **Ordenação combinada** — combina o percentual global do Steam com o percentual local do SteamHunters para determinar a ordem natural de desbloqueio
- **Filtro de inobtaináveis** — conquistas de eventos expirados ou DLCs removidos são ignoradas automaticamente
- **Previsão de progresso** — mostra quantas horas faltam para as próximas +1, +5, +10 conquistas e para 100%
- **Farm de horas** — mantém sessões Steamworks simultâneas em múltiplos jogos com desbloqueio progressivo
- **Leitura direta via Steamworks** — lê o estado real das conquistas sem depender de cache da API
- **Bilíngue** — Português e Inglês

**Exclusivo da GUI**

- Interface gráfica com tema escuro, busca de jogos, listas duplas de conquistas e barra de status ao vivo
- Barras de progresso individuais com tempo decorrido/definido durante o farm
- Botão de processamento em lote para toda a biblioteca com um clique
- Diálogo de Configurações — edite API key, Steam ID, caminho do DLL e idioma sem reiniciar

**Exclusivo do CLI**

- Lista de jogos paginada com navegação por teclado
- Confirmação antes de aplicar qualquer alteração
- Log detalhado impresso no terminal e salvo em arquivo

---

### Requisitos

- Windows 10/11
- Python 3.8 ou superior
- Steam instalado, aberto e logado na sua conta
- Pelo menos um jogo Steam instalado (o `steam_api64.dll` é detectado automaticamente)
- Conta Steam com perfil **público** (ou use Steamworks para leitura direta)

---

### Instalação

```bash
pip install requests customtkinter
```

`customtkinter` é necessário apenas para o modo GUI. Os demais módulos (`ctypes`, `winreg`, `json`, `math`) são parte da biblioteca padrão do Python.

---

### Configuração

Ambos os modos compartilham o mesmo arquivo de configuração (`steam_config.json`).

| Campo | Onde obter |
|---|---|
| **Steam API Key** | [steamcommunity.com/dev/apikey](https://steamcommunity.com/dev/apikey) |
| **Steam ID (64-bit)** | [steamidfinder.com](https://www.steamidfinder.com/) |
| **steam_api64.dll** | Detectado automaticamente nos jogos instalados; presente na pasta de qualquer jogo Steam |

- **GUI**: abra o botão **Configurações** (canto inferior esquerdo) na primeira execução
- **CLI**: o script solicita os dados ausentes automaticamente na primeira execução

As configurações são salvas em `steam_config.json` na pasta do script.

---

### Modo GUI

#### Executar

```bash
python steam_achievements.py
```

A GUI abre por padrão. A janela do terminal é ocultada automaticamente.

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

1. Selecione um jogo no painel esquerdo (use a busca se necessário)
2. O app consulta o Steam e o SteamHunters **em paralelo** e calcula o progresso esperado
3. As conquistas a desbloquear e remover aparecem no painel direito
4. Clique em **Desbloquear** para desbloquear as conquistas listadas, ou **Remover** para remover o excesso
5. O painel atualiza automaticamente após aplicar

#### Farm de horas

1. Clique em **Farm Horas** para abrir o diálogo de farm
2. Cada linha de jogo tem uma caixa de seleção e um campo individual de **horas** (padrão: `1.0`)
3. Selecione os jogos, ajuste o tempo de cada um, clique em **Iniciar Farm**
4. Todos os jogos selecionados são farmados **simultaneamente** — cada linha mostra uma barra de progresso ao vivo com tempo decorrido / tempo definido
5. Cores: azul = rodando · verde = concluído · vermelho = parado
6. Clique em **Parar Farm** a qualquer momento; clique em **Iniciar Farm** novamente para um novo lote sem fechar o diálogo

#### Processar Todos

Clique em **Processar Todos** para analisar e aplicar conquistas em toda a biblioteca. Uma confirmação é exibida antes de iniciar.

---

### Modo CLI

#### Executar

```bash
python steam_achievements.py --cli
```

#### Navegação

```
  #   Nome                                          Tempo
  1.  Nome do Jogo                                 12.5h
  2.  Outro Jogo                                    3.2h
  ...

  [N] Próxima  |  [A] Anterior  |  [B] Buscar  |  [F] Farmar horas  |  [T] Todos  |  [R] Reconfigurar  |  [S] Sair
```

| Tecla | Ação |
|---|---|
| Número | Selecionar jogo |
| `B` | Buscar por nome |
| `F` | Abrir modo farm |
| `T` | Modo em lote (todos os jogos) |
| `N` / `A` | Próxima / página anterior |
| `R` | Reconfigurar configurações |
| `S` / `Q` | Sair |

#### Fluxo principal

1. Selecione um jogo por número ou busca
2. O script carrega os dados e exibe:
   - Total / desbloqueadas / bloqueadas
   - Tempo estimado de conclusão e progresso atual
   - Previsão (horas para as próximas conquistas)
   - Lista numerada de conquistas a desbloquear e remover
3. Confirme com `s`/`y` para aplicar, ou Enter para pular

#### Modo farm (CLI)

Selecione `[F]` no menu principal:

- Selecione um ou mais jogos (ou `[T]` para todos)
- Informe o número de horas para farmar
- Um display ao vivo no terminal mostra tempo decorrido e conquistas desbloqueadas por jogo
- Pressione `Ctrl+C` para parar

---

### Arquivos gerados

| Arquivo | Descrição |
|---|---|
| `steam_config.json` | Configurações do usuário (API key, Steam ID, caminho do DLL, idioma) |
| `logs/` | Histórico de desbloqueios por jogo com timestamp |

---

### Observações

- O Steam deve estar **aberto e logado** durante qualquer operação de desbloqueio ou farm
- A remoção de conquistas usa `ResetAllStats`, o que também **zera estatísticas de jogo** (contadores, kills, etc.)
- Conquistas marcadas como inobtaináveis pelo SteamHunters são ignoradas automaticamente
- Os dados do SteamHunters são opcionais — se indisponíveis, o app usa uma estimativa baseada na raridade
- As chamadas de API são feitas em paralelo para minimizar o tempo de carregamento

---

### Aviso

Este projeto é para fins educacionais. O uso de ferramentas que manipulam conquistas Steam pode violar os [Termos de Serviço da Steam](https://store.steampowered.com/subscriber_agreement/). Use por sua conta e risco.
