# Command List

> Use `-h` or `help` after a command to view detailed help, e.g., `/stat help`

| Command  | Description                        | Notes                      | Link                   |
| -------- | ---------------------------------- | -------------------------- | ---------------------- |
| `/cls`   | Clear cache files                  | Admin only                 | [Jump](#cls-command)   |
| `/admin` | View bot running status            | Admin only                 | [Jump](#admin-command) |
| `/link`  | Link game account (UID or IGN)     | Supports UID or IGN format | [Jump](#link-command)  |
| `/alias` | Manage aliases (list/add/delete)   | Use `list`, `del`, `add`   | [Jump](#alias-command) |
| `/lang`  | Switch display language            | Supports `cn`, `en`, `ja`  | [Jump](#lang-command)  |
| `/algo`  | Set scoring algorithm              | Use `default` or `none`    | [Jump](#algo-command)  |
| `/mode`  | Switch image display mode          | Use `light` / `dark`       | [Jump](#mode-command)  |
| `/theme` | Set or view available image themes | Supports various themes    | [Jump](#theme-command) |
| `/stat`  | Query battle stats (user & mode)   | Can specify battle mode    | [Jump](#stat-command)  |

## `/cls` Command Guide

**Used to clear unnecessary cache files generated during the Bot's operation.**

> 🔐 Only available to users with admin privileges.

### 🧩 Command Format

```bash
/cls
```

### 🔧 Parameter Description

No parameters

### 📌 Examples

```bash
/cls
```

### 💡 Notes

- This action is irreversible. Use with caution.

---

## `/admin` Command Guide

**Used to check the current day’s bot status, including server resource usage and the amount of data processed.**

> 🔐 Only available to users with admin privileges.

### 🧩 Command Format

```bash
/admin
```

### 🔧 Parameter Description

No parameters

### 📌 Examples

```bash
/admin
```

---

## `/link` Command Guide

**Used to link your game account. You can bind via UID or "Server + IGN".**

### 🧩 Command Format

```bash
/link user:<user identifier>
```

### 🔧 Parameter Description

| Parameter | Required | Description                                                          |
| --------- | -------- | -------------------------------------------------------------------- |
| `user`    | ✅       | Enter your game UID, or use `Server IGN` format (separated by space) |

### 📌 Examples

```bash
# Example 1: Link with UID
/link 2023619512

# Example 2: Link with Server and IGN
/link asia SangonomiyaKokomi_
```

---

## `/alias` Command Guide

**Used to manage user account aliases to simplify future queries.**

Supports adding, deleting, and viewing aliases. Once set, you can use the alias instead of UID or IGN to quickly query stats and other data.

### 🧩 Command Format

```bash
# View aliases
/alias list
# Delete alias
/alias del index:<index>
# Add alias
/alias add alias:<alias> player:<player identifier>
```

### 🔧 Parameter Description

| Parameter | Required | Description                                                           |
| --------- | -------- | --------------------------------------------------------------------- |
| `index`   | ✅       | The number of the alias to be deleted                                 |
| `alias`   | ✅       | The alias name. Must not be purely numeric and max 15 characters long |
| `player`  | ✅       | Game UID or `Server IGN` format (space-separated)                     |

### 📌 Examples

```bash
# View current aliases
/alias list

# Delete the second alias
/alias del 2

# Add an alias for UID
/alias add myfriend 2023619512

# Add an alias for server + IGN
/alias add captain asia SangonomiyaKokomi_
```

### 💡 Notes

- Alias must not exceed 15 characters.
- Alias **cannot be purely numeric** to avoid confusion with UID.

---

## `/lang` Command Guide

**Used to switch the Bot’s display language. Currently supports Chinese (cn), English (en), and Japanese (ja).**

### 🧩 Command Format

```bash
/lang lang:<language_code>
```

### 🔧 Parameter Description

| Parameter | Required | Description                    |
| --------- | -------- | ------------------------------ |
| `lang`    | ✅       | Valid values: `cn`, `en`, `ja` |

### 📌 Examples

```bash
/lang cn
```

---

## `/algo` Command Guide

**Used to switch the user rating algorithm.**

Currently supported algorithms:

- `default`: Default rating algorithm.
- `none`: Disable rating display (no rating).

### 🧩 Command Format

```bash
/algo mode:<rating_mode>
```

### 🔧 Parameter Description

| Parameter | Required | Description                       |
| --------- | -------- | --------------------------------- |
| `mode`    | ✅       | Allowed values: `default`, `none` |

### 📌 Examples

```bash
/algo default
/algo none
```

---

## `/mode` Command Guide

**Used to switch the image rendering mode (Light / Dark) for the Bot.**

Currently supported modes:

- `light`: Light mode with bright background.
- `dark`: Dark mode with dark background.

### 🧩 Command Format

```bash
/mode mode:<display_mode>
```

### 🔧 Parameter Description

| Parameter | Required | Description                     |
| --------- | -------- | ------------------------------- |
| `mode`    | ✅       | Allowed values: `light`, `dark` |

### 📌 Examples

```bash
/mode dark
/mode light
```

---

## `/theme` Command Guide

**Used to switch the visual theme of image outputs or view the list of available themes.**

Two usage modes:

1. Use `list` to view available themes and their codes.
2. Provide a theme code to change the current theme.

### 🧩 Command Format

```bash
/theme list
# or
/theme theme:<theme_code>
```

### 🔧 Parameter Description

| Parameter | Required | Description                                           |
| --------- | -------- | ----------------------------------------------------- |
| `theme`   | ✅       | Enter theme code or use `list` to view available ones |

### 📌 Examples

```bash
/theme list
/theme mygo
```

---

## `/stat` Command Guide

**Check a user’s battle performance stats. Supports summary view and filtering by game mode.**

### 🧩 Command Format

```bash
/stat player:[user param] mode:[mode param]
```

### 🔧 Parameter Description

| Name     | Required | Description                                                                                                                                                    |
| -------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `player` | Optional | Specifies the account to query. Supports the following:<br>1. `Server IGN` (space-separated)<br>2. UID<br>3. @user with bound account<br>4. Alias via `/alias` |
| `mode`   | Optional | View stats for a specific game mode. If omitted, general stats will be shown. See list below for supported modes.                                              |

#### Supported Mode Parameters

| Mode Param     | Description                           |
| -------------- | ------------------------------------- |
| `random`       | Random battles                        |
| `ranked`       | Ranked battles                        |
| `solo`         | Solo queue (random)                   |
| `div2`         | 2-player division (random)            |
| `div3`         | 3-player division (random)            |
| `AirCarrier`   | Aircraft carrier (random)             |
| `Battleship`   | Battleship (random)                   |
| `Cruiser`      | Cruiser (random)                      |
| `Destroyer`    | Destroyer (random)                    |
| `Submarine`    | Submarine (random)                    |
| `SurfaceShips` | Surface ships only (no carriers/subs) |

### 📌 Examples

```bash
# Example 1: View your own general stats
/stat

# Example 2: View your PVP stats
/stat pvp

# Example 3: View another user’s stats by IGN
/stat asia SangonomiyaKokomi_

# Example 4: Query by UID
/stat 2023123456

# Example 5: Query via @mention
/stat @Someone

# Example 6: Query via alias (e.g., "myfriend")
/stat myfriend

# Example 7: View someone's Ranked stats
/stat asia SangonomiyaKokomi_ rank
```

### 💡 Notes

- Parameter order matters: **user comes first, then mode**
- You can only provide one `user` and one `mode` parameter

---
