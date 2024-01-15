package org.example.in_class_s11;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;

public class Reader {
    public static void main(String[] args) {
        try (BufferedReader br = new BufferedReader(new FileReader("C:\\Users\\GIGABYTE\\IdeaProjects\\LFTC\\lab2\\lab2_part2\\src\\main\\java\\org\\example\\in_class_s11\\gramatica.txt"))) {
            String line;
            Set<String> terminali = new HashSet<>();
            Set<String> neterminali = new HashSet<>();
            List<String> reguliProductie = new ArrayList<>();
            while ((line = br.readLine()) != null) {
                String[] parts = line.split(" ");
                neterminali.add(parts[0]);
                String[] dreapta = parts[2].split("");
                for(String d: dreapta){
                    for(int i = 0; i < d.length(); i++){
                        char ch = d.charAt(i);
                        if(Character.isLowerCase(ch)){
                            terminali.add(d);
                        } else {
                            neterminali.add(d);
                        }
                    }
                }
                reguliProductie.add(line);
            }
            Gramatica gramatica = new Gramatica(reguliProductie, terminali, neterminali);
            System.out.println(gramatica);
            System.out.println(gramatica.recursivLaDreapta());
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
