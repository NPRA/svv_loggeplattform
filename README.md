# Oppsett av loggeplattform

## Oppsett av Colombus V-800 GPS
Columbus GPS V-800 er benyttet, denne fungerer ut av boksen mot Raspberry Pi 3.  Den dukker opp på /dev/ttyACM0 eller /dev/ttyUSB0. For å sørge for at den alltid gjennkjennes og får en unik "fil" i /dev brukes en udev regel. Dette gjøres ved å legge til noen linjer i følgende fil: /etc/udev/rules.d/10-local.rules

SUBSYSTEM=="tty", ATTRS{idVendor}=="0e8d", ATTRS{idProduct}=="3329", SYMLINK+="ttyGPS"

Infoen som tregns på idVendor og idProduct finnes ved hjelp av: sudo lsusb -v | more

Columbus GPSen kan også sette opp til å logge på 5Hz, men for å få dette til må det sendes en tekst streng til GPSen. Dette kan gjøres via et enkelt python skript: configure_gps.py Det er ikke mulig å kjøre dette skriptet når gpsd kjører. Enten må skriptet kjøres før gpsd starte eller så må gpsd stoppes og startes etter at scriptet er kjørt.

### Vedlagte filer
* logg.py: dette er filen som logger data fra akselerometer og skriver til disk. I tillegg skrives verdier ut til et NOKIA display.
* configure_gps.py: dette er et script som setter GPSen i 5Hz modus.
* \_etc_default_gpsd: er fila som setter opp GPSD på riktig måte.
