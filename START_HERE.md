# 👋 Start Here: Set Up and Run Your First Notebook

> **Who is this for?** Complete beginners: you have never set up Python, never opened a Jupyter notebook, or don't know where to begin in this repo.
> **Time needed:** 20–60 minutes, mostly waiting for downloads.
> **After this page:** follow [`LEARNING_PATH.md`](LEARNING_PATH.md), the study order for the whole repo. Look up unknown words in [`GLOSSARY.md`](GLOSSARY.md).

---

## 1. What you need

| | Minimum | Comfortable |
|---|---|---|
| Computer | Any Windows, macOS or Linux laptop from the last ~6 years | — |
| Memory (RAM) | 8 GB | 16 GB |
| Free disk space | 5 GB | 15 GB (some advanced modules download models) |
| GPU | **Not needed**: every 🌱 Start Here and 🏭 industry notebook runs on a normal CPU | A GPU only helps in a few advanced deep-learning / fine-tuning notebooks |
| Money / API keys | **Not needed** to learn | Some advanced LLM notebooks *can* use paid APIs (OpenAI, Anthropic, Google), but always have a free path |

You have two ways to work. Pick one:

- **Option A: Google Colab** (nothing to install, runs in your browser): best if you just want to start right now, or your computer is old.
- **Option B: your own computer** (recommended for the long run): everything runs locally and you learn the tools real engineers use.

---

## 2. Option A: Google Colab (no installation)

1. Sign in to a Google account and go to <https://colab.research.google.com>.
2. Choose **File → Open notebook → GitHub**, paste `Ibtasam-Ahmad/zero-to-ai-engineer`, and pick a notebook.
   Or open a notebook directly with a link of this form:
   `https://colab.research.google.com/github/Ibtasam-Ahmad/zero-to-ai-engineer/blob/main/00_AI_Fundamentals/00_start_here_what_is_ai.ipynb`
3. Colab already has NumPy, pandas, scikit-learn, PyTorch, Transformers and most core libraries. If a cell says `ModuleNotFoundError: No module named 'xyz'`, add a cell with `%pip install xyz` at the top and run it.
4. **Save your work:** use **File → Save a copy in Drive**. Colab sessions reset after some idle time and files you created are lost.

> 💡 Notebooks that use a small local language model download it once (about 1 GB) the first time. On Colab this takes a minute or two.

---

## 3. Option B: your own computer

### Step 1: Install Python and Git

| | Windows | macOS | Linux (Ubuntu/Debian) |
|---|---|---|---|
| Python **3.12** (3.10 and 3.11 also work for beginners) | Download from <https://www.python.org/downloads/>. **Tick "Add python.exe to PATH"** during installation. | Download from <https://www.python.org/downloads/>, or `brew install python@3.12` | `sudo apt install python3 python3-venv python3-pip` |
| Git | <https://git-scm.com/download/win> | `xcode-select --install` | `sudo apt install git` |

Check that it worked. Open a **terminal** (Windows: *PowerShell*; macOS: *Terminal*; Linux: *Terminal*) and type:

```bash
python --version      # macOS/Linux may need: python3 --version
git --version
```

You should see something like `Python 3.12.x` and `git version 2.x`.

### Step 2: Download this repo

```bash
git clone https://github.com/Ibtasam-Ahmad/zero-to-ai-engineer.git
cd zero-to-ai-engineer
```

(No Git? On the GitHub page click **Code → Download ZIP**, unzip it, and open a terminal in that folder.)

### Step 3: Create a virtual environment

A **virtual environment** is a private folder of Python packages just for this course, so it never clashes with anything else on your computer.

