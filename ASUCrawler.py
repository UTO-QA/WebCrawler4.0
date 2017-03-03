from variables import resultObject
from urllib2 import urlopen, Request, HTTPError, URLError
from bs4 import BeautifulSoup
import os
import re
from sqliteDB import sqliteDB
from  urlparse import urljoin

class Crawler:
	def __init__(self):
		self.links=[];
		self.urlList=[];
		self.result=[]; #old	
		self.resultList=[]; #new
	
	def writeResults(self):
		dir=os.path.dirname(os.path.abspath(__file__));
		filename=dir+"\Results\Crawl.csv";
		f=open(filename,'w');
		
		for r in self.urlList:

			f.write(r.l+","+r.status_code+","+r+"\n");
		
		f.close();
		
	def dbResults(self,website):
		db=sqliteDB();
		row_id=sqliteDB.insertResults(db,self.resultList,website);
		rows=sqliteDB.getResults(db,row_id);
		return rows;
		
	def getLinks(self,website):
		print "In Get links";
		#Get the page response
		page=urlopen(website);
		redirectUrl=page.geturl();
		soup=BeautifulSoup(page);
		
		for l in soup.findAll('a'):
			if l is not None and l.get("href") is not None:
				temp=urljoin(redirectUrl,l.get("href"));
				self.urlList.append([temp,1,redirectUrl]);
				print [str(temp),1];
				
	def crawlLinks(self):
		global links;
		
		print "In crawler";
		print "Number of links found %d" %(len(self.urlList));
		
		for l in self.urlList:
			try:
				if l[0].startswith("//") or l[0].startswith("http") or l[0].startswith("https") or l[0].startswith("Http") or l[0].startswith("Http"):
					#request=Request(l[0],data=None,headers={});
					page=urlopen(l[0]);
					status_code=str(page.code)
					comment="";
					redirectUrl=page.geturl();
					if l[1]<1:
						#Get the new url in the page
						soup=BeautifulSoup(page);
						for lnk in soup.findAll("a"):
							if lnk is not None:
								temp=lnk.get("href");
								temp=urljoin(redirectUrl,temp);
								if temp is not None and [temp,2,l[0]] not in self.urlList:
									self.urlList.append([temp,2,l[0]]);
									#print [str(temp),2];
				else:
					status_code="-1";
					
			except HTTPError, URLError:
				status_code=str(URLError.code);
				try:
					comment=str(URLError);
				except Exception as e1:
					comment="Error"
			except Exception as e:
				status_code='0';
				try:
					comment=str(e);
				except Exception as e1:
					comment="Error"
					
			
			#result object
			if status_code!="-1" and l is not None and len(l)>1:
				tempRes=resultObject(l[0],status_code,comment,l[2]);
				try:
					print tempRes.l,
					print ",",
					print tempRes.status_code,
					print ",",
					print tempRes.comment;
					self.resultList.append(tempRes);
				except Exception as e:
					print "Unincode Exception";
						
		
		print "Done";
		
	def performCrawl(self,website):
		rows=()
		try:
			self.getLinks(website);
			self.crawlLinks();
			rows=self.dbResults(website);
			print "Total Links Crawled %d" %(len(self.urlList));
			return rows;
		except Exception as e:
			rows=self.dbResults(website);
			print "Exception Occured Saving current state:";
			print str(e);
			return rows;
		
		
	
if __name__=="__main__":
	Crawler.performCrawl(Crawler(),'https://about.asu.edu/');
	