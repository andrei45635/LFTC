package org.example;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;

public class Main {
    private static String stareInitiala = "";
    private static Set<String> alfabetIntrare = new HashSet<>();
    private static Set<String> multimeStari = new HashSet<>();
    private static List<Tranzitie> tranzitii = new ArrayList<>();
    private static Set<String> stariFinale = new HashSet<>();
    private static AF af;

    public static void readFromFile(String filename){
        stareInitiala = "";
        alfabetIntrare = new HashSet<>();
        multimeStari = new HashSet<>();
        tranzitii = new ArrayList<>();
        stariFinale = new HashSet<>();
        try {
            File file = new File(filename);
            Scanner reader = new Scanner(file);
            String[] data = reader.nextLine().split(" ");
            multimeStari.addAll(List.of(data));
            stareInitiala = reader.nextLine();
            int k = Integer.parseInt(reader.nextLine());
            for(int i = 0; i < k; i++){
                data = reader.nextLine().split(" ");
                tranzitii.add(new Tranzitie(data[0], data[1], data[2]));
                alfabetIntrare.add(data[2]);
                if(Objects.equals(data[3],"1")){
                    stariFinale.add(data[0]);
                }
            }
            af = new AF(multimeStari, alfabetIntrare, tranzitii, stareInitiala, stariFinale);
            finiteAutomatonMenu(af);
        } catch (FileNotFoundException fe) {
            System.out.println("Error: " + fe.getMessage());
        }
    }

    public static void readFromKeyboard(){
        stareInitiala = "";
        alfabetIntrare = new HashSet<>();
        multimeStari = new HashSet<>();
        tranzitii = new ArrayList<>();
        stariFinale = new HashSet<>();
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter states (separated by spaces): ");
        String statesLine = scanner.nextLine();
        String[] statesArray = statesLine.split(" ");
        Collections.addAll(multimeStari, statesArray);

        System.out.print("Enter initial state: ");
        stareInitiala = scanner.nextLine();

        System.out.print("Enter final states: ");
        String finalStateLine = scanner.nextLine();
        String[] finalStatesArr = finalStateLine.split(" ");
        Collections.addAll(stariFinale, finalStatesArr);

        System.out.print("Enter the alphabet: ");
        String alphabetLine = scanner.nextLine();
        String[] alphabetArr = alphabetLine.split(" ");
        Collections.addAll(alfabetIntrare, alphabetArr);

        System.out.print("Enter the number of transitions: ");
        int numTransitions = Integer.parseInt(scanner.nextLine());

        for (int i = 0; i < numTransitions; i++) {
            System.out.print("Enter a transition (e.g., q0 q1 - 0): ");
            String transitionLine = scanner.nextLine();
            System.out.println(transitionLine);
            String[] tranzitieStr = transitionLine.split(" ");
            Tranzitie tranzitie = new Tranzitie(tranzitieStr[0], tranzitieStr[1], tranzitieStr[2]);
            tranzitii.add(tranzitie);
        }

        System.out.println("States: " + multimeStari);
        System.out.println("Entry alphabet: " + alfabetIntrare);
        System.out.println("Initial State: " + stareInitiala);
        System.out.println("Transitions:");
        for (Tranzitie transition : tranzitii) {
            System.out.println(transition);
        }
        AF af = new AF(multimeStari, alfabetIntrare, tranzitii, stareInitiala, stariFinale);

        finiteAutomatonMenu(af);
        //scanner.close();
    }

    public static void finiteAutomatonMenu(AF af){
        Scanner scanner = new Scanner(System.in);

        while (true) {
            System.out.println("\nMenu:");
            System.out.println("1. View Elements of the Finite Automaton");
            System.out.println("2. Check if a Sequence is Valid");
            System.out.println("3. Find the Longest Prefix");
            System.out.println("4. Exit");
            System.out.print("Enter your choice: ");

            int choice = scanner.nextInt();
            scanner.nextLine();

            switch (choice) {
                case 1 -> {
                    System.out.println("States: " + af.getStari());
                    System.out.println("Initial State: " + af.getStareInitiala());
                    System.out.println("Final States: " + af.getStariFinale());
                    System.out.println("Entry alphabet: " + af.getAlfabet());
                    System.out.println("Transitions:");
                    for (Tranzitie transition : af.getTranzitii()) {
                        System.out.println(transition);
                    }
                }
                case 2 -> {
                    System.out.print("Enter a sequence to check: ");
                    String sequenceToCheck = scanner.nextLine();
                    boolean isValid = af.verifySequence(sequenceToCheck);
                    System.out.println("Sequence is " + (isValid ? "valid" : "invalid"));
                }
                case 3 -> {
                    System.out.print("Enter a sequence to find the longest prefix: ");
                    String sequenceToFindPrefix = scanner.nextLine();
                    String longestPrefix = af.findLongestPrefix(sequenceToFindPrefix);
                    System.out.println("Longest Prefix: " + longestPrefix);
                }
                case 4 -> {
                    menu();
                    scanner.close();
                    return;
                }
                default -> System.out.println("Invalid choice. Please try again.");
            }
        }
    }

    public static void menu(){
        Scanner scanner = new Scanner(System.in);
        while(true){
            System.out.println("Choose how you want to build the FA: ");
            System.out.println(">>> 0) Exit ");
            System.out.println(">>> 1) Read values from the keyboard ");
            System.out.println(">>> 2) Read values from a file ");
            System.out.print(">>> ");
            int choice = Integer.parseInt(scanner.nextLine());
            switch(choice) {
                case 1 -> readFromKeyboard();
                case 2 -> readFromFile("C:\\Users\\GIGABYTE\\IdeaProjects\\LFTC\\lab2\\src\\main\\resources\\input.txt");
                case 0 -> {
                    scanner.close();
                    return;
                }
            }
        }
    }

    public static void main(String[] args) {
        menu();
    }
}