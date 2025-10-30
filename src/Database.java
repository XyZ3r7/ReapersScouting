public class Database {
    private int score;
    private String description;
    private String name;
    private int ID;
    /*
    missing implementation for video importation.
    Just need a FileWriter Logic...(MUST CONSIDER THREADS FREE)
     */

    public Database(int score, String description, String name, int ID){
        this.score = score;
        this.description = description;
        this.name = name;
        this.ID = ID;
    }

    public int getScore(){
        return score;
    }

    public String getDescription(){
        return description;
    }

    public String getName(){
        return name;
    }

    public int ID(){
        return ID;
    }

    public void setScore(int score){
        this.score = score;
    }

    public void setDescription(String description){
        this.description = description;
    }

    public void setName(String name){
        this.name = name;
    }

    public void setID(int ID){
        this.ID = ID;
    }
}
