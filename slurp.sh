for i in $(seq 1 13000); do
  echo $i
  curl -o pages/$i.html "https://gis.vgsi.com/somervillema/Parcel.aspx?Pid=$i" -sS
  sleep 0.1
done
