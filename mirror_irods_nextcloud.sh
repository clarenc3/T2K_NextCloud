#!/bin/bash

### README
#
# Download QMUL iRODS directory to local, and the upload to KCL NextCloud, removing the file from local once it's uploaded. Runs file by file, directory by directory, and maintains the directory structure.
#
# DOES NOT maintain timestamps of files on QMUL iRODS
#
# Requires QMUL iRODS to be set up and able to read directories
# Uses the "icd" and "ils" in your PATH; be sure they exist
#
### END OF README

# QMUL irods directory to back up
irods_dir="/QMULZone1/home/asg/asg2019oa"

# The directory we're on at iRODS
dir=""
# The local directory
local_dir=""
# Counter of how many uploads we've done
counter=0
# Max number of uploads: mostly for debugging to check 10 files etc work
maxcount=999999999999999999999999999999

# NextCloud user and password
user="clarencewret:8nCAi-rDcMy-Lut9D-2G3JA-PjMZe"
# NextCloud upload directory
nextcloud_dir="https://nextcloud.nms.kcl.ac.uk/remote.php/dav/files/${user%%:*}/ASG/asg_backup"

# Number of threads to use to download from iRODS
irods_threads=8

# Make the backup directories
curl -u ${user} -X MKCOL ${nextcloud_dir}
curl -u ${user} -X MKCOL ${nextcloud_dir}/asg

icd ${irods_dir}
echo "Operating in irods directory ${irods_dir}..."
# Where we're running this script
homepath=$(pwd -P)

# ls recursively on iRODS and run through every single file
for i in $(ils -r); do

  # Check we haven't uploaded more files than requestsed
  if [[ ${counter} -ge ${maxcount} ]]; then
    echo "Ran ${maxcount}, exiting"
    break;
  fi

  # If we find a backslash and ":" we're in a directory
  # Make the directory structure locally
  # Strip out sub-directories
  if [[ $i == "C-" ]]; then
    continue;
  fi

  # If we've found a sub directory, make it locally and on NextCloud
  if [[ $i == "${irods_dir}"*":" ]]; then
    dir=${i%%:}

    echo -e "\n\n"
    echo "Found Remote Directory: $dir"
    # cd back into the top dir to make the path
    cd ${homepath}

    # Make a new local directory where we put the file
    local_dir=${dir#*home/}
    echo "Making Local Directory: ${local_dir}..."
    mkdir -pv ${local_dir}
    cd ${local_dir}
    echo "In $(pwd -P)"

    # Make directory on the remote NextCloud reflecting the iRODS dir
    echo "Making directory ${nextcloud_dir}/${local_dir} on remote..."
    curl -u ${user} -X MKCOL ${nextcloud_dir}/${local_dir}
    echo -e "Now putting files...\n"
    
  # C- is for collection on irods, strip these out
  elif [[ $i != *"C- ${irods_dir}"* ]]; then

    # Skip dirs which trail the collection but due to the loop comes on its own
    if [[ $i == *"${irods_dir}"* ]]; then
      continue;
    fi

    # Check if the file already exists on the remote
    return=$(curl -u ${user} --silent -X PROPFIND ${nextcloud_dir}/${local_dir}/${i} | tr '\n' ' ' | grep -c 'getcontentlength')
    # If there's at least one match, means there's a file with non-zero size and the same name on the remote
    if [[ $return -ge 1 ]]; then
      echo "Already found file ${i} on remote ${nextcloud_dir}/${local_dir}/${i}"
      echo "Skipping..."
      continue;
    fi

    counter=$((${counter}+1))
    echo "Making transfer #${counter}..."

    # Get the file
    echo "Putting remote ${dir}/${i} to local ${local_dir}/${i}"
    # Run on user specified number of threads
    iget -v -N ${irods_threads} ${dir}/${i}

    # Then put on NextCloud through curl
    echo "Putting ${local_dir}/${i} onto NextCloud ${nextcloud_dir}/${local_dir}..."
    curl -u ${user} -T ${i} ${nextcloud_dir}/${local_dir}/

    # Remove the local file to avoid filling up the local host
    echo "Removing ${i} locally..."
    rm -fv ${i}
    echo -e "\n"
  fi
done

echo "Uploaded ${counter} files"
