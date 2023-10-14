package org.example;

import java.io.*;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Main {
    public static void main(String[] args) {
        try {
            File file = new File("lab1_part2/src/main/resources/mlp_example.txt");
            Scanner reader = new Scanner(file);
            StringBuilder data = new StringBuilder();
            while(reader.hasNextLine()){
                data.append(reader.nextLine());
            }
            Set<String> constants = findConstants(data.toString());
            Set<String> operators = findOperators(data.toString());
            Set<String> keywords = findKeywords(data.toString());
            Set<String> separators = findSeparators(data.toString());
            writeAnalysis(keywords, operators, constants, separators);
        } catch (FileNotFoundException fe) {
            System.out.println("Error: " + fe.getMessage());
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    private static Set<String> findOperators(String data) {
        Pattern OPERATORS_PATTERN = Pattern.compile("(?<![<>=+\\-*\\/]|#include\\s)([+\\-*=\\\\<>]=?|<<|>>|[<>]=)(?![<>=])");
        Matcher matcher = OPERATORS_PATTERN.matcher(data);
        Set<String> operators = new HashSet<>();
        while(matcher.find()){
            operators.add(matcher.group());
        }
        System.out.println("OPERATORS:\n" + operators);
        return operators;
    }

    private static Set<String> findConstants(String data){
        Pattern CONSTANTS_PATTERN = Pattern.compile("[0-9]\\.\\d*|\\d");
        Matcher matcher = CONSTANTS_PATTERN.matcher(data);
        Set<String> constants = new HashSet<>();
        while(matcher.find()){
            constants.add(matcher.group());
        }
        System.out.println("CONSTANTS:\n" + constants);
        return constants;
    }

    private static Set<String> findSeparators(String data){
        Pattern SEPARATORS_PATTERN = Pattern.compile("[,;(){}[\\]:]]");
        Matcher matcher = SEPARATORS_PATTERN.matcher(data);
        Set<String> separators = new HashSet<>();
        while(matcher.find()){
            separators.add(matcher.group());
        }
        System.out.println("SEPARATORS:\n" + separators);
        return separators;
    }

    private static Set<String> findKeywords(String data){
        Pattern KEYWORDS_PATTERN = Pattern.compile("#include|iostream|using|namespace|std|int|main|cin|cout|double|if|while/gm");
        Matcher matcher = KEYWORDS_PATTERN.matcher(data);
        Set<String> keywords = new HashSet<>();
        while(matcher.find()){
            keywords.add(matcher.group());
        }
        System.out.println("KEYWORDS:\n" + keywords);
        return keywords;
    }

    private static void writeAnalysis(Set<String> keywords,Set<String> operators,Set<String> constants,Set<String> separators) throws IOException {
        FileWriter fileWriter = new FileWriter("lab1_part2/src/main/resources/output.txt");
        PrintWriter printWriter = new PrintWriter(fileWriter);
        printWriter.print("KEYWORDS:\n" + keywords + "\n");
        printWriter.print("OPERATORS:\n" + operators + "\n");
        printWriter.print("SEPARATORS:\n" + separators + "\n");
        printWriter.print("CONSTANTS:\n" + constants + "\n");
        printWriter.close();
    }
}