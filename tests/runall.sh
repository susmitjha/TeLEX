python test_scale.py -i 6 -o "gradient" > scale_gradient_6.log
echo "Gradient run done and output is in scale_gradient_6.log"
python test_scale.py -i 6 -o "nogradient" > scale_nogradient_6.log
echo "No gradient (DE) run done and output is in scale_nogradient_6.log"

