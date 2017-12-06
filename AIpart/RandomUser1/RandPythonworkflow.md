Introduction
===========

This workflow describes how to input the datasets, preprocess the data, set up the deep learning modules in python and read the results back into R for further processing and plotting.

Requirements
------------

We assume basic knowledge of R and RStudio. For those whose first time it is encountering R and RStudio we recommend going through the tutorials on Datacamp and http://tryr.codeschool.com


For this particular workflow the dataset has been extracted from the Ethereum Blockchain and is all of a users transactions (Random User 5) from block 4085615 to 4514465. The file is called 0x0ff24158220a14398f047a80a513617ddc4f5289(From _Block_4085615_To_Block_4514465).csv

There are several packages that may need to be installed. For example if the ggplot2 package needs to be installed use `install.packages('ggplot2')`.


### Load needed packages


```{r Initial - version}
library(reshape)
library(ggplot2)
library(scales)

```

### Read in the data, extract, normalise and write to file
```{r Initial - version}
options(digits = 22, scipen = 999) # suppresses scientific notaion and reads up to 22 digits

jammers2<- read.csv("0x0ff24158220a14398f047a80a513617ddc4f5289(From _Block_4085615_To_Block_4514465).csv", numerals = "no.loss")
jammers2value <- jammers2[,c(9)] # extract single column of ether price values
jammers2value <- data.frame(jammers2value) # change to dataframe
jammers2value$jammers2value <- as.numeric(as.character(jammers2value$jammers2value)) # format values to numeric
siraj <- (jammers2value$jammers2value/5000000000000000000)-1 # Normalise values
siraj <- data.frame(siraj)
write.csv(siraj, file="siraj.csv", row.names = F) # write to file
```

Open up a bash terminal, navigate to working directory and run the following commands to remove header and quotation marks

```bash
tail -n +2 siraj.csv > siraj.tmp && mv siraj.tmp siraj.csv
sed 's/"//g' -i siraj.csv
```

Run LSTM python module on preprocessed dataset
==============================================

In the same bash terminal as previously opened run the following command

```bash 

python betterrun.py

```

The loading, training, prediction and output process should take around 10 minutes. When complete a file of predictions for the test set will have been generated. The is file is called ```betterPreditions2.csv```. The true values of the testset are in the file called ```ytest.csv```.



Further data processing and ploting of predictions versus true values
=====================================================================


```{r Initial - version}
#read in the predictions file

db <- read.csv('betterPreditions2.csv', header = F,
               colClasses=c("numeric", "numeric", "numeric", "numeric", "numeric","numeric", "numeric", "numeric", "numeric", "numeric",
                            "numeric", "numeric", "numeric", "numeric", "numeric","numeric", "numeric", "numeric", "numeric", "numeric",
                            "numeric", "numeric", "numeric", "numeric", "numeric","numeric", "numeric", "numeric", "numeric", "numeric",
                            "numeric", "numeric", "numeric", "numeric", "numeric","numeric", "numeric", "numeric", "numeric", "numeric",
                            "numeric", "numeric", "numeric", "numeric", "numeric","numeric", "numeric", "numeric", "numeric", "numeric"))

# The predictions file is organised in matrix form where the columns are the sequence of points predicted at 50 timestep intervals. To match up these points with the true values in the test set the following commands in R need to executed.

tmp1db <- melt(predtranspdb, id.vars = 1)
y_testdb <- read.csv('ytest.csv', header = F,
                     colClasses=c("numeric"))
y_testdb <- y_testdb[,c(2)]
y_testdb <- data.frame(y_testdb)
ytestcutdb <- y_testdb[1:950,]
ytestcutdb <- data.frame(ytestcutdb)
tmp2db <- cbind(tmp1db,ytestcutdb)
tmp3db <- tmp2db[,c(2,3,4)]
colnames(tmp3db) <- c("TIME", "PREDICTION", "YTEST")
tmp3db$timestep <- 1:nrow(tmp3db)
dataset2db <- tmp3db[,c(4,2,3)]

# To plot the resulting table (dataset2b) run the following the commamnds in R

dataset3db <- melt(dataset2db, id.vars = 1)
deNorm <- 27670473370000000000*(1 + dataset3db$value) # Denormalises data
denormed <- deNorm/1000000000000000000 # Change to ether value units
dataset4 <- cbind(dataset3db, denormed)
colnames(dataset4) <- c("timestep", "variable", "value", "Ether_Price_Value")
dataset5 <- dataset4[dataset4$Ether_Price_Value < 40,]
dataset6 <- dataset5[dataset5$Ether_Price_Value > 15,]
pdf(file="lstm13.pdf",paper="A4r",width=16, height=8.5, onefile = FALSE,useDingbats = FALSE)
ggplot(dataset6, aes(x = timestep, y = Ether_Price_Value, group=variable, col=variable)) + 
  geom_point(size=1) +
  geom_smooth() +
  theme(axis.text=element_text(angle = 0,size=10),
        axis.title=element_text(size=15,face="bold"),legend.text=element_text(size = 20), legend.title=element_text(size=10,face="bold")) +
  ggtitle("predictions vs test set")
dev.off()  
``` 


# Statistical Analysis

dataset9 <- dataset4[1:950,]
dataset10 <- dataset4[951:1900,]
smooth_vals3 = predict(loess(Ether_Price_Value~timestep,dataset9), dataset9$timestep)
smooth_vals3 <- data.frame(smooth_vals3)
smooth_vals4 = predict(loess(Ether_Price_Value~timestep,dataset10), dataset10$timestep)
smooth_vals4 <- data.frame(smooth_vals4)
diffpredtrue <- smooth_vals - smooth_vals2
mean(smooth_vals3$smooth_vals3) - mean(smooth_vals4$smooth_vals4)
median(smooth_vals3$smooth_vals3) - median(smooth_vals4$smooth_vals4)
summary(dataset4$Ether_Price_Value)
grangertest(dataset10$Ether_Price_Value, dataset9$Ether_Price_Value, 50)
