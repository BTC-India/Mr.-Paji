echo "Creating env"
python3 -m venv myenv   


echo "Activating env"
source myenv/bin/activate

echo "Installing requirements"
pip3 install -r requirements.txt

echo "Done"