#!/usr/bin/env python

from os import *
import sys

repo = sys.argv[1]

renameCloseToDestroy = True
renameLayoutToLayoutView = True
renameItemToChild = True
apiCleanup = True

codemod = "./bin/codemod.py"

def confirm():
  ch = sys.stdin.read(1)
  if ch == "\n" or ch == "y":
    return True
  if ch == "n":
    return False
  elif ch == "q":
    sys.exit()
  else:
    print "sorry, didn\'t understand"

def sub(search, replace):
  print "\n\033[94mReplace:\n\n\033[91m    %s \033[0m with \033[92m %s \033[0m \033[93m\n\n[y,n,q]\033[0m " % (search, replace),
  good = confirm()
  global repo

  if good:
    cmd = ("%s -m -d %s %s %s" % (codemod, repo, search, replace))
    print cmd
    system(cmd)


def subString(search, replace):
  searchTermS = "\"\'%s\'\"" % (search)
  replaceTermS  = "\"\'%s\'\"" % (replace)
  searchTermD = '\'\"%s\"\'' % (search)
  replaceTermD  = '\'\"%s\"\'' % (replace)
  sub(searchTermS, replaceTermS)
  sub(searchTermD, replaceTermD)

def subMethod(search, replace):
  searchTerm = "'.%s\\('" % (search)
  replaceTerm  = "'.%s('" % (replace)
  sub(searchTerm, replaceTerm)

def subEvent(search, replace):
  searchTermCbk = "\"%s\"" % (eventToCbk(search))
  replaceTermCbk = "\"%s\"" % (eventToCbk(replace))

  sub(searchTermCbk, replaceTermCbk)
  subString(search, replace)


def subTerm(search, replace):
  searchTerm = "\"%s\"" % search
  replaceTerm = "\"%s\"" % replace
  sub(searchTerm, replaceTerm)

def subString(search, replace):
  searchTerm = "\"%s\"" % search
  replaceTerm = "\"%s\"" % replace
  sub(searchTerm, replaceTerm)

def subKey(search, replace):
  searchTerm = "\"%s:\"" % search
  replaceTerm = "\"%s:\"" % replace
  sub(searchTerm, replaceTerm)

def eventToCbk(event):
  parts = event.split(':')
  parts = [part.capitalize() for part in parts]
  cbk = "on"+ ''.join(parts)
  return cbk




#
#
#
#
#
# UPGRADER CHANGES
#
#
#
#
#
#




if (renameCloseToDestroy):
  subMethod("close", "destroy")
  subMethod("closeRegions", "destroyRegions")
  subMethod("closeChildren", "destroyChildren")

  subEvent('collection:before:close', 'before:destroy')
  subEvent('collection:closed', 'destroy')
  subEvent('item:before:close', 'before:destroy')
  subEvent('item:closed', 'destroy')
  subTerm("closed", "destroy")
  subEvent("close", "destroy")

  subTerm('isClosed', 'isDestroyed')

  subKey('preventClose', 'preventDestroy')

if (renameLayoutToLayoutView):
  subTerm("Marionette.Layout\.", "Marionette.LayoutView.")
  subTerm("Marionette.Layout\(", "Marionette.LayoutView(")

if (renameItemToChild):
  subTerm("itemView", "childView")
  subTerm("itemViewEventPrefix", "childViewEventPrefix")
  subTerm("itemViewOptions", "childViewOptions")
  subTerm("itemEvents", "childEvents")
  subTerm("itemViewContainer", "childViewContainer")

  subMethod("addChildView", "onChildAdd")
  subMethod("removeItemView", "onChildRemove")
  subMethod("getItemView", "getChildView")
  subMethod("addItemView", "addChild")
  subMethod("removeItemView", "removeChildView")
  subMethod("renderItemView", "renderChildView")
  subMethod("closeChildren", "destroyChildren")
  subMethod("resetItemViewContainer", "resetChildViewContainer")
  subMethod("getItemViewContainer", "getChildViewContainer")

  subEvent("before:item:added", "before:add:child")
  subEvent("after:item:added", "add:child")
  subEvent("before:item:rendered", "before:render")
  subEvent("item:rendered", "render")
  subEvent("item:before:render", "before:render")
  subTerm("itemview", "childview")
  subTerm("onItemview", "onChildview")

if (apiCleanup):
  subMethod("renderModel", "_renderRoot")
  subEvent("region:add", "add:region")
  subEvent("region:remove", "remove:region")
  subEvent("initialize:before", "before:start")
  subEvent("initialize:after", "start")
  subTerm("regionType", "regionClass")

  subEvent("composite:collection:before:render", "before:render:template")
  subEvent("composite:model:rendered", "render:template")
  subEvent("composite:rendered", "render")
  subEvent("composite:before:render:collection", "before:render:collection")
  subEvent("composite:collection:rendered", "render:collection")

  subEvent("collection:before:destroy", "before:destroy:collection")
  subEvent("collection:destroy", "destroy:collection")
  subEvent("collection:before:render", "before:render:collection")
  subEvent("collection:rendered", "render")
  subEvent("before:child:added", "before:add:child")
  subEvent("after:child:added", "add:child")
  subEvent("before:child:remove", "before:remove:child")
  subEvent("child:removed", "remove:child")
  subEvent("region:add", "add:region")
  subEvent("region:remove", "remove:region")


# THINGS WE MIGHT NOT BE ABLE TO CHANGE
# this is a todo list of things I found when working on adding regex
# that were not immediately obvious to change. Sorry, you'll have to do these yourself :)
#
#
# 1. Module's initialize function now accepts these params(options, moduleName, app) it used to be these (moduleName, app, options)
# 2. regions need to have an element when they're showing a view. Previously you could show a view in a region and if the region didn't have an element on the page at the time, nothing would happen. Now we through an error so you know immediately that you need to fix something.
# I'm sure there other changes as well, so don't treat this as an exhaustive list.
