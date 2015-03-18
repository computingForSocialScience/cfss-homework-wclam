Census Project, Explanations, and Instructions

Well then, this project was rather ambitious.
Had it worked properly, the goal was to use the data to help draw some conclusions about the situation of minorities and second language learners.  The tables we used are below.

B01001. Sex by Age
B02001. Race
B16008. Citizenship Status by Age by Language Spoken At Home for the Population 5+ Yrs 
B16009. Poverty Status in the Past 12 Months by Age by Language Spoken At Home for the Population 5+ Yrs 
B16010. Educational Attainment and Employment Status by Language Spoken At Home for the Population 25 Years and Over 
B99163. Imputation of Ability to Speak English for the Population 5 Years and Over 


Start by running downloadscript.py
This script (intends to) identify and gather specific information and data from specific questions asked on the census for every state given its own FIPS code.
It creates two different lists, one specified as "table_info" and another as "table_data".
The two lists are then combined into a MySQL table, where they can be manipulated and compared.

Of course, we ran into our share of issues that did not allow us to get past populating the MySQL table.  Many of the issues arose were a result not of our own fault, but of the public data that we accessed.
The initial issue that we ran into that stopped us was the collection of the data.  The code was gathering properly when we had printed individual parts, as well as putting it all together, but when it came time to append that big collection of data to a dictionary, the data became incorrectly formatted.  We found a way around the problem by simply omitting the append to the dictionary for both "table_info" and "table_data".  Returning the tuple list instead of the dictionary correctly formatted the data.
With the bypassed .append line, I was able to populate a MySQL table with the table_info, which was good progress, I suppose.
The issue that we have since have come across is that the table_data takes far too long to scrape the data we have programmed it to collect.  Often, the connection is aborted before the scraping is completed due to timeout restraints.

Without concrete data, it is impossible to populate the MySQL table, making everything after this point a theoretical process.
The next step would be to run application.py
The code is a skeleton of what it should be, due to the lack of ability to do trial and error and seeing how the data would actually look like.  It would be guesswork to try and find out which variable would go where in the code that scatterplots and tables.  For that reason, there are a lot of gaps in between where the code is and where it should be.  Also, it is challenging to guess how the variables would be called and how they would be manipulated into dataframes for pandas and bokeh.  As a result, the html files in the templates folder are pretty bare as well.

I have been working through the issues that have come up in the TA sessions and outside of them, but time is not on my side, and I must stop.  You guys were really really helpful the whole way, and I'm disappointed that there isn't very much to show for that help.

-Cuyler Lam