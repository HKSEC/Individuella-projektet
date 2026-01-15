#!/usr/bin/python3

import socket
import threading
import logging
import sys
import time
from queue import Queue

def setup_logging():

    logging.basicConfig(level= logging.INFO, filename = "port_scanner.log", filemode= "a",
                        format = "%(asctime)s -  %(levelname)s - %(message)s")

    logging.info("PORT SCANNER INITIALIZING ")

    return "port_scanner.log"

def e_control():
    print("\n [*] RUNNING ENVIRONMENT CHECKS ....")
    logging.info("RUNNING ENVIRONMENT")
    
#Python version check
    
    python_v = sys.version_info

    if python_v < (3, 6):
        error_msg = f"Python 3.6+ required. Your version: {sys.version}"
        logging.error(error_msg)
        print("[-] ERROR: ", error_msg)
        return False

    print("[+]  PYTHON VERSION COMPATIBLE: ", sys.version.split()[0])
    logging.info(f"PYTHON VERSION: {sys.version}")
    return True              

#Network access check
    try:
        socket.gethostbyname("LOCALHOST")
        print("[+] NETWORK ACCESS COMPLETE")
        logging.info("NETWORK ACCESS VERIFIED")
        return true
    except socket.error as e:
        error_msg = f"NO NETWORK ACCESS: {e}"
        logging.error(error_msg)
        print("[-] ERROR: NO NETWORK ACCESS")
        print("====CHECK YOUR NETWORK CONNECTION====")
        return False


def meny():  
    print("What do you want to scan:")
    print("1. Your own PC(local host)")
    print("2. Your router")
    print("3. Enter you own IP-address")
    print("4. Try a specific port")
    print("5. End the program")

    while True:
        try:
            choice = int(input("choose (1-5): "))
            if 1 <= choice <= 5:
                logging.info(f"User selected menu option {choice}")
                return choice
            else:
                print("Choose between 1 och 5")
        except ValueError:
            print("Enter a number")
    
def portscan(port):
        try:
            s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s1.settimeout(0.5)
            result = s1.connect_ex((ip, port))
            s1.close()

            if result == 0:
                logging.info(f"Port {port} is OPEN on {ip}")
            
        else:
            logging.debug(f"Port {port} is CLOSED on {ip}")
            
        return result == 0
    except socket.timeout:
        logging.debug(f"Port {port} timeout on {ip}")
        return False
    except ConnectionRefusedError:
        logging.debug(f"Port {port} connection refused on {ip}")
        return False
    except Exception as e:
        logging.error(f"Error scanning port {port} on {ip}: {e}")
        return False    


def scan_target(ip, start_port=1, end_port=1024):
    """Kör port scanning på en IP"""
    queue = Queue()
    open_ports = []    



def worker():
        while not queue.empty():
            port = queue.get()
            if portscan(port):
                print(f"  Port {port}")
                open_ports.append(port)
            queue.task_done()
 # Logga scanning start
    logging.info(f"Starting scan of {ip} (ports {start_port}-{end_port})")
    print(f"\n[*] Scanning {ip} (ports {start_port}-{end_port})...")
    print("[*] This may take a moment...\n")



    # Fyll kön
    for port in range(start_port, end_port + 1):
        queue.put(port)
    
    # Starta trådar
    threads = []
    for i in range(min(100, (end_port - start_port + 1))):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()
        threads.append(t)
    
    # Vänta
    queue.join()
    logging.info(f"Scan complete. Found {len(open_ports)} open ports")
    return open_ports



