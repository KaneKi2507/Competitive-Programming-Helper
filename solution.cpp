#include <iostream>
#include <algorithm>
using namespace std;
int main() {
   int n, l;
   cin >> n >> l;
   int positions[n];
   // Input lantern positions
   for (int i = 0; i < n; i++) {
       cin >> positions[i];
   }
   // Sort positions
   sort(positions, positions + n);
   // Calculate maximum gap
   double maxGap = 0;
   for (int i = 1; i < n; i++) {
       maxGap = max(maxGap, (double)(positions[i] - positions[i - 1]));
   }
   // Consider edges of the street
   double edgeGap = max((double)positions[0], (double)(l - positions[n - 1]));
   // Final radius is max of half maxGap or edgeGap
   double result = max(maxGap / 2.0, edgeGap);
   // Output result with precision
   cout.precision(10);
   cout << fixed << result << endl;
   return 0;
}