# Steam Achievement Auto-Unlocker

**[English](#english) | [Português](#português)**

---

## English

Automatically unlocks and removes Steam achievements based on your actual playtime. Uses SteamHunters data to calculate expected progress and orders achievements by global unlock frequency — no external tools like SAM required.

### Features

- **Graphical interface** — dark-themed GUI with game search, achievement lists, and live status
- **Playtime-based unlocking** — calculates how many achievements you should have based on hours played and unlocks the difference
- **Real data via SteamHunters** — uses actual median completion time instead of estimates
- **Combined ordering** — blends Steam's global percentage with SteamHunters' local percentage to determine the natural unlock order
- **Unobtainable filter** — achievements from expired events or removed DLCs are automatically skipped
- **Progress forecast** — shows how many more hours are needed for the next +1, +5, +10 achievements and 100%
- **Hour farming** — keeps simultaneous sessions on multiple games with individual time settings and live progress per game
- **Batch mode** — process all games in your library in a single click
- **Direct Steamworks reading** — reads real achievement state without relying on API cache
- **Bilingual** — Portuguese and English, selectable from Settings

### Requirements

- Windows 10/11
- Python 3.8 or higher
- Steam installed, running, and logged into your account
- At least one Steam game installed (`steam_api64.dll` is detected automatically)
- Steam profile set to **public** (or use Steamworks for direct reading)

#### Python dependencies

```
pip install requests customtkinter
```

All other modules (`ctypes`, `winreg`, `json`, `math`) are part of the Python standard library.

### Configuration

On first run the app will open with an empty game list. Open **Settings** (bottom-left button) and fill in:

| Field | Where to get it |
|---|---|
| **Steam API Key** | [steamcommunity.com/dev/apikey](https://steamcommunity.com/dev/apikey) |
| **Steam ID (64-bit)** | [steamidfinder.com](https://www.steamidfinder.com/) |
| **steam_api64.dll** | Auto-detected from installed games; use Browse if not found |

Settings are saved to `steam_config.json` in the script's folder.

### Usage

#### Running

```bash
python steam_achievements.py
```

This launches the GUI. To use the original terminal interface instead:

```bash
python steam_achievements.py --cli
```

#### GUI layout

| Area | Description |
|---|---|
| **Left panel** | Searchable game list sorted by playtime |
| **Right panel** | Selected game's name, AppID, playtime, completion time estimate, progress bar, forecast, achievement lists (To Unlock / To Remove), action buttons |
| **Status bar** | Current operation feedback at the bottom |

#### Main flow

1. Select a game from the list on the left
2. The app queries Steam and SteamHunters in parallel to calculate expected progress
3. Achievements to unlock and remove are displayed in separate lists
4. Click **Unlock** or **Remove** — Steam must be open during the process
5. The app refreshes automatically after applying

#### Hour farming

Click **Farm Hours** to open the farm dialog:

- Each game row shows its name, current playtime, and an individual **hours** field
- Select one or more games and set a different duration for each
- Click **Start Farm** — all selected games are farmed **simultaneously**
- Each row shows a live progress bar with elapsed / target time
- Click **Stop Farm** at any time; the farm can be restarted without closing the dialog

#### Process All

Click **Process All** to analyze and apply achievements across every game in your library. A confirmation is shown before starting.

### Generated files

| File | Description |
|---|---|
| `steam_config.json` | User settings (API key, Steam ID, DLL path, language) |
| `logs/` | Unlock history per game with timestamps |

### Notes

- Steam must be **open and logged in** during any unlock or farm operation
- Removing achievements uses `ResetAllStats`, which also **resets in-game statistics** (counters, kills, etc.)
- Achievements marked as unobtainable by SteamHunters are automatically skipped
- SteamHunters data is optional — if unavailable, the app falls back to a rarity-based estimate
- The console window is hidden automatically when launching the GUI

### Disclaimer

This project is for educational purposes. Using tools that manipulate Steam achievements may violate the [Steam Subscriber Agreement](https://store.steampowered.com/subscriber_agreement/). Use at your own risk.

---

## Português

Desbloqueia e remove conquistas Steam automaticamente com base no seu tempo de jogo real. Utiliza dados do SteamHunters para calcular o progresso esperado e ordena as conquistas pela frequência global de desbloqueio — sem necessidade de ferramentas externas como o SAM.

### Funcionalidades

- **Interface gráfica** — GUI com tema escuro, busca de jogos, listas de conquistas e status em tempo real
- **Desbloqueio por tempo de jogo** — calcula quantas conquistas você deveria ter com base nas horas jogadas e desbloqueia a diferença
- **Dados reais via SteamHunters** — usa o tempo mediano real de conclusão em vez de estimativas
- **Ordenação combinada** — combina o percentual global do Steam com o percentual local do SteamHunters para determinar a ordem natural de desbloqueio
- **Filtro de inobtaináveis** — conquistas de eventos expirados ou DLCs removidos são ignoradas automaticamente
- **Previsão de progresso** — mostra quantas horas faltam para as próximas +1, +5, +10 conquistas e para 100%
- **Farm de horas** — sessões simultâneas em múltiplos jogos com tempo individual por jogo e progresso ao vivo
- **Modo em lote** — processa todos os jogos da biblioteca com um clique
- **Leitura direta via Steamworks** — lê o estado real das conquistas sem depender de cache da API
- **Bilíngue** — Português e Inglês, selecionável nas Configurações

### Requisitos

- Windows 10/11
- Python 3.8 ou superior
- Steam instalado, aberto e logado na sua conta
- Pelo menos um jogo Steam instalado (o `steam_api64.dll` é detectado automaticamente)
- Conta Steam com perfil **público** (ou use Steamworks para leitura direta)

#### Dependências Python

```
pip install requests customtkinter
```

Os demais módulos (`ctypes`, `winreg`, `json`, `math`) são parte da biblioteca padrão do Python.

### Configuração

Na primeira execução o app abre com a lista de jogos vazia. Clique em **Configurações** (botão inferior esquerdo) e preencha:

| Campo | Onde obter |
|---|---|
| **Steam API Key** | [steamcommunity.com/dev/apikey](https://steamcommunity.com/dev/apikey) |
| **Steam ID (64-bit)** | [steamidfinder.com](https://www.steamidfinder.com/) |
| **steam_api64.dll** | Detectado automaticamente nos jogos instalados; use Procurar se não encontrado |

As configurações são salvas em `steam_config.json` na pasta do script.

### Como usar

#### Execução

```bash
python steam_achievements.py
```

Isso abre a interface gráfica. Para usar a interface de terminal original:

```bash
python steam_achievements.py --cli
```

#### Layout da GUI

| Área | Descrição |
|---|---|
| **Painel esquerdo** | Lista de jogos com busca, ordenada por tempo de jogo |
| **Painel direito** | Nome do jogo, AppID, tempo jogado, estimativa de conclusão, barra de progresso, previsão, listas de conquistas (Para Desbloquear / Para Remover), botões de ação |
| **Barra de status** | Feedback da operação atual na parte inferior |

#### Fluxo principal

1. Selecione um jogo na lista à esquerda
2. O app consulta o Steam e o SteamHunters em paralelo para calcular o progresso esperado
3. As conquistas a desbloquear e remover são exibidas em listas separadas
4. Clique em **Desbloquear** ou **Remover** — o Steam precisa estar aberto durante o processo
5. O app atualiza automaticamente após aplicar

#### Farm de horas

Clique em **Farm Horas** para abrir o diálogo de farm:

- Cada linha de jogo exibe o nome, tempo atual e um campo individual de **horas**
- Selecione um ou mais jogos e defina um tempo diferente para cada um
- Clique em **Iniciar Farm** — todos os jogos selecionados são farmados **simultaneamente**
- Cada linha mostra uma barra de progresso ao vivo com tempo decorrido / tempo definido
- Clique em **Parar Farm** a qualquer momento; o farm pode ser reiniciado sem fechar o diálogo

#### Processar Todos

Clique em **Processar Todos** para analisar e aplicar conquistas em todos os jogos da biblioteca. Uma confirmação é exibida antes de iniciar.

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
- A janela do terminal é ocultada automaticamente ao abrir a GUI

### Aviso

Este projeto é para fins educacionais. O uso de ferramentas que manipulam conquistas Steam pode violar os [Termos de Serviço da Steam](https://store.steampowered.com/subscriber_agreement/). Use por sua conta e risco.
