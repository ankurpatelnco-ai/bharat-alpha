import os
import subprocess
from pathlib import Path

desktop = Path(os.environ["USERPROFILE"]) / "Desktop"
bat_path = Path(__file__).resolve().parent / "start_live.bat"
work_dir = Path(__file__).resolve().parent
shortcut_path = desktop / "BHARAT ALPHA (GO LIVE).lnk"

vbs_content = f'''
Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{str(shortcut_path)}"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "{str(bat_path)}"
oLink.WorkingDirectory = "{str(work_dir)}"
oLink.Description = "Launch Bharat Alpha Worldwide Public Live Link"
oLink.Save
'''

vbs_file = Path(__file__).resolve().parent / "temp_create_shortcut.vbs"
vbs_file.write_text(vbs_content, encoding="utf-8")
subprocess.run(["cscript", "//nologo", str(vbs_file)], check=True)
if vbs_file.exists():
    vbs_file.unlink()
print("Shortcut created at:", shortcut_path)

