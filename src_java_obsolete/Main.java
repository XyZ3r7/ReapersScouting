import javax.swing.*;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.net.ServerSocket;
import java.time.LocalDate;
import java.util.ArrayList;

/*
    ALL THE System.out.println() ARE ONLY FOR DEBUGGING, FRONTEND DEVELOPER SHOULD IMPLEMENT AND PROCESS ALL THE INTERACTION;
*/
public class Main {
    static void main() throws IOException {

        ArrayList<Database> lists = new ArrayList<>();
        ArrayList<Database> sortedLists = new ArrayList<>();
        System.out.println("This is the basic implementation of scouting application.");



        /**********************************************************************************************/
        try{
            FileReader read = new FileReader("/resources/database.txt");
        }catch (FileNotFoundException e){
            String CreateNewOrNot = JOptionPane.showInputDialog("Press any key to create a new database with data from FTC, press enter to exit");
            if (CreateNewOrNot != null){
                /*
                    This part imports data from FTC API, but I don't have access to it right now
                 */
                /*
                for (int i = 0; i < (API KEY THAT GET THE NUMBER OF TEAMS); i++) {
                    /*
                        imports all of them to database.
                     */
            }

            }
            /*
                Stop JVM to prevent any changes to data, for safety
             */
            System.out.println("Database does not exist, please check the backups");
            System.exit(1);
        /**********************************************************************************************/



        /**************************************************************************************************************************/
        /*
        Start Server, default listening port is 22360
         */
        ServerSocket serverSocket = new ServerSocket(22360);
        Boolean exitTheServer = false;
        while(true){
            /*
                This parts needs to cooperate with front end
             */

            /*
                Returns the data from database based on users' choice
             */

            /*
                Sort the lists of Team based on similarities, from highest to lowest
             */
            if(true){
                sortedLists = lists;
                SortingMethods.mergeSort(sortedLists,0, sortedLists.size() - 1);
            }

            /*
                Detect if user wants to exit the server, normally
             */
            exitTheServer = true;
            if(exitTheServer){
                break;
            }
        }
        /**************************************************************************************************************************/


        /**************************************************************************************************************************/
        /*
            Disable logic
         */
        try{
            FileWriter writerMain = new FileWriter("database.txt");
            FileWriter writer = new FileWriter("database-backup-" + LocalDate.now() + ".txt");
            System.exit(0);
        }catch (IOException e){
            System.out.println("Unknown issue happened, database might not saved, use CTRL + C to exit the program or retry");
        }
        /**************************************************************************************************************************/
    }
}