```bash
# Windows (PowerShell)
py -3.12 -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

Your prompt now starts with `(.venv)`. **Every time** you come back to the course, open a terminal in the repo folder and run the `activate` line again.

> ⚠️ **Windows: "running scripts is disabled on this system"?** Run this once, then try again:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

### Step 4: Install the packages

```bash
python -m pip install --upgrade pip
pip install -r requirements-beginner.txt
```

This downloads about 600 MB (5–40 minutes, depending on your internet). It installs everything the 🌱 Start Here notebooks and most core notebooks need: Jupyter, NumPy, pandas, Matplotlib, scikit-learn, PyTorch (small CPU version), Transformers and FastAPI.

- **Later modules need a few extra packages.** The **Extra installs per module** table in [`LEARNING_PATH.md`](LEARNING_PATH.md#-extra-installs-per-module) tells you exactly what to `pip install` when you get there.
- **The complete environment:** the root `requirements.txt` pins *every* package used anywhere in the repo, about 280 of them. It needs **Python 3.12 or newer**. Use it only if you want everything at once: `pip install -r requirements.txt`.
- **Have an NVIDIA GPU?** First install PyTorch with the command for your system from <https://pytorch.org/get-started/locally/>, then run the `pip install -r ...` line above.

### Step 5: Start Jupyter

```bash
jupyter lab
```

Your browser opens JupyterLab. In the file browser on the left, open `00_AI_Fundamentals/00_start_here_what_is_ai.ipynb`.

(Prefer VS Code? Install the **Python** and **Jupyter** extensions, open the repo folder, open a notebook, and choose the `.venv` interpreter as the kernel in the top-right corner.)

---

## 4. How to use a notebook (2-minute version)

- A notebook is a list of **cells**. *Markdown* cells are text; *code* cells contain Python.
- Click a code cell and press **Shift + Enter** to run it and move to the next one.
- Run cells **from top to bottom**. Later cells use variables created by earlier ones.
- `[*]` next to a cell means "still running". `[5]` means "this was the 5th cell run".
- Something weird? **Kernel → Restart Kernel and Run All Cells** starts fresh. This fixes most "but it worked a minute ago" problems.
- **Experiment!** Change a number and re-run the cell. You can't break the repo: worst case, re-download the notebook.

The notebook `01_Python/00_start_here_jupyter_terminal_and_debugging.ipynb` explains all of this hands-on, including how to read error messages.

---

## 5. Your first week

| Day | Do this |
|---|---|
| 1 | This page, then `00_AI_Fundamentals/00_start_here_what_is_ai.ipynb` |
| 2 | `01_Python/00_start_here_jupyter_terminal_and_debugging.ipynb` |
| 3–5 | `01_Python/01_basic.ipynb` (take your time; Python is the foundation) |
| 6 | `20_Git_and_DevOps/01_git_basics.ipynb`: start saving your own work in Git |
| 7 | Re-read anything unclear; write down 5 things you learned |

Then continue with [`LEARNING_PATH.md`](LEARNING_PATH.md).

---

## 6. Troubleshooting

| Problem | Fix |
|---|---|
| `python: command not found` / `'python' is not recognized` | macOS/Linux: use `python3`. Windows: reinstall Python with **"Add python.exe to PATH"** ticked, or use `py`. |
| `ModuleNotFoundError: No module named 'xyz'` | Your virtual environment is not active (activate it, Step 3), **or** the package is an extra: `pip install xyz`. Some names differ: `cv2` → `opencv-python-headless`, `sklearn` → `scikit-learn`, `faiss` → `faiss-cpu`. |
| The notebook uses the wrong Python / packages are "missing" in Jupyter but installed in the terminal | Start Jupyter **from the activated environment** (`jupyter lab` after `activate`). In VS Code, pick the `.venv` kernel. |
| `pip install` fails on one package | Upgrade pip first (`python -m pip install --upgrade pip`). Check that you use Python 3.10–3.12 for `requirements-beginner.txt`, or 3.12+ for `requirements.txt`. Copy the **last lines** of the error into a search engine. |
| Download of a model is very slow or fails | Check your internet connection and re-run the cell; downloads resume. Models are stored in `~/.cache/huggingface` and downloaded only once. |
| A cell runs forever | Press the ■ (stop) button, or **Kernel → Interrupt**. Training cells can take a few minutes on a CPU; the notebook says so when that's expected. |
| A cell prints "needs an API key" or "skipped" | That's expected: that part uses a paid service. Read the code and output, and use the free 🌱 / 🏭 notebooks for hands-on practice. Never paste a key into a notebook; use environment variables (shown in the notebooks). |
| "Out of memory" / computer freezes | Close other programs, restart the kernel, and run one notebook at a time. Use Google Colab for the heaviest notebooks. |

**Still stuck?** Search the exact last line of the error message, or open an issue on the GitHub repo with: what you ran, the full error, your operating system, and your Python version (`python --version`).
