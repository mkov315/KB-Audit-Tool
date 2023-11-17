# -*- coding: utf-8 -*-
"""
Spyder Editor

Mary Kate O'Leary - Wayne State University MLIS '23
Cleveland State University Practicum Student
Fall 2023

Knowledge Base Audit Tool
This tool is compatible with EBSCO's Holding Management package export
and its purpose is twofold:
    1. Output the unique package list (something EBSCO exports currently does not support)
    2. Distill the export into a document only including relevant data so that the file side is manageable in Excel (currently the exports are too large for Excel to support).

The fields chosen in this program are PackageName, PackageID, VendorName, VendorID, PackageType, IsCustom, HideOnPublicationFinder, and HideOnFullTextFinder.

This tool will be used to aid in the CSU holdings audit process, but can be generalized for library institutions elsewhere.
"""

# First, we import the pandas package
import pandas as pd

# This is the open access extract from Cleveland State's EBSCO holdings
# For wider use, this file name will be changed to your institution's EBSCO export file name
myfile = 'CSU_open_access_export.csv'

# Next, we use the pandas read_csv function to import the large export file as a dataframe called df
# Setting the low_memory parameter to False prevents mixed type interference with such a large file

df = pd.read_csv(myfile, index_col=False, on_bad_lines='warn', low_memory=False)

# The relevant columns are selected as a subset of the full dataframe
df = df[["PackageName", "PackageID", "VendorName", "VendorID", "PackageType", "IsCustom", "HideOnPublicationFinder", "HideOnFullTextFinder" ]]

# Then we compute the number of titles in each package in a separate dataframe called df_title
# The new column added here is called TitleCount
df_title = df.value_counts("PackageID").rename_axis('PackageID').reset_index(name='TitleCount')

# Now we take the original dataframe and drop any rows that have duplicate PackageIDs
# This gives us our unique list of packages. 
df = df.drop_duplicates(['PackageID'], ignore_index=True)

# Finally we join the two created dataframes on the PackageID
# The result has unique packages only and has the TitleCount appended as a new column
df_final = df.join(df_title.set_index('PackageID'), on='PackageID')

# The resulting df_final dataframe is then exported as a csv called "KB_Output.csv"
# It will be saved in the same folder where the .py file is kept
df_final.to_csv('KB_Output.csv')
