#Überprüfen ob die Imports funktioniert haben.
python3 ImportPi.py
if [ $? -ne "0" ]
then
	echo "Failed";
	exit;
fi

#Anlegen der .service Dateien
sudo cp PSE_Main.service /etc/systemd/system/
sudo cp PSE_Website.service /etc/systemd/system/

#Verknüpfung auf den Einstiegspunkt der beiden Programme setzten.
cd ..
cd src
main=$(pwd)
cd website
website=$(pwd)
cd /usr/local/bin
sudo ln -s $main/main.py
sudo ln -s $website/website_pi.py

#Anlegen der Aliases zur leichteren Handhabung.
echo 'alias restart="sudo systemctl restart PSE_Main.service PSE_Website.service"' >> ~/.bash_aliases
echo 'alias status="sudo systemctl status PSE_Main.service PSE_Website.service"' >> ~/.bash_aliases
echo 'alias stop="sudo systemctl stop PSE_Main.service PSE_Website.service"' >> ~/.bash_aliases

sudo systemctl daemon-reload
