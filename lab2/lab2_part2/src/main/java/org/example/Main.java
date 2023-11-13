package org.example;

import org.example.automaton.ConstAF;
import org.example.automaton.FloatAF;
import org.example.automaton.IdAF;
import org.example.symbol_table.ConstTS;
import org.example.symbol_table.IdentifierTS;
import org.example.utils.HashTable;
import org.example.utils.Position;

import java.io.*;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Main {
    private static List<FIP> fip;
    private static IdentifierTS identifierTS;
    private static ConstTS constTS;
    private static HashTable<String> atoms;
    private static ConstAF constAF;
    private static FloatAF floatAF;
    private static IdAF idAF;
    private static final String[] KEYWORDS = new String[]{"#include", "<iostream>", "using", "namespace", "std", "int", "main", "cin", "cout", "double", "if", "while"};

    private static void getAllAtoms() {
        atoms = new HashTable<>(30);
        atoms.add("ID");
        atoms.add("CONST");
        atoms.add("#include");
        atoms.add("<iostream>");
        atoms.add("using");
        atoms.add("namespace");
        atoms.add("std");
        atoms.add(";");
        atoms.add("int");
        atoms.add("main");
        atoms.add("(");
        atoms.add(")");
        atoms.add("{");
        atoms.add("cin");
        atoms.add(">>");
        atoms.add("double");
        atoms.add("=");
        atoms.add("*");
        atoms.add("cout");
        atoms.add("<<");
        atoms.add("}");
    }

    public static void main(String[] args) {
        getAllAtoms();
        constTS = new ConstTS(30);
        identifierTS = new IdentifierTS(30);
        fip = new ArrayList<>();
        constAF = new ConstAF("lab2/lab2_part2/src/main/resources/constAF_input.txt");
        System.out.println(constAF.verifySequence("3.14"));
        floatAF = new FloatAF("lab2/lab2_part2/src/main/resources/floatAF_input.txt");
        idAF = new IdAF("lab2/lab2_part2/src/main/resources/idAF_input.txt");
        try {
            File file = new File("lab2/lab2_part2/src/main/resources/mlp_example.txt");
            Scanner reader = new Scanner(file);
            int line = 0;
            while (reader.hasNextLine()) {
                processData(reader.nextLine(), line);
                line++;
            }
            writeAnalysis();
        } catch (FileNotFoundException fe) {
            System.out.println("Error: " + fe.getMessage());
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        System.out.println("TABELA DE SIMBOLURI ID:\n");
        identifierTS.getIdentifiers().iterateOverElements();
        System.out.println('\n');
        System.out.println("TABELA DE SIMBOLURI PT CONST:\n");
        constTS.getIntConstants().iterateOverElements();
        System.out.println("\nFORMA INTERNA A PROGRAMULUI:");
        for (FIP f : fip) {
            System.out.println(f.toString());
        }
    }

    public static boolean isKeyword(String input) {
        for (String keyword : KEYWORDS) {
            if (input.equals(keyword)) {
                return true;
            }
        }
        return false;
    }

    private static void processData(String nextLine, int line) {
        List<String> elements = List.of(nextLine.split("\\s+|(?<=[()])|(?=[();])"));
        for (String e : elements) {
            Atom atom = new Atom(e);
            if(constAF.verifySequence(e) && !isKeyword(e)){
                Position pos = constTS.addIntConstant(Integer.parseInt(atom.getInput()));
                constTS.addIntConstant(Integer.parseInt(atom.getInput()));
                FIP f = new FIP(atom, pos.getPair().getKey(), atoms.get("CONST").getKey());
                fip.add(f);
            } else if(floatAF.verifySequence(e) && !isKeyword(e)){
                Position pos = constTS.addDoubleConstant(Double.parseDouble(atom.getInput()));
                constTS.addDoubleConstant(Double.parseDouble(atom.getInput()));
                FIP f = new FIP(atom, pos.getPair().getKey(), atoms.get("CONST").getKey());
                fip.add(f);
            } else if(idAF.verifySequence(e) && !isKeyword(e)){
                Position pos = identifierTS.addIdentifier(atom.getInput());
                System.out.println("POSITION: " + pos.toString() + " ATOM: " + atom.getInput());
                FIP f = new FIP(atom, pos.getPair().getKey(), atoms.get("ID").getKey());
                fip.add(f);
            } else if(atoms.get(e) != null){
                FIP f = new FIP(atom, -1, -1);
                fip.add(f);
            } else if(e.equals(" ")){
                continue;
            } else {
                System.out.println("Error on line " + line + " for atom " + e + "!");
            }
        }
    }

    private static Set<String> findOperators(String data) {
        Pattern OPERATORS_PATTERN = Pattern.compile("(?<![<>=+\\-*\\/]|#include\\s)([+\\-*=\\\\<>]=?|<<|>>|[<>]=)(?![<>=])");
        Matcher matcher = OPERATORS_PATTERN.matcher(data);
        Set<String> operators = new HashSet<>();
        while (matcher.find()) {
            operators.add(matcher.group());
        }
        System.out.println("OPERATORS:\n" + operators);
        return operators;
    }

    private static Set<String> findStringConstants(String data) {
        Pattern STRING_CONST_PATTERN = Pattern.compile("(?<=int|double)\\s\\w+(?=\\s*;)");
        Matcher matcher = STRING_CONST_PATTERN.matcher(data);
        Set<String> operators = new HashSet<>();
        while (matcher.find()) {
            operators.add(matcher.group());
        }
        System.out.println("STRING CONSTANTS:\n" + operators);
        return operators;
    }

    private static Set<String> findConstants(String data) {
        Pattern CONSTANTS_PATTERN = Pattern.compile("[0-9]\\.\\d*|\\d");
        Matcher matcher = CONSTANTS_PATTERN.matcher(data);
        Set<String> constants = new HashSet<>();
        while (matcher.find()) {
            constants.add(matcher.group());
        }
        System.out.println("CONSTANTS:\n" + constants);
        return constants;
    }

    private static Set<String> findSeparators(String data) {
        Pattern SEPARATORS_PATTERN = Pattern.compile("[,;(){}[\\]:]]");
        Matcher matcher = SEPARATORS_PATTERN.matcher(data);
        Set<String> separators = new HashSet<>();
        while (matcher.find()) {
            separators.add(matcher.group());
        }
        System.out.println("SEPARATORS:\n" + separators);
        return separators;
    }

    private static Set<String> findKeywords(String data) {
        Pattern KEYWORDS_PATTERN = Pattern.compile("#include|<iostream>|using|namespace|std|int|main|cin|cout|double|if|while/gm");
        Matcher matcher = KEYWORDS_PATTERN.matcher(data);
        Set<String> keywords = new HashSet<>();
        while (matcher.find()) {
            keywords.add(matcher.group());
        }
        System.out.println("KEYWORDS:\n" + keywords);
        return keywords;
    }

    private static void writeAnalysis() throws IOException {
        Set<String> constants = new HashSet<>();
        Set<String> operators = new HashSet<>();
        Set<String> keywords = new HashSet<>();
        Set<String> separators = new HashSet<>();
        Set<String> string_constants = new HashSet<>();
        try {
            File file = new File("lab2/lab2_part2/src/main/resources/mlp_example.txt");
            Scanner reader = new Scanner(file);
            StringBuilder data = new StringBuilder();
            int line = 0;
            while (reader.hasNextLine()) {
                data.append(reader.nextLine());
            }
            constants = findConstants(data.toString());
            operators = findOperators(data.toString());
            keywords = findKeywords(data.toString());
            separators = findSeparators(data.toString());
            string_constants = findStringConstants(data.toString());
        } catch (FileNotFoundException fe) {
            System.out.println("Error: " + fe.getMessage());
        }

        FileWriter fileWriter = new FileWriter("lab2/lab2_part2/src/main/resources/output.txt");
        PrintWriter printWriter = new PrintWriter(fileWriter);
        printWriter.print("KEYWORDS:\n" + keywords + "\n");
        printWriter.print("OPERATORS:\n" + operators + "\n");
        printWriter.print("SEPARATORS:\n" + separators + "\n");
        printWriter.print("CONSTANTS:\n" + constants + "\n");
        printWriter.print("STRING CONSTANTS:\n" + string_constants + "\n");
        printWriter.printf("TABELA SIMBOLURI PT ID:\n" + identifierTS.getIdentifiers().iterateOverElements() + '\n');
        printWriter.printf("TABELA SIMBOLURI PT CONST:\n" + constTS.getIntConstants().iterateOverElements() + constTS.getDoubleConstants().iterateOverElements() + '\n');
        StringBuilder fipRes = new StringBuilder();
        for (FIP f : fip) {
            fipRes.append(f.toString()).append('\n');
        }
        printWriter.printf("FORMA INTERNA A PROGRAMULUI:\n" + fipRes + '\n');
        printWriter.close();
    }
}