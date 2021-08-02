import pprint
from html.parser import HTMLParser

class ParcelParser(HTMLParser):
  def __init__(self, parcel_id):
    super().__init__()
    self.state = "initial"
    self.parcel_id = parcel_id
    self.values = {
      "MainContent_lblGenAssessment": None,
      "MainContent_lblLndAcres": None,
      "MainContent_lblZone": None,
      "MainContent_lblLocation": None,
    }
    self.occupancy = 0

  def record(self):
    for k, v in self.values.items():
      if v is None:
        raise Exception("Missing %s in %s" % (k, self.parcel_id))

    pretty_assessment = self.values["MainContent_lblGenAssessment"]
    assessment = int(pretty_assessment.replace("$", "").replace(",", ""))
    sqft = round(float(self.values["MainContent_lblLndAcres"]) * 43560)
    zone = self.values["MainContent_lblZone"]
    address = self.values["MainContent_lblLocation"]

    score = 0
    if sqft > 0 and zone in ['MR4', 'MR5', 'MR6']:
      score = assessment / sqft
    return [score, self.parcel_id, pretty_assessment, sqft, zone, address, self.occupancy]

  def handle_starttag(self, tag, attrs):
    if tag == "span":
      for k, v in attrs:
        if k == "id" and v in self.values:
          self.state = v
    elif tag == "td":
      if self.state == "occupancy":
        self.state = "read-occupancy"
      else:
        self.state = "td"

  def handle_endtag(self, tag):
    if self.state not in ["occupancy"]:
      self.state = "initial"

  def handle_data(self, data):
    if self.state in self.values:
      self.values[self.state] = data
    elif self.state == "td" and data == "Occupancy":
      self.state = "occupancy"
    elif self.state == "read-occupancy":
      data = data.strip()
      if data:
        self.occupancy = int(data)

def get_records():
  records = []
  for parcel_id in range(1, 13001):
    with open("pages/%s.html" % parcel_id) as inf:
      parser = ParcelParser(parcel_id)
      html = inf.read()
      if "There was an error loading the parcel" in html:
        continue
      parser.feed(html)
      record = parser.record()
      records.append(record)

  return records

def print_records(records):
  print("valuation per sqft\taddress\tzone\tsqft\tvaluation\tlink\toccupancy")
  for score, parcel_id, pretty_assessment, sqft, zone, address, occupancy in records:
    if score < 1:
      continue
    print("%.0f\t%s\t%s\t%s\t%s\thttps://gis.vgsi.com/somervillema/Parcel.aspx?Pid=%s\t%s" % (
      score, address, zone, sqft, pretty_assessment, parcel_id, occupancy
    ))
    #print("%.2f: %s (#%s) -- %s @ %s in %s" % (
    #  score, address, parcel_id, sqft, pretty_assessment, zone))

def start():
  records = get_records()
  records.sort()
  print_records(records)

if __name__ == "__main__":
  start()
