class exportToFile:
	def __init__(self):
		pass
		
	def writeToFile(self,filename,content):
		try:
			f=open("/Results/"+filename,'w');
			f.write(content);
			f.close()
		except Exception as e:
			print(str(e));
			
		