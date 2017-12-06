BEGIN {
RS="\n\n";
FS="\n";
ORS=",";
}

{
    for (i=1;i<=NF;i++)
    {
        split($i, sf, "= ")
        print sf[2]
    }
    printf "\n"
 }

