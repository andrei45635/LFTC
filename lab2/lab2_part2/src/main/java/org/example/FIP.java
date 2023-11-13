package org.example;

public class FIP {
    private Atom atom;
    private int codTS;
    private int codAtom;

    public FIP(Atom atom, int codTS, int codAtom) {
        this.atom = atom;
        this.codTS = codTS;
        this.codAtom = codAtom;
    }

    @Override
    public String toString() {
        //this.atom.getInput() + "\t|\t" +
        //this.atom.getInput() + "\t|\t" +
        if (this.codTS == -1)
            return this.codAtom + "\t|\t-\t|\t" + this.atom.getInput();
        return this.codTS + "\t|\t" + this.codAtom + "\t|\t" + atom.getInput();
    }
}
