[app]
title = moOde Audio Mobile
package.name = moodemobile
package.domain = org.moodeaudio
source.dir = .
source.include_exts = py,png,jpg,json
version = 1.0

# Vain yksi puhdas requirements-rivi
requirements = python3, kivy, android, pyjnius

orientation = portrait
fullscreen = 1

# Vain yksi puhdas permissions-rivi
android.permissions = INTERNET

android.api = 33
android.minapi = 24
android.ndk_api = 24
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
