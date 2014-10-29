#!/bin/bash
DIGITS_DIR='/home/kuba/Magisterka/local/img/objects'
DIGIT='front'
LINES=$(wc -l < $DIGITS_DIR'/'$DIGIT'_p.txt')

opencv_createsamples -vec $DIGITS_DIR/$DIGIT.vec -info $DIGITS_DIR/$DIGIT'_p.txt' -w 100 -h 100 -num $LINES
