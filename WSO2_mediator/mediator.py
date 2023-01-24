import re


class   mediator:

	def __init__(self,name,value,urls):
		self.name = name;
		self.value = value;
		self.urls = urls;
		self.regex_urls = [];
	
	def create_mediator(self):
		f = open(str(self.name)+".xml", "w")
		f.close()
		
	def create_content(self):
		f = open(str(self.name)+".xml", "w")
		f.write("<?xml version='1.0' encoding='UTF-8'?>\n")
		f.write("<sequence xmlns=\"http://ws.apache.org/ns/synapse\" name=\"" + self.name +".xml\" trace=\"disable\">\n\n")
		f.write("\t<log level=\"custom\">\n")
		f.write("\t\t<property expression=\"get-property('REST_SUB_REQUEST_PATH')\" name=\""+self.name+" API\"/>\n")
		f.write("\t</log>\n\n")
		if(self.value == '1'):
			f.write("\t<call-template target=\"entityid-mapper\">\n")
			f.write("\t\t<with-param name=\"JWT_TOKEN\" value=\"{substring-after($trp:Authorization, 'Bearer')}\"/>\n")
			f.write("\t</call-template>\n\n")
		f.write("\t<property name=\"rootHost\" value=\"http://localhost:8280\"/>\n\n")
		f.write("\t<property action=\"remove\" name=\"REST_URL_POSTFIX\" scope=\"axis2\"/>\n\n")
		if(self.urls != ""):
			f.write("\t<switch source=\"get-property('REST_SUB_REQUEST_PATH')\">\n\n")
		f.close()
		
	def direct_mapping(self):
		f = open(str(self.name)+".xml", "a")
		f.write("\t<property name=\"endpoint\" expression=\"fn:concat(get-property('rootHost'),get-property('REST_SUB_REQUEST_PATH'))\"/>\n")
		f.write("\t<log level=\"custom\">\n")
		f.write("\t\t<property name=\"Selected Resource: \" expression=\"fn:concat(get-property('api.ut.HTTP_METHOD'),' ',get-property('REST_SUB_REQUEST_PATH'))\"/>\n")
		f.write("\t\t<property name=\"Backend Endpoint: \" expression=\"get-property('endpoint')\"/>\n")
		f.write("\t</log>\n")
		f.write("\t<header expression=\"get-property('endpoint')\" name=\"To\" scope=\"default\"/>\n\n")
		f.close()
		
	def create_mappings(self):
		sub_request_path = []
		sub_request_path_query_params = []
		urls = (self.urls).split(",")
		self.create_regex(urls)
		for url in self.regex_urls:
			if('?.*' in url):
				sub_request_path_query_params.append(url.replace("?.*","?"))
			else:
				if(url[-1] != '*'):
					sub_request_path.append(url)
				else:
					sub_request_path_query_params.append(url)
		sub_request_path = (sorted(sub_request_path))
		self.case_creation(sub_request_path)
		sub_request_path_query_params = (sorted(sub_request_path_query_params))
		self.case_creation(sub_request_path_query_params[::-1])
		
	
	def create_regex(self,urls):
		for url in urls:
			regex = str(re.sub('{[a-z || A-Z]*}', '.*', url))
			self.regex_urls.append(regex)
			
	def case_creation(self,sub_request_path):
		for path in sub_request_path:
			f = open(str(self.name)+".xml", "a")
			if("?" in path):
				if(".*" in path):
					f.write("\t\t<case regex=\"" +(path.replace('?',''))+ "\">\n")
				else:
					f.write("\t\t<case regex=\"" +(path.replace('?','.*'))+ "\">\n")
				f.write("\t\t\t<filter source=\"\" regex=\"true\">\n\t\t\t\t<then>\n")
				if(path[path.find('?')-1] == '*'):
					f.write("\t\t\t\t\t<property name=\"queryParams\" expression=\"substring-after(get-property('REST_SUB_REQUEST_PATH'), '" +"?"+ "')\"/>\n")
				else:
					f.write("\t\t\t\t\t<property name=\"queryParams\" expression=\"substring-after(get-property('REST_SUB_REQUEST_PATH'), '"+ "/" +(str(path.split('/')[-1])).replace("?","")+ "')\"/>\n")
				f.write("\t\t\t\t</then>\n")
				f.write("\t\t\t\t<else>\n")
				f.write("\t\t\t\t\t<property name=\"queryParams\" value=\"\"/>\n")
				f.write("\t\t\t\t</else>\n\t\t\t</filter>\n")
			else:
				f.write("\t\t<case regex=\"" +(path)+ "\">\n")
			f.write("\t\t\t<property name=\"endpoint\" expression=\"fn:concat(get-property('rootHost'))\"/>\n")
			f.write("\t\t\t\t<log level=\"custom\">\n")
			f.write("\t\t\t\t\t<property name=\"Selected Resource: \" expression=\"fn:concat(get-property('api.ut.HTTP_METHOD'),' ',get-property('REST_SUB_REQUEST_PATH'))\"/>\n")
			f.write("\t\t\t\t\t<property name=\"Endpoint: \" expression=\"$ctx:endpoint\"/>\n")
			f.write("\t\t\t\t</log>\n")
			f.write("\t\t\t<header expression=\"$ctx:endpoint\" name=\"To\" scope=\"default\"/>\n")
			f.write("\t\t</case>\n\n")
			f.close()
		
	
	def close_file(self):
		f = open(str(self.name)+".xml", "a")
		if(self.urls != ""):
			f.write("\t\t<default/>\n\n")
			f.write("\t</switch>\n\n")
		f.write("</sequence>\n\n")
		f.close()