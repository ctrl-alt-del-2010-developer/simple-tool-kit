#!/bin/bash                                         

RED='\e[31m'
GREEN='\e[32m'
YELLOW='\e[33m'
RESET='\e[0m'

while true; do
    clear
    cat ascii.txt  
    echo -e "${RED}[${YELLOW}01${RED}]${RESET} Red Hawk      ${RED}[${YELLOW}07${RED}]${RESET} Ping Test"
    echo -e "${RED}[${YELLOW}02${RED}]${RESET} Tor IP        ${RED}[${YELLOW}08${RED}]${RESET} Tor Browser"
    echo -e "${RED}[${YELLOW}03${RED}]${RESET} Network Scan"
    echo -e "${RED}[${YELLOW}04${RED}]${RESET} DDoS Tool"
    echo -e "${RED}[${YELLOW}05${RED}]${RESET} Cmatrix"
    echo -e "${RED}[${YELLOW}06${RED}]${RESET} İwctl Shell"
    echo ""
    echo -e "${YELLOW}Tip:${RESET} Please Do Not Run Simple Tool Kit As Sudo Permissions."
    echo ""
    read -p "> " secim

    case "$secim" in
        1)
            clear
            python3 ~/simple-tool-kit/STK/Programs/red_hawk.py
            clear
            read -p "Press Enter Button For Continue..."
            ;;
        2)
            clear
            sudo systemctl start tor
            xterm -e python3 ~/simple-tool-kit/STK/Programs/ip_changer.py
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
            python3 ~/simple-tool-kit/STK/Programs/DDoS-tool.py
            clear
            read -p "Press Enter Button For Continue..."
            ;;
        5)  
            clear
            xterm -e cmatrix
            clear
            read -p "Press Enter Button For Continue..."
            ;;
        6)  
            clear
            sudo systemctl start iwd 
            xterm -e iwctl
            read -p "Press Enter Button For Continue..."
            ;;
        7)  
            xterm -e ping 1.1.1.1 
            read -p "Press Enter Button For Continue..."
            ;;
        8)  
            torbrowser-launcher
            read -p "Press Enter Button For Continue..."
            ;;
        *)
            clear
            echo "Invalid Selection!"
            read -p "Devam etmek için Enter tuşuna basın..."
            ;;
    esac
done
