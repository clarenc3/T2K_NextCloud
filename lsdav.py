#!/env/bin/python

import xml.etree.cElementTree as ET
import sys
import datetime

# First check stream
data = sys.stdin.read()
FromPipe = False
if data != None:
  FromPipe = True

FromArg = False
if len(sys.argv) == 2:
  FromArg = True

if FromArg == False and FromPipe == False:
  print "Need to run from argument or pipe, but am doing neither"
  sys.exit(-1)

if FromPipe == True:
  tree = ET.ElementTree(ET.fromstring(data))

if FromArg == True:
  tree = ET.parse(sys.argv[1])

# Get the root of the tree
root = tree.getroot()

# Loop over each entry
First = ""
for child in root:
  Folder = ""
  Mod = ""
  Size = 0
  for kid in child:
    # Extract the hyperlink folder
    if kid.tag == "{DAV:}href":
      Folder = kid.text

    # Get the propstat
    elif kid.tag == "{DAV:}propstat":
      prop  = kid.find("{DAV:}prop")
      mod   = prop.find("{DAV:}getlastmodified")
      size  = prop.find("{DAV:}getcontentlength")
      if mod is not None:
        Mod = mod.text
        Mod = datetime.datetime.strptime(Mod, "%a, %d %b %Y %H:%M:%S %Z")
      if size is not None and Size != 0:
        Size = float(size.text)/(1024**2)


    if Folder == "" or Mod == "":
      continue

  if First == "":
    First = Folder
    print "Folder: ",
  else:
    #print len(First), len(Folder)
    #Folder = Folder[len(First), len(Folder)]
    Folder = Folder.split(First)[-1]
    print " ",
    #Folder = Folder[:Folder.lfind(First)]

  print Folder
  print "    Size:", '{0:.2f}'.format(Size), "MB"
  print "    Last Modified:", Mod

      #for each in prop:
      #for mod in prop.find("{DAV:}getlastmodified"):
        #print mod.text

  #print child.tag, child.attrib
  #for kid in child:
    #print kid.tag, kid.attrib

#for elem in tree.iter():
  #print elem.tag, elem.attrib, elem.text

#for response in root.findall('{DAV:}response'):
  #print response
  #print response.tag, response.attrib
  #propstat = response.find('{DAV:}propstat')
  #prop = propstat.find('{DAV:}prop')
  #getlastmodified = prop.find('{DAV:}getlastmodified')
  #print getlastmodified.text
