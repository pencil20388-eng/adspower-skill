# 🌐 AdsPower Skill for Claude Code

A [Claude Code skill](https://code.claude.com/docs/en/skills) that lets Claude manage [AdsPower](https://www.adspower.net/) antidetect browser profiles through natural language.

> "Create 50 browser profiles with random fingerprints" → Done.
> "Bind these proxies to all profiles in my campaign group" → Done.
> "Open each profile, visit Google, take a screenshot, close" → Done.

Compatible with **Claude Code**, **Codex CLI**, **Cursor**, **Gemini CLI**, and other agents that support the SKILL.md standard.

## What It Does

| You say | Claude does |
|---|---|
| "Create 20 profiles" | Calls AdsPower API to batch create profiles with randomized fingerprints |
| "Bind proxies from this CSV" | Reads your proxy list, updates each profile via API |
| "Open profile X and check the fingerprint" | Opens browser, connects Selenium/Playwright, visits BrowserScan |
| "Export cookies from my campaign group" | Queries all profiles in the group, exports cookie data |
| "What profiles do I have?" | Lists all profiles with IDs, names, groups, and proxy status |

## Installation

### Claude Code

```bash
# From your project directory
mkdir -p .claude/skills
cp -r adspower .claude/skills/
```

Or clone this repo directly:

```bash
cd your-project
mkdir -p .claude/skills
git clone https://github.com/pencil20388-eng/adspower-skill.git .claude/skills/adspower
```

### Other Agents

Copy the `adspower/` folder into wherever your agent reads skills from.

## Prerequisites

- [AdsPower](https://www.adspower.net/download) installed and running (paid plan with API access)
- API Key generated (AdsPower → Automation → API → Generate)
- Python 3.8+ with `requests` package

## Usage

Once installed, just talk to Claude naturally:

```
> Create 30 browser profiles in a group called "US Campaign" with HTTP proxies from proxies.csv

> Open profile h1abc123, visit https://www.amazon.com, wait 10 seconds, take a screenshot, and close

> Show me all profiles that don't have a proxy configured

> Export cookies from all profiles in the "EU Accounts" group
```

Claude will use the AdsPower Local API to execute these operations automatically.

## Skill Structure

```
adspower/
└── SKILL.md          # Instructions, API reference, code patterns
```

Intentionally minimal — a single file, no dependencies beyond `requests`. Claude reads the SKILL.md and generates the appropriate Python code for each task.

## API Endpoints Covered

| Endpoint | What it does |
|---|---|
| `GET /api/v1/status` | Check if API is running |
| `GET /api/v1/browser/start` | Open a browser profile |
| `GET /api/v1/browser/stop` | Close a browser profile |
| `POST /api/v1/user/create` | Create a new profile |
| `POST /api/v1/user/update` | Update profile (proxy, fingerprint, etc.) |
| `GET /api/v1/user/list` | Query profiles |
| `POST /api/v1/group/create` | Create a profile group |

## More Resources

- 📦 [Awesome AdsPower Automation](https://github.com/pencil20388-eng/awesome-adspower-automation) — Ready-to-use scripts, templates, and guides
- 📖 [AdsPower API Docs](https://localapi-doc-en.adspower.com/)
- 🌐 [AdsPower Official](https://www.adspower.net/)

## License

[MIT](LICENSE)

---

**⭐ Star this repo if you found it useful!**
