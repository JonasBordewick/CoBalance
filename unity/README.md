# CoBalance for Unity

Unity UPM package providing the runtime and editor components of the CoBalance game-balancing toolchain.

The package exposes balance parameters to the CoBalance desktop application, bootstraps headless simulations in Unity batch mode, and reports fitness scores back — enabling the desktop app's genetic algorithm to find optimised parameter configurations automatically.

📖 **Full documentation:** [cobalance.bordewick.dev](https://cobalance.bordewick.dev)

---

## Requirements

- Unity **6000.0** or newer

---

## Installation

Install via the **Unity Package Manager** using a Git URL:

1. Open **Window → Package Manager**
2. Click **+** → **Add package from git URL...**
3. Enter:

```text
https://github.com/JonasBordewick/CoBalance.git?path=unity
```

After installation a **CoBalance** menu entry will appear in the Unity menu bar.

---

## Package contents

| Folder          | Contents                                                    |
| --------------- | ----------------------------------------------------------- |
| `Runtime/`      | Balance parameter components, simulation bootstrap, logging |
| `Editor/`       | Inspector windows, menu builder, GA finalizer               |
| `Documentation/`| Package-level API docs                                      |

---

## License

MIT — see [LICENSE.md](LICENSE.md)
