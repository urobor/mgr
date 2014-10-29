#!/bin/bash
DIGITS_DIR='/home/kuba/Magisterka/local/img/objects'
DIGIT='front'
LINES=$(wc -l < $DIGITS_DIR'/'$DIGIT'_p.txt')
LINES=$((LINES-10))
echo -data $DIGITS_DIR/detector_tmp -vec $DIGITS_DIR/$DIGIT.vec -bg $DIGITS_DIR/$DIGIT'_n.txt' -w 10 -h 15 -numPos $LINES -numNeg 50
opencv_traincascade -featureType LBP -minHitRate 0.995 -data $DIGITS_DIR/detector_tmp -vec $DIGITS_DIR/$DIGIT.vec -bg $DIGITS_DIR/$DIGIT'_n.txt' -w 100 -h 100 -numPos $LINES -numNeg 500