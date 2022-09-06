# cnn_traindata_preperator
Compys Images from a Folder to another , resizes and Greyscale it (Configurable)
And Creates a Label File in .csv Format

CSV Outout Example :
```
folder,label,
prepared_data/pictures/animals\Bear\0.jpg,Bear,
prepared_data/pictures/animals\Bear\1.jpg,Bear,
prepared_data/pictures/animals\Bear\2.jpg,Bear,
prepared_data/pictures/animals\Bear\3.jpg,Bear,
...
```

Usage:

Call Function
```
rename_and_move()
```

Params youn can Adjust :
```
Default :
base_folder='./Pictures/*'
prepared_data_path="prepared_data/pictures/",
copy_testfolder=False,
resize=True, 
height=128, 
width=128, 
greyScale=True  

Meanings :
base_folder='./Pictures/*'                     # The Folder you wish to Copy Data From
prepared_data_path="prepared_data/pictures/"   # The Target Folder for the Prepared Data
copy_testfolder=False                          # If you have Test Data you can Convert it to True/False means the wish to copy or not
resize=True                                    # No Resize only Copy
height=12/                                     # Set the Target Height of the TrainData
width=128                                      # Set the Target Width of the Traindata
greyscale=True                                 # If you wanna GreyScale the Pictures in Target Folder or want the Root Format
```

Examples :
```
# Set the target size to : 256x256 without GreyScale it
rename_and_move(width=256, height=256, greyscale=False)

# Just Copy the Files and Generate the labels.csv
rename_and_move(resize=False, greyscale=False)

# Set the Source path of the Collected Data you wish do Process to your Custom
rename_and_move(base_folder="anyOtherPath")
```
