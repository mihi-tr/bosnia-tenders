import urllib2
import re
import lxml.html
import csv

base="http://www.ekapija.com/website/bih/search.php?terId=3&doctype=3&st=tw&from=%s&to=%s&pg="%("01.04.2013","31.10.2013")

params={"title":".//td[@class='tenderWinnerTitle']/a",
    "amount":".//div[@class='tenderWinnerMoney']",
    "winner":".//a[@class='tenderWinnerLink']",
    "winnerUrl":".//a[@class='tenderWinnerLink']/@href",
    "tenderer":".//a[@class='tenderWinnerTendererLink']",
    "tendererUrl":".//a[@class='tenderWinnerTendererLink']/@href",
    "date":".//td[@class='tenderWinnerPublishingDate']"}

def dom_for_url(url):
  u=urllib2.urlopen(url)
  return lxml.html.fromstring(u.read())
  
def get_number_of_pages():
  r=dom_for_url(base+"1")
  c=r.xpath("//td[@class='allCount']")[0].text
  return int(re.search(".*?([0-9]+).*?",c).group(1))/10

def get_value(e):
  if not len(e):
    return ""
  if hasattr(e[0],"text"):
    return e[0].text
  else:
    return e[0]

def process_entry(e):
  return dict(((k,get_value(e.xpath(v))) for (k,v) in params.items()))
  


def process_page(url):
  r=dom_for_url(url)
  dts=r.xpath("//table[@class='tenderWinnerDataTable']")
  return [process_entry(e) for e in dts]



urls=(base+str(i) for i in range(1,get_number_of_pages()+2))

if __name__=="__main__":
  f=open("../data/bosnia-tenders.csv","wb")
  w=csv.writer(f)
  c=params.keys()
  w.writerow(c)
  for u in urls:
    print "processing: %s"%u
    for d in process_page(u):
      try:
        w.writerow([d[i].encode("utf-8") for i in c])
      except AttributeError:
        print "error in %s"%d
  f.close()
