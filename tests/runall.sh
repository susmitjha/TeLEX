python test_scale.py -i 2 -o "gradient" > scale_gradient_10.log
echo "Gradient run done and output is in scale_gradient_10.log"
python test_scale.py -i 2 -o "nogradient" > scale_nogradient_10.log
echo "No gradient (DE) run done and output is in scale_nogradient_10.log"

