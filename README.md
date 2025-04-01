# Spectral parametrization project
Blessing Oladunjoye
Supervisor: Balázs Knakker

Implementing a spectral parametrization-based analysis on an EEG dataset.

## UV
(Balázs 2025-04-01)
Note: Balázs added the uv package/environment manager to the repository.

It can be installled via (see also https://docs.astral.sh/uv/getting-started/installation/):
``
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
``



It gives you instructions on how to add uv to your system PATH, don't forget that. For that to take effect you might need to restart your IDE.

then in a terminal in the project folder you just type

uv sync

and it installs everything that is necessary. It also sets up a venv with a python.exe, you need to specify that as your interpreter. (I don't know which IDE you are using)

If you want to install a package, you can e.g. (in terminal)

uv add mne

I already added this, so this is just an example. But it adds it to the lockfile (uv.lock), and if you commit your lockfile and I pull it to my local repo, I just have to uv sync to get the packages that you've installed.

It didn't take too much time to figure this out, so I hope this will work good for you as well