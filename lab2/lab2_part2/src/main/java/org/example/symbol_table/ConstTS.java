package org.example.symbol_table;

import org.example.utils.HashTable;
import org.example.utils.Pair;
import org.example.utils.Position;
import org.example.utils.PositionType;

public class ConstTS {
    private int size;
    private HashTable<String> stringConstants;
    private HashTable<Integer> intConstants;

    public ConstTS(int size) {
        this.size = size;
        this.stringConstants = new HashTable<>(size);
        this.intConstants = new HashTable<>(size);
    }

    public HashTable<Integer> getIntConstants() {
        return intConstants;
    }

    public Position addStringConstant(String name) {
        Pair<Integer, Integer> pair = this.stringConstants.add(name);
        return new Position(PositionType.STRING_CONST, pair);
    }

    public Position addIntConstant(int constant) {
        Pair<Integer, Integer> pair = this.intConstants.add(constant);
        return new Position(PositionType.INT_CONST, pair);
    }

    public String getStringConstant(int posInBucket, int posInList) throws Exception {
        return stringConstants.findByPair(posInBucket, posInList);
    }

    public int getIntConstant(int posInBucket, int posInList) throws Exception {
        return intConstants.findByPair(posInBucket, posInList);
    }

    public Pair<Integer, Integer> hasStringConstant(String name){
        return stringConstants.get(name);
    }

    public Pair<Integer, Integer> hasIntConstant(int constant){
        return intConstants.get(constant);
    }

    @Override
    public String toString() {
        return "ConstTS{" +
                "stringConstants=" + stringConstants +
                ", intConstants=" + intConstants +
                '}';
    }
}
