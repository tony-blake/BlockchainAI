# BlockchainAI - Data Extraction


Downloading the Blockchain
--------------------------

* open up Bash terminal

* run ```geth --syncmode "fast" cache=4096```

Extracting the Data
-------------------

* open up second Bash terminal

* Navigate to your working directory. (For example ```cd /Users/your_user_name/Desktop/WorkingDir```)
  or if on the bash terminal in windows ```cd /mnt/c/Users/your_user_name/Desktop/WorkingDir```

* Navigate to BlockchainAI directory ```cd BlockchainAI/BlockchainPart```

* run ```sudo geth --cache=4096 --exec 'loadScript("usersTransactions.js"); getTransactionsByAccount("*",4391479,4476560)' attach > From439to447AllTheJSONs.txt```

In our case extracting the relevant information in all blocks between 4391479 and 4476560 resulted in the limit of what we could import into R for data analysis and for training the AI. Of course if one had the requsite hardware (multi-thread processing or MPI) and memory capacity and one could just extract all of the blockchain data (upto and including 4476560) into a single textfile by using the following command.

```sudo geth --cache=4096 --exec 'loadScript("usersTransactions.js"); getTransactionsByAccount("*", 1, 4476560)' attach > AllTheJSONs.txt``` 


Converting the key-value pair data into CSV form
-------------------------------------------------

run the following series of commands (Also if you are using macOS install gsed)

```bash

#insert blank line between each set transaction information
sed '/input           : 0x/{G;}' AllTheJSONS.txt > AllTheJSONSspace.txt

#Use split.awk file to turn key-value pair format into csv format
awk -f split.awk AllTheJSONSspace2.txt > AllTheJSONS.csv

#If a new line is created for every comma separated value use the following command to move all transaction info onto single line
awk -v RS="" -F'\n' -v OFS=, '{$1=$1} 1' AllTheJSONS.csv | sed -r 's/ +([[:digit:]-]+)$/, \1/' > AllTheJSONS2.csv

#get rid of blank space between commas
gsed 's/,,/,/g' AllTheJSONS2.csv > AllTheJSONS3.csv 
``` 


