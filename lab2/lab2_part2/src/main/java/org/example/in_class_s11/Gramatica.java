package org.example.in_class_s11;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;

public class Gramatica {
    private List<String> reguliProductie;
    private Set<String> terminali;
    private Set<String> neterminali;

    public Gramatica(List<String> reguliProductie, Set<String> terminali, Set<String> neterminali) {
        this.reguliProductie = reguliProductie;
        this.terminali = terminali;
        this.neterminali = neterminali;
    }

    public List<String> getReguliProductie() {
        return reguliProductie;
    }

    public Set<String> getTerminali() {
        return terminali;
    }

    public Set<String> getNeterminali() {
        return neterminali;
    }

    public List<String> recursivLaDreapta() {
        List<String> res = new ArrayList<>();
        List<String> reguliProductie = this.getReguliProductie();
        for(String r: reguliProductie){
            String[] parts = r.split(" ");
            for(String d: parts[2].split("")){
                if(parts[0].equals(d)){
                    res.add(r);
                }
            }
        }
        return res;
    }

    @Override
    public String toString() {
        return "Gramatica{" +
                "reguliProductie=" + reguliProductie +
                ", terminali=" + terminali +
                ", neterminali=" + neterminali +
                '}';
    }
}
