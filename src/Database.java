import java.awt.*;
import java.io.File;
import java.io.FileWriter;
import java.util.ArrayList;

public class Database {
    private ArrayList<Double> score = new ArrayList<Double>();
    private ArrayList<String> description = new ArrayList<String>();
    private ArrayList<String> teammates = new ArrayList<String>();
    private ArrayList<Image> images = new ArrayList<>();
    private ArrayList<String> nameOfVideo = new ArrayList<String>();
    private ArrayList<String> Mactches = new ArrayList<String>();
    private String name;
    private int ID;
    private double highestScore;

    /*
    missing implementation for video importation.
    Just need a FileWriter Logic...(MUST CONSIDER THREADS FREE)
     */
    public Database(double score, ArrayList<String> description, String name, int ID, ArrayList<Image> images, ArrayList<String> VideoName, ArrayList<String> teammates, ArrayList<String> Matches){
        try{
            this.name = name;
            this.description = description;
            this.score.add(score);
            this.teammates = teammates;
            this.ID = ID;
            this.images = images;
            this.nameOfVideo = VideoName;
            this.Mactches = Matches;
            this.highestScore = score;
        } catch (ClassCastException e) {
            System.out.println("I want to kill people who can't pass correct type of data");
        }
    }

    public double getScore(int index){
        try{

        } catch (Exception e) {
            System.out.println("The index you were asking does not exists.");
        }
        return score.get(index);
    }

    public String getDescription(int index){
        return this.description.get(index);
    }

    public String getName(){
        return name;
    }

    public int ID(){
        return ID;
    }

    public void saveVideos(String FileName){
        try{
            FileWriter writer = new FileWriter(FileName);
        }catch (Exception e){
            System.out.println("The video you imported or the file path is invalid");
        }
    }

    public void setScore(double score, int index){
        this.score.set(index, Double.valueOf(score));
        if (score >= highestScore){
            highestScore = score;
        }
    }

    public void setDescription(String description, int index){
        this.description.set(index, description);
    }

    public void setName(String name){
        this.name = name;
    }

    public void setID(int ID){
        this.ID = ID;
    }

    public void setTeammates(int index, String teammateNames){
        teammates.set(index, teammateNames);
    }

    public String getMatches(int index){
        return Mactches.get(index);
    }

    public double getHighestScore(){
        return highestScore;
    }
}
