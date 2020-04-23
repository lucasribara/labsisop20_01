import time
import BaseHTTPServer
import os
import subprocess, re
import platform
import psutil

HOST_NAME = '192.168.1.10' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8000


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
#---------------------------------------------------------------------------------------------------------------------

	def get_processor_name():
	    allInfo = (subprocess.check_output("cat /proc/cpuinfo", shell=True).strip()).decode()
	    for line in allInfo.split("\n"):
                if "model name" in line:
                    return re.sub( ".*model name.*:", "", line,1)
    	    return ""
#---------------------------------------------------------------------------------------------------------------------

	def get_processor_speed():
	    allInfo = (subprocess.check_output("cat /proc/cpuinfo", shell=True).strip()).decode()
	    for line in allInfo.split("\n"):
                if "cpu MHz" in line:
                    return re.sub( ".*cpu MHz.*:", "", line,1)
    	    return ""
#---------------------------------------------------------------------------------------------------------------------

	def get_running_process():
	    for proc in psutil.process_iter():
    		try:
        	# Get process name & pid from process object.
        	    processName = proc.name()
        	    processID = proc.pid
        	    temp = "( " + processName + " ::: " + str(processID) + " )"
		    s.wfile.write("<p>Process : %s <p>" %temp)
    		except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        	    pass	    
#---------------------------------------------------------------------------------------------------------------------

	def uptime():
	    return (subprocess.check_output("uptime", shell=True).strip()).decode()
#---------------------------------------------------------------------------------------------------------------------

        """Respond to a GET request."""
	percent = "%"
	datahora = os.popen('date').read()
	sys = platform.platform()
	cpupc = psutil.cpu_percent()
	memory = psutil.virtual_memory()
	#procInfo = get_processor_info()
	ut = uptime()
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write("<html><head><title>Pagina Trabalho 1 - LABSISOP.</title></head>")
        s.wfile.write("<body><p>---------- Apresentando dados ---------</p>")
	s.wfile.write("<p>--> Data e Hora: %s.</p>" %datahora)
	s.wfile.write("<p>--> Uptime: %s.</p>" %ut)
	s.wfile.write("<p>--> Modelo do processador: %s.</p>" %get_processor_name())
	s.wfile.write("<p>--> Velocidade do processador: %s MHz.</p>" %get_processor_speed())
	s.wfile.write("<p>--> Capacidade ocupada do processador: %s percent.</p>" %cpupc)
	s.wfile.write("<p>--> Quantidade de memoria RAM total: %s mb.</p>" %memory[0])
	s.wfile.write("<p>--> Quantidade de memoria RAM usada: %s percent.</p>" %memory[2])
	s.wfile.write("<p>--> Versao do sistema: %s.</p>" %sys)
	s.wfile.write("<p style={font-weight=bold}>--> Processos executando: </p>")
	get_running_process()
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        s.wfile.write("<p>You accessed path: %s</p>" % s.path)
        s.wfile.write("</body></html>")	

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)

