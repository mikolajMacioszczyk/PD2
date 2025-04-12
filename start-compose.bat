@echo off
echo Uruchamiam FHIR...
docker compose -f fhir-docker-compose.yml up -d

echo Uruchamiam OpenEHR...
docker compose -f openehr-docker-compose.yml up -d

echo Wszystko uruchomione!
pause