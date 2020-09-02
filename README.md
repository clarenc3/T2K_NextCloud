# T2K NextCloud operations
Simple file operations using NextCloud at KCL for the T2K experiment.

Currently supporting `ls` operation using `curl` and `python`'s `xml` parser through NextCloud and WebDAV. 

Aiming to keep ***dependencies absolutely minimal*** to easily deploy at multiple Universities and clusters.

### Example usage

`ls` the `ASGReader` directory, and return the contents:

```
./ls_files
```

`ls` the ASGReader/ASG directory, and return the contents:

```
./ls_files ASG
```

### Modifications
* To change the user and passwords passed to NextCloud, modify the `user` variable in `ls_files.sh`

* To change the DAV folder for the NextCloud server, modify the `folder` variable in `ls_files.sh`

### Extensions and plans
* File getter (with support for recursive operations)

* File putter (with support for recursive operations)

* `mkdir` operations on the remote NextCloud server
