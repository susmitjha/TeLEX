rm scale_gradient_10.log
python test_scale.py -i 10 -o "gradient" 
echo "Gradient run done and output is in scale_gradient_10.log"
rm scale_nogradient_10.log
python test_scale.py -i 10 -o "nogradient"
echo "No gradient (DE) run done and output is in scale_nogradient_10.log"

