An editor for Mario Kard Double Dash's race tracks.

### changes in this fork
load a file-name as argument, and add another argument "bmd" to always load a bmd when you load a bol file (else it'll load a bco by default)

currently, loading a bmd at startup throws an error, if you want to try to load it anyways or fix the error,
change line 1743 of mkdd_editor.py to
```            mkdd_gui.load_bol(bol, False, load_model_type, False)```

added a executable launcher, this way, you can open bol files with it.
make sure that you've created a file named "mkdd_bol_editor.txt" that contains the full python executable path (without quotes) at the first line and the full path to the mkdd_editor.py at the second line.
if this text file doesn't exists, the launcher will try to smartly locate python.exe, but the mkdd_editor.py path is up to you

change the arguments in the registry and add "bmd" after it if you want to load bmds by default
