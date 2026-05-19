# Steam Achievement Auto-Unlocker

**[English](#english) | [Português](#português)**

---

## English

Automatically unlocks and removes Steam achievements based on your actual playtime. Uses SteamHunters data to calculate expected progress and orders achievements by global unlock frequency — no external tools like SAM required.

### Features

- **Playtime-based unlocking** — calculates how many achievements you should have based on hours played and unlocks the difference
- **Real data via SteamHunters** — uses actual median completion time instead of estimates
- **Combined ordering** — blends Steam's global percentage with SteamHunters' local percentage to determine the natural unlock order
- **Unobtainable filter** — achievements from expired events or removed DLCs are automatically ignored
- **Progress forecast** — shows how many more hours are needed to reach the next achievements
- **Hour farming** — keeps active sessions on multiple games simultaneously with progressive unlocking
- **Direct Steamworks reading** — reads real achievement state without relying on API cache

### Requirements

- Windows 10/11
- Python 3.8 or higher
- Steam installed, running, and logged into your account
- At least one Steam game installed (`steam_api64.dll` is detected automatically)
- Steam profile set to **public** (or use Steamworks for direct reading)

#### Python dependencies

```
pip install requests
```

All other modules used (`ctypes`, `winreg`, `json`, `math`) are part of the Python standard library.

### Configuration

On first run the script will ask for two values:

| Field | Where to get it |
|---|---|
| **Steam API Key** | [steamcommunity.com/dev/apikey](https://steamcommunity.com/dev/apikey) |
| **Steam ID (64-bit)** | [steamidfinder.com](https://www.steamidfinder.com/) |

The `steam_api64.dll` is located automatically from installed games. If not found, the script asks for the path manually — the file is present in the folder of any Steam game that uses the Steamworks API.

Settings are saved to `steam_config.json` in the script's folder.

### Usage

#### Running

```bash
python steam_achievements.py
```

Or use the included `executar_steam_achievements.bat` file.

#### Main flow

1. Select a game from your library (sorted by playtime)
2. The script queries Steam and SteamHunters to calculate expected progress
3. A list of achievements to unlock and/or remove is displayed
4. Confirm the actions — Steam must be open during the process
5. Restart Steam for changes to appear on your profile

#### Hour farming

Select **[F] Farmar horas** from the game list to start simultaneous sessions. Achievements are unlocked progressively as accumulated hours increase.

### Generated files

| File | Description |
|---|---|
| `steam_config.json` | User settings (API key, Steam ID, DLL path) |
| `logs/` | Unlock history per game with timestamps |

### Notes

- Steam must be **open and logged in** during any unlock operation
- Removing achievements uses `ResetAllStats`, which also **resets in-game statistics** (counters, kills, etc.)
- Achievements marked as unobtainable by SteamHunters are automatically skipped
- SteamHunters data is optional — if unavailable, the script falls back to a rarity-based estimate

### Disclaimer

This project is for educational purposes. Using tools that manipulate Steam achievements may violate the [Steam Subscriber Agreement](https://store.steampowered.com/subscriber_agreement/). Use at your own risk.

---

## Português

Desbloqueia e remove conquistas Steam automaticamente com base no seu tempo de jogo real. Utiliza dados do SteamHunters para calcular o progresso esperado e ordena as conquistas pela frequência global de desbloqueio — sem necessidade de ferramentas externas como o SAM.

### Funcionalidades

- **Desbloqueio por tempo de jogo** — calcula quantas conquistas você deveria ter com base nas horas jogadas e desbloqueia a diferença
- **Dados reais via SteamHunters** — usa o tempo mediano real de conclusão em vez de estimativas
- **Ordenação combinada** — combina o percentual global do Steam com o percentual local do SteamHunters para determinar a ordem natural de desbloqueio
- **Filtro de inobtaináveis** — conquistas de eventos expirados ou DLCs removidos são ignoradas automaticamente
- **Previsão de progresso** — mostra quantas horas de jogo faltam para as próximas conquistas
- **Farm de horas** — mantém sessões ativas em múltiplos jogos simultaneamente com desbloqueio progressivo
- **Leitura direta via Steamworks** — lê o estado real das conquistas sem depender de cache da API

### Requisitos

- Windows 10/11
- Python 3.8 ou superior
- Steam instalado, aberto e logado na sua conta
- Pelo menos um jogo Steam instalado (o `steam_api64.dll` é detectado automaticamente)
- Conta Steam com perfil **público** (ou use Steamworks para leitura direta)

#### Dependências Python

```
pip install requests
```

Os demais módulos utilizados (`ctypes`, `winreg`, `json`, `math`) são parte da biblioteca padrão do Python.

### Configuração

Na primeira execução o script pedirá dois dados:

| Campo | Onde obter |
|---|---|
| **Steam API Key** | [steamcommunity.com/dev/apikey](https://steamcommunity.com/dev/apikey) |
| **Steam ID (64-bit)** | [steamidfinder.com](https://www.steamidfinder.com/) |

O `steam_api64.dll` é localizado automaticamente nos jogos instalados. Se não for encontrado, o script solicita o caminho manualmente — o arquivo está presente na pasta de qualquer jogo Steam que use a Steamworks API.

As configurações são salvas em `steam_config.json` na pasta do script.

### Como usar

#### Execução

```bash
python steam_achievements.py
```

Ou use o arquivo `executar_steam_achievements.bat` incluído.

#### Fluxo principal

1. Selecione um jogo da sua biblioteca (ordenada por tempo de jogo)
2. O script consulta o Steam e o SteamHunters para calcular o progresso esperado
3. É exibida a lista de conquistas a desbloquear e/ou remover
4. Confirme as ações — o Steam precisa estar aberto durante o processo
5. Reinicie o Steam para as alterações aparecerem no perfil

#### Farm de horas

Selecione **[F] Farmar horas** na lista de jogos para iniciar sessões simultâneas. As conquistas são desbloqueadas progressivamente conforme as horas acumuladas aumentam.

### Arquivos gerados

| Arquivo | Descrição |
|---|---|
| `steam_config.json` | Configurações do usuário (API key, Steam ID, caminho do DLL) |
| `logs/` | Histórico de desbloqueios por jogo com timestamp |

### Observações

- O Steam deve estar **aberto e logado** durante qualquer operação de desbloqueio
- A remoção de conquistas usa `ResetAllStats`, o que também **zera estatísticas de jogo** (contadores, kills, etc.)
- Conquistas marcadas como inobtaináveis pelo SteamHunters são ignoradas automaticamente
- Os dados do SteamHunters são opcionais — se indisponíveis, o script usa uma estimativa baseada na raridade das conquistas

### Aviso

Este projeto é para fins educacionais. O uso de ferramentas que manipulam conquistas Steam pode violar os [Termos de Serviço da Steam](https://store.steampowered.com/subscriber_agreement/). Use por sua conta e risco.
