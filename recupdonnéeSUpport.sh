echo "Support $1;"
anfr=`cat SUP_SUPPORT.txt | cut -d ";" -f "1 2" | grep "^$1\;" | cut -d ";" -f "2" `
echo "liste num sta anfr :"
echo $anfr
echo $anfr > temporaire.txt
sed "s+ +\n+g" temporaire.txt > sortietemporaire.txt
echo "nombre d'émetteurs : "`cat SUP_EMETTEUR.txt | cut -d ";" -f "3" | grep -c -f sortietemporaire.txt `";"

echo "nombre d'émetteurs interessants : "`cat SUP_EMETTEUR.txt | cut -d ";" -f "2 3" | grep -f sortietemporaire.txt | grep -f triefinal.txt | grep -v "GSM R" | wc -l`";"
cat SUP_EMETTEUR.txt | cut -d ";" -f "2 3" | grep -f sortietemporaire.txt | grep -f triefinal.txt | grep -v "GSM R" | cut -d ";" -f 2 > good.txt
sed "s+ +\n+g" good.txt > goodfinal.txt

echo "liste id antenne interesante : "
for i in `cat SUP_ANTENNE.txt | cut -d ";" -f "1 2 5" | grep -f goodfinal.txt | cut -d ";" -f "2 3" | sort | uniq `
do
    echo $i";"
done
echo "liste id toutes antenne : "
for i in `cat SUP_ANTENNE.txt | cut -d ";" -f "1 2 5" | grep -f sortietemporaire.txt | cut -d ";" -f "2 3" | sort | uniq `
do
    echo $i";"
done

rm temporaire.txt
echo "exploitants : "
for k in  `cat SUP_EMETTEUR.txt | cut -d ";" -f "2 3" | grep -f sortietemporaire.txt | grep -f triefinal.txt | grep -v "GSM R" | cut -d ";" -f 2`
do
    echo `cat SUP_STATION.txt | cut -d ";" -f "1 2" | grep "^$k\;" | cut -d ";" -f 2` >> temporaire.txt
done

for l in `cat temporaire.txt | sort | uniq`
do 
    echo `cat SUP_EXPLOITANT.txt | grep "^$l\;" | cut -d ";" -f 2`
done



if [ `cat temporaire.txt |sort |uniq | wc -l` -eq 1 ]
then
    echo "types d'émetteurs : "
    cat SUP_EMETTEUR.txt | cut -d ";" -f "2 3" | grep -f sortietemporaire.txt | grep -f triefinal.txt | grep -v "GSM R"| sed -e "s/ //g" |  cut -d ";" -f 1  | sort | uniq -c
else
    rm temporaire.txt
    echo "types d'émetteurs : "
    for y in `cat SUP_EMETTEUR.txt | cut -d ";" -f "2 3" | grep -f sortietemporaire.txt | grep -f triefinal.txt | grep -v "GSM R" | sed -e "s/ //g"`
    do
        u=`echo $y | cut -d ";" -f 2`
        m=`cat SUP_STATION.txt | grep "^$u\;" | cut -d ";" -f 2`
        echo `echo $y | cut -d ";" -f 1` `cat SUP_EXPLOITANT.txt | grep "^$m\;" | cut -d ";" -f 2 ` >> temporaire.txt
    done
    cat temporaire.txt | sort | uniq -c
fi

rm temporaire.txt
rm sortietemporaire.txt
rm goodfinal.txt
rm good.txt