def banner_grab(ip, port, timeout=2):
    """Försöker hämta banner från en tjänst"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((ip, port))
        
        # Skicka något för att få svar
        if port == 80 or port == 443:
            sock.send(b"GET / HTTP/1.0\r\n\r\n")
        elif port == 21:
            sock.send(b"\r\n")
        elif port == 22:
            sock.send(b"SSH-2.0-Client\r\n")
        else:
            sock.send(b"\r\n")
        
        # Ta emot banner
        banner = sock.recv(1024).decode('utf-8', errors='ignore')
        sock.close()
        
        if banner:
            logging.info(f"Banner from {ip}:{port}: {banner[:100]}...")
        
        return banner.strip()[:200]
        
    except Exception as e:
        logging.warning(f"Could not grab banner from {ip}:{port}: {e}")
        return f"No banner or error: {e}"








def main():

    # 1. Setup logging
    log_file = setup_logging()
    print(f"[*] Logging to: {log_file}")
    
    # 2. Check environment
    if not check_environment():
        print("\n[-] Cannot continue due to environment issues")
        logging.error("Exiting due to failed environment checks")
        return
    
    print("\n" + "="*60)
    print("        WELCOME TO PORT SCANNER")
    print("="*60)
    logging.info("Port Scanner started successfully")


    while True:
        choice = meny()  # <-- FUNKAR NU! (meny() istället för show_menu())
        
        if choice == 5:
            print("Ending...")
            print(f"[*] Log saved to: {log_file}")
            logging.info("Program ending normally")
            break
        
        if choice == 1:
            target = "127.0.0.1"
            logging.info(f"\nScanning localhost ({target})...")
            
        elif choice == 2:
            target = "192.168.1.1"  # Vanlig router IP
            print(f"\nScanning router ({target})...")
            print("Attention: Your router can have another IP!")
            logging.info(f"Scanning router ({target})")

        elif choice == 3:
            target = input("Enter IP-adress or domainname: ")
            print(f"\nScanning {target}...")
            logging.info(f"Scanning custom target: {target}")

        elif choice == 4:
            target = input("Enter IP-adress: ")
            if not target:
                target = "127.0.0.1"
            try:
                port = int(input("Enter port to test (1-65535): "))
                if port < 1 or port > 65535:
                    print("[-] Invalid port, using 80")
                    port = 80
            except ValueError:
                print("[-] Invalid port, using 80")
                port = 80

            logging.info(f"Testing single port {port} on {target}")
            print(f"\n[*] Testing {target}:{port}...")
           

            
            # Testa en port
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((target, port))
            sock.close()



            if result == 0:
                print(f"\n[+] Port {port} is OPEN on {target}")
                logging.info(f"Port {port} is OPEN on {target}")

                banner = banner_grab(target, port)
                if banner and "No banner" not in banner:
                    print(f"    Banner: {banner[:100]}...")


                try:
                    service = socket.getservbyport(port)
                    print(f"    Service: {service}")
                    logging.info(f"Service on port {port}: {service}")
                except:
                    print("    Service: Unknown")
                    logging.info(f"Service on port {port}: Unknown")
            else:
                print(f"\n[-] Port {port} is CLOSED on {target}")
                logging.info(f"Port {port} is CLOSED on {target}")
                
            input("\nPress Enter to CONTINUE...")  
            continue

        
      # Fråga om portintervall för scanning
        print("\n[*] Port range settings:")
        
        try:
            start = int(input("Start port (1-65535) [default 1]: ") or "1")
            if start < 1 or start > 65535:
                print("[!] Invalid, using 1")
                logging.warning(f"Invalid start port, using 1")
                start = 1
        except ValueError:
            print("[!] Invalid, using 1")
            logging.warning("Invalid start port input, using 1")
            start = 1
        
        try:
            end = int(input(f"End port ({start}-65535) [default 1024]: ") or "1024")
            if end < start or end > 65535:
                print(f"[!] Invalid, using {min(start + 1023, 65535)}")
                logging.warning(f"Invalid end port, using {min(start + 1023, 65535)}")
                end = min(start + 1023, 65535)
        except ValueError:
            print(f"[!] Invalid, using {min(start + 1023, 65535)}")
            logging.warning("Invalid end port input, using default")
            end = min(start + 1023, 65535)




            
         # Kör scanning
         open_ports = scan_target(target)
        
        # Visa resultat
        print(f"\n{'='*50}")
        if open_ports:
            open_ports.sort()
            print(f"Found {len(open_ports)} open ports:")
            logging.info(f"Open ports found: {open_ports}")

            for port in open_ports:
                # Försök identifiera tjänst
                try:
                    service = socket.getservbyport(port)
                    print(f"  • Port {port:5} - {service}")
                    
                    # Försök hämta banner för viktiga portar
                    if port in [21, 22, 23, 25, 80, 443]:
                        banner = banner_grab(target, port)
                        if banner and "No banner" not in banner:
                            print(f"      Banner: {banner[:80]}...")
                except:
                    print(f"  • Port {port:5} - Unknown service")
        else:
            print("\n[-] No open ports found")
            logging.info("No open ports found")
        
        print('='*60)
        
        input("\n[*] Press Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[*] Program interrupted by user")
        logging.warning("Program interrupted by user")
    except Exception as e:
        print(f"\n[-] Unexpected error: {e}")
        logging.critical(f"Unexpected error: {e}")

            

