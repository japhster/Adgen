rm $2
echo "formulating plan from \"$1\" and saving to file \"$2\""
echo "Initial state of plan:"
echo ""
python3 generate_world.py $1 $2
echo ""
echo "Testing file \"$2\" using strips:"
echo ""
python strips/strips.py $2
echo ""
