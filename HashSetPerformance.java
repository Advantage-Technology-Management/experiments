
import java.util.HashSet;
import java.util.Random;

public class HashSetPerformance {
    public static void main(String[] args) {
        // Create a HashSet to store random strings
        HashSet<String> stringHashSet = new HashSet<>();

        // Generate 10000 random strings and add them to the HashSet
        Random random = new Random();
        for (int i = 0; i < 10000; i++) {
            String randomString = generateRandomString();
            stringHashSet.add(randomString);
            // Add one controlled string that will be known to be found
            stringHashSet.add("TestString");
        }

        // Choose a random string to search in the HashSet, not likely to be found
        String searchString = generateRandomString();

        // Measure the time taken to check if the string exists in the HashSet
        long startTime = System.nanoTime();
        boolean exists = stringHashSet.contains(searchString);
        long endTime = System.nanoTime();
        long duration = (endTime - startTime) ; // Convert nanoseconds to milliseconds

        System.out.println("String '" + searchString + "' exists in HashSet: " + exists);
        System.out.println("Time taken to search: " + duration + " nanoseconds");

        
        // Measure the time taken to check if the known TestString exists in the HashSet
        startTime = System.nanoTime();
        exists = stringHashSet.contains("TestString");
        endTime = System.nanoTime();
        duration = (endTime - startTime) ; // Convert nanoseconds to milliseconds

        System.out.println("String TestString exists in HashSet: " + exists);
        System.out.println("Time taken to search: " + duration + " nanoseconds");

    }

    // Method to generate a random string of 10 characters
    private static String generateRandomString() {
        int leftLimit = 97; // letter 'a'
        int rightLimit = 122; // letter 'z'
        int targetStringLength = 10;
        Random random = new Random();

        String generatedString = random.ints(leftLimit, rightLimit + 1)
          .limit(targetStringLength)
          .collect(StringBuilder::new, StringBuilder::appendCodePoint, StringBuilder::append)
          .toString();

        return generatedString;
    }
}
