Whether it's clarifying how to use them, requesting new features, finding bugs,
or contributing to writing them yourself, the Xively libraries are completely
open-source and always being updated, and we want to hear your thoughts.

Feel free to fork and improve this library any way you want. If you feel that
the library benefits from your changes, please open a pull request and
contribute back!


## Getting Help with Using a Library
For discussion, questions, and help with implementation, we use [Stack
Overflow](http://stackoverflow.com/questions/tagged/xively).  Be sure to use a
`xively` tag.

## Requesting New Features
If you've got a feature request for this library, file it with the GitHub issue
tracker.  (You can find it on the Github page for each library, under the
"Issues" tab.)  We're always expanding our libraries, and would love to hear
your ideas.

## Submitting Bug Reports
If you find a problem with a library, whether you are stuck or want to address
it yourself, first log it using the GitHub issue tracker.  That way, we can
take a look and let you know how best to proceed, and if work is already
underway on this issue.

**Note:** The issue tracker is for *bugs* and *new features*, not help
requests. For procedural questions - like help - see the above "Getting Help"
section.

#### Reporting bugs effectively

Please include as much information as you have available.  Where possible:
  - your IDE software and library version (e.g. Visual Studio 2012, mbed Online
    IDE, Xively Java Lib 1.0)
  - what device you were running the code on (e.g. iOS 5, Android 4.0, Arduino
    Uno)
  - how you are connected to the web (e.g. Gainspan wireless module, Ethernet)
  - and any more detail you have (e.g. what are the underlying versions of
    software stack)

Mention very precisely what went wrong. For example, instead of "I can't add a
datapoint", it is more helpful to say "the library returned an error 'X' when I
tried datapoint.upload()".  What did you expect to happen? What happened
instead? Describe the exact steps you could take to recreate it.


## Contributing to Xively Libraries
If you see an improvement that you can make to a library, bring it on!  All of
our libraries are open-source and constantly improving, so take a look at our
guidelines below and send in your contribution.

### Include Tests
All of our libraries are set up to be tested by Travis CI, with full-coverage
unit tests, and integration tests where possible.  If you are going to
contribute, please ensure that your contributions can be tested as well.  If
you need help with this, let us know!

### Use Pull Requests
If you know exactly how to implement the feature being suggested or fix the bug
being reported, please open a pull request instead of an issue. Pull requests
are easier than patches or inline code blocks for discussing and merging the
changes.

### Contributing (Step-by-step)

1) Clone the Repo of the library you want to contribute to:
```
git clone git://github.com/xively/xively-python.git
```
2) Create a new Branch, named for the feature you're addressing or adding:
```
cd xively-python
git checkout -b new_feature_branch
```
3) Code:

Do what you do best here!  Follow these guidelines, and be mindful of how your
change will impact the whole of the library:
- write with testing in mind (and write tests!)
- keep the transport layer of a library (e.g. TCP/HTTP) separate from the
  Xively layer (e.g. Xively Feed object)
- make sure it won't break anything that relied on a previous version
- check to see if documentation updates are needed

4) Rebase your commits

Many fixes require a multitude of commits, but when submitting a pull request,
we'd prefer if you'd squash them into a single commit for readability:
```
git remote add upstream https://github.com/xively/xively-python
git fetch upstream
git checkout new_feature_branch
git rebase upstream/master
git rebase -i
```
Choose 'squash' for all of your commits except the first one.  Edit the commit
message to describe the whole of your contribution and changes.
```
git push origin new_feature_branch -f
git checkout master
git pull --rebase
```

5) Update the docs

If you've made a change that introduces changes that will alter or break the
API for users of the library, then we'd appreciate you also updating the docs.

The documentation files are located in the `docs` folder, so please remember to
update all affected examples, and add any new features that you've developed, and
include this in the pull request that you are planning to submit.

6) Issue a Pull Request

First, push your rebased single commit to your remote fork of the Xively library
```
git remote add mine git@github.com:<your user name>/xively-python.git
git push mine new_feature_branch
```
Then:
- Navigate to the  repository you just pushed to (e.g.
  https://github.com/your-user-name/xively-python)
- Click "Pull Request"
- Select your branch name (new_feature_branch) in the branch field
- Click "Update Commit Range"
- Ensure the changes you introduced are included in the "Commits" and "Files
  Changed" tabs
- Fill in some details about your potential contribution including a meaningful
  title
- Click "Send pull request".

Once these steps are done, we'll take a look and get back to you!

### Responding to Feedback

The team may recommend adjustments to your code, and this is perfectly normal.
Part of interacting with a healthy open-source community requires you to be
open to learning new techniques and strategies; don't get discouraged!
Remember: if the team suggest changes to your code, they care enough about your
work that they want to include it, and hope that you can assist by implementing
those revisions on your own.
