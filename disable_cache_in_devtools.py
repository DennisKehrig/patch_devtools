#!/usr/bin/env python

import os
import sys
import re
import shutil
import paktools

'''Patches devtools_resources.pak to disable the cache by default'''

def patch(devtools_js):
  print "Patching %s" % devtools_js
  with open(devtools_js, "rb") as file:
    contents = file.read()
    
    # in:  this.cacheDisabled = this.createSetting("cacheDisabled", false);
    # out: this.cacheDisabled = this.createSetting("cacheDisabled", true);
    contents = re.sub("(this\.createSetting\s*\((['\"])cacheDisabled\\2,\s*)false(\s*\))", "\\1true\\3", contents)
    
    # delete:  if (WebInspector.settings.cacheDisabled.get())
    #          NetworkAgent.setCacheDisabled(true);
    contents = re.sub("if\s*\(WebInspector\.settings\.cacheDisabled\.get\s*\(\)\s*\)\s*[\s\r\n]*NetworkAgent\.setCacheDisabled\s*\(true\)\s*;?[\s\r\n]*", "", contents)
    
    # find: _reset: function(preserveItems)
    #       {
    # add:  if (WebInspector.settings.cacheDisabled.get())
    #         NetworkAgent.setCacheDisabled(true);
    contents = re.sub("(_reset:\s*function\s*\(\s*preserveItems\s*\)[\s\r\n]*\{[\s\r\n]*)", "\\1if (WebInspector.settings.cacheDisabled.get())\n{\nwindow.setTimeout(function() { NetworkAgent.setCacheDisabled(true); }, 1000);\n}", contents)
  
  with open(devtools_js, "wb") as file:
    file.write(contents)

def main():
  if len(sys.argv) == 1:
    id = 20501
  else:
    arg = sys.argv[1]
    if arg.isdigit():
      id = int(arg)
    else:
      id = paktools.FindIdForNameInHeaderFile("DEVTOOLS_JS", arg)
  
  original = "devtools_resources.pak.bak"
  target   = "devtools_resources.pak"
  tempDir  = "devtools_resources"
  
  if not os.path.exists(original):
    print "Copying %s to %s" % (target, original)
    shutil.copy2(target, original)
  
  paktools.UnpackFileIntoDirectory(original, tempDir)
  patch(os.path.join(tempDir, str(id)))
  paktools.PackDirectoryIntoFile(tempDir, target)
  
  shutil.rmtree(tempDir)

if __name__ == '__main__':
  main()