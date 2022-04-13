#Überprüfen ob die Imports funktioniert haben.
python3 ImportWebsite.py
if [ $? -ne "0" ]
then
	echo "Failed";
	exit;
fi

#Anlegen der .service Dateien
sudo cp PSE_Website_Server.service /etc/systemd/system/

#Verknüpfung auf den Einstiegspunkt der beiden Programme setzten.
cd ..
cd src
cd website
website=$(pwd)
cd /usr/local/bin
sudo ln -s $website/website_controller.py

#Anlegen der Aliases zur leichteren Handhabung.
echo 'alias restart="sudo systemctl restart PSE_Website_Server.service"' >> ~/.bash_aliases
echo 'alias status="sudo systemctl status PSE_Website_Server.service"' >> ~/.bash_aliases
echo 'alias stop="sudo systemctl stop PSE_Website_Server.service"' >> ~/.bash_aliases

sudo systemctl daemon-reload
