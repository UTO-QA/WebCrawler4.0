import sqlite3

class sqliteDB:
	insert_run_details="INSERT INTO RUN_DETAILS(D_RUN_DATE, WEBSITE) VALUES(CURRENT_TIMESTAMP, ?)";
	insert_run_results="INSERT INTO RUN_RESULTS(N_RUN_ID,V_LINK_URL,V_STATUS_CODE,V_COMMENT,V_ONPAGE) VALUES(?,?,?,?,?)";
	
	get_run_results="SELECT * FROM RUN_DETAILS RD JOIN RUN_RESULTS RR ON RR.N_RUN_ID=RD.N_RUN_ID WHERE RD.N_RUN_ID=? AND RR.V_STATUS_CODE NOT IN ('200','302')";
	get_prev_runs="SELECT * FROM RUN_DETAILS";
	
	def connectToDB(self):
		conn=sqlite3.connect('Results/results.db');
		cur=conn.cursor();
		return cur;
	
	def insertResults(self,results,website):
		
		try:
			conn=sqlite3.connect('Results/results.db');
			cur=conn.cursor();
			cur.execute("PRAGMA foreign_keys = ON");
			cur.execute(sqliteDB.insert_run_details,(website,));
			run_id=cur.lastrowid;
			for r in results:
				#print "In res";
				
				cur.execute(sqliteDB.insert_run_results,(run_id,  r.l, r.status_code, r.comment,r.onPage));
			conn.commit();       
			conn.close();
			return run_id;
		except Exception as e:
			print e;
	
	def getResults(self,run_id):
		try:
			conn=sqlite3.connect('Results/results.db');
			cur=conn.cursor();
			cur.execute(sqliteDB.get_run_results,(run_id,));
			rows=cur.fetchall();
			return rows;
		except Exception as e:
			print e;
			
	def getRuns(self):
		try:
			conn=sqlite3.connect('Results/results.db');
			cur=conn.cursor();
			cur.execute(sqliteDB.get_prev_runs);
			rows=cur.fetchall();
			return rows;
		except Exception as e:
			print e;