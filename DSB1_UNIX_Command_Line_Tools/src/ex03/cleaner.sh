#!/bin/sh

awk '
BEGIN {
  FPAT = "([^,]+)|(\"([^\"]|\"\")*\")"
}
NR==1 { print; next } 
{
  name=$3
  result=""

  if (name ~ /Junior/) {
    result = (result=="" ? "Junior" : result"/Junior")
  }
  if (name ~ /Middle/) {
    result = (result=="" ? "Middle" : result"/Middle")
  }
  if (name ~ /Senior/) {
    result = (result=="" ? "Senior" : result"/Senior")
  }

  if (result=="") {
    result="-"
  }

  $3="\"" result "\""   
  print $1 "," $2 "," $3 "," $4 "," $5
}' ../ex02/hh_sorted.csv > hh_positions.csv


