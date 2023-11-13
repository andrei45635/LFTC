package org.example.symbol_table;

import org.example.utils.HashTable;
import org.example.utils.Pair;
import org.example.utils.Position;
import org.example.utils.PositionType;

public class IdentifierTS {
    private int size;
    private HashTable<String> identifiers;

    public IdentifierTS(int size) {
        this.size = size;
        this.identifiers = new HashTable<>(size);
    }

    public int getSize() {
        return size;
    }

    public HashTable<String> getIdentifiers() {
        return identifiers;
    }

    public Position addIdentifier(String name) {
        Pair<Integer, Integer> position = identifiers.add(name);
        return new Position(PositionType.ID, position);
    }

    public String getIdentifier(int posInBucket, int posInList) throws Exception {
        return identifiers.findByPair(posInBucket, posInList);
    }

    public Pair<Integer, Integer> hasIdentifier(String name){
        return identifiers.get(name);
    }

    @Override
    public String toString() {
        return "IdentifierTS{" +
                "identifiers=" + identifiers +
                '}';
    }
}
