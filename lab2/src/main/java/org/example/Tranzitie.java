package org.example;

public class Tranzitie {
    private String stareInitiala;
    private String stareFinala;
    private String valoare;

    public Tranzitie(String stareInitiala, String stareFinala, String valoare) {
        this.stareInitiala = stareInitiala;
        this.stareFinala = stareFinala;
        this.valoare = valoare;
    }

    public String getStareInitiala() {
        return stareInitiala;
    }

    public String getStareFinala() {
        return stareFinala;
    }

    public String getValoare() {
        return valoare;
    }

    @Override
    public String toString() {
        return this.stareInitiala + "   ->(" + this.valoare + ")    " + this.stareFinala;
    }
}
