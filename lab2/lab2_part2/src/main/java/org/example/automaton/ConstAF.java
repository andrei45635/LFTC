package org.example.automaton;

import org.example.Tranzitie;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class ConstAF {
    private Set<String> stari;
    private Set<String> alfabet;
    private List<Tranzitie> tranzitii;
    private String stareInitiala;
    private Set<String> stariFinale;

    private Set<String> letters;
    private Set<String> digits;

    public ConstAF(String filename) {
        stareInitiala = "";
        alfabet = new HashSet<>();
        stari = new HashSet<>();
        tranzitii = new ArrayList<>();
        stariFinale = new HashSet<>();
        try {
            File file = new File(filename);
            Scanner reader = new Scanner(file);
            String[] data = reader.nextLine().split(" ");
            stari.addAll(List.of(data));
            stareInitiala = reader.nextLine();
            int k = Integer.parseInt(reader.nextLine());
            for(int i = 0; i < k; i++){
                data = reader.nextLine().split(" ");
                tranzitii.add(new Tranzitie(data[0], data[1], data[2]));
                alfabet.add(data[2]);
                if(Objects.equals(data[3],"1")){
                    stariFinale.add(data[0]);
                }
            }
        } catch (FileNotFoundException fe) {
            System.out.println("Error: " + fe.getMessage());
        }

        letters = IntStream.rangeClosed('a', 'z')
                .mapToObj(c -> String.valueOf((char) c))
                .collect(Collectors.toSet());
        digits = IntStream.range(0, 10).mapToObj(String::valueOf).collect(Collectors.toSet());
    }

    public boolean checkDeterminism() {
        List<String> stari = new ArrayList<>();
        for (Tranzitie t : this.tranzitii) {
            if (stari.contains(t.getStareInitiala())) {
                return false;
            } else stari.add(t.getStareInitiala());
        }
        return true;
    }

    public boolean verifySequence(String sequence) {
        boolean stareGasita = true;
        String stareFinala = "";

        for (char c : sequence.toCharArray()) {
            String cs = String.valueOf(c);
            String nextChar = "";

            for (Tranzitie t : tranzitii) {
                if (t.getStareInitiala().equals(stareInitiala)) {
                    if (t.getValoare().equals("digit") && digits.contains(cs)) {
                        nextChar = t.getStareFinala();
                        break;
                    }

                    if (t.getValoare().equals("-") && cs.equals("-")) {
                        nextChar = t.getStareFinala();
                        break;
                    }

                    if (letters.contains(cs)) {
                        return false;
                    }
                }
            }

            if (nextChar.equals("")) {
                stareGasita = false;
            }

            if (stariFinale.contains(nextChar)) {
                stareGasita = true;
                stareFinala = nextChar;
            }

            //stareInitiala = nextChar;
            stareFinala = nextChar;
        }

        if (!stariFinale.contains(stareFinala)) {
            stareGasita = false;
        }

        //stareInitiala = "q0";

        return stareGasita;
    }

    public String findLongestPrefix(String sequence) {
        String currentState = this.stareInitiala;
        String longestPrefix = "";
        StringBuilder currentPrefix = new StringBuilder();

        for (int i = 0; i < sequence.length(); i++) {
            String character = String.valueOf(sequence.charAt(i));
            String nextCharacter = null;

            if (digits.contains(character)) {
                for (Tranzitie tranzitie : tranzitii) {
                    if (tranzitie.getStareInitiala().equals(currentState)) {
                        nextCharacter = tranzitie.getStareFinala();
                        currentPrefix.append(character);
                        break;
                    }
                }
            }

            if (nextCharacter != null) {
                if (stariFinale.contains(nextCharacter)) {
                    if (currentPrefix.length() > longestPrefix.length()) {
                        longestPrefix = currentPrefix.toString();
                    }
                }
                currentState = nextCharacter;
            } else {
                currentPrefix = new StringBuilder();
                currentState = this.stareInitiala;
            }
        }
        return longestPrefix;
    }

    public Set<String> getStari() {
        return stari;
    }

    public Set<String> getAlfabet() {
        return alfabet;
    }

    public List<Tranzitie> getTranzitii() {
        return tranzitii;
    }

    public String getStareInitiala() {
        return stareInitiala;
    }

    public Set<String> getStariFinale() {
        return stariFinale;
    }
}
