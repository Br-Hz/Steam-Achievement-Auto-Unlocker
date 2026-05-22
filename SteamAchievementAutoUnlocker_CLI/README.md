# Steam Achievement Auto-Unlocker — CLI

**[English](#english) | [Português](#português)**

---

## English

Terminal-based tool that automatically unlocks and removes Steam achievements based on your actual playtime. Uses SteamHunters data to calculate expected progress and orders achievements by global unlock frequency.

### Features

- **Playtime-based unlocking** — calculates how many achievements you should have based on hours played and unlocks the difference
- **Real data via SteamHunters** — uses actual median completion time and local unlock percentages
- **Combined ordering** — blends Steam's global percentage with SteamHunters' local percentage to determine the natural unlock order
- **Unobtainable filter** — achievements from expired events or removed DLCs are automatically skipped
- **Progress forecast** — shows how many more hours are needed for the next +1, +5, +10 achievements and for 100%
- **Hour farming** — keeps simultaneous Steamworks sessions on multiple games with progressive achievement unlocking
- **Batch mode** — scan and process achievements across your entire library in one pass
- **Direct Steamworks reading** — reads real achievement state without relying on API cache
- **Bilingual** — Portuguese and English, selected on first run

### Requirements

- Windows 10/11
- Python 3.8 or higher
- Steam installed, running, and logged into your account
- At least one Steam game installed (`steam_api64.dll` is detected automatically)
- Steam profile set to **public** (or use Steamworks for direct reading)

### Installation

```bash
pip install requests
```

All other modules (`ctypes`, `winreg`, `json`, `math`) are part of the Python standard library.

### Configuration

On first run the script prompts for:

| Field | Where to get it |
|---|---|
| **Steam API Key** | [steamcommunity.com/dev/apikey](https://steamcommunity.com/dev/apikey) |
| **Steam ID (64-bit)** | [steamidfinder.com](https://www.steamidfinder.com/) |

The `steam_api64.dll` is located automatically from installed games. If not found, the script asks for the path — the file is present in the folder of any Steam game that uses the Steamworks API.

Settings are saved to `steam_config.json` in the script's folder.

### Usage

```bash
python steam_achievements.py
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

1. Select a game by number or search by name
2. The script loads achievement data and displays:
   - Total / unlocked / locked count
   - Estimated completion time and current progress percentage
   - Forecast: hours needed for the next +1, +5, +10 achievements and 100%
   - Numbered list of achievements to unlock and to remove
3. Confirm with `s`/`y` to apply, or press Enter to skip

#### Hour farming

1. Select `[F]` from the main menu
2. Select one or more games (or `[T]` for all)
3. Enter the number of hours to farm
4. A live progress display updates in the terminal with elapsed time and achievement count per game
5. Press `Ctrl+C` to stop at any time

#### Batch mode

Select `[T]` from the main menu to scan all games in your library and apply achievement changes automatically.

### Generated files

| File | Description |
|---|---|
| `steam_config.json` | User settings (API key, Steam ID, DLL path, language) |
| `logs/` | Per-game unlock history with timestamps |

### Notes

- Steam must be **open and logged in** during any unlock or farm operation
- Removing achievements uses `ResetAllStats`, which also **resets in-game statistics** (counters, kills, etc.)
- Achievements marked as unobtainable by SteamHunters are automatically skipped
- SteamHunters data is optional — if unavailable, the script falls back to a rarity-based estimate

### Disclaimer

This project is for educational purposes. Using tools that manipulate Steam achievements may violate the [Steam Subscriber Agreement](https://store.steampowered.com/subscriber_agreement/). Use at your own risk.

---

## Português

Ferramenta de terminal que desbloqueia e remove conquistas Steam automaticamente com base no seu tempo de jogo real. Utiliza dados do SteamHunters para calcular o progresso esperado e ordena as conquistas pela frequência global de desbloqueio.

### Funcionalidades

- **Desbloqueio por tempo de jogo** — calcula quantas conquistas você deveria ter com base nas horas jogadas e desbloqueia a diferença
- **Dados reais via SteamHunters** — usa o tempo mediano real de conclusão e percentuais locais de desbloqueio
- **Ordenação combinada** — combina o percentual global do Steam com o percentual local do SteamHunters para determinar a ordem natural de desbloqueio
- **Filtro de inobtaináveis** — conquistas de eventos expirados ou DLCs removidos são ignoradas automaticamente
- **Previsão de progresso** — mostra quantas horas faltam para as próximas +1, +5, +10 conquistas e para 100%
- **Farm de horas** — mantém sessões Steamworks simultâneas em múltiplos jogos com desbloqueio progressivo
- **Modo em lote** — escaneia e processa conquistas de toda a biblioteca em uma única passagem
- **Leitura direta via Steamworks** — lê o estado real das conquistas sem depender de cache da API
- **Bilíngue** — Português e Inglês, selecionado na primeira execução

### Requisitos

- Windows 10/11
- Python 3.8 ou superior
- Steam instalado, aberto e logado na sua conta
- Pelo menos um jogo Steam instalado (o `steam_api64.dll` é detectado automaticamente)
- Conta Steam com perfil **público** (ou use Steamworks para leitura direta)

### Instalação

```bash
pip install requests
```

Os demais módulos (`ctypes`, `winreg`, `json`, `math`) são parte da biblioteca padrão do Python.

### Configuração

Na primeira execução o script solicita:

| Campo | Onde obter |
|---|---|
| **Steam API Key** | [steamcommunity.com/dev/apikey](https://steamcommunity.com/dev/apikey) |
| **Steam ID (64-bit)** | [steamidfinder.com](https://www.steamidfinder.com/) |

O `steam_api64.dll` é localizado automaticamente nos jogos instalados. Se não for encontrado, o script solicita o caminho — o arquivo está presente na pasta de qualquer jogo Steam que use a Steamworks API.

As configurações são salvas em `steam_config.json` na pasta do script.

### Como usar

```bash
python steam_achievements.py
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

1. Selecione um jogo por número ou busque pelo nome
2. O script carrega os dados e exibe:
   - Total / desbloqueadas / bloqueadas
   - Tempo estimado de conclusão e percentual de progresso atual
   - Previsão: horas para as próximas +1, +5, +10 conquistas e 100%
   - Lista numerada de conquistas a desbloquear e a remover
3. Confirme com `s`/`y` para aplicar, ou pressione Enter para pular

#### Farm de horas

1. Selecione `[F]` no menu principal
2. Selecione um ou mais jogos (ou `[T]` para todos)
3. Informe o número de horas para farmar
4. Um display ao vivo no terminal mostra o tempo decorrido e conquistas desbloqueadas por jogo
5. Pressione `Ctrl+C` para parar a qualquer momento

#### Modo em lote

Selecione `[T]` no menu principal para escanear todos os jogos da biblioteca e aplicar as alterações automaticamente.

### Arquivos gerados

| Arquivo | Descrição |
|---|---|
| `steam_config.json` | Configurações do usuário (API key, Steam ID, caminho do DLL, idioma) |
| `logs/` | Histórico de desbloqueios por jogo com timestamp |

### Observações

- O Steam deve estar **aberto e logado** durante qualquer operação de desbloqueio ou farm
- A remoção de conquistas usa `ResetAllStats`, o que também **zera estatísticas de jogo** (contadores, kills, etc.)
- Conquistas marcadas como inobtaináveis pelo SteamHunters são ignoradas automaticamente
- Os dados do SteamHunters são opcionais — se indisponíveis, o script usa uma estimativa baseada na raridade

### Aviso

Este projeto é para fins educacionais. O uso de ferramentas que manipulam conquistas Steam pode violar os [Termos de Serviço da Steam](https://store.steampowered.com/subscriber_agreement/). Use por sua conta e risco.
