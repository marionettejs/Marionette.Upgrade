# Marionette Upgrade

### Using

* 1 `$ git clone https://github.com/marionettejs/Marionette.Upgrade.git`
* 2 `$ cd Marionette.Upgrade && chmod +x upgrade.py`
* 3a. If possible remove all of your vendor scripts in your project as these will only generate more noise for you to sort through during your upgrade process.

* 3b. `$ ./upgrade.py PATH_TO_PROJECT_DIR --all`

> Ensure that you are using Python2 when you run the tool, otherwise it will not work.

### Why

We made lots of changes to Marionette's API in 2.0. In many ways, we're taking out the garbage that accumulated over the past couple years. With all of these changes, it's easy to wonder if they'll really help or if it's worth it to take the time to fix them. I think it is, there are lots of great projects planned for 2.x that if you're a fan of Marionette you'll want to enjoy.

Even though we made lots of changes to the API, the vast majority of them were simple renamings of methods, events and properties. This tool will help walk you through all of the changes.

The way it works is a lot like `git add -p`. When you run the tool, you'll be shown each change and prompted to approve it, reject it, or edit it.

I realize that this is still a scary process because you'll be covering a lot of ground fairly quickly and the final diff will still be large. I hope that this tool will be a good starting off point. If you're like me, you'll quickly start playing with the regular expressions to fine-tune the searches for your project and approach this change-set as methodically as possible in whatever way works out for you.

Lastly, this is an experiment in coming up with the right workflow for organizing a large API upgrade. The tool is decidedly very simple, so that it's flexible and can change with time. If you find something works particulary well, please share your successes. If you find that there's a glaring hole, please don't be a stranger.


![](http://f.cl.ly/items/1W1M2H0V1n3v1E012S1x/Image%202014-05-14%20at%2010.59.40%20AM.png)


### Additional Information

+ The upgrade tool is organized in three categories based on the type of change. By default, they're all turned on, but it's suggested that you do one change at a time.
+ There's nothing magical here. I wrote each of these changes to work off of simple regexes, if there are additional changes that you think would help feel free to add them. Also, if there are places where I missed things, please file a Pull Request!
+ This works. I know, I was surprised too. I ran this tool against our v1.8 test suite and it fared surprisingly well. It made over 500 changes and only missed a couple things:
	+ methods that referenced spies with "foobar" instead of "foobar("
	+ semantic changes like onBeforeDestroy, which no longer work the same way
	+ function parameter changes like appendHtml losing a param. We could write a regex for this, but meh.


### Changes

The two big changes in v2.0 are the change in collection view from itemViews to childViews and the change in Views going from closing to destroying.

The childView change should be relatively simple to search out and change and none of the semantics changed.

The close to destroy view change should also be easy to find, but unlike childView the behavior of destroy is different from close, when a view was closed it could be re-opened, now that view's are being destroyed there's no bringing them back. So, when you change your code to start destroying your views, you should double check that you don't try to re-open them again.
