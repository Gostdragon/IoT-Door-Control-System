cd ..
mkdir Certifications
cd Certifications
openssl genrsa -des3 -out myCA.key 2048
openssl req -x509 -new -nodes -key myCA.key -sha256 -days 1825 -out myCA.pem -reqexts v3_req -extensions v3_ca

openssl genrsa -out app.cert.key 2048
openssl req -new -key app.cert.key -out app.cert.csr
cat <<EOT >> app.cert.ext
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = 192.168.25.43
EOT
openssl x509 -req -in app.cert.csr -CA myCA.pem -CAkey myCA.key -CAcreateserial -out app.cert.crt -days 825 -sha256 -extfile app.cert.ext
