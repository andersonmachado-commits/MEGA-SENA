# Mega-Sena Fechamento — Android

Versão Android baseada no programa Python/Tkinter enviado, convertida para Kivy.

## Gerar o APK

O projeto usa Buildozer/python-for-android. Em Linux/WSL:

```bash
pip install buildozer cython
buildozer -v android debug
```

O APK será criado em `bin/`.

## GitHub Actions

O workflow em `.github/workflows/build-apk.yml` gera automaticamente o APK em um runner Ubuntu. Depois do build, o APK fica disponível como artefato da execução.
