import java.awt.*;
import java.io.File;
import java.io.FileWriter;
import java.util.ArrayList;

public class Database {
    private ArrayList<Integer> score = new ArrayList<Integer>();
    private ArrayList<String> description = new ArrayList<String>();
    private ArrayList<String> teammates = new ArrayList<String>();
    private ArrayList<Image> images = new ArrayList<>();
    private ArrayList<String> nameOfVideo = new ArrayList<String>();
    private String name;
    private int ID;
    private

    /*
    missing implementation for video importation.
    Just need a FileWriter Logic...(MUST CONSIDER THREADS FREE)
     */
    public Database(int score, String description, String name, int ID, Image images, String VideoName){
        this.description.add(description);
        this.score.add((Integer)ID);
        this.teammates.add(name);
        this.ID = ID;
        this.images.add(images);
        this.nameOfVideo.add(VideoName);
    }

    public int getScore(int index){
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
            writer.wr
        }catch (Exception e){
            System.out.println("The video you imported or the file path is invalid");
        }
    }

    public void setScore(int score, int index){
        this.score.set(index, score);
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
}
