#!/bin/bash

# This checks if the number of arguments is correct
# If the number of arguments is incorrect ( $# != 2) print error message and exit
if [[ $# != 2 ]]
then
  echo "backup.sh target_directory_name destination_directory_name"
  exit
fi

# This checks if argument 1 and argument 2 are valid directory paths
if [[ ! -d $1 ]] || [[ ! -d $2 ]]
then
  echo "Invalid directory path provided"
  exit
fi

# [TASK 1]
targetDirectory=$(echo $1)
destinationDirectory=$(echo $2)

# [TASK 2]
echo "target Directory is $targetDirectory"
echo "destinationDirectory is $destinationDirectory"

# [TASK 3]
currentTS=$(date +%s)

# [TASK 4]
backupFileName="backup-$currentTS.tar.gz"
echo "backup file name is $backupFileName"

# We're going to:
  # 1: Go into the target directory
  # 2: Create the backup file
  # 3: Move the backup file to the destination directory

# To make things easier, we will define some useful variables...

# [TASK 5]
origAbsPath=$(pwd)

# [TASK 6]
# Go the target directory and get the path via pwd
cd $destinationDirectory
destDirAbsPath=$(pwd)
#
# alternative way I've done it instead work this way:
# we know that destinationDirectory is a directory (based on the parameters checks )
# it can be either absolute or relative
#  - if it is absolute (i.e. starts with /), then I just set destDirAbsPath to the same value
#  - if it is relative I just add the current path
#if [[ "$destinationDirectory" = /* ]]; then
#  destDirAbsPath=$(echo $destinationDirectory)
#else
#  destDirAbsPath=$(echo "$origAbsPath/$destinationDirectory")
#fi  
echo "Abs path for dest directory is: $destDirAbsPath"

# [TASK 7]
#
# because I moved from the original path, we can't point directly to targetDirectory 
# that supposedely is a relative path
cd $origAbsPath
cd $targetDirectory

# [TASK 8]
#yesterdayTS=$(date --date="yesterday" +%s)
# he does it differently as a math operation
yesterdayTS=$(($currentTS - 24*3600))

##
## This declares an empty array
## remember you can appen values via myArray+=($myVariable)
## echo ${myArray[@]}  to print all the values
declare -a toBackup

for file in $(ls) # [TASK 9]
do
  # [TASK 10]
  file_timestamp=$(date -r $file +%s)
  if (($file_timestamp > $yesterdayTS))
  then
    toBackup+=($file)
  fi
done
echo "Files to backup: ${toBackup[@]}"
# [TASK 12]
tar -czvf $backupFileName ${toBackup[@]}
# [TASK 13]
mv $backupFileName $destDirAbsPath

# Congratulations! You completed the final project for this course!
