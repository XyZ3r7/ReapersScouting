import ai.djl.Application;
import ai.djl.inference.Predictor;
import ai.djl.repository.zoo.Criteria;
import ai.djl.repository.zoo.ZooModel;
import ai.djl.training.util.ProgressBar;

public class DeepLearningMethods {
    public static double compare(String mainText, String compareText){
        try (ZooModel<String, float[]> model = loadModel();
             Predictor<String, float[]> predictor = model.newPredictor()) {

            float[] v1 = predictor.predict(mainText);
            float[] v2 = predictor.predict(compareText);

            return cosineSimilarity(v1, v2);
        } catch (Exception e) {
            /*
             Main.java must respond to this -1 and prompt user that there's a issue with model
             */
            return -1;
        }
    }

    private static ZooModel<String, float[]> loadModel() throws Exception {
        Criteria<String, float[]> criteria = Criteria.builder()
                .setTypes(String.class, float[].class)
                .optApplication(Application.NLP.TEXT_EMBEDDING)
                .optModelUrls("djl://ai.djl.huggingface/sentence-transformers/all-MiniLM-L6-v2")
                .optProgress(new ProgressBar())
                .build();
        return criteria.loadModel();
    }

    private static double cosineSimilarity(float[] a, float[] b) {
        double dot = 0.0, na = 0.0, nb = 0.0;
        for (int i = 0; i < a.length; i++) {
            dot += a[i] * b[i];
            na += a[i] * a[i];
            nb += b[i] * b[i];
        }
        return dot / (Math.sqrt(na) * Math.sqrt(nb) + 1e-12);
    }
}