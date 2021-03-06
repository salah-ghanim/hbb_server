
import json
import logging
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
import datetime

class Record(db.Model):
    """Models an individual RecordItem entry with device, marks, and extras."""
    user      = db.StringProperty()
    first     = db.IntegerProperty()
    second    = db.IntegerProperty()
    third     = db.IntegerProperty()
    fourth    = db.IntegerProperty()
    time      = db.IntegerProperty()
    extra     = db.StringProperty()
    

def record_key(record_name=None):
    return db.Key.from_path('Record', record_name or 'default_records')
  
class MainPage(webapp.RequestHandler):
    def get(self):
        page = 0
        try:
            page = int(self.request.get('page')) 
             
        except ValueError:
            "log error scilently"
        """href="http://helpingbabybreath.appspot.com/generate"""
        response = """
          <html>
          <HEAD> <title>Helping Baby Breath</title></HEAD>
            <body>
                <p align= "center" style="font-size:20px">Helping Baby Breath</p>

               <div style="background-color:#6ABA71; text-align:center; padding:10px; margin-bottom:25px;">
            <a style="  border:none; outline:none; text-decoration:none;" 
            href="http://helpingbabybreath.appspot.com/generate"
            >Generate Report</a>
        </div>
            """
        query =  """SELECT * 
                            FROM Record 
                            WHERE ANCESTOR IS :1 
                            ORDER BY time DESC LIMIT page, 100"""
                               
        if page > 0:   
             
            records = db.GqlQuery(query.replace('page', str(page * 100)),
                            record_key('default_records'))
        
        else :
            records = db.GqlQuery("SELECT * "
                            "FROM Record "
                            "WHERE ANCESTOR IS :1 "
                            "ORDER BY time DESC LIMIT 100",
                            record_key('default_records'))
        
        if records:
            response = response + """ <table border="1" align="center">
            <tr bgcolor="#F5F5D0">
                    <td>User name</td>
                    <td>Record Time</td>                    
                    <td>First Mark</td>
                    <td>Second Mark</td>
                    <td>Third Mark</td>
                    <td>Fourth Mark</td>
                    <td>Extra</td>                                       
                    </tr>"""
                    
            for record in records:
                date = datetime.datetime.fromtimestamp(record.time / 1e3)
                txt = date.strftime("%Y-%m-%d %H:%M:%S")
                extra = 'No Report Available'
                if record.extra and record.extra != '{}':
                    extra = """<a href="http://helpingbabybreath.appspot.com/report?id=$reportid$">Report</a> """.replace("$reportid$", str(record.key()))
                response = response + """<tr>
                    <td>%s</td>
                    <td>%s</td>                    
                    <td>%d</td>
                    <td>%d</td>
                    <td>%d</td>
                    <td>%d</td>
                    <td>%s</td>                                       
                    </tr>""" % \
                    (record.user ,txt ,record.first 
                     ,record.second ,record.third ,record.fourth ,extra)
                
            response += "</table> "
              
        response +="""<div style="text-align: center ;" >"""
                   
        if page > 0 :
            response = response + """
                           <a href="http://helpingbabybreath.appspot.com/?page=$page$">Previous</a>
            
            """.replace('$page$', str(page - 1));
        if records:
            response += """
             <a href="http://helpingbabybreath.appspot.com/?page=$page$">Next</a>
            
            """.replace('$page$', str(page + 1))   
        response +=  '</div></body></html>'
        self.response.out.write(response)
    
  
class ReportPage(webapp.RequestHandler):
    def get(self):
        key = 0
        try:
            key = self.request.get('id') 
             
        except ValueError:
            " self.request.GET.items()"
        
        response = """
          <html>
          <HEAD> <title>Helping Baby Breath Report</title></HEAD>
            <body><div align= "center" >"""
     
                               
        if key == 0:   
            response += "invalid report id"
        
        else :
                record = db.get(key)
                if record.extra:
                    try: 
                        j = json.loads(record.extra)
                        if 'extra_id' in j :
                            response += " <br>Report id: " + j['extra_id'] + "</br>"
                        if 'extra_cry' in j :    
                            response += " <br>Did the baby cry spontaneously at birth? " + j['extra_cry'] + "</br>"
                        if 'exra_vent' in j :        
                            response += " <br>Did you have to start bag and mask ventilation? " + j['exra_vent'] + "</br>"
                        if 'extra_alive' in j :                                    
                            response += " <br>New born is: " + j['extra_alive'] + "</br>"
                        if 'extra_primary' in j :
                            response += " <br>Primary cause of death: " + j['extra_primary'] + "</br>"
                            if 'extra_other' in j:
                                response += " <br>details: " + j['extra_other'] + "</br>"
                            if 'extra_problem' in j:
                                response += "<div> "
                                response += "<br>Problems with the system:" + j['extra_problem'] +            "   </div>"       
                    
                   
                    except ValueError:
                        print "parse Error"
                         
        response += "</div></body></html>"           
        self.response.out.write(response)

