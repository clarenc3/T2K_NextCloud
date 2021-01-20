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

#for elem in tree.iter():
  #print elem.tag, elem.text

# Loop over each entry
First = ""

# Check first for errors
if root.tag == "{DAV:}error":
  message = root.find('{http://sabredav.org/ns}message')
  print "Error: ",message.text
  sys.exit(-1)

# Loop over all the children in the root
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
      if size is not None and size.text is not None and Size == 0:
        Size = float(size.text)
        if Size != 0:
          Size = Size/(1024**2)

    if Folder == "" or Mod == "":
      continue

  # If this is the top folder, print it
  topfolder = False
  if First == "":
    First = Folder
    print "Top folder: ",
    topfolder = True
  else:
    Folder = Folder.split(First)[-1]
    print " ",

  print Folder
  if not topfolder:
    if Size != 0:
      print "    File"
      print "    Size:", '{0:.2f}'.format(Size), "MB"
    else:
      print "    Directory"

    print "    Last Modified:", Mod


'''
for response in root.findall('{DAV:}response'):
  # The main text
  href = response.find("{DAV:}href")
  name=href.text
  print name

  for propstat in response.find('{DAV:}propstat'):
    # Make sure we're getting a property and not a status
    if propstat.tag != "{DAV:}prop": 
      continue
    lastmod = propstat.find('{DAV:}getlastmodified')
    lastmodtext = lastmod.text
    print lastmodtext

    size  = propstat.find("{DAV:}getcontentlength")
    if size is not None:
      print "File"
      print float(size.text)/(1024**2)
    else:
      print "Directory"
'''
