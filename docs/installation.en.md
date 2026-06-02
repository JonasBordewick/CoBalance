# Installation & Setup

**Goal:** Get the CoBalance toolchain running on your machine before the first real exercise. By the end of this step you will have the example Unity project open, the Balancing Tool launched, and you'll have confirmed that the two can exchange files.

---

## Step 1 – Prepare the Unity Project

- Create a new project: **New Project → 2D (Built-in Render Pipeline)**, Unity 6.
- Download [TODO: package name]() from the release page or Digicampus.
- In Unity: **Assets → Import Package → Custom Package...**, select the downloaded `.unitypackage`.
- In the import dialog, leave everything selected and click **Import**.

---

## Step 2 – Install the CoBalance Plugin

The plugin is installed through the Unity Package Manager via a Git URL — no manual file copying required.

1. Open **Window → Package Manager**
2. Click the **+** button in the top-left corner
3. Choose **Add package from git URL...**
4. Enter this URL and confirm:

```text
https://github.com/JonasBordewick/CoBalance.git?path=unity
```

> ✅ **Verify:** A new **CoBalance** entry appears in the Unity menu bar.

---

## Step 3 – Set Up the CoBalance Tool

The tool ships as a standalone application — no Python installation needed.

> ⚠️ The app is **not code-signed**, so your OS will warn you the first time you open it. This is expected. Follow the steps for your system:

### Windows

1. Download [Windows](https://github.com/USER/REPO/releases/latest/download/CoBalance.exe)
2. Double-click the `.exe`. If you see "_Windows protected your PC_", click **More Info → Run anyway**.

### macOS

1. Download [macOS](https://github.com/USER/REPO/releases/latest/download/CoBalance.dmg) 
2. Double-clicking will likely say the developer cannot be verified. Instead:
    1. **Right-click** the app → **Open** → click **Open** again in the dialog.
    2. Alternatively: **System Settings → Privacy & Security**, scroll down to the blocked-app message → **Open Anyway**.

### Linux

1. Download [Linux (AppImage)](https://github.com/USER/REPO/releases/latest/download/CoBalance-x86_64.AppImage)
2. Make it executable (file manager → Properties → Permissions → "Allow executing", or in a terminal):

```sh
chmod +x CoBalance-x86_64.AppImage
```

3. Run it.

---

## Step 4 – Confirm Everything Works

This is the real checkpoint: Unity sees the plugin **and** the tool can open the project file.

1. **In Unity:** confirm that a **CoBalance** entry is present in the menu bar.
2. Locate the file **`project.cb`** in your project folder under **`CoBalance/`** (it was created automatically when the plugin was installed).
3. **In the Balancing Tool:** open that file via **Project → Open** (`Ctrl+O`).

> ✅ **Setup complete:** The `project.cb` file opens in the Balancing Tool and shows the Parameters view. If you got here, your toolchain is ready — continue with [Getting Started](getting-started.md).
