import java.util.ArrayList;

public class SortingMethods {
    public static void mergeSort(ArrayList<Database> list, int left, int right) {
        if (left < right) {
            int mid = (left + right) / 2;
            mergeSort(list, left, mid);
            mergeSort(list, mid + 1, right);
            merge(list, left, mid, right);
        }
    }

    public static void merge(ArrayList<Database> list, int left, int mid, int right) {
        ArrayList<Database> leftList = new ArrayList<>();
        ArrayList<Database> rightList = new ArrayList<>();

        for (int i = left; i <= mid; i++) {
            leftList.add(list.get(i));
        }
        for (int i = mid + 1; i <= right; i++) {
            rightList.add(list.get(i));
        }

        int i = 0, j = 0, k = left;

        while (i < leftList.size() && j < rightList.size()) {
            if (leftList.get(i).getHighestScore() >= rightList.get(j).getHighestScore()) {
                list.set(k, leftList.get(i));
                i++;
            } else {
                list.set(k, rightList.get(j));
                j++;
            }
            k++;
        }

        while (i < leftList.size()) {
            list.set(k, leftList.get(i));
            i++;
            k++;
        }

        while (j < rightList.size()) {
            list.set(k, rightList.get(j));
            j++;
            k++;
        }
    }
}
