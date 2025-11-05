### Main.java
*  [ ]  Reads Database: if database does not exists, use API key to fetch Data from FTC
*  [x]  Starts Server (Sockets) 
* [ ]  Write out when making changes
* [ ] Returns the data from database based on users' choice
* [ ] Check if user wants to sort the data && return a list of data
* [ ] Find a way to store database into file
* [ ] Read the database

### SortingMethods.java
* ##### public static void mergeSort(ArrayList\<Database\> list, int left, int right)
	* Main function of _**MERGE SORT**_, it sorts the Teams based on their highest similarities score, _***FROM HIGHEST TO LOWEST**_

* ##### public static void merge(ArrayList\<Database\> list, int left, int mid, int right)
	* Helper method of mergeSort(). Again, just for mergeSort

### DeepLearningMethods
* ##### public static double compare(String mainText, String compareText)
	* It returns the similarities score based on mainText(The text that describe our robot) and compareText(The Text that we are comparing to)
* ##### private static ZooModel\<String, float\[]\> loadModel() throws Exception
	* Helper methods for **public static double compare(String mainText, String compareText)**, it loads the Machine Learning model.
*  ##### private static double cosineSimilarity(float\[] a, float[] b)
	* Helper methods for **public static double compare(String mainText, String compareText**, it calculates the result of dot product and divide by the magnitude of two vectors in order to compare their cosine similarities and get similarities score.
	
* ### Database.java
* #### It is the data base that score the team information.

* ##### public Database(double score, ArrayList\<String\> description, ArrayList\<String\> name, int ID, ArrayList\<Image\> images, ArrayList\<String> VideoName, ArrayList\<String> teammates, ArrayList\<String> Matches)
	* The constructor of Database, it stores the score, list of description, ID, photos, The path of the Video records, name of teammates and Matches
	* [ ] Do we need Video records? It's stressful for the compute stick.
	* [ ] Do we need different descriptions or not

* ##### public double getScore(int index)
	* It gets score from specific match. 
	* [ ] I can create a version where index binds everything. This might make programmers has easier life. 

* ##### public String getDescription(int index)
	* It gets the specific Descriptions based on index.

* ##### public String getName()
	* Returns team name

* ##### public int ID()
	* Returns ID of the team

* ##### public void saveVideos(String fileName)
	* [ ] Incomplete, I promise the Intel Compute Stick won't be able to play any videos above 1080p fluently.
	* It saves the Video files to where **fileName** point to.

* ##### public void setScore(double score, int index)
	* It changes the similarities score. 
	* If the score is higher than previous highest score, then the score in parameter will become next highest score.

* ##### _***(Most likely will be deprecated)**_ public void setName(String name)
	* It changes the name of team

* ##### _***(Most likely will be deprecated)**_ public void setID(int ID)
	* It changes the ID of the name

* ##### _***(Most likely will be deprecated)**_ public void setTeammates(int index, String teammateNames)
	* It changes the teammates on where the index at.

* ##### public String getMatches(int index)
	* It gets the information of the specifics Matches

* ##### pbulic double getHighestScore()
	* It returns the highest similarities score (compare to the team)
	* _***REMINDER: THE MAIN TEAM IS NOT SPECIFIC, PROGRAMMERS MUST STATE WHAT TEAM ARE THEY COMPARING TO AND WHAT ARE THEIR MAIN TEAM**_