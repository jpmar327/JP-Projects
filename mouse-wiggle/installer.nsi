; Windows NSIS installer script that creates Mouse-Wiggler-Setup.exe

OutFile "Mouse-Wiggler-Setup.exe"

Section "Install"
  SetOutPath "$INSTDIR"
  File "my_application.exe"
  File "my_library.dll"
SectionEnd