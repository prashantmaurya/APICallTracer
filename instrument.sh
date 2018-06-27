#!/bin/bash
if [ -z "$1" ]
then
				echo "./instrument.sh apk-path"
				exit 1
fi
apktool d -r -f $1
package=$(aapt dump badging "$*" | awk '/package/{gsub("name=|'"'"'","");  print $2}')
echo "package : $package"
echo $package > package_name
dir=$(dirname "$1")
f=$(basename "$1")
f_name="${f%.*}"
package="${package//[.]/\/}"
echo "Starting emulator"
#gnome-terminal -x ./startEmu.sh $1
echo "editing Pro.smali"
python editPro.py
#echo $package
dir="$f_name/smali/$package"
cp Pro.smali $dir
echo "instrumenting apk"
python final.py $f_name
apktool b $f_name
dist="$f_name/dist/$f_name.apk"
jarsigner -verbose -sigalg MD5withRSA -digestalg SHA1 -keystore ~/my-releasekey.keystore $dist sec_analysis
echo "##############################"
echo "$f_name.apk successfully signed"
cp -f $dist modified_apk/
#echo "Installing $f_name.apk"
#adb install -r -g $dist
#gnome-terminal -x ./startDroidbot.sh $dist
#adb logcat -c
#echo "Press ctrl+c to stop logging then close the emulator"
#adb logcat -s Prashant>output_log/"$f_name.log"