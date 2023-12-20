#!/bin/bash
#

location="Casablanca"
file_path="/home/vale6811/Desktop/Coursera/Introduction_to_bash_Scripting/temperatures.csv"
#
# on the website the date is identified by this format: Mon 18 Dec
# in our file instead we want the format as year(NNNN), month(mm), day(d),
# in the exercise, thi is done like this:
# TZ='Morocco/Casablanca'
# hour=$(TZ='Morocco/Casablanca' date -u +%H) 
# day=$(TZ='Morocco/Casablanca' date -u +%d) 
# month=$(TZ='Morocco/Casablanca' date +%m)
# year=$(TZ='Morocco/Casablanca' date +%Y)
today_date=$(date "+%a %d %b")city
tomorrow_date=$(date --date="tomorrow" "+%a %d %b")
file_date=$(date "+%Y,%m,%d")
#
# redirecting the stderr to stdout with 2>&1
# Note in the exercise they write to a file
# curl -s wttr.in/$city?T --output weather_report
# Format can be changed, see https://github.com/chubin/wttr.in#one-line-output
# $ curl wttr.in/Casablanca?format=3
#  Casablanca: ☀️   +17°C
# Using $T to get text mode back and not ansi
web_content=$(curl "wttr.in/$location?T" 2>&1)

# note
# tr -dc "[0-9]"
# the option -d is for delete
# the option -c is for complement of the first set1 (only set in this case as we do a delete)
# so the result deletes all the numbers
# this works by:
# - looking for a line with the date and getting 4 lines after (that's where the temp is)
# - getting only the last of the 4 lines
# - splitting the line around any capital C (for celsius)
# - getting the field for noon (f2)
# - removing any nont digit character
# in the exercise, they do it like this:
#  note: 
#  for today temp they actually get the live data, and not the value under the Date of today
#
#  obs_temp=$(curl -s wttr.in/$city?T | grep -m 1 '°.' | grep -Eo -e '-?[[:digit:]].*')
#  fc_temp=$(curl -s wttr.in/$city?T | head -23 | tail -1 | grep '°.' | cut -d 'C' -f2 | grep -Eo -e '-?[[:digit:]].*')
today_noon=$(echo "$web_content" | grep  "$today_date" -A4 | tail -n1 | cut -d"C" -f2 | tr -dc "[0-9]")
tomorrow_noon=$(echo "$web_content" | grep  "$tomorrow_date" -A4 | tail -n1 | cut -d"C" -f2 | tr -dc "[0-9]")
echo "$today_date - Location $location ,temperature at noon is $today_noon"
echo "$tomorrow_date - Location $location ,forecast at noon is $tomorrow_noon"
#
# in the exercise they do it like this
# record=$(echo -e "$year\t$month\t$day\t$obs_temp\t$fc_temp C")
# echo $record>>rx_poc.log  <- the file is called rx_poc.sh
echo "Now recording to temperatures.txt in format year(NNNN), month(mm), day(d), today_temperature, tomorrow_forecast"
echo "$file_date,$today_noon,$tomorrow_noon >> $file_path" 
echo "$file_date,$today_noon,$tomorrow_noon" >> $(echo "$file_path")


