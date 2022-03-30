An editor for Mario Kard Double Dash's race tracks.

### changes in this fork
load a file-name as argument, and add another argument "bmd" to always load a bmd when you load a bol file (else it'll load a bco by default)

currently, loading a bmd at startup throws an error, if you want to try to load it anyways or fix the error,
change line 1805 of mkdd_editor.py to
```            mkdd_gui.load_bol(bol, False, load_model_type, False)```
