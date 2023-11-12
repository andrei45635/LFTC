package org.example;

public class Atom {
    private String input;
    private final String ID = "[a-zA-Z][a-zA-Z0-9]{0,255}";
    private final String CONST = "[0-9]\\.\\d*|\\d";
    private final String[] BOOL_OPERATORS = {"<", ">", "<>"};
    private final String[] OPERATORS = {"+", "-", "*", ":="};
    private final String[] SEPARATORS = {".", ",", ";"};
    private final String[] KEYWORDS = new String[]{"#include", "<iostream>", "using", "namespace", "std", "int", "main", "cin", "cout", "double", "if", "while"};

    public Atom(String input) {
        this.input = input;
    }

    public String getInput() {
        return input;
    }

    public boolean isID() {
        return input.matches(ID);
    }

    public boolean isCONST() {
        return input.matches(CONST);
    }

    public boolean isBoolOperator() {
        for (String bool : BOOL_OPERATORS) {
            return input.equals(bool);
        }
        return false;
    }

    public boolean isOperator() {
        for (String operator : OPERATORS) {
            return input.equals(operator);
        }
        return false;
    }

    public boolean isKeyword() {
        for (String keyword : KEYWORDS) {
            if (this.input.equals(keyword)) {
                return true;
            }
        }
        return false;
    }

    public boolean isSeparator() {
        for (String separator : SEPARATORS) {
            return input.equals(separator);
        }
        return false;
    }

    @Override
    public String toString() {
        return "Atom{" +
                "input='" + input + '\'' +
                '}';
    }
}
