#!/bin/bash                                         

RED='\e[31m'
GREEN='\e[32m'
YELLOW='\e[33m'
RESET='\e[0m'

while true; do
    clear
    cat ascii.txt  
    echo -e "${RED}[${YELLOW}01${RED}]${RESET} Red Hawk"
    echo -e "${RED}[${YELLOW}02${RED}]${RESET} Tor IP"
    echo -e "${RED}[${YELLOW}03${RED}]${RESET} Scan Networks"
    echo -e "${RED}[${YELLOW}04${RED}]${RESET} DDoS Tool"
    echo -e "${RED}[${YELLOW}05${RED}]${RESET} Cmatrix"
    echo ""
    echo -e "${YELLOW}Tip:${RESET} Please Do Not Run This Program As Sudo."
    echo ""
    read -p "> " secim

    case "$secim" in
        1)
            clear
            python3 ~/STK/Programs/red_hawk.py
            clear
            read -p "Press Enter Button For Continue..."
            ;;
        2)
            clear
            sudo systemctl start tor
            xterm -e python3 ~/STK/Programs/ip_changer.py
            clear
            read -p "Press Enter Button For Continue..."
            ;;
        3)  
            clear
            xterm -e sudo airodump-ng wlan0
            read -p "Press Enter Button For Continue..."
            ;;
        4)  
            clear
            python3 ~/STK/Programs/DDoS-tool.py
            clear
            read -p "Press Enter Button For Continue..."
            ;;
        5)  
            clear
            xterm -e cmatrix
            clear
            read -p "Press Enter Button For Continue..."
            ;;
        *)
            clear
            echo "Invalid Selection!"
            read -p "Devam etmek için Enter tuşuna basın..."
            ;;
    esac
done
