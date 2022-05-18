#!/bin/bash
pico2wave -l fr-FR -w /tmp/text.wav "$1"
aplay -q /tmp/text.wav
rm /tmp/text.wav