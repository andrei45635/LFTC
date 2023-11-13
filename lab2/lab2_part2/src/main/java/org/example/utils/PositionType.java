package org.example.utils;

public enum PositionType {
    ID(0),
    STRING_CONST(1),
    INT_CONST(1),
    DOUBLE_CONST(2),
    OTHER(-1);

    public final int code;

    PositionType(int code) {
        this.code = code;
    }
}