class POST(webapp.RequestHandler):
    def post(self):
        key = self.request.get("key")
        if key and key != '':
            record = db.get(key)
        else:
            record = Record(parent=record_key())
        record.user = self.request.get('user')
        record.first = int(self.request.get('first_mark'))
        record.second = int(self.request.get('second_mark'))
        record.third = int(self.request.get('third_mark'))
        record.fourth = int(self.request.get('fourth_mark'))
        record.time = int(self.request.get('time_created'))
        record.extra = self.request.get('extra')
        record.put()
        self.response.out.write(str(record.key()))
    
class ExcelPage(webapp.RequestHandler):
    def get(self): 
        response = """
            <!doctype html>
 
    <html lang="en">
    <head>
      <meta charset="utf-8" />
      <title>Helping Baby Breath - Record Generator</title>
      <link rel="stylesheet" href="http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css" />
      <script src="http://code.jquery.com/jquery-1.9.1.js"></script>
      <script src="http://code.jquery.com/ui/1.10.3/jquery-ui.js"></script>
      <link rel="stylesheet" href="/resources/demos/style.css" />
      <style type="text/css">
        div { text-align:center; vertical-align:middle;  margin-top: 50px; }
        </style>
      <script>
      $(function() {
        $( "#startdate" ).datepicker();
        $( "#enddate" ).datepicker();

      });
      </script>
    </head>
    <body>
    <form action="http://helpingbabybreath.appspot.com//generate" method="post" accept-charset="utf-8">
    <div>
    <p>Please select the record starting and end dates </p>
    <p >From: </p>
    <input type="text" id="startdate" name="from"/>
    <p>To:</p>
    <input type="text" id="enddate" align="right" name="to"/>
    </div>
    <div >
    <input type="submit" value="Generate" />
    </div>
    </form>
    </body>
    </html>
        
        """
        self.response.out.write(response)
        
    def post(self):
     try:
        import time
        start = self.request.get("from");
        end  = self.request.get("to");
        fmt = "%m/%d/%Y"
        start_time = 0
        end_time = 0
        if (len(start) and len(end)):
            
            start_time    = int(round(time.mktime(time.strptime(start, fmt)))) * 1000
            end_time      = int(round(time.mktime(time.strptime(end, fmt)))) * 1000
            
        q = "SELECT * FROM Record WHERE time >= $start$ AND time <= $end$".replace("$start$", str(start_time)).replace("$end$", str(end_time))
        logging.error(q)
        records = db.GqlQuery(q)
        
        if records:
            self.response.headers["Content-Type"] = "text/csv"
            self.response.headers["Content-Disposition"] = "attachment; filename='hbb_report_%s.csv'".replace("%s", start);
            response =   """User name,Record Time,First Mark,Second Mark,Third Mark,Fourth Mark,ID,Alive,Cry,Cause of Death,venting,other,problem
"""
            import json_parser        
            for record in records:
                date = datetime.datetime.fromtimestamp(record.time / 1e3)
                txt = date.strftime("%Y-%m-%d %H:%M:%S")
                extra = ',,,,,,,,'
                if record.extra and record.extra != '{}':
                    extra = json_parser.toCSV(record.extra)
                    
                response = response + """%s,%s,%d,%d,%d,%d,%s
""" % \
                    (record.user ,txt ,record.first 
                     ,record.second ,record.third ,record.fourth ,extra)
                
            self.response.out.write(response)
            return
        
     except:
        ""
     self.response.out.write("Unable to generate Report")
   
        
application = webapp.WSGIApplication(
                                     [('/', MainPage), ('/report', ReportPage), ('/generate', ExcelPage),
                                      ('/data', POST)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
