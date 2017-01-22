rm scale_gradient_6.log
python test_scale.py -i 6 -o "gradient" 
echo "Gradient run done and output is in scale_gradient_6.log"
rm scale_nogradient_6.log
python test_scale.py -i 6 -o "nogradient"
echo "No gradient (DE) run done and output is in scale_nogradient_6.log"

