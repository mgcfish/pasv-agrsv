#!/usr/bin/env python
'''
@author: Matthew C. Jones, CPA, CISA, OSCP
IS Audits & Consulting, LLC
TJS Deemer Dana LLP

Core functions

See README.md for licensing information and credits

'''
import sys
import os
import shutil
import subprocess
import tools
import dns.resolver, dns.reversename

# exit routine
def exit_program():
    print "\n\nQuitting...\n"
    sys.exit()
    
# cleanup old or stale files
def cleanup_routine(output_dir):
    '''Returns 'False' if the output directory is dirty and users select not to clean'''
    
    try:
        if not os.listdir(output_dir) == []:
            response = raw_input("\nOutput directory is not empty - delete existing contents? (enter no if you want to append data to existing output files)? [no] ")
            if "y" in response or "Y" in response:
                print("Deleting old output files...\n")
                shutil.rmtree(output_dir, True)
            else:             
                return False
    except:
        pass

def check_config(config_file):
    if os.path.exists(config_file):
        pass
    else:
        print "Specified config file not found. Copying example config file..."
        shutil.copyfile("config/default.example", config_file)

def execute(command, suppress_stdout=False):
    '''
    Execute a shell command and return output as a string
    
    By default, shell command output is also displayed in standard out, which can be suppressed
    with the boolean suppress_stdout
    '''
    
    output = ""
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
        # Poll process for new output until finished
        while True:
            nextline = process.stdout.readline()
            output += nextline
            if nextline == '' and process.poll() != None:
                break
            if not suppress_stdout:
                sys.stdout.write(nextline)
            sys.stdout.flush()
        
        return output
    except KeyboardInterrupt:
        print "\n[!] Keyboard Interrupt - command '%s' killed..." % command
        print "[!] Continuing script execution..."
        return ""

    except Exception as exception:
        print "\n[!] Error running command '%s'" % command
        print "[!] Exception: %s" % exception
        return ""

def write_outfile(path, filename, output_text):
    if output_text:
        if not os.path.exists(path):
            os.makedirs(path)
            
        outfile = os.path.join(path, filename)
        
        file = open(outfile, 'a+')
        file.write(output_text)
        file.close

def list_to_text(itemlist):
    ''' iterate through list and return a string of the list items separated by newlines'''
    
    output_text = ""
    for item in itemlist:
        output_text += item + "\n"
    return output_text

def nslookup_fwd(address):
    result=[]
    try:
        for rdata in dns.resolver.query(address):
            result.append(str(rdata))
        print "Forward lookup results for " + address
        print result
        
    except dns.resolver.NXDOMAIN:
        print "Error resolving DNS - No such domain %s" % address
    except dns.resolver.Timeout:
        print "Error resolving DNS - Timed out while resolving %s" % address
    except dns.exception.DNSException:
        print "Error resolving DNS - Unhandled exception"
    
    return result

def nslookup_rev(ip):
    result=[]
    
    try:
        addr = dns.reversename.from_address(ip)
        for rdata in dns.resolver.query(addr, "PTR"):
            result.append(str(rdata)[:-1])
        
        print "Reverse lookup results for " + ip
        print result
        
    except dns.resolver.NXDOMAIN:
        print "Error resolving DNS - reverse DNS record found for %s" % ip
    except dns.resolver.Timeout:
        print "Error resolving DNS - Timed out while resolving %s" % ip
    except dns.exception.DNSException:
        print "Error resolving DNS - Unhandled exception"
    return result

def sanitise(string):
    '''this function makes a string safe for use in sql query (not necessarily to prevent SQLi)'''
    s = string.replace('\'', '\'\'')
    return s

if __name__ == '__main__':
    #self test code goes here!!!
    pass