import java.io.*;
import java.util.*;
import java.text.*;
import java.math.*;
import java.util.regex.*;
import static java.util.regex.Pattern.*;
import static java.util.regex.Matcher.*;
import static java.math.BigInteger.*;
import static java.lang.System.*;
import static java.lang.Integer.*;
import static java.lang.Double.*;
import static java.util.Collections.*;
import static java.lang.Math.*;
import static java.util.Arrays.*;


public class Solution {

    private Set<String> dictionary;
    private Map<String, List<String>> map;
    
    public Solution() throws IOException {
        this.dictionary = buildDictionary();
        this.map = new HashMap<>();
    }
    
    public static void main(String... args) throws Exception {
        Solution solution = new Solution();
        for(int index = 1; index <= 6; index++)
            solution.testFile("test" + index + ".txt");
        
    }
    
    public void testFile(String filename) throws IOException {
        Scanner scanner = new Scanner(new File(filename));
        String rawString = scanner.nextLine();
        
        findK(rawString);
        
    }
    
    public Set<String> buildDictionary()  throws IOException {
        Scanner scanner = new Scanner(new File("dictionary.txt"));
        Set<String> dictionary = new HashSet<>();
        while(scanner.hasNextLine()) {
            dictionary.add(scanner.nextLine());
        }
        
        return dictionary;
    }
    
    
    
    public void findK(String rawString) {
        for(int k = 0; k < 26; k++) {
            String reversed = reverseShift(rawString, k);
            List<String> output = breaksInDictionary(reversed);
            if(output != null) {
                System.out.printf("K: %d: Words: %s\n", k, output.toString());
                return;
            }
        }
        
        System.out.printf("No Solution!\n");
        
    }
    
    public String reverseShift(String raw, int k) {
        char[] output = new char[raw.length()];
        
        for(int index = 0; index < raw.length(); index++) {
            int letterValue = raw.charAt(index) - 'a';
            letterValue -= k;
            if(letterValue < 0) letterValue += 26;
            output[index] = (char)(letterValue + 'a');
        }
        
        return new String(output);
    }
    
    public List<String> breaksInDictionary(String sentence) {
        if(sentence.length() == 0) {
            return new LinkedList<>();
        }
        
        if(map.containsKey(sentence)) {
            return map.get(sentence);
        }
        
        for(int size = sentence.length(); size > 0; size--) {
            String prefix = sentence.substring(0, size);
            if(dictionary.contains(prefix)) {
                List<String> found = breaksInDictionary(sentence.substring(size));
                if(found != null) {
                    found.add(0, prefix);
                    map.put(sentence, found);
                    return found;
                }
            }
        }
        
        map.put(sentence, null);
        return null;
    }
}