package org.example;

import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import java.util.stream.Stream;

public class AF {
    private Set<String> stari;
    private Set<String> alfabet;
    private List<Tranzitie> tranzitii;
    private String stareInitiala;
    private Set<String> stariFinale;

    private Set<String> letters;
    private Set<String> digits;

    public AF(Set<String> stari, Set<String> alfabet, List<Tranzitie> tranzitii, String stareInitiala, Set<String> stariFinale) {
        this.stari = stari;
        this.alfabet = alfabet;
        this.tranzitii = tranzitii;
        this.stareInitiala = stareInitiala;
        this.stariFinale = stariFinale;

//        letters = IntStream.range('a', 'z' + 1).mapToObj(String::valueOf).collect(Collectors.toSet());
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
                        //stareGasita = true;
                        //break;
                    }

                    if (stareInitiala.equals("-") && t.getValoare().equals("-") && cs.equals("-")) {
                        nextChar = t.getStareFinala();
                        //stareGasita = true;
                        //break;
                    }

                    if(letters.contains(cs)){
                        return false;
                    }

                    if (t.getValoare().equals(cs)) {
                        nextChar = t.getStareFinala();
                        //stareGasita = true;
                        //break;
                    }
                }
            }

            if (nextChar.equals("")) {
                stareGasita = false;
            }

            if (stariFinale.contains(nextChar)) {
                stareGasita = true;
                stareFinala = nextChar;
                //break;
            }
        }

        if (!stariFinale.contains(stareFinala)) {
            stareGasita = false;
        }

        return stareGasita;
    }

    public String findLongestPrefix(String sequence) {
        String currentState = this.stareInitiala;
        String longestPrefix = "";
        StringBuilder currentPrefix = new StringBuilder();
        boolean foundNonZero = false;

        for (int i = 0; i < sequence.length(); i++) {
            char character = sequence.charAt(i);
            String nextCharacter = null;

            if (Character.isDigit(character)) {
                if (character != '0' || foundNonZero) {
                    foundNonZero = true;
                    for (Tranzitie tranzitie : tranzitii) {
                        if (tranzitie.getStareInitiala().equals(currentState)) {
                            nextCharacter = tranzitie.getStareFinala();
                            currentPrefix.append(character);
                            break;
                        }
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
