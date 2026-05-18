import java.util.Scanner;
import java.util.Arrays;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        if (scanner.hasNextInt()) {
            int n = scanner.nextInt();
            int l = scanner.nextInt();
            int[] a = new int[n];
            
            for (int i = 0; i < n; i++) {
                a[i] = scanner.nextInt();
            }

            // Step 1: Sort the array of lantern positions
            Arrays.sort(a);

            // Step 2: Find the maximum gap between adjacent lanterns
            double maxGap = 0;
            for (int i = 0; i < n - 1; i++) {
                if (a[i + 1] - a[i] > maxGap) {
                    maxGap = a[i + 1] - a[i];
                }
            }

            // The radius needed for the inner lanterns is half the max gap
            double ans = maxGap / 2.0;
            
            // Step 3: Handle the edge cases (start and end of the street)
            if (a[0] > ans) {
                ans = a[0];
            }
            if (l - a[n - 1] > ans) {
                ans = l - a[n - 1];
            }

            // Print with high precision to satisfy the problem's strict floating-point requirements
            System.out.printf("%.10f\n", ans);
        }
        scanner.close();
    }
}