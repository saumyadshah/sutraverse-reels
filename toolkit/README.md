# SutraVerse toolkit

The SutraVerse production toolkit is an overlay for [OpenMontage](https://github.com/calesthio/OpenMontage). It contains:
- the skill, scripts and brand kit;
- the patched TTS tools;
- the vendored Ootto content skills (MIT).

To set up a fresh Linux workspace, run from this repo's root:

    bash toolkit/bootstrap.sh "$PWD/toolkit/sutraverse-skill.zip" "$HOME/OpenMontage"

The script clones OpenMontage, unpacks the overlay, and installs the Python/Node dependencies, free local Hindi voices, the Whisper verifier and a headless Chromium. If `GEMINI_API_KEY` is set in the environment, the script writes it to OpenMontage/.env. The key is never stored in this repo.
