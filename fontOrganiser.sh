#!/bin/sh
cd ./fonts-master

for a in ./*/ ; do( 
    for d in "$a"/*/ ; do (cd "$d" && find ./ -name "*.ttf" -print0 | cpio -pdmv0 ~/Desktop/Final-Year-Project-2017/fonts); done ); done
