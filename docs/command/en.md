# Command List

> DocsTemple

## `/` Command Guide

**.**

> 🔐 Only available to users with admin privileges.

### 🧩 Command Format

```bash
/
```

### 🔧 Parameter Description

No parameters

### 📌 Examples

```bash
/
```

### 💡 Notes

- ***

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
