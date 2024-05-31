# Extra simple WinRar Installer
> [!NOTE]  
> rarreg.key was obtained from open sources in the Internet

> [!IMPORTANT]  
> App is requires an Internet connection!  
> Also in current state u need manualy config explorer integration (for some reason) and if you know how to launch WinRar post-setup (first launch) screen create an issue with it or integrate in code with pull request, thx!

## Usage
Just download an executable from Releases and launch it!

## Building
1. Create `.venv` and enter it with  
    ```
    python -m venv .venv
    ./.venv/Scripts/Activate.ps1
    ```
2. Install requirements from `req` with `pip install -r req`
3. Launch `build.py` with `python build.py`.  
Also you can build app with console enabled (debug mode) with `python build.py -v`
4. Built `.exe` will appear in `build` folder