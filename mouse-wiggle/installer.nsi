; Windows installer script

OutFile "mouse-wiggle-installer.exe"
InstallDir "$PROGRAMFILES\MouseWiggle"

Section
   SetOutPath "$INSTDIR"
   File "mouse-wiggle.exe"
SectionEnd