package org.example.utils;

public class Position {
    private Pair<Integer, Integer> pair;
    private PositionType type;

    public Position(PositionType type, Pair<Integer, Integer> pair) {
        this.type = type;
        this.pair = pair;
    }

    public static final Position NullPosition = new Position(PositionType.OTHER, new Pair<>(-1, -1));

    @Override
    public String toString() {
        return "Position{" +
                "pair=" + pair +
                ", type=" + type +
                '}';
    }

    public Pair<Integer, Integer> getPair() {
        return pair;
    }
}
